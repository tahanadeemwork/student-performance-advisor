# ============================================
# Analyze Route
# POST /api/analyze
# ============================================

import sys
import os
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from flask                           import Blueprint, jsonify, request
from inference_engine.engine         import InferenceEngine
from knowledge_base.rules            import build_knowledge_base
from input_handler.student_profile   import StudentProfile
from input_handler.input_validator   import InputValidator
from output_handler.recommendation   import RecommendationProcessor
from output_handler.report_generator import ReportGenerator

analyze_bp = Blueprint("analyze", __name__)

# Build knowledge base once when server starts
kb     = build_knowledge_base()
engine = InferenceEngine(kb)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Main analysis endpoint.
    Receives student data from React frontend.
    Runs expert system and returns results.
    """
    try:
        # Get JSON data from React
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error"  : "No data received"
            }), 400

        # Build student profile
        profile                             = StudentProfile()
        profile.name                        = data.get("name", "")
        profile.student_id                  = data.get("student_id", "")
        profile.semester                    = int(data.get("semester", 1))
        profile.is_first_semester           = data.get("semester", 1) == 1
        profile.midterm_score               = float(data.get("midterm_score", 0))
        profile.assignment_completion_rate  = float(data.get("assignment_completion_rate", 0))
        profile.quiz_average                = float(data.get("quiz_average", 0))
        profile.lab_completion_rate         = float(data.get("lab_completion_rate", 0))
        profile.prev_semester_avg           = float(data.get("prev_semester_avg", 0))
        profile.failed_subjects_count       = int(data.get("failed_subjects_count", 0))
        profile.academic_trend              = data.get("academic_trend", "stable")
        profile.attendance                  = float(data.get("attendance", 0))
        profile.days_absent_consecutively   = int(data.get("days_absent_consecutively", 0))
        profile.attendance_trend            = data.get("attendance_trend", "stable")
        profile.study_hours_per_day         = float(data.get("study_hours_per_day", 0))
        profile.participation_level         = float(data.get("participation_level", 0))
        profile.has_part_time_job           = bool(data.get("has_part_time_job", False))
        profile.financial_stress_level      = int(data.get("financial_stress_level", 1))
        profile.health_issues               = bool(data.get("health_issues", False))
        profile.family_responsibilities     = int(data.get("family_responsibilities", 0))

        # Validate
        validation = InputValidator.validate_profile(profile)

        if not validation.is_valid:
            return jsonify({
                "success": False,
                "errors" : validation.get_error_messages()
            }), 422

        # Run inference engine
        student_dict   = profile.to_dict()
        engine_results = engine.run(student_dict)

        # Process results
        processed = RecommendationProcessor.process(
            engine_results, profile.name
        )
        st_data = ReportGenerator.generate_streamlit_data(
            processed, student_dict
        )
        console_report = ReportGenerator.generate_console_report(
            processed, student_dict
        )

        # Build response
        response = {
            "success"              : True,
            "student_name"         : st_data["student_name"],
            "student_id"           : st_data["student_id"],
            "semester"             : st_data["semester"],
            "generated_at"         : st_data["generated_at"],
            "performance_level"    : st_data["performance_level"],
            "performance_label"    : st_data["performance_label"],
            "performance_emoji"    : st_data["performance_emoji"],
            "performance_desc"     : st_data["performance_desc"],
            "risk_score"           : st_data["risk_score"],
            "intervention_priority": st_data["intervention_priority"],
            "attendance"           : st_data["attendance"],
            "midterm_score"        : st_data["midterm_score"],
            "assignment_rate"      : st_data["assignment_rate"],
            "quiz_average"         : st_data["quiz_average"],
            "study_hours"          : st_data["study_hours"],
            "participation"        : st_data["participation"],
            "prev_avg"             : st_data["prev_avg"],
            "risk_factors"         : st_data["risk_factors"],
            "strengths"            : st_data["strengths"],
            "recommendations"      : st_data["recommendations"],
            "reasoning_trace"      : st_data["reasoning_trace"],
            "rules_fired"          : st_data["rules_fired"],
            "total_rules"          : st_data["total_rules"],
            "console_report"       : console_report,
            "warnings"             : validation.get_warning_messages()
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error"  : f"Server error: {str(e)}"
        }), 500