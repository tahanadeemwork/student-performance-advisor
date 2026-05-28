# ============================================
# Student Profile
# Student Performance Prediction Advisor
# Defines the complete student data structure
# ============================================


class StudentProfile:
    """
    Represents a complete student profile.
    All data collected from the UI will be
    stored in this structure before being
    passed to the inference engine.
    """

    def __init__(self):
        # ── Personal Information ──────────────
        self.name                    = ""
        self.student_id              = ""
        self.semester                = 1
        self.is_first_semester       = False

        # ── Academic Factors ──────────────────
        self.midterm_score           = 0.0
        self.assignment_completion_rate = 0.0
        self.quiz_average            = 0.0
        self.lab_completion_rate     = 0.0
        self.prev_semester_avg       = 0.0
        self.failed_subjects_count   = 0
        self.academic_trend          = "stable"

        # ── Attendance Factors ────────────────
        self.attendance              = 0.0
        self.days_absent_consecutively = 0
        self.attendance_trend        = "stable"

        # ── Behavioral Factors ────────────────
        self.study_hours_per_day     = 0.0
        self.participation_level     = 0.0
        self.has_part_time_job       = False

        # ── Personal Factors ──────────────────
        self.financial_stress_level  = 1
        self.health_issues           = False
        self.family_responsibilities = 0

    def to_dict(self):
        """
        Convert student profile to dictionary
        for the inference engine working memory.
        """
        return {
            # Personal
            "name"                      : self.name,
            "student_id"                : self.student_id,
            "semester"                  : self.semester,
            "is_first_semester"         : self.is_first_semester,

            # Academic
            "midterm_score"             : self.midterm_score,
            "assignment_completion_rate": self.assignment_completion_rate,
            "quiz_average"              : self.quiz_average,
            "lab_completion_rate"       : self.lab_completion_rate,
            "prev_semester_avg"         : self.prev_semester_avg,
            "failed_subjects_count"     : self.failed_subjects_count,
            "academic_trend"            : self.academic_trend,

            # Attendance
            "attendance"                : self.attendance,
            "days_absent_consecutively" : self.days_absent_consecutively,
            "attendance_trend"          : self.attendance_trend,

            # Behavioral
            "study_hours_per_day"       : self.study_hours_per_day,
            "participation_level"       : self.participation_level,
            "has_part_time_job"         : self.has_part_time_job,

            # Personal
            "financial_stress_level"    : self.financial_stress_level,
            "health_issues"             : self.health_issues,
            "family_responsibilities"   : self.family_responsibilities,
        }

    def get_summary(self):
        """
        Returns a readable summary of the student profile.
        """
        return f"""
╔══════════════════════════════════════╗
  STUDENT PROFILE SUMMARY
╚══════════════════════════════════════╝
  Name            : {self.name}
  Student ID      : {self.student_id}
  Semester        : {self.semester}

  ACADEMIC
  Midterm Score   : {self.midterm_score}%
  Assignments     : {self.assignment_completion_rate}%
  Quiz Average    : {self.quiz_average}%
  Lab Completion  : {self.lab_completion_rate}%
  Previous Avg    : {self.prev_semester_avg}%
  Failed Subjects : {self.failed_subjects_count}
  Academic Trend  : {self.academic_trend}

  ATTENDANCE
  Attendance      : {self.attendance}%
  Consec. Absences: {self.days_absent_consecutively}
  Trend           : {self.attendance_trend}

  BEHAVIORAL
  Study Hours/Day : {self.study_hours_per_day} hrs
  Participation   : {self.participation_level}%
  Part-Time Job   : {"Yes" if self.has_part_time_job else "No"}

  PERSONAL
  Financial Stress: {self.financial_stress_level}/5
  Health Issues   : {"Yes" if self.health_issues else "No"}
  Family Burden   : {self.family_responsibilities}/5
════════════════════════════════════════
        """

    @staticmethod
    def create_sample_profiles():
        """
        Returns a list of sample student profiles
        for testing purposes.
        """
        profiles = []

        # Profile 1 — Excellent Student
        p1 = StudentProfile()
        p1.name                     = "Ahmed Khan"
        p1.student_id               = "F21-001"
        p1.semester                 = 4
        p1.midterm_score            = 88
        p1.assignment_completion_rate = 95
        p1.quiz_average             = 82
        p1.lab_completion_rate      = 90
        p1.prev_semester_avg        = 85
        p1.failed_subjects_count    = 0
        p1.academic_trend           = "stable"
        p1.attendance               = 92
        p1.days_absent_consecutively = 0
        p1.attendance_trend         = "stable"
        p1.study_hours_per_day      = 4
        p1.participation_level      = 80
        p1.has_part_time_job        = False
        p1.financial_stress_level   = 1
        p1.health_issues            = False
        p1.family_responsibilities  = 1
        profiles.append(("Excellent Student", p1))

        # Profile 2 — At-Risk Student
        p2 = StudentProfile()
        p2.name                     = "Sara Ali"
        p2.student_id               = "F21-002"
        p2.semester                 = 4
        p2.midterm_score            = 48
        p2.assignment_completion_rate = 55
        p2.quiz_average             = 45
        p2.lab_completion_rate      = 50
        p2.prev_semester_avg        = 65
        p2.failed_subjects_count    = 1
        p2.academic_trend           = "declining"
        p2.attendance               = 68
        p2.days_absent_consecutively = 4
        p2.attendance_trend         = "declining"
        p2.study_hours_per_day      = 1
        p2.participation_level      = 25
        p2.has_part_time_job        = True
        p2.financial_stress_level   = 4
        p2.health_issues            = False
        p2.family_responsibilities  = 3
        profiles.append(("At-Risk Student", p2))

        # Profile 3 — Failing Student
        p3 = StudentProfile()
        p3.name                     = "Usman Malik"
        p3.student_id               = "F21-003"
        p3.semester                 = 4
        p3.midterm_score            = 30
        p3.assignment_completion_rate = 35
        p3.quiz_average             = 28
        p3.lab_completion_rate      = 30
        p3.prev_semester_avg        = 45
        p3.failed_subjects_count    = 3
        p3.academic_trend           = "declining"
        p3.attendance               = 52
        p3.days_absent_consecutively = 7
        p3.attendance_trend         = "declining"
        p3.study_hours_per_day      = 0.5
        p3.participation_level      = 10
        p3.has_part_time_job        = True
        p3.financial_stress_level   = 5
        p3.health_issues            = True
        p3.family_responsibilities  = 4
        profiles.append(("Failing Student", p3))

        # Profile 4 — Average Student
        p4 = StudentProfile()
        p4.name                     = "Ayesha Raza"
        p4.student_id               = "F21-004"
        p4.semester                 = 4
        p4.midterm_score            = 63
        p4.assignment_completion_rate = 72
        p4.quiz_average             = 60
        p4.lab_completion_rate      = 68
        p4.prev_semester_avg        = 65
        p4.failed_subjects_count    = 0
        p4.academic_trend           = "stable"
        p4.attendance               = 78
        p4.days_absent_consecutively = 1
        p4.attendance_trend         = "stable"
        p4.study_hours_per_day      = 2
        p4.participation_level      = 50
        p4.has_part_time_job        = False
        p4.financial_stress_level   = 2
        p4.health_issues            = False
        p4.family_responsibilities  = 2
        profiles.append(("Average Student", p4))

        # Profile 5 — Conflict Case
        # Good grades but poor attendance
        p5 = StudentProfile()
        p5.name                     = "Bilal Ahmed"
        p5.student_id               = "F21-005"
        p5.semester                 = 4
        p5.midterm_score            = 80
        p5.assignment_completion_rate = 88
        p5.quiz_average             = 78
        p5.lab_completion_rate      = 85
        p5.prev_semester_avg        = 75
        p5.failed_subjects_count    = 0
        p5.academic_trend           = "stable"
        p5.attendance               = 55
        p5.days_absent_consecutively = 5
        p5.attendance_trend         = "declining"
        p5.study_hours_per_day      = 5
        p5.participation_level      = 40
        p5.has_part_time_job        = False
        p5.financial_stress_level   = 1
        p5.health_issues            = False
        p5.family_responsibilities  = 1
        profiles.append(("Conflict: Good Grades Poor Attendance", p5))

        return profiles


# ============================================
# QUICK TEST
# ============================================

if __name__ == "__main__":
    print("Testing StudentProfile...")

    # Create a sample student
    student = StudentProfile()
    student.name                     = "Test Student"
    student.student_id               = "TEST-001"
    student.semester                 = 4
    student.midterm_score            = 65
    student.assignment_completion_rate = 75
    student.quiz_average             = 60
    student.lab_completion_rate      = 70
    student.prev_semester_avg        = 68
    student.failed_subjects_count    = 0
    student.academic_trend           = "stable"
    student.attendance               = 80
    student.days_absent_consecutively = 1
    student.attendance_trend         = "stable"
    student.study_hours_per_day      = 2.5
    student.participation_level      = 55
    student.has_part_time_job        = False
    student.financial_stress_level   = 2
    student.health_issues            = False
    student.family_responsibilities  = 1

    # Print summary
    print(student.get_summary())

    # Convert to dict
    data = student.to_dict()
    print(f"✅ to_dict() works — {len(data)} fields")
    print(f"\n✅ StudentProfile is working perfectly!")