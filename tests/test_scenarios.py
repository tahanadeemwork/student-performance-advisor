# ============================================
# Test Scenarios
# Student Performance Prediction Advisor
# 10+ diverse student profiles for testing
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference_engine.engine         import InferenceEngine
from knowledge_base.rules            import build_knowledge_base
from input_handler.student_profile   import StudentProfile
from input_handler.input_validator   import InputValidator
from output_handler.recommendation   import RecommendationProcessor
from output_handler.report_generator import ReportGenerator


# ============================================
# BUILD ENGINE ONCE
# ============================================

kb     = build_knowledge_base()
engine = InferenceEngine(kb)


# ============================================
# DEFINE ALL TEST SCENARIOS
# ============================================

def get_all_scenarios():
    """Returns all 10 test student profiles"""

    scenarios = []

    # ── Scenario 1: Excellent Student ────────
    s1 = {
        "name"                      : "Ahmed Khan",
        "student_id"                : "F21-001",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 88,
        "assignment_completion_rate": 95,
        "quiz_average"              : 85,
        "lab_completion_rate"       : 92,
        "prev_semester_avg"         : 86,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "stable",
        "attendance"                : 93,
        "days_absent_consecutively" : 0,
        "attendance_trend"          : "stable",
        "study_hours_per_day"       : 5,
        "participation_level"       : 85,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 1,
        "health_issues"             : False,
        "family_responsibilities"   : 1,
    }
    scenarios.append(("Excellent Student", s1))

    # ── Scenario 2: Good Student ─────────────
    s2 = {
        "name"                      : "Fatima Malik",
        "student_id"                : "F21-002",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 74,
        "assignment_completion_rate": 85,
        "quiz_average"              : 72,
        "lab_completion_rate"       : 80,
        "prev_semester_avg"         : 75,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "stable",
        "attendance"                : 87,
        "days_absent_consecutively" : 1,
        "attendance_trend"          : "stable",
        "study_hours_per_day"       : 3,
        "participation_level"       : 68,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 2,
        "health_issues"             : False,
        "family_responsibilities"   : 1,
    }
    scenarios.append(("Good Student", s2))

    # ── Scenario 3: Average Student ──────────
    s3 = {
        "name"                      : "Usman Raza",
        "student_id"                : "F21-003",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 62,
        "assignment_completion_rate": 70,
        "quiz_average"              : 58,
        "lab_completion_rate"       : 65,
        "prev_semester_avg"         : 64,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "stable",
        "attendance"                : 78,
        "days_absent_consecutively" : 2,
        "attendance_trend"          : "stable",
        "study_hours_per_day"       : 2,
        "participation_level"       : 48,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 2,
        "health_issues"             : False,
        "family_responsibilities"   : 2,
    }
    scenarios.append(("Average Student", s3))

    # ── Scenario 4: At Risk Student ──────────
    s4 = {
        "name"                      : "Sara Ahmed",
        "student_id"                : "F21-004",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 48,
        "assignment_completion_rate": 55,
        "quiz_average"              : 44,
        "lab_completion_rate"       : 50,
        "prev_semester_avg"         : 62,
        "failed_subjects_count"     : 1,
        "academic_trend"            : "declining",
        "attendance"                : 68,
        "days_absent_consecutively" : 4,
        "attendance_trend"          : "declining",
        "study_hours_per_day"       : 1,
        "participation_level"       : 25,
        "has_part_time_job"         : True,
        "financial_stress_level"    : 4,
        "health_issues"             : False,
        "family_responsibilities"   : 3,
    }
    scenarios.append(("At-Risk Student", s4))

    # ── Scenario 5: Failing Student ──────────
    s5 = {
        "name"                      : "Bilal Hassan",
        "student_id"                : "F21-005",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 28,
        "assignment_completion_rate": 30,
        "quiz_average"              : 25,
        "lab_completion_rate"       : 28,
        "prev_semester_avg"         : 42,
        "failed_subjects_count"     : 3,
        "academic_trend"            : "declining",
        "attendance"                : 50,
        "days_absent_consecutively" : 8,
        "attendance_trend"          : "declining",
        "study_hours_per_day"       : 0.5,
        "participation_level"       : 10,
        "has_part_time_job"         : True,
        "financial_stress_level"    : 5,
        "health_issues"             : True,
        "family_responsibilities"   : 4,
    }
    scenarios.append(("Failing Student", s5))

    # ── Scenario 6: Conflict Case 1 ──────────
    # Good grades but poor attendance
    s6 = {
        "name"                      : "Zara Khan",
        "student_id"                : "F21-006",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 82,
        "assignment_completion_rate": 90,
        "quiz_average"              : 80,
        "lab_completion_rate"       : 88,
        "prev_semester_avg"         : 78,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "stable",
        "attendance"                : 55,
        "days_absent_consecutively" : 6,
        "attendance_trend"          : "declining",
        "study_hours_per_day"       : 6,
        "participation_level"       : 35,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 1,
        "health_issues"             : False,
        "family_responsibilities"   : 1,
    }
    scenarios.append(("Conflict: Good Grades Poor Attendance", s6))

    # ── Scenario 7: Conflict Case 2 ──────────
    # Good attendance but poor grades
    s7 = {
        "name"                      : "Omar Farooq",
        "student_id"                : "F21-007",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 38,
        "assignment_completion_rate": 88,
        "quiz_average"              : 40,
        "lab_completion_rate"       : 85,
        "prev_semester_avg"         : 55,
        "failed_subjects_count"     : 1,
        "academic_trend"            : "declining",
        "attendance"                : 92,
        "days_absent_consecutively" : 0,
        "attendance_trend"          : "stable",
        "study_hours_per_day"       : 4,
        "participation_level"       : 75,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 2,
        "health_issues"             : False,
        "family_responsibilities"   : 1,
    }
    scenarios.append(("Conflict: Good Attendance Poor Grades", s7))

    # ── Scenario 8: Improving Student ────────
    s8 = {
        "name"                      : "Hina Baig",
        "student_id"                : "F21-008",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 65,
        "assignment_completion_rate": 78,
        "quiz_average"              : 62,
        "lab_completion_rate"       : 72,
        "prev_semester_avg"         : 52,
        "failed_subjects_count"     : 1,
        "academic_trend"            : "improving",
        "attendance"                : 82,
        "days_absent_consecutively" : 1,
        "attendance_trend"          : "improving",
        "study_hours_per_day"       : 3,
        "participation_level"       : 60,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 3,
        "health_issues"             : False,
        "family_responsibilities"   : 2,
    }
    scenarios.append(("Improving Student", s8))

    # ── Scenario 9: External Pressure ────────
    s9 = {
        "name"                      : "Ali Nawaz",
        "student_id"                : "F21-009",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 55,
        "assignment_completion_rate": 65,
        "quiz_average"              : 52,
        "lab_completion_rate"       : 60,
        "prev_semester_avg"         : 70,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "declining",
        "attendance"                : 72,
        "days_absent_consecutively" : 3,
        "attendance_trend"          : "declining",
        "study_hours_per_day"       : 1.5,
        "participation_level"       : 40,
        "has_part_time_job"         : True,
        "financial_stress_level"    : 5,
        "health_issues"             : True,
        "family_responsibilities"   : 5,
    }
    scenarios.append(("High External Pressure", s9))

    # ── Scenario 10: First Semester ──────────
    s10 = {
        "name"                      : "Maryam Iqbal",
        "student_id"                : "F26-001",
        "semester"                  : 1,
        "is_first_semester"         : True,
        "midterm_score"             : 52,
        "assignment_completion_rate": 68,
        "quiz_average"              : 50,
        "lab_completion_rate"       : 62,
        "prev_semester_avg"         : 0,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "stable",
        "attendance"                : 76,
        "days_absent_consecutively" : 2,
        "attendance_trend"          : "stable",
        "study_hours_per_day"       : 2,
        "participation_level"       : 35,
        "has_part_time_job"         : False,
        "financial_stress_level"    : 2,
        "health_issues"             : False,
        "family_responsibilities"   : 1,
    }
    scenarios.append(("First Semester Student", s10))

    return scenarios


# ============================================
# RUN ALL TESTS
# ============================================

def run_all_tests():
    """Run all 10 scenarios and print results"""

    scenarios = get_all_scenarios()
    passed    = 0
    failed    = 0
    results   = []

    print("\n" + "=" * 65)
    print("  STUDENT PERFORMANCE ADVISOR — TEST SUITE")
    print("  Running 10 Diverse Student Scenarios")
    print("=" * 65)

    for i, (scenario_name, student_data) in enumerate(scenarios, 1):

        print(f"\n[{i:02d}] Testing: {scenario_name}")
        print(f"      Student : {student_data['name']}")
        print(f"      ID      : {student_data['student_id']}")

        try:
            # Validate input
            from input_handler.student_profile import StudentProfile
            profile = StudentProfile()
            for key, val in student_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, val)

            validation = InputValidator.validate_profile(profile)

            if not validation.is_valid:
                print(f"      Status  : ❌ VALIDATION FAILED")
                for err in validation.get_error_messages():
                    print(f"      Error   : {err}")
                failed += 1
                continue

            # Run inference engine
            engine_results = engine.run(student_data)

            # Process results
            processed = RecommendationProcessor.process(
                engine_results, student_data["name"]
            )

            # Get key results
            perf_level = processed["performance_label"]
            risk_score = processed["risk_score"]
            rules_fired = processed["rules_fired_count"]
            risk_factors_count = len(processed["risk_factors"])
            recs_count = len(processed["recommendations"])

            print(f"      Status      : ✅ PASSED")
            print(f"      Performance : {processed['performance_emoji']} "
                  f"{perf_level}")
            print(f"      Risk Score  : {risk_score}/100")
            print(f"      Rules Fired : {rules_fired}")
            print(f"      Risk Factors: {risk_factors_count}")
            print(f"      Recs Given  : {recs_count}")

            results.append({
                "scenario"   : scenario_name,
                "student"    : student_data["name"],
                "performance": perf_level,
                "risk_score" : risk_score,
                "status"     : "PASSED"
            })
            passed += 1

        except Exception as e:
            print(f"      Status  : ❌ ERROR — {str(e)}")
            failed += 1
            results.append({
                "scenario" : scenario_name,
                "status"   : "FAILED",
                "error"    : str(e)
            })

    # Final Summary
    print("\n" + "=" * 65)
    print("  TEST SUITE SUMMARY")
    print("=" * 65)
    print(f"  Total Scenarios : {len(scenarios)}")
    print(f"  Passed          : {passed} ✅")
    print(f"  Failed          : {failed} "
          f"{'✅' if failed == 0 else '❌'}")
    print(f"  Success Rate    : "
          f"{(passed/len(scenarios)*100):.0f}%")

    print("\n  RESULTS TABLE")
    print("  " + "-" * 60)
    print(f"  {'Scenario':<35} {'Performance':<12} {'Risk':>5}")
    print("  " + "-" * 60)
    for r in results:
        if r["status"] == "PASSED":
            print(
                f"  {r['scenario']:<35} "
                f"{r['performance']:<12} "
                f"{r['risk_score']:>4}/100"
            )
    print("  " + "-" * 60)
    print(f"\n{'✅ ALL TESTS PASSED!' if failed == 0 else '❌ SOME TESTS FAILED'}")
    print("=" * 65 + "\n")

    return passed, failed


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    run_all_tests()