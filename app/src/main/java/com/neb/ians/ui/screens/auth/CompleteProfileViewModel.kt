package com.neb.ians.ui.screens.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserPhoto
import com.neb.ians.data.api.UserProfileRequest
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ProfileSaveResult
import com.neb.ians.data.repository.UserProfileCache
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import com.neb.ians.data.api.ApiSocialLink
import com.neb.ians.data.api.CreateSocialLinkRequest
import javax.inject.Inject
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody

private const val SESSION_EXPIRED_MESSAGE =
    "Your sign-in expired. Sign in again with the same account to finish setting up your profile."

data class CompleteProfileUiState(
    val username: String = "",
    val displayName: String = "",
    val email: String = "",
    val bio: String = "",
    val dob: String = "",
    val gender: String = "Male",
    val role: String = "student",
    val classLevel: String = "Class 11",
    val subjects: List<String> = emptyList(),
    val teachingSubjects: List<String> = emptyList(),
    val institutionType: String = "",
    val pradesh: String = "Bagmati",
    val district: String = "Kathmandu",
    val school: String = "",
    val isLocked: Boolean = false,
    val photoUrl: String = "",
    val bannerUrl: String = "",
    val coverArt: String = "",
    val isPhotoUploading: Boolean = false,
    val isCheckingUsername: Boolean = false,
    val usernameAvailable: Boolean? = null,
    val usernameError: String? = null,
    val isSubmitting: Boolean = false,
    val submissionResult: Boolean? = null,
    val submissionError: String? = null,
    val needsReauth: Boolean = false,
    val signOutReady: Boolean = false,
    val isEditing: Boolean = false,
    val showPhotoGallery: Boolean = false,
    val photos: List<ApiUserPhoto> = emptyList(),
    val photosLoading: Boolean = false,
    val photoBusy: Boolean = false,
    val socialLinks: List<ApiSocialLink> = emptyList(),
    val schoolUsername: String = "",
    val schoolSlug: String = "",
    val headline: String = "",
    val eduStatus: String = "",
    val eduProgram: String = "",
    val eduTerm: String = "",
    val eduCompleted: String = "",
    val eduCatalog: com.neb.ians.data.api.ApiEduCatalog? = null,
    val skills: List<String> = emptyList(),
    val openTo: List<String> = emptyList(),
    val teachLevels: List<String> = emptyList(),
    val experienceYears: String = "",
    val employment: String = "",
    val portfolioLoaded: Boolean = false,
    /** True once the server has said whether this account owns an institution; the claim button waits for it. */
    val ownedKnown: Boolean = false,
    val institutions: List<com.neb.ians.data.api.ApiInstitution> = emptyList()
)

@OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)
@HiltViewModel
class CompleteProfileViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val apiService: ApiService
) : ViewModel() {

    private val _uiState = MutableStateFlow(CompleteProfileUiState())
    val uiState: StateFlow<CompleteProfileUiState> = _uiState.asStateFlow()

    private val _usernameQuery = MutableStateFlow("")

    private var cachedUsername: String = ""

    private var institutionsRequested = false

    init {
        viewModelScope.launch {
            var initializedOnce = false
            authRepository.userProfileFlow.collect { cached ->
                if (cached == null) return@collect
                if (cached.username.isNotEmpty() && cachedUsername.isEmpty()) {
                    cachedUsername = cached.username
                }
                val isCompleted = authRepository.isProfileCompletedFlow.first()
                val fallbackDisplayName = cached.displayName?.takeIf { it.isNotBlank() }
                    ?: cached.email?.substringBefore("@")?.takeIf { it.length >= 2 }
                    ?: cached.username
                _uiState.update { state ->
                    if (!initializedOnce) {
                        state.copy(
                            isEditing = isCompleted,
                            username = cached.username,
                            displayName = fallbackDisplayName,
                            email = cached.email ?: "",
                            bio = cached.bio ?: "",
                            dob = cached.dob,
                            gender = cached.gender?.takeIf { it.isNotBlank() } ?: "Male",
                            role = cached.role?.takeIf { it.isNotBlank() } ?: "student",
                            classLevel = cached.classLevel?.takeIf { it.isNotBlank() } ?: "Class 11",
                            subjects = cached.subjects?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
                            teachingSubjects = cached.teachingSubjects?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
                            institutionType = cached.institutionType ?: "",
                            pradesh = cached.pradesh?.takeIf { it.isNotBlank() } ?: "Bagmati",
                            district = cached.district?.takeIf { it.isNotBlank() } ?: "Kathmandu",
                            school = cached.school ?: "",
                            schoolUsername = cached.schoolUsername ?: "",
                            photoUrl = cached.photoUrl ?: "",
                            bannerUrl = cached.bannerUrl ?: "",
                            isLocked = cached.isLocked
                        )
                    } else {
                        // Fill in fields that arrived asynchronously from ensureProfile() without overwriting user edits
                        state.copy(
                            username = state.username.ifBlank { cached.username },
                            displayName = state.displayName.ifBlank { cached.displayName ?: "" },
                            email = state.email.ifBlank { cached.email ?: "" },
                            photoUrl = state.photoUrl.ifBlank { cached.photoUrl ?: "" }
                        )
                    }
                }
                if (cached.username.isNotEmpty() && _usernameQuery.value.isEmpty()) {
                    _usernameQuery.value = cached.username
                }
                if (!initializedOnce) {
                    initializedOnce = true
                    if (isCompleted) {
                        fetchSocialLinks()
                        fetchPortfolioFields(cached.username)
                    }
                }
            }
        }

        viewModelScope.launch {
            _usernameQuery
                .debounce(500)
                .distinctUntilChanged()
                .mapLatest { query ->
                    if (query.length < 3) {
                        _uiState.update { it.copy(
                            usernameAvailable = null,
                            usernameError = if (query.isNotEmpty()) "Must be at least 3 characters" else null,
                            isCheckingUsername = false
                        )}
                        return@mapLatest
                    }
                    if (!query.matches(Regex("^[a-zA-Z0-9_]+$"))) {
                        _uiState.update { it.copy(
                            usernameAvailable = null,
                            usernameError = "Letters, numbers, underscores only",
                            isCheckingUsername = false
                        )}
                        return@mapLatest
                    }
                    if (query == cachedUsername) {
                        _uiState.update { it.copy(
                            usernameAvailable = true,
                            usernameError = null,
                            isCheckingUsername = false
                        )}
                        return@mapLatest
                    }
                    _uiState.update { it.copy(isCheckingUsername = true, usernameError = null) }
                    try {
                        val response = apiService.checkUsername(query)
                        _uiState.update { it.copy(usernameAvailable = response.available, isCheckingUsername = false) }
                    } catch (e: Exception) {
                        _uiState.update { it.copy(usernameAvailable = null, isCheckingUsername = false) }
                    }
                }
                .collect()
        }
    }

    fun onUsernameChange(value: String) {
        val trimmed = value.trim()
        _uiState.update { it.copy(username = trimmed) }
        _usernameQuery.value = trimmed
    }

    fun onDisplayNameChange(value: String) {
        _uiState.update { it.copy(displayName = value) }
    }

    fun onEmailChange(value: String) {
        _uiState.update { it.copy(email = value.trim()) }
    }

    fun onBioChange(value: String) {
        _uiState.update { it.copy(bio = value) }
    }

    fun onDobChange(dob: String) {
        _uiState.update { it.copy(dob = dob) }
    }

    fun onGenderChange(gender: String) {
        _uiState.update { it.copy(gender = gender) }
    }

    fun onRoleChange(role: String) {
        _uiState.update { it.copy(role = role) }
    }

    fun onClassChange(classLevel: String) {
        _uiState.update { it.copy(classLevel = classLevel, eduProgram = if (classLevel == it.classLevel) it.eduProgram else "", eduTerm = if (classLevel == it.classLevel) it.eduTerm else "") }
    }

    fun onEduStatus(v: String) = _uiState.update { it.copy(eduStatus = if (it.eduStatus == v) "" else v) }
    fun onEduProgram(v: String) = _uiState.update { it.copy(eduProgram = if (it.eduProgram == v) "" else v) }
    fun onEduTerm(v: String) = _uiState.update { it.copy(eduTerm = if (it.eduTerm == v) "" else v) }
    fun onEduCompleted(v: String) = _uiState.update { it.copy(eduCompleted = if (it.eduCompleted == v) "" else v) }

    /** Statuses, programs and terms come from the server so the app and the site never disagree. */
    fun loadEduCatalog() {
        if (_uiState.value.eduCatalog != null) return
        eduCatalogCache?.let { c -> _uiState.update { it.copy(eduCatalog = c) }; return }
        viewModelScope.launch {
            val c = runCatching { apiService.educationCatalog() }.getOrNull() ?: return@launch
            eduCatalogCache = c
            _uiState.update { it.copy(eduCatalog = c) }
        }
    }

    fun onSubjectToggle(subject: String) {
        _uiState.update { state ->
            val current = state.subjects.toMutableList()
            if (current.contains(subject)) current.remove(subject) else current.add(subject)
            state.copy(subjects = current)
        }
    }

    fun onTeachingSubjectToggle(subject: String) {
        _uiState.update { state ->
            val current = state.teachingSubjects.toMutableList()
            if (current.contains(subject)) current.remove(subject) else current.add(subject)
            state.copy(teachingSubjects = current)
        }
    }

    fun onInstitutionTypeChange(value: String) {
        _uiState.update { it.copy(institutionType = value) }
    }

    fun onPradeshChange(pradesh: String) {
        _uiState.update { it.copy(pradesh = pradesh) }
    }

    fun onDistrictChange(district: String) {
        _uiState.update { it.copy(district = district) }
    }

    fun onSchoolChange(school: String) {
        _uiState.update { it.copy(school = school) }
    }

    fun onLockedChange(locked: Boolean) {
        _uiState.update { it.copy(isLocked = locked) }
    }




    fun openPhotoGallery() {
        _uiState.update { it.copy(showPhotoGallery = true) }
        loadPhotos()
    }

    fun closePhotoGallery() {
        _uiState.update { it.copy(showPhotoGallery = false) }
    }

    private fun loadPhotos() {
        viewModelScope.launch {
            _uiState.update { it.copy(photosLoading = true) }
            try {
                val token = authRepository.getBearerToken() ?: run {
                    _uiState.update { it.copy(photosLoading = false) }
                    return@launch
                }
                val photos = apiService.getUserPhotos(token)
                _uiState.update { it.copy(photos = photos, photosLoading = false) }
            } catch (_: Exception) {
                _uiState.update { it.copy(photosLoading = false) }
            }
        }
    }

    fun activatePhoto(photoId: Int) {
        if (_uiState.value.photoBusy) return
        viewModelScope.launch {
            _uiState.update { it.copy(photoBusy = true) }
            try {
                val token = authRepository.getBearerToken() ?: run {
                    _uiState.update { it.copy(photoBusy = false) }
                    return@launch
                }
                apiService.activatePhoto(token, photoId)
                authRepository.refreshProfile()
                val photos = try { apiService.getUserPhotos(token) } catch (_: Exception) { _uiState.value.photos }
                val current = photos.firstOrNull { it.isCurrent }?.url ?: _uiState.value.photoUrl
                _uiState.update { it.copy(photos = photos, photoUrl = current, photoBusy = false) }
            } catch (_: Exception) {
                _uiState.update { it.copy(photoBusy = false) }
            }
        }
    }

    fun uploadPhoto(bytes: ByteArray, mimeType: String) {
        uploadProfilePhoto(bytes, "profile_photo", mimeType)
    }

    fun uploadProfilePhoto(bytes: ByteArray, fileName: String, mimeType: String) {
        _uiState.update { it.copy(isPhotoUploading = true, photoBusy = true) }
        viewModelScope.launch {
            try {
                val ext = when (mimeType) {
                    "image/png" -> ".png"
                    "image/webp" -> ".webp"
                    "image/gif" -> ".gif"
                    "image/jpeg", "image/jpg" -> ".jpg"
                    else -> {
                        val suffix = mimeType.substringAfter("/", "")
                        if (suffix.isNotBlank()) ".$suffix" else ".jpg"
                    }
                }
                val requestBody = bytes.toRequestBody(mimeType.toMediaTypeOrNull())
                val filePart = okhttp3.MultipartBody.Part.createFormData("file", "$fileName$ext", requestBody)
                val url = authRepository.uploadProfilePhoto(filePart)
                authRepository.refreshProfile()
                val token = authRepository.getBearerToken()
                val photos = if (token != null) {
                    try { apiService.getUserPhotos(token) } catch (_: Exception) { _uiState.value.photos }
                } else _uiState.value.photos
                _uiState.update { it.copy(
                    isPhotoUploading = false,
                    photoBusy = false,
                    photos = photos,
                    photoUrl = url ?: photos.firstOrNull { photo -> photo.isCurrent }?.url ?: it.photoUrl
                ) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isPhotoUploading = false, photoBusy = false) }
            }
        }
    }

    fun submitProfile() {
        val state = _uiState.value
        if (state.isSubmitting) return

        _uiState.update {
            it.copy(
                isSubmitting = true,
                submissionResult = null,
                submissionError = null,
                needsReauth = false
            )
        }

        viewModelScope.launch {
            val cachedUser = authRepository.userProfileFlow.first()
            val request = UserProfileRequest(
                username = state.username,
                email = state.email.ifBlank { cachedUser?.email },
                photoUrl = state.photoUrl.ifBlank { cachedUser?.photoUrl },
                displayName = state.displayName.ifBlank { cachedUser?.displayName ?: state.email.substringBefore("@") },
                dob = if (state.role == "institution") "" else state.dob,
                gender = if (state.role == "institution") "" else state.gender,
                role = state.role,
                classLevel = state.classLevel,
                subjects = state.subjects.joinToString(","),
                teachingSubjects = state.teachingSubjects.joinToString(","),
                institutionType = state.institutionType,
                pradesh = state.pradesh,
                district = state.district,
                school = state.school,
                schoolUsername = state.schoolUsername,
                schoolSlug = state.schoolSlug.ifBlank { null },
                // Only sent once read (or for a new account), so an edit never blanks what it never saw.
                headline = state.headline.takeIf { !state.isEditing || state.portfolioLoaded },
                eduStatus = state.eduStatus.takeIf { !state.isEditing || state.portfolioLoaded },
                eduProgram = state.eduProgram.takeIf { !state.isEditing || state.portfolioLoaded },
                eduTerm = state.eduTerm.takeIf { !state.isEditing || state.portfolioLoaded },
                eduCompleted = state.eduCompleted.takeIf { !state.isEditing || state.portfolioLoaded },
                skills = state.skills.joinToString(",").takeIf { !state.isEditing || state.portfolioLoaded },
                openTo = state.openTo.joinToString(",").takeIf { !state.isEditing || state.portfolioLoaded },
                teachLevels = state.teachLevels.joinToString(",").takeIf { !state.isEditing || state.portfolioLoaded },
                experienceYears = state.experienceYears.toIntOrNull(),
                employment = state.employment.takeIf { !state.isEditing || state.portfolioLoaded },
                isLocked = state.isLocked,
                bannerUrl = "",
                bio = state.bio
            )

            when (val result = authRepository.saveProfile(request)) {
                ProfileSaveResult.Success -> _uiState.update {
                    it.copy(isSubmitting = false, submissionResult = true, submissionError = null)
                }
                ProfileSaveResult.SessionExpired -> _uiState.update {
                    it.copy(
                        isSubmitting = false,
                        submissionResult = false,
                        needsReauth = true,
                        submissionError = SESSION_EXPIRED_MESSAGE
                    )
                }
                is ProfileSaveResult.Failure -> _uiState.update {
                    it.copy(
                        isSubmitting = false,
                        submissionResult = false,
                        submissionError = result.message
                    )
                }
            }
        }
    }

    fun skipOnboarding(onDone: () -> Unit) {
        viewModelScope.launch {
            runCatching { authRepository.markProfileCompleted() }
            onDone()
        }
    }

    fun restartSignIn() {
        if (_uiState.value.isSubmitting) return
        _uiState.update { it.copy(isSubmitting = true, submissionError = null) }
        viewModelScope.launch {
            authRepository.logout()
            _uiState.update { it.copy(isSubmitting = false, signOutReady = true) }
        }
    }

    fun fetchSocialLinks() {
        viewModelScope.launch {
            runCatching {
                apiService.getSocialLinks()
            }.onSuccess { response ->
                _uiState.update { it.copy(socialLinks = response.links) }
            }.onFailure { e ->
                _uiState.update { it.copy(submissionError = e.localizedMessage) }
            }
        }
    }

    fun addSocialLink(platform: String, url: String, label: String = "") {
        viewModelScope.launch {
            _uiState.update { it.copy(photoBusy = true) }
            runCatching {
                apiService.createSocialLink(CreateSocialLinkRequest(platform = platform, url = url, label = label))
            }.onSuccess { response ->
                _uiState.update { it.copy(photoBusy = false) }
                if (response.ok) {
                    fetchSocialLinks()
                } else {
                    _uiState.update { it.copy(submissionError = response.error ?: "Failed to add link") }
                }
            }.onFailure { e ->
                _uiState.update { it.copy(photoBusy = false, submissionError = e.localizedMessage) }
            }
        }
    }

    fun deleteSocialLink(linkId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(photoBusy = true) }
            runCatching {
                apiService.deleteSocialLink(linkId)
            }.onSuccess { response ->
                _uiState.update { it.copy(photoBusy = false) }
                if (response.ok) {
                    fetchSocialLinks()
                } else {
                    _uiState.update { it.copy(submissionError = response.error ?: "Failed to delete link") }
                }
            }.onFailure { e ->
                _uiState.update { it.copy(photoBusy = false, submissionError = e.localizedMessage) }
            }
        }
    }

    fun setIsEditing(editing: Boolean) {
        _uiState.update { it.copy(isEditing = editing) }
    }

    /** Picks a profile cover from the M3X art library; "" goes back to the default. Shown at once, undone if the server refuses. */
    fun setCoverArt(id: String) {
        val before = _uiState.value.coverArt
        _uiState.update { it.copy(coverArt = id) }
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: throw IllegalStateException("no token")
                apiService.setCoverArt(token, mapOf("coverArt" to id))
            } catch (_: Exception) {
                _uiState.update { it.copy(coverArt = before) }
            }
        }
    }

    private fun csv(value: String?) = value?.split(",")?.map { it.trim() }?.filter { it.isNotEmpty() } ?: emptyList()

    /** The portfolio header and teacher fields are not in the cached profile; read them once. */
    private fun fetchPortfolioFields(username: String) {
        viewModelScope.launch {
            val p = runCatching { apiService.getProfile(authRepository.getBearerToken(), username) }.getOrNull() ?: return@launch
            // A verified owner keeps no school of their own, so the slug can come back blank; the institution they own is the answer.
            val ownerToken = authRepository.getBearerToken()
            var ownedKnown = p.role != "institution" || !p.schoolSlug.isNullOrBlank()
            val ownedSlug = if (ownerToken != null && p.schoolSlug.isNullOrBlank() && p.role == "institution") {
                runCatching { apiService.myInstitution(ownerToken).institution?.slug.also { ownedKnown = true } }.getOrNull().orEmpty()
            } else ""
            _uiState.update {
                it.copy(
                    headline = p.headline.orEmpty(), skills = csv(p.skills), openTo = csv(p.openTo),
                    eduStatus = p.eduStatus.orEmpty(), eduProgram = p.eduProgram.orEmpty(), eduTerm = p.eduTerm.orEmpty(),
                    eduCompleted = p.eduCompleted.orEmpty(),
                    teachLevels = csv(p.teachLevels), experienceYears = if (p.experienceYears > 0) p.experienceYears.toString() else "",
                    employment = p.employment.orEmpty(), portfolioLoaded = true, ownedKnown = ownedKnown,
                    schoolSlug = p.schoolSlug.orEmpty().ifBlank { ownedSlug }, coverArt = p.coverArt.orEmpty()
                )
            }
        }
    }

    fun onHeadlineChange(v: String) = _uiState.update { it.copy(headline = v.take(120)) }
    fun onExperienceChange(v: String) = _uiState.update { it.copy(experienceYears = v.filter(Char::isDigit).take(2)) }
    fun onEmploymentChange(v: String) = _uiState.update { it.copy(employment = if (it.employment == v) "" else v) }
    fun toggleSkill(v: String) = _uiState.update { it.copy(skills = if (v in it.skills) it.skills - v else (it.skills + v).take(15)) }
    fun toggleOpenTo(v: String) = _uiState.update { it.copy(openTo = if (v in it.openTo) it.openTo - v else it.openTo + v) }
    fun toggleTeachLevel(v: String) = _uiState.update { it.copy(teachLevels = if (v in it.teachLevels) it.teachLevels - v else it.teachLevels + v) }

    fun onSchoolChange(schoolName: String, username: String = "") {
        _uiState.update { it.copy(school = schoolName, schoolUsername = username, schoolSlug = "") }
    }

    /** A school picked from the catalogue: its slug is what the school page counts people by. */
    fun onSchoolPicked(row: com.neb.ians.data.api.ApiInstRow) {
        _uiState.update {
            it.copy(
                school = row.name,
                schoolSlug = row.slug,
                schoolUsername = row.username,
                institutionType = if (it.role == "institution") {
                    when (row.kind) { "school" -> "school"; "college", "university" -> "college"; else -> "other" }
                } else it.institutionType,
                district = if (it.district.isBlank() && row.district.isNotBlank()) row.district else it.district
            )
        }
    }

    fun fetchInstitutions() {
        if (institutionsRequested && _uiState.value.institutions.isNotEmpty()) return
        institutionsRequested = true
        viewModelScope.launch {
            try {
                val response = apiService.getInstitutions()
                _uiState.update { it.copy(institutions = response.institutions) }
            } catch (e: Exception) {
                institutionsRequested = false
            }
        }
    }
}
/** The catalogue does not change while the app runs; one fetch serves every screen. */
private var eduCatalogCache: com.neb.ians.data.api.ApiEduCatalog? = null
