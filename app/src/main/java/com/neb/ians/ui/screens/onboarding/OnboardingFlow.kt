package com.neb.ians.ui.screens.onboarding

import com.neb.ians.ui.screens.auth.CompleteProfileUiState

// ---------------------------------------------------------------------------
// The shape of the journey: which steps exist, which ones a given role sees, and
// what each one needs before it will let the user move on. The host screen and
// the step content both read from here, so there is one answer to "am I done".
// ---------------------------------------------------------------------------

enum class OnboardingStep {
    Welcome,
    Role,
    Name,
    Handle,
    Birthday,
    Gender,
    Level,
    Subjects,
    Place,
    Campus,
    Portrait,
    Bio,
    Finish
}

data class OnboardingRole(
    val key: String,
    val title: String,
    val subtitle: String
)

val NEB_ROLES = listOf(
    OnboardingRole("student", "Student", "Learn, ask questions, save resources"),
    OnboardingRole("teacher", "Teacher", "Teach, guide, publish resources"),
    OnboardingRole("institution", "Institution", "Represent a school, college or academy"),
    OnboardingRole("explorer", "Explorer", "Look around first, fill this in later")
)

val NEB_GENDERS = listOf("Male", "Female", "Other")

val NEB_PRADESH = listOf(
    "Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"
)

val NEB_DISTRICTS = listOf(
    "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", "Banke", "Bara", "Bardiya", "Bhaktapur",
    "Bhojpur", "Chitwan", "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading", "Dhankuta", "Dhanusha", "Dolakha",
    "Dolpa", "Doti", "Gorkha", "Gulmi", "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali", "Kalikot",
    "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok", "Khotang", "Lalitpur", "Lamjung", "Mahottari",
    "Makwanpur", "Manang", "Mustang", "Myagdi", "Nawalpur", "Nuwakot", "Okhaldhunga", "Palpa", "Panchthar", "Parasi",
    "Parbat", "Parsa", "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat", "Rolpa", "Rukum East", "Rukum West", "Rupandehi",
    "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu", "Sunsari",
    "Surkhet", "Syangja", "Tanahun", "Taplejung", "Terhathum", "Udayapur"
)

val NEB_SUBJECTS = listOf(
    "English", "Nepali", "Mathematics", "Physics", "Chemistry",
    "Biology", "Computer Science", "Accountancy", "Economics", "Social Studies"
)

val NEB_STUDENT_LEVELS = listOf(
    "Class 8", "Class 9", "Class 10 / SEE", "Class 11", "Class 12",
    "+2 Passout", "Diploma", "Bachelors", "Masters", "PhD", "Other"
)

val NEB_TEACHER_LEVELS = listOf(
    "Class 11", "Class 12", "+2 Passout", "Diploma", "Bachelors", "Masters", "Other"
)

val NEB_INSTITUTION_TYPES = listOf("school", "college", "academy", "other")

fun levelsForRole(role: String): List<String> =
    if (role == "teacher") NEB_TEACHER_LEVELS else NEB_STUDENT_LEVELS

/**
 * The step list for a role. Everyone establishes an identity; only the roles that
 * have a level, a syllabus or a campus are asked about them.
 */
fun stepsForRole(role: String): List<OnboardingStep> = buildList {
    add(OnboardingStep.Welcome)
    add(OnboardingStep.Role)
    add(OnboardingStep.Name)
    add(OnboardingStep.Handle)
    add(OnboardingStep.Birthday)
    add(OnboardingStep.Gender)
    when (role) {
        "student", "teacher" -> {
            add(OnboardingStep.Level)
            add(OnboardingStep.Subjects)
            add(OnboardingStep.Place)
            add(OnboardingStep.Campus)
        }
        "institution" -> {
            add(OnboardingStep.Place)
            add(OnboardingStep.Campus)
        }
        else -> add(OnboardingStep.Place)
    }
    add(OnboardingStep.Portrait)
    add(OnboardingStep.Bio)
    add(OnboardingStep.Finish)
}

/** Steps the user may pass through without answering. */
fun isStepSkippable(step: OnboardingStep): Boolean =
    step == OnboardingStep.Portrait || step == OnboardingStep.Bio

/** Whether the primary action on [step] should be enabled. */
fun isStepComplete(step: OnboardingStep, state: CompleteProfileUiState): Boolean = when (step) {
    OnboardingStep.Welcome -> true
    OnboardingStep.Role -> state.role.isNotBlank()
    OnboardingStep.Name -> state.displayName.trim().length >= 2
    OnboardingStep.Handle -> state.username.length >= 3 &&
        state.usernameAvailable == true &&
        state.usernameError == null
    OnboardingStep.Birthday -> state.dob.isNotBlank()
    OnboardingStep.Gender -> state.gender.isNotBlank()
    OnboardingStep.Level -> state.classLevel.isNotBlank()
    OnboardingStep.Subjects -> if (state.role == "teacher") {
        state.teachingSubjects.isNotEmpty()
    } else {
        state.subjects.isNotEmpty()
    }
    OnboardingStep.Place -> state.pradesh.isNotBlank() && state.district.isNotBlank()
    OnboardingStep.Campus -> if (state.role == "institution") {
        state.school.isNotBlank() && state.institutionType.isNotBlank()
    } else {
        state.school.isNotBlank()
    }
    OnboardingStep.Portrait -> true
    OnboardingStep.Bio -> true
    OnboardingStep.Finish -> true
}

fun primaryLabelFor(step: OnboardingStep): String = when (step) {
    OnboardingStep.Welcome -> "Let's begin"
    OnboardingStep.Finish -> "Enter NEBians"
    else -> "Continue"
}
