package com.neb.ians.ui.screens.auth

import android.app.DatePickerDialog
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import java.util.*

private val PRADESH_LIST = listOf("Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim")

private val DISTRICT_MAP = mapOf(
    "Koshi" to listOf("Taplejung", "Panchthar", "Ilam", "Jhapa", "Sankhuwasabha", "Tehrathum", "Bhojpur", "Dhankuta", "Morang", "Sunsari", "Solukhumbu", "Khotang", "Okhaldhunga", "Udayapur"),
    "Madhesh" to listOf("Saptari", "Siraha", "Dhanusha", "Mahottari", "Sarlahi", "Rautahat", "Bara", "Parsa"),
    "Bagmati" to listOf("Kathmandu", "Bhaktapur", "Lalitpur", "Dolakha", "Sindhupalchok", "Rasuwa", "Dhading", "Nuwakot", "Kavrepalanchok", "Ramechhap", "Sindhuli", "Makwanpur", "Chitwan"),
    "Gandaki" to listOf("Kaski", "Gorkha", "Manang", "Mustang", "Myagdi", "Lamjung", "Tanahun", "Syangja", "Parbat", "Baglung", "Nawalpur"),
    "Lumbini" to listOf("Rupandehi", "Kapilvastu", "Palpa", "Arghakhanchi", "Gulmi", "Pyuthan", "Rolpa", "Rukum East", "Nawalparasi West", "Bardiya", "Banke", "Dang"),
    "Karnali" to listOf("Surkhet", "Rukum West", "Salyan", "Dolpa", "Jumla", "Mugu", "Humla", "Kalikot", "Jajarkot", "Dailekh"),
    "Sudurpashchim" to listOf("Kailali", "Kanchanpur", "Dadeldhura", "Baitadi", "Darchula", "Bajhang", "Bajura", "Doti", "Achham")
)

private val SUBJECTS_LIST = listOf(
    "English", "Nepali", "Mathematics", "Physics", "Chemistry",
    "Biology", "Computer Science", "Accountancy", "Economics", "Social Studies"
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

    val isFormValid = uiState.username.length >= 3 &&
        (uiState.usernameAvailable == true || (uiState.isEditing && uiState.username == uiState.username)) &&
        uiState.dob.isNotEmpty()

    LaunchedEffect(uiState.submissionResult) {
        when (uiState.submissionResult) {
            true -> {
                if (uiState.isEditing && onNavigateBack != null) {
                    onNavigateBack()
                } else {
                    onNavigateToHome()
                }
            }
            false -> {
                // Show nothing here — handled by the button state
            }
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
                Spacer(modifier = Modifier.height(16.dp))
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
            }

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = uiState.username,
                onValueChange = viewModel::onUsernameChange,
                label = { Text("Username") },
                leadingIcon = { Icon(Icons.Default.Email, contentDescription = null) },
                trailingIcon = {
                    when {
                        uiState.isCheckingUsername -> CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                        uiState.usernameAvailable == true || (uiState.isEditing && uiState.username.isBlank()) ->
                            Icon(Icons.Default.Check, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        uiState.usernameAvailable == false || uiState.usernameError != null ->
                            Icon(Icons.Default.Warning, contentDescription = null, tint = MaterialTheme.colorScheme.error)
                    }
                },
                isError = uiState.usernameError != null || uiState.usernameAvailable == false,
                supportingText = {
                    when {
                        uiState.usernameError != null -> Text(uiState.usernameError!!)
                        uiState.isEditing && uiState.username.isBlank() -> Text("Your current username", color = MaterialTheme.colorScheme.primary)
                        uiState.usernameAvailable == true -> Text("Username is available", color = MaterialTheme.colorScheme.primary)
                        uiState.usernameAvailable == false -> Text("Username is already taken", color = MaterialTheme.colorScheme.error)
                    }
                },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            )

            Spacer(modifier = Modifier.height(12.dp))

            val calendar = Calendar.getInstance()
            val datePickerDialog = DatePickerDialog(
                context,
                { _, year, month, dayOfMonth ->
                    viewModel.onDobChange("$year-${month + 1}-$dayOfMonth")
                },
                calendar.get(Calendar.YEAR) - 17,
                calendar.get(Calendar.MONTH),
                calendar.get(Calendar.DAY_OF_MONTH)
            )

            OutlinedTextField(
                value = uiState.dob,
                onValueChange = {},
                readOnly = true,
                label = { Text("Date of Birth") },
                leadingIcon = { Icon(Icons.Default.DateRange, contentDescription = null) },
                placeholder = { Text("YYYY-MM-DD") },
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { datePickerDialog.show() },
                enabled = false,
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    disabledTextColor = MaterialTheme.colorScheme.onSurface,
                    disabledBorderColor = MaterialTheme.colorScheme.outline,
                    disabledLeadingIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    disabledLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    disabledPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant
                ),
                shape = RoundedCornerShape(12.dp)
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text("Gender", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(bottom = 6.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf("Male", "Female", "Other").forEach { gender ->
                    FilterChip(
                        selected = uiState.gender == gender,
                        onClick = { viewModel.onGenderChange(gender) },
                        label = { Text(gender, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                        shape = RoundedCornerShape(50),
                        leadingIcon = if (uiState.gender == gender) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text("Class", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(bottom = 6.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf("Class 11", "Class 12", "Both/Passout").forEach { classLvl ->
                    FilterChip(
                        selected = uiState.classLevel == classLvl,
                        onClick = { viewModel.onClassChange(classLvl) },
                        label = { Text(classLvl, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                        shape = RoundedCornerShape(50),
                        leadingIcon = if (uiState.classLevel == classLvl) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text("Subjects of Interest", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(bottom = 6.dp))
            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                SUBJECTS_LIST.forEach { subj ->
                    FilterChip(
                        selected = uiState.subjects.contains(subj),
                        onClick = { viewModel.onSubjectToggle(subj) },
                        label = { Text(subj, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                        shape = RoundedCornerShape(50),
                        leadingIcon = if (uiState.subjects.contains(subj)) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null
                    )
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            var pradeshExpanded by remember { mutableStateOf(false) }
            var districtExpanded by remember { mutableStateOf(false) }

            Text("Location", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(bottom = 6.dp))
            ExposedDropdownMenuBox(
                expanded = pradeshExpanded,
                onExpandedChange = { pradeshExpanded = !pradeshExpanded }
            ) {
                OutlinedTextField(
                    value = uiState.pradesh,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Pradesh / Province") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = pradeshExpanded) },
                    modifier = Modifier.menuAnchor().fillMaxWidth(),
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

            Spacer(modifier = Modifier.height(12.dp))

            val currentDistricts = DISTRICT_MAP[uiState.pradesh] ?: emptyList()

            LaunchedEffect(uiState.pradesh) {
                if (uiState.district !in currentDistricts && currentDistricts.isNotEmpty()) {
                    viewModel.onDistrictChange(currentDistricts.first())
                }
            }

            ExposedDropdownMenuBox(
                expanded = districtExpanded,
                onExpandedChange = { districtExpanded = !districtExpanded }
            ) {
                OutlinedTextField(
                    value = uiState.district,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("District") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = districtExpanded) },
                    modifier = Modifier.menuAnchor().fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp)
                )
                ExposedDropdownMenu(
                    expanded = districtExpanded,
                    onDismissRequest = { districtExpanded = false }
                ) {
                    currentDistricts.forEach { district ->
                        DropdownMenuItem(
                            text = { Text(district) },
                            onClick = {
                                viewModel.onDistrictChange(district)
                                districtExpanded = false
                            }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = uiState.school,
                onValueChange = viewModel::onSchoolChange,
                label = { Text("School / College Name") },
                leadingIcon = { Icon(androidx.compose.ui.res.painterResource(id = com.neb.ians.R.drawable.ic_school), contentDescription = null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            )

            Spacer(modifier = Modifier.height(20.dp))

            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceContainerHigh
                ),
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.Lock,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Lock Profile", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        }
                        Text(
                            text = "Keep profile details private. Only your username will be visible on posts.",
                            fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(top = 4.dp, end = 8.dp)
                        )
                    }
                    Switch(checked = uiState.isLocked, onCheckedChange = viewModel::onLockedChange)
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            Button(
                onClick = viewModel::submitProfile,
                enabled = isFormValid && !uiState.isSubmitting,
                modifier = Modifier.fillMaxWidth().height(56.dp).padding(bottom = 8.dp),
                shape = RoundedCornerShape(50)
            ) {
                if (uiState.isSubmitting) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(24.dp))
                } else {
                    Text(
                        text = if (uiState.isEditing) "Save Changes" else "Register & Enter NEBians",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            if (uiState.submissionResult == false) {
                Text(
                    text = "Failed to submit profile. Please try again.",
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
            }

            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}