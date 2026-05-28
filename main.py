# ============================================
# Student Performance Prediction Advisor
# Main Entry Point
# ============================================

import sys
import os


def run_streamlit():
    """Launch Streamlit UI"""
    os.system("streamlit run ui/app.py")


def run_flask():
    """Launch Flask API"""
    os.system("python api/app.py")


def run_tests():
    """Run all test scenarios"""
    from tests.test_scenarios import run_all_tests
    run_all_tests()


def run_demo():
    """Quick demo in terminal"""
    from inference_engine.engine         import InferenceEngine
    from knowledge_base.rules            import build_knowledge_base
    from output_handler.recommendation   import RecommendationProcessor
    from output_handler.report_generator import ReportGenerator

    print("\n🎓 Student Performance Prediction Advisor")
    print("Running quick demo...\n")

    kb     = build_knowledge_base()
    engine = InferenceEngine(kb)

    student = {
        "name"                      : "Demo Student",
        "student_id"                : "DEMO-001",
        "semester"                  : 4,
        "is_first_semester"         : False,
        "midterm_score"             : 55,
        "assignment_completion_rate": 65,
        "quiz_average"              : 50,
        "lab_completion_rate"       : 60,
        "prev_semester_avg"         : 65,
        "failed_subjects_count"     : 0,
        "academic_trend"            : "declining",
        "attendance"                : 70,
        "days_absent_consecutively" : 3,
        "attendance_trend"          : "declining",
        "study_hours_per_day"       : 1.5,
        "participation_level"       : 35,
        "has_part_time_job"         : True,
        "financial_stress_level"    : 3,
        "health_issues"             : False,
        "family_responsibilities"   : 2,
    }

    results   = engine.run(student)
    processed = RecommendationProcessor.process(results, "Demo Student")
    report    = ReportGenerator.generate_console_report(processed, student)
    print(report)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "streamlit":
            run_streamlit()
        elif command == "flask":
            run_flask()
        elif command == "test":
            run_tests()
        elif command == "demo":
            run_demo()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python main.py [streamlit|flask|test|demo]")
    else:
        run_demo()