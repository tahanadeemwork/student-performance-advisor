# ============================================
# Input Validator
# Student Performance Prediction Advisor
# Validates all student data before inference
# ============================================


class ValidationResult:
    """
    Holds the result of a validation check.
    Contains errors and warnings separately.
    """

    def __init__(self):
        self.errors   = []
        self.warnings = []
        self.is_valid = True

    def add_error(self, field, message):
        """Add a hard error — input cannot be accepted"""
        self.errors.append({
            "field"  : field,
            "message": message,
            "type"   : "error"
        })
        self.is_valid = False

    def add_warning(self, field, message):
        """Add a soft warning — input is accepted but flagged"""
        self.warnings.append({
            "field"  : field,
            "message": message,
            "type"   : "warning"
        })

    def get_all_messages(self):
        """Return all errors and warnings as list"""
        return self.errors + self.warnings

    def get_error_messages(self):
        """Return just error messages as strings"""
        return [e["message"] for e in self.errors]

    def get_warning_messages(self):
        """Return just warning messages as strings"""
        return [w["message"] for w in self.warnings]

    def summary(self):
        """Print validation summary"""
        status = "✅ VALID" if self.is_valid else "❌ INVALID"
        print(f"\nValidation Result: {status}")
        if self.errors:
            print(f"  Errors ({len(self.errors)}):")
            for e in self.errors:
                print(f"    ❌ {e['field']}: {e['message']}")
        if self.warnings:
            print(f"  Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"    ⚠️  {w['field']}: {w['message']}")
        if not self.errors and not self.warnings:
            print("  All fields valid — no issues found.")


class InputValidator:
    """
    Validates all student input data.

    Validation Rules:
    - Scores must be 0 to 100
    - Percentages must be 0 to 100
    - Study hours must be 0 to 24
    - Stress levels must be 1 to 5
    - Required fields must not be empty
    - Trend values must be valid options
    """

    # Valid options for dropdown fields
    VALID_TRENDS      = ["improving", "stable", "declining"]
    VALID_STRESS      = [1, 2, 3, 4, 5]
    VALID_SEMESTERS   = list(range(1, 9))

    @staticmethod
    def validate_percentage(value, field_name, result):
        """Validate a percentage value (0-100)"""
        if value is None:
            result.add_error(field_name, f"{field_name} is required")
            return
        try:
            val = float(value)
            if val < 0 or val > 100:
                result.add_error(
                    field_name,
                    f"{field_name} must be between 0 and 100. Got: {val}"
                )
            elif val == 0:
                result.add_warning(
                    field_name,
                    f"{field_name} is 0 — please confirm this is correct"
                )
        except (TypeError, ValueError):
            result.add_error(
                field_name,
                f"{field_name} must be a number. Got: {value}"
            )

    @staticmethod
    def validate_score(value, field_name, result):
        """Validate an exam score (0-100)"""
        InputValidator.validate_percentage(value, field_name, result)

    @staticmethod
    def validate_study_hours(value, result):
        """Validate study hours per day (0-24)"""
        if value is None:
            result.add_error("study_hours_per_day", "Study hours is required")
            return
        try:
            val = float(value)
            if val < 0:
                result.add_error(
                    "study_hours_per_day",
                    "Study hours cannot be negative"
                )
            elif val > 18:
                result.add_error(
                    "study_hours_per_day",
                    f"Study hours {val} seems too high — maximum realistic is 18"
                )
            elif val > 12:
                result.add_warning(
                    "study_hours_per_day",
                    f"Study hours {val} is very high — please confirm"
                )
            elif val == 0:
                result.add_warning(
                    "study_hours_per_day",
                    "0 study hours — please confirm this is correct"
                )
        except (TypeError, ValueError):
            result.add_error(
                "study_hours_per_day",
                f"Study hours must be a number. Got: {value}"
            )

    @staticmethod
    def validate_trend(value, field_name, result):
        """Validate trend field"""
        if value not in InputValidator.VALID_TRENDS:
            result.add_error(
                field_name,
                f"{field_name} must be one of: "
                f"{InputValidator.VALID_TRENDS}. Got: {value}"
            )

    @staticmethod
    def validate_stress_level(value, result):
        """Validate stress level (1-5)"""
        if value is None:
            result.add_error(
                "financial_stress_level",
                "Financial stress level is required"
            )
            return
        try:
            val = int(value)
            if val not in InputValidator.VALID_STRESS:
                result.add_error(
                    "financial_stress_level",
                    f"Stress level must be 1-5. Got: {val}"
                )
        except (TypeError, ValueError):
            result.add_error(
                "financial_stress_level",
                f"Stress level must be a whole number. Got: {value}"
            )

    @staticmethod
    def validate_name(value, result):
        """Validate student name"""
        if not value or str(value).strip() == "":
            result.add_error("name", "Student name is required")
        elif len(str(value).strip()) < 2:
            result.add_error("name", "Name must be at least 2 characters")

    @staticmethod
    def validate_student_id(value, result):
        """Validate student ID"""
        if not value or str(value).strip() == "":
            result.add_error("student_id", "Student ID is required")

    @staticmethod
    def validate_semester(value, result):
        """Validate semester number"""
        try:
            val = int(value)
            if val not in InputValidator.VALID_SEMESTERS:
                result.add_error(
                    "semester",
                    f"Semester must be 1-8. Got: {val}"
                )
        except (TypeError, ValueError):
            result.add_error(
                "semester",
                f"Semester must be a whole number. Got: {value}"
            )

    @staticmethod
    def validate_family_responsibilities(value, result):
        """Validate family responsibilities (0-5)"""
        try:
            val = int(value)
            if val < 0 or val > 5:
                result.add_error(
                    "family_responsibilities",
                    f"Family responsibilities must be 0-5. Got: {val}"
                )
        except (TypeError, ValueError):
            result.add_error(
                "family_responsibilities",
                f"Must be a number. Got: {value}"
            )

    @classmethod
    def validate_profile(cls, profile):
        """
        Run complete validation on a StudentProfile object.
        Returns a ValidationResult with all errors and warnings.
        """
        result = ValidationResult()

        # Personal info
        cls.validate_name(profile.name, result)
        cls.validate_student_id(profile.student_id, result)
        cls.validate_semester(profile.semester, result)

        # Academic scores
        cls.validate_score(
            profile.midterm_score, "midterm_score", result)
        cls.validate_percentage(
            profile.assignment_completion_rate,
            "assignment_completion_rate", result)
        cls.validate_score(
            profile.quiz_average, "quiz_average", result)
        cls.validate_percentage(
            profile.lab_completion_rate,
            "lab_completion_rate", result)
        cls.validate_score(
            profile.prev_semester_avg,
            "prev_semester_avg", result)

        # Attendance
        cls.validate_percentage(
            profile.attendance, "attendance", result)
        cls.validate_trend(
            profile.attendance_trend, "attendance_trend", result)
        cls.validate_trend(
            profile.academic_trend, "academic_trend", result)

        # Behavioral
        cls.validate_study_hours(
            profile.study_hours_per_day, result)
        cls.validate_percentage(
            profile.participation_level,
            "participation_level", result)

        # Personal
        cls.validate_stress_level(
            profile.financial_stress_level, result)
        cls.validate_family_responsibilities(
            profile.family_responsibilities, result)

        return result

    @classmethod
    def validate_dict(cls, data: dict):
        """
        Validate a raw dictionary of student data.
        Used when data comes directly from Streamlit UI.
        """
        result = ValidationResult()

        # Personal
        cls.validate_name(data.get("name"), result)
        cls.validate_student_id(data.get("student_id"), result)
        cls.validate_semester(data.get("semester", 1), result)

        # Academic
        cls.validate_score(
            data.get("midterm_score"), "midterm_score", result)
        cls.validate_percentage(
            data.get("assignment_completion_rate"),
            "assignment_completion_rate", result)
        cls.validate_score(
            data.get("quiz_average"), "quiz_average", result)
        cls.validate_percentage(
            data.get("lab_completion_rate"),
            "lab_completion_rate", result)
        cls.validate_score(
            data.get("prev_semester_avg"),
            "prev_semester_avg", result)

        # Attendance
        cls.validate_percentage(
            data.get("attendance"), "attendance", result)
        cls.validate_trend(
            data.get("attendance_trend", "stable"),
            "attendance_trend", result)
        cls.validate_trend(
            data.get("academic_trend", "stable"),
            "academic_trend", result)

        # Behavioral
        cls.validate_study_hours(
            data.get("study_hours_per_day"), result)
        cls.validate_percentage(
            data.get("participation_level"),
            "participation_level", result)

        # Personal
        cls.validate_stress_level(
            data.get("financial_stress_level", 1), result)
        cls.validate_family_responsibilities(
            data.get("family_responsibilities", 0), result)

        return result


# ============================================
# QUICK TEST
# ============================================

if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from input_handler.student_profile import StudentProfile

    print("Testing InputValidator...")
    print("\n--- Test 1: Valid Student ---")
    student = StudentProfile()
    student.name                     = "Ali Hassan"
    student.student_id               = "F21-001"
    student.semester                 = 4
    student.midterm_score            = 72
    student.assignment_completion_rate = 85
    student.quiz_average             = 68
    student.lab_completion_rate      = 80
    student.prev_semester_avg        = 70
    student.failed_subjects_count    = 0
    student.academic_trend           = "stable"
    student.attendance               = 82
    student.days_absent_consecutively = 1
    student.attendance_trend         = "stable"
    student.study_hours_per_day      = 3
    student.participation_level      = 65
    student.has_part_time_job        = False
    student.financial_stress_level   = 2
    student.health_issues            = False
    student.family_responsibilities  = 1

    result = InputValidator.validate_profile(student)
    result.summary()

    print("\n--- Test 2: Invalid Student ---")
    bad_student = StudentProfile()
    bad_student.name                     = ""
    bad_student.student_id               = ""
    bad_student.semester                 = 10
    bad_student.midterm_score            = 150
    bad_student.assignment_completion_rate = -5
    bad_student.quiz_average             = 60
    bad_student.lab_completion_rate      = 70
    bad_student.prev_semester_avg        = 65
    bad_student.attendance               = 80
    bad_student.attendance_trend         = "unknown"
    bad_student.academic_trend           = "stable"
    bad_student.study_hours_per_day      = 25
    bad_student.participation_level      = 50
    bad_student.financial_stress_level   = 7
    bad_student.family_responsibilities  = 3

    result2 = InputValidator.validate_profile(bad_student)
    result2.summary()

    print("\n✅ InputValidator testing complete!")