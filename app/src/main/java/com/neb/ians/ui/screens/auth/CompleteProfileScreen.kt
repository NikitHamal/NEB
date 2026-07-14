package com.neb.ians.ui.screens.auth

import android.app.DatePickerDialog
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.ui.layout.ContentScale
import coil.compose.rememberAsyncImagePainter
import coil.compose.AsyncImage
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.ProfileBanner
import com.neb.ians.ui.components.bannerPresetFor
import com.neb.ians.ui.screens.profile.PhotoGalleryDialog
import java.util.*

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Link
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.ArrowDropDown

private val PRADESH_LIST = listOf("Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim")

private val DISTRICTS_LIST = listOf(
    "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", "Banke", "Bara", "Bardiya", "Bhaktapur",
    "Bhojpur", "Chitwan", "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading", "Dhankuta", "Dhanusha", "Dolakha",
    "Dolpa", "Doti", "Gorkha", "Gulmi", "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali", "Kalikot",
    "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok", "Khotang", "Lalitpur", "Lamjung", "Mahottari",
    "Makwanpur", "Manang", "Mustang", "Myagdi", "Nawalpur", "Nuwakot", "Okhaldhunga", "Palpa", "Panchthar", "Parasi",
    "Parbat", "Parsa", "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat", "Rolpa", "Rukum East", "Rukum West", "Rupandehi",
    "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu", "Sunsari",
    "Surkhet", "Syangja", "Tanahun", "Taplejung", "Terhathum", "Udayapur"
)

private val SUBJECTS_LIST = listOf(
    "English", "Nepali", "Mathematics", "Physics", "Chemistry",
    "Biology", "Computer Science", "Accountancy", "Economics", "Social Studies"
)

private val STUDENT_CLASS_OPTIONS = listOf(
    "Class 8", "Class 9", "Class 10 / SEE", "Class 11", "Class 12",
    "+2 Passout", "Diploma", "Bachelors", "Masters", "PhD", "Other"
)

private val TEACHER_CLASS_OPTIONS = listOf(
    "Class 11", "Class 12", "+2 Passout", "Diploma", "Bachelors", "Masters", "Other"
)

@OptIn(ExperimentalLayoutApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CompleteProfileScreen(
    onNavigateToHome: () -> Unit,
    onNavigateBack: (() -> Unit)? = null,
    isEditing: Boolean = false,
    viewModel: CompleteProfileViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val scrollState = rememberScrollState()

    LaunchedEffect(isEditing) {
        viewModel.setIsEditing(isEditing)
    }

    LaunchedEffect(Unit) {
        viewModel.fetchInstitutions()
    }

    var showGenderDialog by remember { mutableStateOf(false) }
    var showClassDialog by remember { mutableStateOf(false) }
    var showProvinceDialog by remember { mutableStateOf(false) }
    var showDistrictDialog by remember { mutableStateOf(false) }
    var showInstTypeDialog by remember { mutableStateOf(false) }
    var showSchoolDialog by remember { mutableStateOf(false) }

    val isFormValid = uiState.username.length >= 3 &&
        (uiState.usernameAvailable == true || (uiState.isEditing && uiState.username.isNotEmpty())) &&
        uiState.dob.isNotEmpty() &&
        uiState.displayName.isNotEmpty() &&
        (uiState.role != "student" || uiState.classLevel.isNotEmpty()) &&
        (uiState.role != "teacher" || uiState.teachingSubjects.isNotEmpty()) &&
        (uiState.role != "institution" || uiState.school.isNotEmpty())

    val isUsernameServerError = uiState.submissionError?.contains("username", ignoreCase = true) == true
    val isDobServerError = uiState.submissionError?.contains("date of birth", ignoreCase = true) == true || uiState.submissionError?.contains("dob", ignoreCase = true) == true
    val isDisplayNameServerError = uiState.submissionError?.contains("display name", ignoreCase = true) == true

    LaunchedEffect(uiState.submissionResult) {
        when (uiState.submissionResult) {
            true -> {
                if (uiState.isEditing && onNavigateBack != null) {
                    onNavigateBack()
                } else {
                    onNavigateToHome()
                }
            }
            false -> {}
            null -> {}
        }
    }

    Scaffold(
        topBar = {
            if (uiState.isEditing && onNavigateBack != null) {
                TopAppBar(
                    title = { Text("Edit Profile", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                )
            }
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp)
                .imePadding()
                .verticalScroll(scrollState)
        ) {
            if (!uiState.isEditing) {
                Spacer(modifier = Modifier.statusBarsPadding().height(24.dp))
                Text(
                    text = "Complete Your Profile",
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = "NEBians community requires username and basic info to provide relevant materials.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(top = 4.dp, bottom = 24.dp)
                )
            } else {
                Spacer(modifier = Modifier.height(16.dp))
            }

            Card(
                colors = CardDefaults.cardColors(
                    containerColor = Color.White
                ),
                shape = RoundedCornerShape(22.dp),
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // Profile Picture Section
                    Column {
                        Text(
                            text = "Profile Picture",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 8.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(16.dp)
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(64.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape)
                                    .clickable { viewModel.openPhotoGallery() },
                                contentAlignment = Alignment.Center
                            ) {
                                if (uiState.photoUrl.isNotEmpty()) {
                                    Image(
                                        painter = rememberAsyncImagePainter(uiState.photoUrl),
                                        contentDescription = "Avatar",
                                        modifier = Modifier.fillMaxSize(),
                                        contentScale = ContentScale.Crop
                                    )
                                } else {
                                    val initial = if (uiState.username.isNotEmpty()) uiState.username.take(1).uppercase() else "N"
                                    Text(
                                        text = initial,
                                        style = MaterialTheme.typography.headlineMedium,
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.primary
                                    )
                                }
                                if (uiState.isPhotoUploading) {
                                    CircularProgressIndicator(
                                        modifier = Modifier.size(24.dp),
                                        color = MaterialTheme.colorScheme.primary,
                                        strokeWidth = 2.dp
                                    )
                                }
                            }

                            Column(
                                verticalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                OutlinedButton(
                                    onClick = { viewModel.openPhotoGallery() },
                                    shape = RoundedCornerShape(20.dp),
                                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Upload,
                                        contentDescription = null,
                                        modifier = Modifier.size(18.dp)
                                    )
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("Manage photos", fontWeight = FontWeight.SemiBold, maxLines = 1)
                                }
                                Text(
                                    text = "JPG, PNG or WebP. Max 5MB.",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }

                    // Role Selector: I am a...
                    Column {
                        Text(
                            text = "I am a...",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            ProfileRoleOption("Student", "Learn, ask, and save resources", uiState.role == "student") { viewModel.onRoleChange("student") }
                            ProfileRoleOption("Teacher", "Teach, guide, and share resources", uiState.role == "teacher") { viewModel.onRoleChange("teacher") }
                            ProfileRoleOption("Institution", "Represent a school, college, or academy", uiState.role == "institution") { viewModel.onRoleChange("institution") }
                            ProfileRoleOption("Explorer", "Browse first and complete details later", uiState.role == "explorer") { viewModel.onRoleChange("explorer") }
                        }
                    }

                    // Username *
                    Column {
                        Text(
                            text = "Username *",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        OutlinedTextField(
                            value = uiState.username,
                            onValueChange = viewModel::onUsernameChange,
                            placeholder = { Text("username") },
                            trailingIcon = {
                                when {
                                    uiState.isCheckingUsername -> CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                                    uiState.usernameAvailable == true || (uiState.isEditing && uiState.username.isNotEmpty() && uiState.usernameError == null && uiState.usernameAvailable == null) ->
                                        Icon(Icons.Default.Check, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                    uiState.usernameAvailable == false || uiState.usernameError != null ->
                                        Icon(Icons.Default.Warning, contentDescription = null, tint = MaterialTheme.colorScheme.error)
                                }
                            },
                            isError = uiState.usernameError != null || uiState.usernameAvailable == false || isUsernameServerError,
                            supportingText = {
                                when {
                                    uiState.usernameError != null -> Text(uiState.usernameError!!)
                                    uiState.usernameAvailable == true -> Text("Username is available", color = MaterialTheme.colorScheme.primary)
                                    uiState.usernameAvailable == false -> Text("Username is already taken", color = MaterialTheme.colorScheme.error)
                                    isUsernameServerError -> Text(uiState.submissionError!!, color = MaterialTheme.colorScheme.error)
                                }
                            },
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
                    }

                    // Display Name *
                    Column {
                        Text(
                            text = "Display Name *",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        OutlinedTextField(
                            value = uiState.displayName,
                            onValueChange = viewModel::onDisplayNameChange,
                            placeholder = { Text("Your full name") },
                            isError = isDisplayNameServerError,
                            supportingText = if (isDisplayNameServerError) {
                                { Text(uiState.submissionError!!, color = MaterialTheme.colorScheme.error) }
                            } else null,
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
                    }

                    // Email
                    Column {
                        Text(
                            text = "Email",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        OutlinedTextField(
                            value = uiState.email,
                            onValueChange = viewModel::onEmailChange,
                            placeholder = { Text("example@domain.com") },
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
                    }

                    // Bio
                    Column {
                        Text(
                            text = "Bio",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        OutlinedTextField(
                            value = uiState.bio,
                            onValueChange = viewModel::onBioChange,
                            placeholder = { Text("Tell others about yourself...") },
                            minLines = 3,
                            maxLines = 5,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
                    }

                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        Column {
                            Text(
                                text = "Date of Birth *",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            val calendar = Calendar.getInstance()
                            val datePickerDialog = DatePickerDialog(
                                context,
                                { _, year, month, dayOfMonth ->
                                    val m = if (month + 1 < 10) "0${month + 1}" else "${month + 1}"
                                    val d = if (dayOfMonth < 10) "0$dayOfMonth" else "$dayOfMonth"
                                    viewModel.onDobChange("$year-$m-$d")
                                },
                                calendar.get(Calendar.YEAR) - 17,
                                calendar.get(Calendar.MONTH),
                                calendar.get(Calendar.DAY_OF_MONTH)
                            )
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(top = 4.dp)
                            ) {
                                OutlinedTextField(
                                    value = uiState.dob,
                                    onValueChange = {},
                                    readOnly = true,
                                    placeholder = { Text("YYYY-MM-DD", maxLines = 1) },
                                    trailingIcon = { Icon(Icons.Default.DateRange, contentDescription = null) },
                                    isError = isDobServerError,
                                    supportingText = if (isDobServerError) {
                                        { Text(uiState.submissionError!!, color = MaterialTheme.colorScheme.error) }
                                    } else null,
                                    modifier = Modifier.fillMaxWidth(),
                                    enabled = false,
                                    singleLine = true,
                                    colors = OutlinedTextFieldDefaults.colors(
                                        disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                        disabledBorderColor = if (isDobServerError) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.outline,
                                        disabledTrailingIconColor = if (isDobServerError) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurfaceVariant,
                                        disabledPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant
                                    ),
                                    shape = RoundedCornerShape(12.dp)
                                )
                                Box(
                                    modifier = Modifier
                                        .matchParentSize()
                                        .clickable { datePickerDialog.show() }
                                )
                            }
                        }

                        Column {
                            Text(
                                text = "Gender *",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(top = 4.dp)
                                    .clickable { showGenderDialog = true }
                            ) {
                                OutlinedTextField(
                                    value = uiState.gender,
                                    onValueChange = {},
                                    readOnly = true,
                                    enabled = false,
                                    placeholder = { Text("Select gender", maxLines = 1) },
                                    trailingIcon = { Icon(Icons.Default.ArrowDropDown, null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = OutlinedTextFieldDefaults.colors(
                                        disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                        disabledBorderColor = MaterialTheme.colorScheme.outline,
                                        disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant
                                    ),
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp)
                                )
                            }
                            if (showGenderDialog) {
                                SelectionDialog(
                                    title = "Select Gender",
                                    options = listOf("Male", "Female", "Other"),
                                    onDismiss = { showGenderDialog = false },
                                    onSelect = viewModel::onGenderChange
                                )
                            }
                        }
                    }

                    // Role-specific field boxes
                    when (uiState.role) {
                        "student" -> {
                            Column {
                                Text(
                                    text = "Subjects",
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                FlowRow(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    verticalArrangement = Arrangement.spacedBy(4.dp)
                                ) {
                                    SUBJECTS_LIST.forEach { subj ->
                                        val isSelected = uiState.subjects.contains(subj)
                                        FilterChip(
                                            selected = isSelected,
                                            onClick = { viewModel.onSubjectToggle(subj) },
                                            label = { Text(subj, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                            shape = RoundedCornerShape(50),
                                            leadingIcon = if (isSelected) {
                                                { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                                            } else null
                                        )
                                    }
                                }
                            }
                        }
                        "teacher" -> {
                            Column {
                                Text(
                                    text = "Teaching Subjects *",
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                FlowRow(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    verticalArrangement = Arrangement.spacedBy(4.dp)
                                ) {
                                    SUBJECTS_LIST.forEach { subj ->
                                        val isSelected = uiState.teachingSubjects.contains(subj)
                                        FilterChip(
                                            selected = isSelected,
                                            onClick = { viewModel.onTeachingSubjectToggle(subj) },
                                            label = { Text(subj, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                            shape = RoundedCornerShape(50),
                                            leadingIcon = if (isSelected) {
                                                { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                                            } else null
                                        )
                                    }
                                }
                            }
                        }
                        "institution" -> {
                            Column {
                                Text(
                                    text = "Institution Type *",
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(top = 4.dp)
                                        .clickable { showInstTypeDialog = true }
                                ) {
                                    val displayedText = uiState.institutionType.replaceFirstChar { it.uppercase() }
                                    OutlinedTextField(
                                        value = displayedText,
                                        onValueChange = {},
                                        readOnly = true,
                                        enabled = false,
                                        placeholder = { Text("Select type") },
                                        trailingIcon = { Icon(Icons.Default.ArrowDropDown, null) },
                                        modifier = Modifier.fillMaxWidth(),
                                        colors = OutlinedTextFieldDefaults.colors(
                                            disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                            disabledBorderColor = MaterialTheme.colorScheme.outline,
                                            disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant
                                        ),
                                        singleLine = true,
                                        shape = RoundedCornerShape(12.dp)
                                    )
                                }
                                if (showInstTypeDialog) {
                                    SelectionDialog(
                                        title = "Select Institution Type",
                                        options = listOf("school", "college", "academy", "other").map { it.replaceFirstChar { c -> c.uppercase() } },
                                        onDismiss = { showInstTypeDialog = false },
                                        onSelect = { viewModel.onInstitutionTypeChange(it.lowercase()) }
                                    )
                                }
                            }
                        }
                        "explorer" -> Unit
                        }

                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        // Class / Level
                        val isStudent = uiState.role == "student"
                        val classLabel = if (isStudent) "Class *" else "Class / Level"
                        val classOptions = if (isStudent) STUDENT_CLASS_OPTIONS else TEACHER_CLASS_OPTIONS

                        Column {
                            Text(
                                text = classLabel,
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(top = 4.dp)
                                    .clickable { showClassDialog = true }
                            ) {
                                OutlinedTextField(
                                    value = uiState.classLevel,
                                    onValueChange = {},
                                    readOnly = true,
                                    enabled = false,
                                    placeholder = { Text("Select class") },
                                    trailingIcon = { Icon(Icons.Default.ArrowDropDown, null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = OutlinedTextFieldDefaults.colors(
                                        disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                        disabledBorderColor = MaterialTheme.colorScheme.outline,
                                        disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant
                                    ),
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp)
                                )
                            }
                            if (showClassDialog) {
                                SelectionDialog(
                                    title = "Select Class / Level",
                                    options = classOptions,
                                    onDismiss = { showClassDialog = false },
                                    onSelect = viewModel::onClassChange
                                )
                            }
                        }

                        // Province
                        Column {
                            Text(
                                text = "Province",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(top = 4.dp)
                                    .clickable { showProvinceDialog = true }
                            ) {
                                OutlinedTextField(
                                    value = uiState.pradesh,
                                    onValueChange = {},
                                    readOnly = true,
                                    enabled = false,
                                    placeholder = { Text("Select") },
                                    trailingIcon = { Icon(Icons.Default.ArrowDropDown, null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = OutlinedTextFieldDefaults.colors(
                                        disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                        disabledBorderColor = MaterialTheme.colorScheme.outline,
                                        disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant
                                    ),
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp)
                                )
                            }
                            if (showProvinceDialog) {
                                SelectionDialog(
                                    title = "Select Province",
                                    options = PRADESH_LIST,
                                    onDismiss = { showProvinceDialog = false },
                                    onSelect = viewModel::onPradeshChange
                                )
                            }
                        }
                    }

                    // District
                    Column {
                        Text(
                            text = "District",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp)
                                .clickable { showDistrictDialog = true }
                        ) {
                            OutlinedTextField(
                                value = uiState.district,
                                onValueChange = {},
                                readOnly = true,
                                enabled = false,
                                placeholder = { Text("Select District") },
                                trailingIcon = { Icon(Icons.Default.ArrowDropDown, null) },
                                modifier = Modifier.fillMaxWidth(),
                                colors = OutlinedTextFieldDefaults.colors(
                                    disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                    disabledBorderColor = MaterialTheme.colorScheme.outline,
                                    disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant
                                ),
                                singleLine = true,
                                shape = RoundedCornerShape(12.dp)
                            )
                        }
                        if (showDistrictDialog) {
                            SelectionDialog(
                                title = "Select District",
                                options = DISTRICTS_LIST,
                                showSearch = true,
                                onDismiss = { showDistrictDialog = false },
                                onSelect = viewModel::onDistrictChange
                            )
                        }
                    }

                    // School/College
                    val schoolLabel = when (uiState.role) {
                        "institution" -> "Institution Name *"
                        else -> "School/College"
                    }
                    val schoolPlaceholder = when (uiState.role) {
                        "student" -> "Your school or college name"
                        "teacher" -> "Where you teach"
                        "institution" -> "Official institution name"
                        "explorer" -> "Your school or college name (optional)"
                        else -> "Your school or college name"
                    }
                    Column {
                        Text(
                            text = schoolLabel,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp)
                                .clickable { showSchoolDialog = true }
                        ) {
                            OutlinedTextField(
                                value = uiState.school,
                                onValueChange = {},
                                readOnly = true,
                                enabled = false,
                                placeholder = { Text(schoolPlaceholder) },
                                modifier = Modifier.fillMaxWidth(),
                                colors = OutlinedTextFieldDefaults.colors(
                                    disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                    disabledBorderColor = MaterialTheme.colorScheme.outline
                                ),
                                singleLine = true,
                                shape = RoundedCornerShape(12.dp)
                            )
                            if (uiState.school.isNotEmpty()) {
                                IconButton(
                                    onClick = { viewModel.onSchoolChange("", "") },
                                    modifier = Modifier
                                        .align(Alignment.CenterEnd)
                                        .padding(end = 4.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Clear,
                                        contentDescription = "Clear School",
                                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            } else {
                                Icon(
                                    imageVector = Icons.Default.ArrowDropDown,
                                    contentDescription = null,
                                    modifier = Modifier
                                        .align(Alignment.CenterEnd)
                                        .padding(end = 12.dp),
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                        if (showSchoolDialog) {
                            SchoolSelectionDialog(
                                institutions = uiState.institutions,
                                initialValue = uiState.school,
                                onDismiss = { showSchoolDialog = false },
                                onSelect = { name, username ->
                                    viewModel.onSchoolChange(name, username)
                                }
                            )
                        }
                    }



                    // Lock Profile Switch Toggle
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Lock Profile (private)",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                        Switch(
                            checked = uiState.isLocked,
                            onCheckedChange = viewModel::onLockedChange
                        )
                    }
                }
            }

            if (uiState.isEditing) {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = "Social Links",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(8.dp))

                if (uiState.socialLinks.isEmpty()) {
                    Text(
                        text = "No social links added yet.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        uiState.socialLinks.forEach { link ->
                            Surface(
                                shape = RoundedCornerShape(12.dp),
                                color = MaterialTheme.colorScheme.surfaceContainerLow,
                                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        painter = when (link.platform.lowercase()) {
                                            "github" -> painterResource(id = R.drawable.ic_github)
                                            else -> painterResource(id = R.drawable.ic_globe)
                                        },
                                        contentDescription = null,
                                        tint = MaterialTheme.colorScheme.primary,
                                        modifier = Modifier.size(20.dp)
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(
                                            text = link.platformLabel.ifBlank { link.platform.replaceFirstChar { it.uppercase() } },
                                            fontWeight = FontWeight.Bold,
                                            style = MaterialTheme.typography.bodyMedium
                                        )
                                        Text(
                                            text = link.url,
                                            style = MaterialTheme.typography.bodySmall,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }
                                    IconButton(
                                        onClick = { viewModel.deleteSocialLink(link.id) },
                                        modifier = Modifier.size(36.dp)
                                    ) {
                                        Icon(
                                            imageVector = Icons.Default.Delete,
                                            contentDescription = "Delete link",
                                            tint = MaterialTheme.colorScheme.error,
                                            modifier = Modifier.size(20.dp)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                var showAddLinkDialog by remember { mutableStateOf(false) }
                OutlinedButton(
                    onClick = { showAddLinkDialog = true },
                    modifier = Modifier.fillMaxWidth().height(44.dp),
                    shape = RoundedCornerShape(22.dp)
                ) {
                    Icon(Icons.Default.Add, null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Add Social Link", fontWeight = FontWeight.Bold)
                }

                if (showAddLinkDialog) {
                    var selectedPlatformDisplay by remember { mutableStateOf("Instagram") }
                    val selectedPlatformKey = remember(selectedPlatformDisplay) {
                        when (selectedPlatformDisplay) {
                            "X (Twitter)" -> "twitter"
                            "Website / Custom" -> "website"
                            else -> selectedPlatformDisplay.lowercase()
                        }
                    }
                    var urlOrUsername by remember { mutableStateOf("") }
                    var label by remember { mutableStateOf("") }
                    var showPlatformDropdown by remember { mutableStateOf(false) }

                    val prompt = remember(selectedPlatformKey) {
                        when (selectedPlatformKey) {
                            "instagram" -> Triple("Username or Link", "e.g. username or https://...", "We will automatically format this into an Instagram profile link.")
                            "facebook" -> Triple("Username or Link", "e.g. username or https://...", "We will format this into a Facebook profile link.")
                            "twitter" -> Triple("Username or Link", "e.g. username or https://...", "X (Twitter) handle or full URL.")
                            "youtube" -> Triple("Channel Username or Link", "e.g. channel_name or https://...", "YouTube username or channel URL.")
                            "tiktok" -> Triple("Username or Link", "e.g. username or https://...", "TikTok username or profile URL.")
                            "linkedin" -> Triple("Username or Link", "e.g. username or https://...", "LinkedIn profile link or username.")
                            "github" -> Triple("Username or Link", "e.g. username or https://...", "GitHub username or link.")
                            "telegram" -> Triple("Username or Link", "e.g. username or https://...", "Telegram username or link.")
                            "whatsapp" -> Triple("Phone Number or Link", "e.g. 98XXXXXXXX or https://...", "WhatsApp phone number or direct chat link.")
                            "discord" -> Triple("Invite Link or Username", "e.g. username or https://...", "Discord server invite link or username.")
                            "snapchat" -> Triple("Username or Link", "e.g. username or https://...", "Snapchat username or profile link.")
                            "pinterest" -> Triple("Username or Link", "e.g. username or https://...", "Pinterest username or profile link.")
                            "reddit" -> Triple("Username or Link", "e.g. username or https://...", "Reddit username or profile link.")
                            else -> Triple("Website URL", "e.g. https://mywebsite.com", "Enter your full custom website URL.")
                        }
                    }

                    AlertDialog(
                        onDismissRequest = { showAddLinkDialog = false },
                        title = { Text("Add Social Link", fontWeight = FontWeight.Bold) },
                        text = {
                            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable { showPlatformDropdown = true }
                                ) {
                                    OutlinedTextField(
                                        value = selectedPlatformDisplay,
                                        onValueChange = {},
                                        readOnly = true,
                                        enabled = false,
                                        label = { Text("Platform") },
                                        trailingIcon = { Icon(Icons.Default.ArrowDropDown, null) },
                                        modifier = Modifier.fillMaxWidth(),
                                        colors = OutlinedTextFieldDefaults.colors(
                                            disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                            disabledBorderColor = MaterialTheme.colorScheme.outline,
                                            disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                                            disabledLabelColor = MaterialTheme.colorScheme.onSurfaceVariant
                                        ),
                                        shape = RoundedCornerShape(12.dp)
                                    )
                                }
                                if (showPlatformDropdown) {
                                    SelectionDialog(
                                        title = "Select Platform",
                                        options = listOf("Instagram", "Facebook", "X (Twitter)", "YouTube", "TikTok", "LinkedIn", "GitHub", "Telegram", "WhatsApp", "Discord", "Snapchat", "Pinterest", "Reddit", "Website / Custom"),
                                        onDismiss = { showPlatformDropdown = false },
                                        onSelect = { selectedPlatformDisplay = it }
                                    )
                                }

                                OutlinedTextField(
                                    value = urlOrUsername,
                                    onValueChange = { urlOrUsername = it },
                                    label = { Text(prompt.first) },
                                    placeholder = { Text(prompt.second) },
                                    singleLine = true,
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(12.dp)
                                )

                                Text(
                                    text = prompt.third,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )

                                if (selectedPlatformKey == "website") {
                                    OutlinedTextField(
                                        value = label,
                                        onValueChange = { label = it },
                                        label = { Text("Label (optional)") },
                                        placeholder = { Text("e.g. My Portfolio") },
                                        singleLine = true,
                                        modifier = Modifier.fillMaxWidth(),
                                        shape = RoundedCornerShape(12.dp)
                                    )
                                }
                            }
                        },
                        confirmButton = {
                            Button(
                                onClick = {
                                    if (urlOrUsername.isNotBlank()) {
                                        viewModel.addSocialLink(selectedPlatformKey, urlOrUsername, label)
                                        showAddLinkDialog = false
                                    }
                                }
                            ) {
                                Text("Add")
                            }
                        },
                        dismissButton = {
                            TextButton(onClick = { showAddLinkDialog = false }) {
                                Text("Cancel")
                            }
                        }
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = viewModel::submitProfile,
                enabled = isFormValid && !uiState.isSubmitting,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                shape = RoundedCornerShape(25.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                if (uiState.isSubmitting) {
                    CircularProgressIndicator(
                        color = MaterialTheme.colorScheme.onPrimary,
                        modifier = Modifier.size(24.dp),
                        strokeWidth = 2.dp
                    )
                } else {
                    Text(
                        text = if (uiState.isEditing) "Save Profile" else "Register & Enter NEBians",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            if (uiState.submissionResult == false) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = uiState.submissionError ?: "Failed to submit profile. Please check required fields.",
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                )
            }

            Spacer(modifier = Modifier.navigationBarsPadding().height(48.dp))
        }
    }

    if (uiState.showPhotoGallery) {
        PhotoGalleryDialog(
            photos = uiState.photos,
            isLoading = uiState.photosLoading,
            isBusy = uiState.photoBusy || uiState.isPhotoUploading,
            onDismiss = viewModel::closePhotoGallery,
            onActivatePhoto = viewModel::activatePhoto,
            onUploadPhoto = viewModel::uploadPhoto
        )
    }

}
@Composable
private fun ProfileRoleOption(
    title: String,
    subtitle: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        color = if (selected) MaterialTheme.colorScheme.primaryContainer else Color.White,
        border = BorderStroke(1.dp, if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            RadioButton(selected = selected, onClick = onClick)
            Column(modifier = Modifier.weight(1f)) {
                Text(title, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(subtitle, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
        }
    }
}

@Composable
private fun SelectionDialog(
    title: String,
    options: List<String>,
    onDismiss: () -> Unit,
    onSelect: (String) -> Unit,
    showSearch: Boolean = false
) {
    var searchQuery by remember { mutableStateOf("") }
    val filteredOptions = remember(searchQuery, options) {
        if (showSearch) {
            options.filter { it.contains(searchQuery, ignoreCase = true) }
        } else {
            options
        }
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                if (showSearch) {
                    OutlinedTextField(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        placeholder = { Text("Search...") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
                LazyColumn(modifier = Modifier.heightIn(max = 280.dp)) {
                    items(filteredOptions) { opt ->
                        Text(
                            text = opt,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    onSelect(opt)
                                    onDismiss()
                                }
                                .padding(vertical = 12.dp, horizontal = 4.dp),
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
private fun SchoolSelectionDialog(
    institutions: List<com.neb.ians.data.api.ApiInstitution>,
    initialValue: String,
    onDismiss: () -> Unit,
    onSelect: (schoolName: String, username: String) -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    var customName by remember { mutableStateOf(initialValue) }

    val filtered = remember(searchQuery, institutions) {
        institutions.filter {
            it.displayName.contains(searchQuery, ignoreCase = true) ||
            it.username.contains(searchQuery, ignoreCase = true)
        }
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Select School / Institution", fontWeight = FontWeight.Bold) },
        text = {
            Column(
                modifier = Modifier.fillMaxWidth().heightIn(max = 350.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    placeholder = { Text("Search institutions...") },
                    leadingIcon = { Icon(Icons.Default.Search, null) },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )

                LazyColumn(
                    modifier = Modifier.weight(1f).fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(filtered) { inst ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    onSelect(inst.displayName, inst.username)
                                    onDismiss()
                                }
                                .padding(8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            AsyncImage(
                                model = inst.photoUrl.ifBlank { "https://nebians.consica.com.np/static/web/images/default_avatar.png" },
                                contentDescription = null,
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant),
                                contentScale = ContentScale.Crop
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Column {
                                Text(inst.displayName, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.bodyMedium)
                                Text("@${inst.username}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                    if (filtered.isEmpty() && searchQuery.isNotBlank()) {
                        item {
                            Text(
                                text = "No platform institutions match search.",
                                style = MaterialTheme.typography.bodySmall,
                                modifier = Modifier.padding(8.dp),
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }

                Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(MaterialTheme.colorScheme.outlineVariant))

                Column {
                    Text("Or type custom school name:", style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold)
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(top = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        OutlinedTextField(
                            value = customName,
                            onValueChange = { customName = it },
                            placeholder = { Text("Custom school/college name") },
                            singleLine = true,
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Button(
                            onClick = {
                                onSelect(customName, "")
                                onDismiss()
                            },
                            enabled = customName.isNotBlank()
                        ) {
                            Text("Use")
                        }
                    }
                }
            }
        },
        confirmButton = {
            if (initialValue.isNotBlank()) {
                TextButton(
                    onClick = {
                        onSelect("", "")
                        onDismiss()
                    }
                ) {
                    Text("Clear Selection", color = MaterialTheme.colorScheme.error)
                }
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Close")
            }
        }
    )
}
