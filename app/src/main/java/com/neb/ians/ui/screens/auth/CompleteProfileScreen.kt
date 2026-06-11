package com.neb.ians.ui.screens.auth

import android.app.DatePickerDialog
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
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
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.ui.layout.ContentScale
import coil.compose.rememberAsyncImagePainter
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.ProfileBanner
import com.neb.ians.ui.components.bannerPresetFor
import java.util.*

private val PRADESH_LIST = listOf("Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim")

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
    viewModel: CompleteProfileViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val scrollState = rememberScrollState()

    val isBannerUrlValid = uiState.bannerUrl.isBlank() || uiState.bannerUrl.startsWith("https://")

    val isFormValid = uiState.username.length >= 3 &&
        (uiState.usernameAvailable == true || (uiState.isEditing && uiState.username.isNotEmpty())) &&
        uiState.dob.isNotEmpty() &&
        uiState.displayName.isNotEmpty() &&
        isBannerUrlValid &&
        (uiState.role != "student" || uiState.classLevel.isNotEmpty()) &&
        (uiState.role != "teacher" || uiState.teachingSubjects.isNotEmpty()) &&
        (uiState.role != "institution" || uiState.school.isNotEmpty())

    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        uri?.let {
            val inputStream = context.contentResolver.openInputStream(it)
            val bytes = inputStream?.readBytes()
            if (bytes != null) {
                val mimeType = context.contentResolver.getType(it) ?: "image/jpeg"
                viewModel.uploadProfilePhoto(bytes, "profile_photo", mimeType)
            }
        }
    }

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
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp)
                .verticalScroll(scrollState)
        ) {
            if (!uiState.isEditing) {
                Spacer(modifier = Modifier.height(24.dp))
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
                    containerColor = MaterialTheme.colorScheme.surface
                ),
                shape = RoundedCornerShape(16.dp),
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(20.dp)
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
                                    .size(80.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape),
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
                                    onClick = { imagePickerLauncher.launch("image/*") },
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
                                    Text("Upload Photo", fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                                }
                                Text(
                                    text = "JPG, PNG or WebP. Max 5MB.",
                                    fontSize = 11.sp,
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
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            listOf("student", "teacher", "institution").forEach { r ->
                                val isSelected = uiState.role == r
                                val label = r.replaceFirstChar { it.uppercase() }
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .clip(RoundedCornerShape(24.dp))
                                        .background(
                                            if (isSelected) MaterialTheme.colorScheme.primaryContainer
                                            else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                                        )
                                        .clickable { viewModel.onRoleChange(r) }
                                        .padding(vertical = 12.dp, horizontal = 8.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = label,
                                        color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer
                                                else MaterialTheme.colorScheme.onSurface,
                                        fontWeight = FontWeight.SemiBold,
                                        fontSize = 14.sp
                                    )
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        val isExplorerSelected = uiState.role == "explorer"
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(24.dp))
                                .background(
                                    if (isExplorerSelected) Color(0xFFFFF7ED)
                                    else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                                )
                                .border(
                                    width = 1.dp,
                                    color = if (isExplorerSelected) Color(0xFFF97316) else Color.Transparent,
                                    shape = RoundedCornerShape(24.dp)
                                )
                                .clickable { viewModel.onRoleChange("explorer") }
                                .padding(vertical = 12.dp, horizontal = 24.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = "Explorer",
                                color = if (isExplorerSelected) Color(0xFFEA580C) else MaterialTheme.colorScheme.onSurface,
                                fontWeight = FontWeight.SemiBold,
                                fontSize = 14.sp
                            )
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
                            isError = uiState.usernameError != null || uiState.usernameAvailable == false,
                            supportingText = {
                                when {
                                    uiState.usernameError != null -> Text(uiState.usernameError!!)
                                    uiState.usernameAvailable == true -> Text("Username is available", color = MaterialTheme.colorScheme.primary)
                                    uiState.usernameAvailable == false -> Text("Username is already taken", color = MaterialTheme.colorScheme.error)
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

                    // Date of Birth * and Gender *
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        // Date of Birth
                        Column(modifier = Modifier.weight(1f)) {
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
                                    .clickable { datePickerDialog.show() }
                            ) {
                                OutlinedTextField(
                                    value = uiState.dob,
                                    onValueChange = {},
                                    readOnly = true,
                                    placeholder = { Text("YYYY-MM-DD") },
                                    trailingIcon = { Icon(Icons.Default.DateRange, contentDescription = null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    enabled = false,
                                    colors = OutlinedTextFieldDefaults.colors(
                                        disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                        disabledBorderColor = MaterialTheme.colorScheme.outline,
                                        disabledTrailingIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                                        disabledPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant
                                    ),
                                    shape = RoundedCornerShape(12.dp)
                                )
                            }
                        }

                        // Gender
                        var genderExpanded by remember { mutableStateOf(false) }
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Gender *",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            ExposedDropdownMenuBox(
                                expanded = genderExpanded,
                                onExpandedChange = { genderExpanded = !genderExpanded },
                                modifier = Modifier.padding(top = 4.dp)
                            ) {
                                OutlinedTextField(
                                    value = uiState.gender,
                                    onValueChange = {},
                                    readOnly = true,
                                    placeholder = { Text("Select gender") },
                                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = genderExpanded) },
                                    modifier = Modifier
                                        .menuAnchor()
                                        .fillMaxWidth(),
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp)
                                )
                                ExposedDropdownMenu(
                                    expanded = genderExpanded,
                                    onDismissRequest = { genderExpanded = false }
                                ) {
                                    listOf("Male", "Female", "Other").forEach { g ->
                                        DropdownMenuItem(
                                            text = { Text(g) },
                                            onClick = {
                                                viewModel.onGenderChange(g)
                                                genderExpanded = false
                                            }
                                        )
                                    }
                                }
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
                            var instTypeExpanded by remember { mutableStateOf(false) }
                            Column {
                                Text(
                                    text = "Institution Type *",
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                ExposedDropdownMenuBox(
                                    expanded = instTypeExpanded,
                                    onExpandedChange = { instTypeExpanded = !instTypeExpanded },
                                    modifier = Modifier.padding(top = 4.dp)
                                ) {
                                    val displayedText = uiState.institutionType.replaceFirstChar { it.uppercase() }
                                    OutlinedTextField(
                                        value = displayedText,
                                        onValueChange = {},
                                        readOnly = true,
                                        placeholder = { Text("Select type") },
                                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = instTypeExpanded) },
                                        modifier = Modifier
                                            .menuAnchor()
                                            .fillMaxWidth(),
                                        singleLine = true,
                                        shape = RoundedCornerShape(12.dp)
                                    )
                                    ExposedDropdownMenu(
                                        expanded = instTypeExpanded,
                                        onDismissRequest = { instTypeExpanded = false }
                                    ) {
                                        listOf("school", "college", "academy", "other").forEach { t ->
                                            DropdownMenuItem(
                                                text = { Text(t.replaceFirstChar { it.uppercase() }) },
                                                onClick = {
                                                    viewModel.onInstitutionTypeChange(t)
                                                    instTypeExpanded = false
                                                }
                                            )
                                        }
                                    }
                                }
                            }
                        }
                        "explorer" -> {
                            val outlineColor = MaterialTheme.colorScheme.outline
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .drawBehind {
                                        val stroke = Stroke(
                                            width = 1.dp.toPx(),
                                            pathEffect = PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                                        )
                                        drawRoundRect(
                                            color = outlineColor,
                                            style = stroke,
                                            cornerRadius = CornerRadius(12.dp.toPx())
                                        )
                                    }
                                    .background(
                                        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f),
                                        shape = RoundedCornerShape(12.dp)
                                    )
                                    .padding(14.dp)
                            ) {
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                                    verticalAlignment = Alignment.Top
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.TravelExplore,
                                        contentDescription = null,
                                        tint = MaterialTheme.colorScheme.tertiary,
                                        modifier = Modifier.size(20.dp)
                                    )
                                    Text(
                                        text = "You're exploring NEBians for now. You can update your role to Student, Teacher, or Institution anytime from this page.",
                                        fontSize = 14.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }

                    // Class / Level and Province
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        // Class / Level
                        var classExpanded by remember { mutableStateOf(false) }
                        val isStudent = uiState.role == "student"
                        val classLabel = if (isStudent) "Class *" else "Class / Level"
                        val classOptions = if (isStudent) STUDENT_CLASS_OPTIONS else TEACHER_CLASS_OPTIONS

                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = classLabel,
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            ExposedDropdownMenuBox(
                                expanded = classExpanded,
                                onExpandedChange = { classExpanded = !classExpanded },
                                modifier = Modifier.padding(top = 4.dp)
                            ) {
                                OutlinedTextField(
                                    value = uiState.classLevel,
                                    onValueChange = {},
                                    readOnly = true,
                                    placeholder = { Text("Select class") },
                                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = classExpanded) },
                                    modifier = Modifier
                                        .menuAnchor()
                                        .fillMaxWidth(),
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp)
                                )
                                ExposedDropdownMenu(
                                    expanded = classExpanded,
                                    onDismissRequest = { classExpanded = false }
                                ) {
                                    classOptions.forEach { opt ->
                                        DropdownMenuItem(
                                            text = { Text(opt) },
                                            onClick = {
                                                viewModel.onClassChange(opt)
                                                classExpanded = false
                                            }
                                        )
                                    }
                                }
                            }
                        }

                        // Province
                        var pradeshExpanded by remember { mutableStateOf(false) }
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Province",
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            ExposedDropdownMenuBox(
                                expanded = pradeshExpanded,
                                onExpandedChange = { pradeshExpanded = !pradeshExpanded },
                                modifier = Modifier.padding(top = 4.dp)
                            ) {
                                OutlinedTextField(
                                    value = uiState.pradesh,
                                    onValueChange = {},
                                    readOnly = true,
                                    placeholder = { Text("Select") },
                                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = pradeshExpanded) },
                                    modifier = Modifier
                                        .menuAnchor()
                                        .fillMaxWidth(),
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp)
                                )
                                ExposedDropdownMenu(
                                    expanded = pradeshExpanded,
                                    onDismissRequest = { pradeshExpanded = false }
                                ) {
                                    PRADESH_LIST.forEach { pradesh ->
                                        DropdownMenuItem(
                                            text = { Text(pradesh) },
                                            onClick = {
                                                viewModel.onPradeshChange(pradesh)
                                                pradeshExpanded = false
                                            }
                                        )
                                    }
                                }
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
                        OutlinedTextField(
                            value = uiState.district,
                            onValueChange = viewModel::onDistrictChange,
                            placeholder = { Text("Your district") },
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
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
                        OutlinedTextField(
                            value = uiState.school,
                            onValueChange = viewModel::onSchoolChange,
                            placeholder = { Text(schoolPlaceholder) },
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
                    }

                    // Profile appearance — live banner preview + banner URL
                    Column {
                        Text(
                            text = "Profile appearance",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Spacer(modifier = Modifier.height(8.dp))

                        // Live preview: entered URL if valid, otherwise the
                        // role-themed animated gradient preset.
                        val previewProfile = remember(uiState.role) {
                            UserProfileResponse(id = "", role = uiState.role)
                        }
                        val previewPreset = remember(uiState.role) { bannerPresetFor(previewProfile) }
                        val previewUrl = uiState.bannerUrl.takeIf {
                            it.isNotBlank() && it.startsWith("https://")
                        }
                        ProfileBanner(
                            bannerUrl = previewUrl,
                            bannerType = previewPreset.first,
                            decoText = previewPreset.second,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(100.dp)
                        )

                        Spacer(modifier = Modifier.height(10.dp))
                        Text(
                            text = "Banner image URL",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        OutlinedTextField(
                            value = uiState.bannerUrl,
                            onValueChange = viewModel::onBannerUrlChange,
                            placeholder = { Text("https://example.com/banner.jpg (optional)") },
                            isError = !isBannerUrlValid,
                            supportingText = {
                                if (!isBannerUrlValid) {
                                    Text(
                                        "Banner URL must start with https://",
                                        color = MaterialTheme.colorScheme.error
                                    )
                                } else {
                                    Text("Leave blank for the role-themed gradient banner.")
                                }
                            },
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 4.dp),
                            shape = RoundedCornerShape(12.dp)
                        )
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
                        fontWeight = FontWeight.Bold,
                        fontSize = 15.sp
                    )
                }
            }

            if (uiState.submissionResult == false) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Failed to submit profile. Please check required fields.",
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                )
            }

            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}