# ============================================
# Report Generator
# Student Performance Prediction Advisor
# Generates complete formatted reports
# from processed recommendation data
# ============================================

from datetime import datetime


class ReportGenerator:
    """
    Generates complete formatted reports
    from processed recommendation data.

    Supports two formats:
    1. Console report  — plain text for terminal
    2. Streamlit data  — structured dict for UI
    """

    @staticmethod
    def generate_console_report(processed: dict,
                                 student_data: dict) -> str:
        """
        Generates a complete plain text report
        for console/terminal display.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sep = "=" * 60
        thin = "-" * 60

        lines = []
        lines.append(f"\n{sep}")
        lines.append("  STUDENT PERFORMANCE PREDICTION ADVISOR")
        lines.append("  Expert System Report")
        lines.append(f"{sep}")
        lines.append(f"  Generated : {now}")
        lines.append(f"  Student   : {processed.get('student_name', 'Unknown')}")
        lines.append(f"  Student ID: {student_data.get('student_id', 'N/A')}")
        lines.append(f"  Semester  : {student_data.get('semester', 'N/A')}")
        lines.append(f"{sep}")

        # Performance verdict
        emoji = processed.get("performance_emoji", "📊")
        label = processed.get("performance_label", "Unknown")
        desc  = processed.get("performance_desc", "")
        score = processed.get("risk_score", 0)
        pri   = processed.get("intervention_priority", "MEDIUM")

        lines.append(f"\n  PERFORMANCE VERDICT")
        lines.append(f"  {thin}")
        lines.append(f"  {emoji} Status           : {label}")
        lines.append(f"  📊 Risk Score        : {score}/100")
        lines.append(f"  ⚡ Priority          : {pri}")
        lines.append(f"  📝 Summary           : {desc}")

        # Input summary
        lines.append(f"\n  STUDENT DATA SUMMARY")
        lines.append(f"  {thin}")
        lines.append(f"  Attendance           : {student_data.get('attendance', 0)}%")
        lines.append(f"  Midterm Score        : {student_data.get('midterm_score', 0)}%")
        lines.append(f"  Assignment Rate      : {student_data.get('assignment_completion_rate', 0)}%")
        lines.append(f"  Quiz Average         : {student_data.get('quiz_average', 0)}%")
        lines.append(f"  Study Hours/Day      : {student_data.get('study_hours_per_day', 0)} hrs")
        lines.append(f"  Class Participation  : {student_data.get('participation_level', 0)}%")
        lines.append(f"  Previous CGPA        : {student_data.get('prev_semester_avg', 0)}%")

        # Risk factors
        risk_factors = processed.get("risk_factors", [])
        lines.append(f"\n  PRIMARY RISK FACTORS ({len(risk_factors)})")
        lines.append(f"  {thin}")
        if risk_factors:
            for i, factor in enumerate(risk_factors, 1):
                lines.append(f"  {i}. {factor}")
        else:
            lines.append("  No significant risk factors identified")

        # Strengths
        strengths = processed.get("strengths", [])
        lines.append(f"\n  IDENTIFIED STRENGTHS ({len(strengths)})")
        lines.append(f"  {thin}")
        if strengths:
            for i, strength in enumerate(strengths, 1):
                lines.append(f"  {i}. {strength}")
        else:
            lines.append("  Keep working — strengths will develop")

        # Recommendations
        recs = processed.get("recommendations", [])
        lines.append(f"\n  PERSONALIZED RECOMMENDATIONS ({len(recs)})")
        lines.append(f"  {thin}")
        if recs:
            for rec in recs:
                lines.append(f"  {rec}")
        else:
            lines.append("  Continue current performance")

        # Reasoning chain
        trace = processed.get("reasoning_trace", [])
        lines.append(f"\n  REASONING CHAIN ({len(trace)} steps)")
        lines.append(f"  {thin}")
        if trace:
            for entry in trace:
                lines.append(
                    f"  Step {entry.get('step', '?')}: "
                    f"{entry.get('rule', 'Unknown Rule')}"
                )
                lines.append(
                    f"    → {entry.get('description', '')}"
                )
                lines.append(
                    f"    → Conclusion : {entry.get('conclusion', '')}"
                )
                lines.append(
                    f"    → Confidence : {entry.get('cf_percent', '?')}"
                )
        else:
            lines.append("  No reasoning trace available")

        # Footer
        rules_count = processed.get("rules_fired_count", 0)
        lines.append(f"\n  SYSTEM INFORMATION")
        lines.append(f"  {thin}")
        lines.append(f"  Rules Fired     : {rules_count}")
        lines.append(f"  Knowledge Base  : 70 rules")
        lines.append(f"  Engine Type     : Forward Chaining")
        lines.append(f"  CF Method       : Certainty Factor Arithmetic")
        lines.append(f"\n{sep}")
        lines.append("  ⚠️  DISCLAIMER")
        lines.append("  This system is for academic advisory purposes only.")
        lines.append("  Always consult a qualified academic advisor.")
        lines.append(f"{sep}\n")

        return "\n".join(lines)

    @staticmethod
    def generate_streamlit_data(processed: dict,
                                 student_data: dict) -> dict:
        """
        Generates structured data dictionary
        optimized for Streamlit UI rendering.
        """
        now = datetime.now().strftime("%B %d, %Y at %H:%M")

        return {
            # Header info
            "generated_at"     : now,
            "student_name"     : processed.get("student_name", ""),
            "student_id"       : student_data.get("student_id", ""),
            "semester"         : student_data.get("semester", ""),

            # Performance verdict
            "performance_level": processed.get("performance_level", ""),
            "performance_label": processed.get("performance_label", ""),
            "performance_emoji": processed.get("performance_emoji", ""),
            "performance_desc" : processed.get("performance_desc", ""),
            "risk_score"       : processed.get("risk_score", 0),
            "intervention_priority": processed.get("intervention_priority", ""),

            # Input data for display
            "attendance"       : student_data.get("attendance", 0),
            "midterm_score"    : student_data.get("midterm_score", 0),
            "assignment_rate"  : student_data.get("assignment_completion_rate", 0),
            "quiz_average"     : student_data.get("quiz_average", 0),
            "study_hours"      : student_data.get("study_hours_per_day", 0),
            "participation"    : student_data.get("participation_level", 0),
            "prev_avg"         : student_data.get("prev_semester_avg", 0),

            # Analysis results
            "risk_factors"     : processed.get("risk_factors", []),
            "strengths"        : processed.get("strengths", []),
            "recommendations"  : processed.get("recommendations", []),
            "reasoning_trace"  : processed.get("reasoning_trace", []),

            # System info
            "rules_fired"      : processed.get("rules_fired_count", 0),
            "total_rules"      : 70,
        }

    @staticmethod
    def get_color_for_level(level: str) -> str:
        """Returns Streamlit color string for performance level"""
        colors = {
            "EXCELLENT" : "#059669",
            "GOOD"      : "#2563eb",
            "AVERAGE"   : "#d97706",
            "AT_RISK"   : "#ea580c",
            "FAILING"   : "#dc2626",
            "Unknown"   : "#64748b",
        }
        return colors.get(level, "#64748b")

    @staticmethod
    def get_gauge_color(risk_score: int) -> str:
        """Returns color based on risk score"""
        if risk_score >= 75:
            return "#dc2626"
        elif risk_score >= 50:
            return "#ea580c"
        elif risk_score >= 25:
            return "#d97706"
        else:
            return "#059669"


# ============================================
# QUICK TEST
# ============================================

if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from output_handler.recommendation import RecommendationProcessor

    print("Testing ReportGenerator...")

    # Sample inference engine results
    engine_results = {
        "attendance_risk_level"  : "HIGH",
        "academic_risk_level"    : "MEDIUM",
        "study_habit_risk"       : "HIGH",
        "participation_risk"     : "HIGH",
        "overall_risk_level"     : "AT_RISK",
        "academic_status"        : "PASSING",
        "assignment_status"      : "GOOD",
        "fired_rules_count"      : 15,
        "fired_rules"            : ["Rule1", "Rule2", "Rule3"],
        "recommendations"        : [
            "1. Schedule meeting with academic advisor this week",
            "2. Increase daily study to 3+ hours",
            "3. Attend every class from now on",
            "4. Form or join a study group",
        ],
        "reasoning_trace" : [
            {
                "step"       : 1,
                "rule"       : "Attendance-High-Risk",
                "description": "Attendance 60-75% — high risk",
                "conclusion" : "attendance_risk_level = HIGH",
                "cf_percent" : "85%"
            },
            {
                "step"       : 2,
                "rule"       : "Academic-Low-Score",
                "description": "Midterm score 50-60 — below passing",
                "conclusion" : "academic_risk_level = MEDIUM",
                "cf_percent" : "75%"
            }
        ]
    }

    student_data = {
        "student_id"                : "F21-007",
        "semester"                  : 4,
        "attendance"                : 68,
        "midterm_score"             : 55,
        "assignment_completion_rate": 78,
        "quiz_average"              : 60,
        "study_hours_per_day"       : 1.5,
        "participation_level"       : 25,
        "prev_semester_avg"         : 65,
    }

    # Process recommendations
    processed = RecommendationProcessor.process(
        engine_results, "Ali Hassan"
    )

    # Generate console report
    report = ReportGenerator.generate_console_report(
        processed, student_data
    )
    print(report)

    # Generate streamlit data
    st_data = ReportGenerator.generate_streamlit_data(
        processed, student_data
    )
    print(f"✅ Streamlit data keys: {list(st_data.keys())}")
    print(f"✅ Risk score         : {st_data['risk_score']}/100")
    print(f"✅ Performance level  : {st_data['performance_label']}")
    print(f"\n✅ ReportGenerator working perfectly!")