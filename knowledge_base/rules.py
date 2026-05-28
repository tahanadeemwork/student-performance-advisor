# ============================================
# KNOWLEDGE BASE — Student Performance Rules
# Student Performance Prediction Advisor
# ============================================
# 
# 5 Categories of Rules:
# Category 1: Attendance Rules (10 rules)
# Category 2: Academic Performance Rules (18 rules)
# Category 3: Behavioral Rules (12 rules)
# Category 4: Composite & Conflict Rules (18 rules)
# Category 5: Recommendation Rules (12 rules)
# TOTAL: 70 rules
#
# ============================================

import sys
sys.path.append('.')

from inference_engine.engine import Rule, KnowledgeBase


# ============================================
# HELPER FUNCTION: Create action with logging
# ============================================

def create_action(conclusion_key, conclusion_value, description, cf_value):
    """Factory function to create rule actions with logging"""
    def action(wm, exp):
        wm.add(conclusion_key, conclusion_value)
        exp.log(
            rule_name=f"Rule-{conclusion_key}",
            description=description,
            conclusion=f"{conclusion_key} = {conclusion_value}",
            cf=cf_value
        )
    return action


# ============================================
# CATEGORY 1: ATTENDANCE RULES (10 rules)
# ============================================

attendance_rules = [
    Rule(
        name="Attendance-Critical-Risk",
        conditions=lambda wm: wm.get("attendance", 100) < 60,
        actions=create_action(
            "attendance_risk_level", "CRITICAL",
            "Attendance < 60% — critical threshold",
            0.95
        ),
        cf=0.95, priority=10,
        description="If attendance < 60% then CRITICAL risk"
    ),

    Rule(
        name="Attendance-High-Risk",
        conditions=lambda wm: (wm.get("attendance", 100) >= 60 and 
                               wm.get("attendance", 100) < 75),
        actions=create_action(
            "attendance_risk_level", "HIGH",
            "Attendance 60-75% — high risk",
            0.85
        ),
        cf=0.85, priority=9,
        description="If attendance 60-75% then HIGH risk"
    ),

    Rule(
        name="Attendance-Medium-Risk",
        conditions=lambda wm: (wm.get("attendance", 100) >= 75 and 
                               wm.get("attendance", 100) < 85),
        actions=create_action(
            "attendance_risk_level", "MEDIUM",
            "Attendance 75-85% — medium risk",
            0.70
        ),
        cf=0.70, priority=8,
        description="If attendance 75-85% then MEDIUM risk"
    ),

    Rule(
        name="Attendance-Good",
        conditions=lambda wm: wm.get("attendance", 100) >= 85,
        actions=create_action(
            "attendance_status", "GOOD",
            "Attendance >= 85% — excellent",
            0.90
        ),
        cf=0.90, priority=7,
        description="If attendance >= 85% then GOOD"
    ),

    Rule(
        name="Attendance-Poor-Pattern",
        conditions=lambda wm: (wm.get("attendance", 100) < 70 and 
                               wm.get("days_absent_consecutively", 0) > 3),
        actions=create_action(
            "attendance_pattern", "CONCERNING",
            "Multiple consecutive absences detected",
            0.88
        ),
        cf=0.88, priority=9,
        description="Consecutive absences = concerning pattern"
    ),

    Rule(
        name="Attendance-Improving",
        conditions=lambda wm: (wm.get("attendance", 100) >= 75 and 
                               wm.get("attendance_trend", "stable") == "improving"),
        actions=create_action(
            "attendance_trajectory", "POSITIVE",
            "Student attendance is improving trend",
            0.75
        ),
        cf=0.75, priority=5,
        description="Improving attendance trend is positive"
    ),

    Rule(
        name="Attendance-Declining",
        conditions=lambda wm: (wm.get("attendance_trend", "stable") == "declining" and 
                               wm.get("attendance", 100) < 80),
        actions=create_action(
            "attendance_trajectory", "NEGATIVE",
            "Student attendance is declining",
            0.82
        ),
        cf=0.82, priority=8,
        description="Declining attendance is warning sign"
    ),

    Rule(
        name="Attendance-Borderline",
        conditions=lambda wm: (wm.get("attendance", 100) >= 70 and 
                               wm.get("attendance", 100) < 76),
        actions=create_action(
            "attendance_status", "BORDERLINE",
            "At threshold — could go either way",
            0.68
        ),
        cf=0.68, priority=7,
        description="Attendance at critical borderline"
    ),

    Rule(
        name="Attendance-Excellent",
        conditions=lambda wm: wm.get("attendance", 100) >= 95,
        actions=create_action(
            "attendance_strength", "EXCELLENT",
            "Perfect or near-perfect attendance",
            0.95
        ),
        cf=0.95, priority=6,
        description="Attendance >= 95% is excellent strength"
    ),

    Rule(
        name="Attendance-Warning",
        conditions=lambda wm: wm.get("attendance", 100) < 65,
        actions=create_action(
            "needs_attendance_intervention", True,
            "Attendance low enough to need immediate action",
            0.93
        ),
        cf=0.93, priority=10,
        description="Low attendance requires intervention"
    ),
]


# ============================================
# CATEGORY 2: ACADEMIC PERFORMANCE RULES (18 rules)
# ============================================

academic_rules = [
    Rule(
        name="Academic-Failing-Score",
        conditions=lambda wm: wm.get("midterm_score", 100) < 40,
        actions=create_action(
            "academic_risk_level", "CRITICAL",
            "Midterm score < 40 — failing range",
            0.95
        ),
        cf=0.95, priority=10,
        description="Midterm < 40 means failing"
    ),

    Rule(
        name="Academic-Very-Low-Score",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 40 and 
                               wm.get("midterm_score", 100) < 50),
        actions=create_action(
            "academic_risk_level", "HIGH",
            "Midterm score 40-50 — very low",
            0.88
        ),
        cf=0.88, priority=9,
        description="Midterm 40-50 is very low performance"
    ),

    Rule(
        name="Academic-Low-Score",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 50 and 
                               wm.get("midterm_score", 100) < 60),
        actions=create_action(
            "academic_risk_level", "MEDIUM",
            "Midterm score 50-60 — below passing",
            0.75
        ),
        cf=0.75, priority=8,
        description="Midterm 50-60 is below passing"
    ),

    Rule(
        name="Academic-Passing-Score",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 60 and 
                               wm.get("midterm_score", 100) < 70),
        actions=create_action(
            "academic_status", "PASSING",
            "Midterm score 60-70 — barely passing",
            0.65
        ),
        cf=0.65, priority=7,
        description="Midterm 60-70 is passing but weak"
    ),

    Rule(
        name="Academic-Good-Score",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 70 and 
                               wm.get("midterm_score", 100) < 80),
        actions=create_action(
            "academic_status", "GOOD",
            "Midterm score 70-80 — good performance",
            0.82
        ),
        cf=0.82, priority=7,
        description="Midterm 70-80 is good"
    ),

    Rule(
        name="Academic-Strong-Score",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 80 and 
                               wm.get("midterm_score", 100) < 90),
        actions=create_action(
            "academic_status", "STRONG",
            "Midterm score 80-90 — strong performance",
            0.90
        ),
        cf=0.90, priority=7,
        description="Midterm 80-90 is strong"
    ),

    Rule(
        name="Academic-Excellent-Score",
        conditions=lambda wm: wm.get("midterm_score", 100) >= 90,
        actions=create_action(
            "academic_status", "EXCELLENT",
            "Midterm score >= 90 — excellent",
            0.95
        ),
        cf=0.95, priority=7,
        description="Midterm >= 90 is excellent"
    ),

    Rule(
        name="Assignment-Completion-Critical",
        conditions=lambda wm: wm.get("assignment_completion_rate", 100) < 40,
        actions=create_action(
            "assignment_risk", "CRITICAL",
            "Assignment completion < 40% — critical gap",
            0.92
        ),
        cf=0.92, priority=9,
        description="Very low assignment completion"
    ),

    Rule(
        name="Assignment-Completion-Low",
        conditions=lambda wm: (wm.get("assignment_completion_rate", 100) >= 40 and 
                               wm.get("assignment_completion_rate", 100) < 70),
        actions=create_action(
            "assignment_risk", "HIGH",
            "Assignment completion 40-70% — concerning",
            0.80
        ),
        cf=0.80, priority=8,
        description="Low assignment completion"
    ),

    Rule(
        name="Assignment-Completion-Good",
        conditions=lambda wm: wm.get("assignment_completion_rate", 100) >= 85,
        actions=create_action(
            "assignment_status", "GOOD",
            "Assignment completion >= 85% — good",
            0.88
        ),
        cf=0.88, priority=6,
        description="Good assignment completion"
    ),

    Rule(
        name="Quiz-Performance-Poor",
        conditions=lambda wm: wm.get("quiz_average", 100) < 50,
        actions=create_action(
            "quiz_risk", "HIGH",
            "Quiz average < 50% — poor understanding",
            0.85
        ),
        cf=0.85, priority=8,
        description="Poor quiz performance indicates knowledge gaps"
    ),

    Rule(
        name="Quiz-Performance-Average",
        conditions=lambda wm: (wm.get("quiz_average", 100) >= 50 and 
                               wm.get("quiz_average", 100) < 70),
        actions=create_action(
            "quiz_risk", "MEDIUM",
            "Quiz average 50-70% — inconsistent",
            0.72
        ),
        cf=0.72, priority=7,
        description="Inconsistent quiz performance"
    ),

    Rule(
        name="Quiz-Performance-Good",
        conditions=lambda wm: wm.get("quiz_average", 100) >= 75,
        actions=create_action(
            "quiz_status", "GOOD",
            "Quiz average >= 75% — consistent understanding",
            0.85
        ),
        cf=0.85, priority=6,
        description="Good quiz performance"
    ),

    Rule(
        name="Combined-Academic-Failure",
        conditions=lambda wm: (wm.get("midterm_score", 100) < 50 and 
                               wm.get("quiz_average", 100) < 50 and
                               wm.get("assignment_completion_rate", 100) < 60),
        actions=create_action(
            "academic_performance_prediction", "LIKELY_FAIL",
            "Multiple academic indicators point to failure",
            0.93
        ),
        cf=0.93, priority=11,
        description="Multiple weak academic signals = likely failure"
    ),

    Rule(
        name="Academic-Trend-Declining",
        conditions=lambda wm: (wm.get("midterm_score", 100) < wm.get("prev_semester_avg", 100) and
                               wm.get("academic_trend", "stable") == "declining"),
        actions=create_action(
            "academic_trajectory", "NEGATIVE",
            "Academic performance declining from last semester",
            0.80
        ),
        cf=0.80, priority=8,
        description="Declining academic trend is warning"
    ),

    Rule(
        name="Academic-Trend-Improving",
        conditions=lambda wm: (wm.get("academic_trend", "stable") == "improving"),
        actions=create_action(
            "academic_trajectory", "POSITIVE",
            "Academic performance is improving",
            0.78
        ),
        cf=0.78, priority=5,
        description="Improving academic trend is positive"
    ),

    Rule(
        name="Lab-Work-Missing",
        conditions=lambda wm: wm.get("lab_completion_rate", 100) < 50,
        actions=create_action(
            "lab_risk", "HIGH",
            "Lab work completion < 50%",
            0.82
        ),
        cf=0.82, priority=8,
        description="Incomplete lab work indicates disengagement"
    ),

        Rule(
        name="Previous-Failures-History",
        conditions=lambda wm: wm.get("failed_subjects_count", 0) > 1,
        actions=create_action(
            "failure_history_risk", "HIGH",
            "Student has history of failing multiple subjects",
            0.83
        ),
        cf=0.83, priority=8,
        description="Multiple failed subjects indicates pattern"
    ),
]


# ============================================
# CATEGORY 3: BEHAVIORAL RULES (12 rules)
# ============================================

behavioral_rules = [
    Rule(
        name="Study-Hours-Critical-Low",
        conditions=lambda wm: wm.get("study_hours_per_day", 5) < 1,
        actions=create_action(
            "study_habit_risk", "CRITICAL",
            "Study hours < 1 per day — insufficient",
            0.90
        ),
        cf=0.90, priority=9,
        description="Less than 1 hour daily study"
    ),

    Rule(
        name="Study-Hours-Low",
        conditions=lambda wm: (wm.get("study_hours_per_day", 5) >= 1 and 
                               wm.get("study_hours_per_day", 5) < 2),
        actions=create_action(
            "study_habit_risk", "HIGH",
            "Study hours 1-2 per day — borderline",
            0.80
        ),
        cf=0.80, priority=8,
        description="1-2 hours daily study is borderline"
    ),

    Rule(
        name="Study-Hours-Adequate",
        conditions=lambda wm: (wm.get("study_hours_per_day", 5) >= 2 and 
                               wm.get("study_hours_per_day", 5) < 3),
        actions=create_action(
            "study_habit_status", "ADEQUATE",
            "Study hours 2-3 per day — adequate",
            0.72
        ),
        cf=0.72, priority=7,
        description="2-3 hours daily study is adequate"
    ),

    Rule(
        name="Study-Hours-Good",
        conditions=lambda wm: (wm.get("study_hours_per_day", 5) >= 3 and 
                               wm.get("study_hours_per_day", 5) < 5),
        actions=create_action(
            "study_habit_status", "GOOD",
            "Study hours 3-5 per day — good",
            0.85
        ),
        cf=0.85, priority=6,
        description="3-5 hours daily study is good"
    ),

    Rule(
        name="Study-Hours-Excellent",
        conditions=lambda wm: wm.get("study_hours_per_day", 5) >= 5,
        actions=create_action(
            "study_habit_status", "EXCELLENT",
            "Study hours >= 5 per day — excellent discipline",
            0.92
        ),
        cf=0.92, priority=6,
        description="5+ hours daily study is excellent"
    ),

    Rule(
        name="Class-Participation-Low",
        conditions=lambda wm: wm.get("participation_level", 50) < 30,
        actions=create_action(
            "participation_risk", "HIGH",
            "Class participation < 30% — very low",
            0.83
        ),
        cf=0.83, priority=8,
        description="Low class participation indicates disengagement"
    ),

    Rule(
        name="Class-Participation-Average",
        conditions=lambda wm: (wm.get("participation_level", 50) >= 30 and 
                               wm.get("participation_level", 50) < 60),
        actions=create_action(
            "participation_status", "AVERAGE",
            "Class participation 30-60% — average",
            0.68
        ),
        cf=0.68, priority=7,
        description="Average class participation"
    ),

    Rule(
        name="Class-Participation-Good",
        conditions=lambda wm: wm.get("participation_level", 50) >= 70,
        actions=create_action(
            "participation_status", "GOOD",
            "Class participation >= 70% — good engagement",
            0.84
        ),
        cf=0.84, priority=6,
        description="Good class participation"
    ),

    Rule(
        name="Part-Time-Job-Strain",
        conditions=lambda wm: (wm.get("has_part_time_job", False) and 
                               wm.get("study_hours_per_day", 5) < 2),
        actions=create_action(
            "time_constraint_risk", "HIGH",
            "Part-time job + low study hours = time strain",
            0.78
        ),
        cf=0.78, priority=8,
        description="Working while studying little = time constraint"
    ),

    Rule(
        name="Family-Responsibilities-Burden",
        conditions=lambda wm: (wm.get("family_responsibilities", 0) > 2 and 
                               wm.get("study_hours_per_day", 5) < 1.5),
        actions=create_action(
            "responsibility_burden", "HIGH",
            "Heavy family responsibilities limiting study",
            0.75
        ),
        cf=0.75, priority=7,
        description="Family obligations straining academics"
    ),

    Rule(
        name="Health-Issues-Present",
        conditions=lambda wm: wm.get("health_issues", False),
        actions=create_action(
            "health_factor", "PRESENT",
            "Student reported health problems",
            0.70
        ),
        cf=0.70, priority=6,
        description="Health issues may impact performance"
    ),

    Rule(
        name="Financial-Stress-High",
        conditions=lambda wm: wm.get("financial_stress_level", 3) >= 4,
        actions=create_action(
            "financial_stress_factor", "HIGH",
            "Significant financial stress reported",
            0.72
        ),
        cf=0.72, priority=7,
        description="High financial stress impacts academics"
    ),
]


# ============================================
# CATEGORY 4: COMPOSITE & CONFLICT RULES (18 rules)
# ============================================

composite_rules = [
    Rule(
        name="Conflict-Good-Grades-Poor-Attendance",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 75 and 
                               wm.get("attendance", 100) < 60),
        actions=create_action(
            "overall_risk_level", "MEDIUM",
            "Strong grades compensate for poor attendance — but warning",
            0.65
        ),
        cf=0.65, priority=9,
        description="Good grades offset poor attendance partially"
    ),

    Rule(
        name="Conflict-Poor-Grades-Good-Attendance",
        conditions=lambda wm: (wm.get("midterm_score", 100) < 50 and 
                               wm.get("attendance", 100) >= 85),
        actions=create_action(
            "overall_risk_level", "HIGH",
            "Attending but not understanding — needs tutoring",
            0.82
        ),
        cf=0.82, priority=9,
        description="Attendance good but understanding weak"
    ),

    Rule(
        name="Conflict-High-Grades-Low-Study",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 80 and 
                               wm.get("study_hours_per_day", 5) < 1.5),
        actions=create_action(
            "study_efficiency", "HIGH",
            "Student is efficient learner — natural ability",
            0.75
        ),
        cf=0.75, priority=5,
        description="High grades with minimal study = natural aptitude"
    ),

    Rule(
        name="Conflict-Low-Grades-High-Study",
        conditions=lambda wm: (wm.get("midterm_score", 100) < 55 and 
                               wm.get("study_hours_per_day", 5) >= 4),
        actions=create_action(
            "learning_challenge", "POSSIBLE",
            "Studying hard but grades low — possible learning issues",
            0.78
        ),
        cf=0.78, priority=9,
        description="Despite effort, performance low — may need different approach"
    ),

    Rule(
        name="Multiple-Risk-Factors",
        conditions=lambda wm: (wm.get("attendance", 100) < 70 and 
                               wm.get("midterm_score", 100) < 50 and
                               wm.get("study_hours_per_day", 5) < 1),
        actions=create_action(
            "performance_prediction", "FAILING",
            "Multiple severe risk factors converge",
            0.95
        ),
        cf=0.95, priority=11,
        description="Multiple factors point to failure"
    ),

    Rule(
        name="All-Factors-Strong",
        conditions=lambda wm: (wm.get("attendance", 100) >= 85 and 
                               wm.get("midterm_score", 100) >= 75 and
                               wm.get("study_hours_per_day", 5) >= 3 and
                               wm.get("participation_level", 50) >= 70),
        actions=create_action(
            "performance_prediction", "EXCELLENT",
            "All indicators point to excellent performance",
            0.94
        ),
        cf=0.94, priority=10,
        description="Across-the-board excellent indicators"
    ),

    Rule(
        name="Mixed-Signals-Attendance-Study",
        conditions=lambda wm: (wm.get("attendance", 100) < 70 and 
                               wm.get("study_hours_per_day", 5) >= 3),
        actions=create_action(
            "behavioral_contradiction", "PRESENT",
            "Studies hard but doesn't attend — motivation question",
            0.68
        ),
        cf=0.68, priority=7,
        description="Contradictory signals about commitment"
    ),

    Rule(
        name="Performance-At-Risk-Cusp",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 55 and 
                               wm.get("midterm_score", 100) < 65 and
                               wm.get("attendance", 100) >= 70 and
                               wm.get("attendance", 100) < 80),
        actions=create_action(
            "overall_risk_level", "AT_RISK",
            "Borderline on multiple dimensions",
            0.70
        ),
        cf=0.70, priority=8,
        description="Teetering on edge — could go either way"
    ),

    Rule(
        name="External-Factors-Compounding",
        conditions=lambda wm: (wm.get("financial_stress_level", 3) >= 4 and 
                               wm.get("health_issues", False) and
                               wm.get("family_responsibilities", 0) > 2),
        actions=create_action(
            "external_pressure", "HIGH",
            "Multiple external stressors compounding",
            0.82
        ),
        cf=0.82, priority=9,
        description="External circumstances are adding pressure"
    ),

    Rule(
        name="Recovery-Possible",
        conditions=lambda wm: (wm.get("academic_trajectory", "stable") == "improving" and 
                               wm.get("midterm_score", 100) >= 50),
        actions=create_action(
            "recovery_potential", "YES",
            "Student showing improvement — recovery possible",
            0.80
        ),
        cf=0.80, priority=6,
        description="Improvement trend suggests turnaround possible"
    ),

    Rule(
        name="Sudden-Performance-Drop",
        conditions=lambda wm: (wm.get("prev_semester_avg", 100) >= 70 and 
                               wm.get("midterm_score", 100) < 55 and
                               wm.get("academic_trend", "stable") == "declining"),
        actions=create_action(
            "concern_level", "URGENT",
            "Sharp performance drop — investigate cause",
            0.88
        ),
        cf=0.88, priority=10,
        description="Dramatic unexpected decline requires investigation"
    ),

    Rule(
        name="Consistent-Underperformance",
        conditions=lambda wm: (wm.get("prev_semester_avg", 100) < 60 and 
                               wm.get("midterm_score", 100) < 60),
        actions=create_action(
            "chronic_underperformance", True,
            "Pattern of consistently low performance",
            0.85
        ),
        cf=0.85, priority=9,
        description="Chronic underperformance — systematic issue"
    ),

    Rule(
        name="Strong-Foundation-Slipping",
        conditions=lambda wm: (wm.get("prev_semester_avg", 100) >= 80 and 
                               wm.get("midterm_score", 100) < wm.get("prev_semester_avg", 100) - 15),
        actions=create_action(
            "concern_level", "HIGH",
            "Previously strong student sliding",
            0.84
        ),
        cf=0.84, priority=9,
        description="Strong student deteriorating — warning sign"
    ),

    Rule(
        name="First-Semester-Struggle",
        conditions=lambda wm: (wm.get("is_first_semester", False) and 
                               wm.get("midterm_score", 100) < 55),
        actions=create_action(
            "adjustment_issue", "POSSIBLE",
            "First semester struggle — possible adjustment issue",
            0.72
        ),
        cf=0.72, priority=7,
        description="First semester low — might be adjustment phase"
    ),

    Rule(
        name="Engagement-Despite-Adversity",
        conditions=lambda wm: (wm.get("external_pressure", "LOW") == "HIGH" and 
                               wm.get("study_hours_per_day", 5) >= 2 and
                               wm.get("attendance", 100) >= 75),
        actions=create_action(
            "resilience_factor", "HIGH",
            "Showing resilience despite external pressures",
            0.81
        ),
        cf=0.81, priority=6,
        description="Student pushing through difficult circumstances"
    ),

    Rule(
        name="Multiple-Strengths",
        conditions=lambda wm: (wm.get("midterm_score", 100) >= 75 and 
                               wm.get("quiz_average", 100) >= 75 and
                               wm.get("assignment_completion_rate", 100) >= 85),
        actions=create_action(
            "academic_strength", "MULTIPLE",
            "Strong across all academic dimensions",
            0.91
        ),
        cf=0.91, priority=7,
        description="Consistent strength across all metrics"
    ),

        Rule(
        name="Conflict-Good-Participation-Poor-Grades",
        conditions=lambda wm: (wm.get("participation_level", 50) >= 70 and
                               wm.get("midterm_score", 100) < 55),
        actions=create_action(
            "learning_style_mismatch", "POSSIBLE",
            "Active in class but exam performance weak — test anxiety possible",
            0.74
        ),
        cf=0.74, priority=8,
        description="High participation but low exam scores — possible test anxiety"
    ),

    Rule(
        name="Conflict-All-Assignments-Done-Poor-Exams",
        conditions=lambda wm: (wm.get("assignment_completion_rate", 100) >= 90 and
                               wm.get("midterm_score", 100) < 55),
        actions=create_action(
            "exam_preparation_issue", "POSSIBLE",
            "Assignments complete but exams poor — exam prep strategy needed",
            0.76
        ),
        cf=0.76, priority=8,
        description="Completes work but underperforms on exams"
    ),
]


# ============================================
# CATEGORY 5: RECOMMENDATION RULES (12 rules)
# ============================================

recommendation_rules = [
    Rule(
        name="Rec-Critical-Intervention",
        conditions=lambda wm: wm.get("overall_risk_level", "LOW") == "CRITICAL" or 
                               wm.get("performance_prediction", "Good") == "FAILING",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. URGENT: Meet with academic advisor TODAY",
                "2. Create detailed study schedule — 4+ hours daily",
                "3. Enroll in tutoring for each weak subject immediately",
                "4. Attend every single remaining class without exception",
                "5. Form or join a study group this week",
                "6. Review all missed assignments — complete all by deadline",
                "7. Meet with professor during office hours weekly",
            ]),
            exp.log("Recommendation-Critical", "Multiple critical risk factors detected", 
                   "Critical level intervention recommended", 0.95)
        ),
        cf=0.95, priority=11,
        description="Failing student needs urgent intervention"
    ),

    Rule(
        name="Rec-At-Risk-Support",
        conditions=lambda wm: wm.get("overall_risk_level", "LOW") == "AT_RISK",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Schedule meeting with academic advisor this week",
                "2. Increase daily study to 3+ hours",
                "3. Identify specific topics causing difficulty",
                "4. Attend at least one tutoring session",
                "5. Join a study group for peer support",
                "6. Catch up on incomplete assignments immediately",
                "7. Improve attendance — aim for 90%+",
            ]),
            exp.log("Recommendation-AtRisk", "At-risk level support recommended", 
                   "Targeted intervention plan needed", 0.88)
        ),
        cf=0.88, priority=10,
        description="At-risk student needs targeted support"
    ),

    Rule(
        name="Rec-Attendance-Focus",
        conditions=lambda wm: wm.get("attendance_risk_level", "GOOD") in ["CRITICAL", "HIGH"],
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Identify barriers to attendance — family, health, transportation",
                "2. Commit to attending next 5 classes without missing",
                "3. Set phone reminders 30 minutes before class",
                "4. Inform professor about attendance concerns",
                "5. Explore campus support services if personal issues",
            ]),
            exp.log("Recommendation-Attendance", "Poor attendance must improve", 
                   "Attendance improvement plan", 0.90)
        ),
        cf=0.90, priority=9,
        description="Student needs to dramatically improve attendance"
    ),

    Rule(
        name="Rec-Study-Skills",
        conditions=lambda wm: (wm.get("study_habit_risk", "GOOD") in ["CRITICAL", "HIGH"] or
                               wm.get("study_hours_per_day", 5) < 2),
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Start with 30-minute focused study sessions",
                "2. Learn Pomodoro technique (25 min work, 5 min break)",
                "3. Remove phone and distractions during study",
                "4. Use active recall and spaced repetition",
                "5. Find quiet study location — library, dorm common area",
                "6. Gradually increase to 2+ hours daily by week 4",
            ]),
            exp.log("Recommendation-StudySkills", "Study habits need improvement", 
                   "Study skills intervention plan", 0.85)
        ),
        cf=0.85, priority=8,
        description="Student needs better study habits and techniques"
    ),

    Rule(
        name="Rec-Tutoring-Academic",
        conditions=lambda wm: (wm.get("academic_risk_level", "GOOD") in ["CRITICAL", "HIGH", "MEDIUM"] or
                               wm.get("quiz_risk", "GOOD") == "HIGH"),
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Enroll in subject-specific tutoring immediately",
                "2. Request one-on-one tutoring if available",
                "3. Meet with professor to understand weak concepts",
                "4. Form study group to discuss difficult topics",
                "5. Use online resources — Khan Academy, YouTube tutorials",
                "6. Take quizzes again after tutoring to track improvement",
            ]),
            exp.log("Recommendation-Tutoring", "Academic support needed", 
                   "Tutoring plan", 0.88)
        ),
        cf=0.88, priority=9,
        description="Student needs tutoring to improve understanding"
    ),

    Rule(
        name="Rec-Time-Management",
        conditions=lambda wm: (wm.get("has_part_time_job", False) and 
                               wm.get("study_hours_per_day", 5) < 2),
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Evaluate if part-time job is sustainable this semester",
                "2. Try to reduce work hours if possible",
                "3. Create master schedule — work, class, study blocks",
                "4. Use weekends for focused study",
                "5. Communicate with employer about academic priorities",
                "6. Track time for 1 week to identify time-wasters",
            ]),
            exp.log("Recommendation-TimeManagement", "Work-study balance needs adjustment", 
                   "Time management plan", 0.82)
        ),
        cf=0.82, priority=8,
        description="Working student needs to balance priorities"
    ),

    Rule(
        name="Rec-External-Support",
        conditions=lambda wm: (wm.get("external_pressure", "LOW") == "HIGH" or
                               wm.get("health_issues", False) or
                               wm.get("financial_stress_level", 3) >= 4),
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Visit campus counseling center — free mental health support",
                "2. Explore financial aid office — emergency funds available",
                "3. Check if campus provides childcare or family services",
                "4. Look into food pantry if financial stress high",
                "5. Speak with dean of students about special circumstances",
                "6. Document personal challenges for academic accommodations",
            ]),
            exp.log("Recommendation-ExternalSupport", "External stressors need institutional support", 
                   "Campus support services plan", 0.83)
        ),
        cf=0.83, priority=9,
        description="Student needs institutional support services"
    ),

    Rule(
        name="Rec-Engagement-Building",
        conditions=lambda wm: wm.get("participation_risk", "GOOD") == "HIGH",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Prepare one question per class",
                "2. Sit in front of classroom — increases engagement",
                "3. Speak with professor about anxiety or hesitation",
                "4. Join relevant clubs or study groups",
                "5. Attend office hours to get more comfortable",
                "6. Practice speaking — toastmasters or debate club",
            ]),
            exp.log("Recommendation-Engagement", "Class participation must increase", 
                   "Engagement building plan", 0.78)
        ),
        cf=0.78, priority=7,
        description="Student needs to increase class participation"
    ),

    Rule(
        name="Rec-Momentum-Build",
        conditions=lambda wm: wm.get("academic_trajectory", "stable") == "improving",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. KEEP DOING WHAT YOU ARE DOING — you are improving!",
                "2. Maintain current study schedule and attendance",
                "3. Set specific goal for final exam (e.g., 75%+)",
                "4. Continue tutoring or study group — clearly working",
                "5. Celebrate progress — you are heading right direction",
                "6. Document what is working — use next semester",
            ]),
            exp.log("Recommendation-Momentum", "Student on upward trajectory — maintain course", 
                   "Momentum building plan", 0.86)
        ),
        cf=0.86, priority=5,
        description="Improving student should maintain momentum"
    ),

    Rule(
        name="Rec-Excellence-Challenge",
        conditions=lambda wm: wm.get("performance_prediction", "Good") == "EXCELLENT",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Consider advanced electives next semester",
                "2. Explore research opportunities in your field",
                "3. Help tutor struggling classmates — solidifies learning",
                "4. Pursue leadership in study groups or clubs",
                "5. Consider double major or minor — you have capacity",
                "6. Build portfolio with deeper projects",
            ]),
            exp.log("Recommendation-Excellence", "Excellent student should be challenged further", 
                   "Advanced challenge plan", 0.91)
        ),
        cf=0.91, priority=5,
        description="Excellent student should pursue advanced opportunities"
    ),

    Rule(
        name="Rec-Recovery-Plan",
        conditions=lambda wm: wm.get("recovery_potential", "NO") == "YES",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. First, identify WHAT CHANGED — what caused initial problem",
                "2. If external factor — address that root cause",
                "3. If academic — get tutoring immediately",
                "4. Set incremental targets — next quiz +10%, next exam +15%",
                "5. Check in with advisor monthly to track recovery",
                "6. Build confidence with quick wins — tackle easier material first",
            ]),
            exp.log("Recommendation-Recovery", "Recovery appears possible with intervention", 
                   "Recovery plan", 0.85)
        ),
        cf=0.85, priority=9,
        description="Student showing improvement can recover if focused"
    ),

    Rule(
        name="Rec-Ongoing-Monitoring",
        conditions=lambda wm: wm.get("overall_risk_level", "LOW") == "MEDIUM",
        actions=lambda wm, exp: (
            wm.add("recommendations", [
                "1. Check in with advisor mid-semester",
                "2. Monitor attendance closely — maintain at 85%+",
                "3. Keep quizzes at 70%+ — early warning indicator",
                "4. Continue current study schedule",
                "5. Be ready to intensify if grades drop further",
                "6. Avoid complacency — risk can quickly increase",
            ]),
            exp.log("Recommendation-Monitoring", "Medium risk requires continued monitoring", 
                   "Ongoing monitoring plan", 0.75)
        ),
        cf=0.75, priority=7,
        description="Monitor medium-risk student for worsening"
    ),
]


# ============================================
# FUNCTION: Build Complete Knowledge Base
# ============================================

def build_knowledge_base():
    """
    Assembles all rules into the knowledge base.
    """
    kb = KnowledgeBase()
    
    # Add all rules in order
    all_rules = (
        attendance_rules +
        academic_rules +
        behavioral_rules +
        composite_rules +
        recommendation_rules
    )
    
    kb.add_rules(all_rules)
    
    print(f"\n✅ Knowledge Base Built Successfully!")
    print(f"   Total Rules: {kb.get_rule_count()}")
    print(f"   - Attendance: {len(attendance_rules)}")
    print(f"   - Academic: {len(academic_rules)}")
    print(f"   - Behavioral: {len(behavioral_rules)}")
    print(f"   - Composite/Conflict: {len(composite_rules)}")
    print(f"   - Recommendations: {len(recommendation_rules)}")
    
    return kb


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    kb = build_knowledge_base()
    print(f"\n📚 Knowledge Base Ready for Inference Engine!")