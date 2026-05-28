package com.neb.ians.ui.screens.auth

import android.app.DatePickerDialog
import android.widget.Toast
import androidx.compose.foundation.background
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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.UserProfileRequest
import com.neb.ians.data.repository.AuthRepository
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import java.util.*

@OptIn(ExperimentalLayoutApi::class, FlowPreview::class, ExperimentalMaterial3Api::class)
@Composable
fun CompleteProfileScreen(
    authRepository: AuthRepository,
    apiService: ApiService,
    onNavigateToHome: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val scrollState = rememberScrollState()

    // Form states
    var username by remember { mutableStateOf("") }
    var dob by remember { mutableStateOf("") }
    var selectedGender by remember { mutableStateOf("Male") }
    var selectedClass by remember { mutableStateOf("Class 11") }
    val selectedSubjects = remember { mutableStateListOf<String>() }
    var selectedPradesh by remember { mutableStateOf("Bagmati") }
    var selectedDistrict by remember { mutableStateOf("Kathmandu") }
    var schoolName by remember { mutableStateOf("") }
    var isLocked by remember { mutableStateOf(false) }

    // Username validation states
    var isCheckingUsername by remember { mutableStateOf(false) }
    var usernameAvailable by remember { mutableStateOf<Boolean?>(null) }
    var usernameError by remember { mutableStateOf<String?>(null) }

    // Loading & Registration states
    var isSubmitting by remember { mutableStateOf(false) }

    // Dropdown UI states
    var pradeshExpanded by remember { mutableStateOf(false) }
    var districtExpanded by remember { mutableStateOf(false) }

    // Location Data mapping
    val pradeshList = listOf("Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim")
    
    val districtMap = remember {
        mapOf(
            "Koshi" to listOf("Taplejung", "Panchthar", "Ilam", "Jhapa", "Sankhuwasabha", "Tehrathum", "Bhojpur", "Dhankuta", "Morang", "Sunsari", "Solukhumbu", "Khotang", "Okhaldhunga", "Udayapur"),
            "Madhesh" to listOf("Saptari", "Siraha", "Dhanusha", "Mahottari", "Sarlahi", "Rautahat", "Bara", "Parsa"),
            "Bagmati" to listOf("Kathmandu", "Bhaktapur", "Lalitpur", "Dolakha", "Sindhupalchok", "Rasuwa", "Dhading", "Nuwakot", "Kavrepalanchok", "Ramechhap", "Sindhuli", "Makwanpur", "Chitwan"),
            "Gandaki" to listOf("Kaski", "Gorkha", "Manang", "Mustang", "Myagdi", "Lamjung", "Tanahun", "Syangja", "Parbat", "Baglung", "Nawalpur"),
            "Lumbini" to listOf("Rupandehi", "Kapilvastu", "Palpa", "Arghakhanchi", "Gulmi", "Pyuthan", "Rolpa", "Rukum East", "Nawalparasi West", "Bardiya", "Banke", "Dang"),
            "Karnali" to listOf("Surkhet", "Rukum West", "Salyan", "Dolpa", "Jumla", "Mugu", "Humla", "Kalikot", "Jajarkot", "Dailekh"),
            "Sudurpashchim" to listOf("Kailali", "Kanchanpur", "Dadeldhura", "Baitadi", "Darchula", "Bajhang", "Bajura", "Doti", "Achham")
        )
    }

    val subjectsList = listOf(
        "English", "Nepali", "Mathematics", "Physics", "Chemistry", 
        "Biology", "Computer Science", "Accountancy", "Economics", "Social Studies"
    )

    // Debounced Username Validator
    LaunchedEffect(username) {
        if (username.length < 3) {
            usernameAvailable = null
            usernameError = if (username.isNotEmpty()) "Must be at least 3 characters" else null
            return@LaunchedEffect
        }
        
        if (!username.matches(Regex("^[a-zA-Z0-9_]+$"))) {
            usernameAvailable = null
            usernameError = "Letters, numbers, underscores only"
            return@LaunchedEffect
        }

        usernameError = null
        isCheckingUsername = true
        
        delay(500) // 500ms debounce
        try {
            val response = apiService.checkUsername(username)
            usernameAvailable = response.available
        } catch (e: Exception) {
            usernameAvailable = null
        } finally {
            isCheckingUsername = false
        }
    }

    // Dynamic District filtering when Pradesh changes
    LaunchedEffect(selectedPradesh) {
        val list = districtMap[selectedPradesh] ?: emptyList()
        if (selectedDistrict !in list && list.isNotEmpty()) {
            selectedDistrict = list.first()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.2f),
                        MaterialTheme.colorScheme.background
                    )
                )
            )
            .padding(16.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState)
        ) {
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "Complete Your Profile",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
            
            Text(
                text = "NEBians community requires username and basic info to provide relevant materials.",
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 4.dp, bottom = 24.dp)
            )

            // USERNAME FIELD
            OutlinedTextField(
                value = username,
                onValueChange = { username = it.trim() },
                label = { Text("Choose Unique Username") },
                leadingIcon = { Icon(Icons.Default.AlternateEmail, contentDescription = null) },
                trailingIcon = {
                    if (isCheckingUsername) {
                        CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                    } else if (usernameAvailable == true) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    } else if (usernameAvailable == false || usernameError != null) {
                        Icon(Icons.Default.Error, contentDescription = null, tint = MaterialTheme.colorScheme.error)
                    }
                },
                isError = usernameError != null || usernameAvailable == false,
                supportingText = {
                    if (usernameError != null) {
                        Text(usernameError!!)
                    } else if (usernameAvailable == true) {
                        Text("Username is available", color = MaterialTheme.colorScheme.primary)
                    } else if (usernameAvailable == false) {
                        Text("Username is already taken", color = MaterialTheme.colorScheme.error)
                    }
                },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            )

            Spacer(modifier = Modifier.height(12.dp))

            // DATE OF BIRTH FIELD
            val calendar = Calendar.getInstance()
            val datePickerDialog = DatePickerDialog(
                context,
                { _, year, month, dayOfMonth ->
                    dob = "$year-${month + 1}-$dayOfMonth"
                },
                calendar.get(Calendar.YEAR) - 17,
                calendar.get(Calendar.MONTH),
                calendar.get(Calendar.DAY_OF_MONTH)
            )

            OutlinedTextField(
                value = dob,
                onValueChange = {},
                readOnly = true,
                label = { Text("Date of Birth") },
                leadingIcon = { Icon(Icons.Default.CalendarToday, contentDescription = null) },
                placeholder = { Text("YYYY-MM-DD") },
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { datePickerDialog.show() },
                enabled = false,
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

            // GENDER FIELD
            Text("Gender", fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 6.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf("Male", "Female", "Other").forEach { gender ->
                    val selected = selectedGender == gender
                    FilterChip(
                        selected = selected,
                        onClick = { selectedGender = gender },
                        label = { Text(gender) },
                        leadingIcon = if (selected) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // CLASS FIELD
            Text("Class", fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 6.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf("Class 11", "Class 12", "Both/Passout").forEach { classLvl ->
                    val selected = selectedClass == classLvl
                    FilterChip(
                        selected = selected,
                        onClick = { selectedClass = classLvl },
                        label = { Text(classLvl) },
                        leadingIcon = if (selected) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // SUBJECTS FIELD (Multi-select)
            Text("Subjects of Interest", fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 6.dp))
            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                subjectsList.forEach { subj ->
                    val isSelected = selectedSubjects.contains(subj)
                    FilterChip(
                        selected = isSelected,
                        onClick = {
                            if (isSelected) selectedSubjects.remove(subj) else selectedSubjects.add(subj)
                        },
                        label = { Text(subj) },
                        leadingIcon = if (isSelected) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null
                    )
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            // LOCATION - PRADESH
            Text("Location", fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 6.dp))
            ExposedDropdownMenuBox(
                expanded = pradeshExpanded,
                onExpandedChange = { pradeshExpanded = !pradeshExpanded }
            ) {
                OutlinedTextField(
                    value = selectedPradesh,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Pradesh / Province") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = pradeshExpanded) },
                    modifier = Modifier
                        .menuAnchor()
                        .fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                ExposedDropdownMenu(
                    expanded = pradeshExpanded,
                    onDismissRequest = { pradeshExpanded = false }
                ) {
                    pradeshList.forEach { pradesh ->
                        DropdownMenuItem(
                            text = { Text(pradesh) },
                            onClick = {
                                selectedPradesh = pradesh
                                pradeshExpanded = false
                            }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // LOCATION - DISTRICT
            ExposedDropdownMenuBox(
                expanded = districtExpanded,
                onExpandedChange = { districtExpanded = !districtExpanded }
            ) {
                OutlinedTextField(
                    value = selectedDistrict,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("District") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = districtExpanded) },
                    modifier = Modifier
                        .menuAnchor()
                        .fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                ExposedDropdownMenu(
                    expanded = districtExpanded,
                    onDismissRequest = { districtExpanded = false }
                ) {
                    val list = districtMap[selectedPradesh] ?: emptyList()
                    list.forEach { district ->
                        DropdownMenuItem(
                            text = { Text(district) },
                            onClick = {
                                selectedDistrict = district
                                districtExpanded = false
                            }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // SCHOOL NAME
            OutlinedTextField(
                value = schoolName,
                onValueChange = { schoolName = it },
                label = { Text("School / College Name") },
                leadingIcon = { Icon(Icons.Default.School, contentDescription = null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            )

            Spacer(modifier = Modifier.height(20.dp))

            // PROFILE PRIVACY (LOCK PROFILE)
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                ),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = if (isLocked) Icons.Default.Lock else Icons.Default.LockOpen,
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
                    Switch(
                        checked = isLocked,
                        onCheckedChange = { isLocked = it }
                    )
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            // SUBMIT BUTTON
            val isFormValid = username.length >= 3 && usernameAvailable == true && dob.isNotEmpty()
            
            Button(
                onClick = {
                    scope.launch {
                        isSubmitting = true
                        val cachedUser = authRepository.userProfileFlow.first()
                        val req = UserProfileRequest(
                            username = username,
                            email = cachedUser?.email,
                            photoUrl = cachedUser?.photoUrl,
                            displayName = cachedUser?.displayName ?: cachedUser?.email?.substringBefore("@"),
                            dob = dob,
                            gender = selectedGender,
                            classLevel = selectedClass,
                            subjects = selectedSubjects.joinToString(","),
                            pradesh = selectedPradesh,
                            district = selectedDistrict,
                            school = schoolName,
                            isLocked = isLocked
                        )
                        
                        val success = authRepository.completeProfile(req)
                        if (success) {
                            onNavigateToHome()
                        } else {
                            Toast.makeText(context, "Failed to submit profile. Please try again.", Toast.LENGTH_LONG).show()
                        }
                        isSubmitting = false
                    }
                },
                enabled = isFormValid && !isSubmitting,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp)
                    .padding(bottom = 8.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                if (isSubmitting) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(24.dp))
                } else {
                    Text("Register & Enter NEBians", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            }

            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}
