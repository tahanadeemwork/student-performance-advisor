# ============================================
# Recommendation Generator
# Student Performance Prediction Advisor
# Processes and formats recommendations
# from the inference engine results
# ============================================


class RecommendationProcessor:
    """
    Processes raw recommendations from the
    inference engine and formats them into
    a clean, structured output.
    """

    # Priority levels for recommendations
    PRIORITY_URGENT    = "URGENT"
    PRIORITY_HIGH      = "HIGH"
    PRIORITY_MEDIUM    = "MEDIUM"
    PRIORITY_LOW       = "LOW"

    # Performance level definitions
    PERFORMANCE_LEVELS = {
        "EXCELLENT" : {
            "label"      : "Excellent",
            "emoji"      : "🌟",
            "color"      : "green",
            "description": "Outstanding performance across all areas",
            "priority"   : PRIORITY_LOW
        },
        "GOOD" : {
            "label"      : "Good",
            "emoji"      : "✅",
            "color"      : "blue",
            "description": "Performing well with minor areas to improve",
            "priority"   : PRIORITY_LOW
        },
        "AVERAGE" : {
            "label"      : "Average",
            "emoji"      : "📊",
            "color"      : "orange",
            "description": "Acceptable but needs focused improvement",
            "priority"   : PRIORITY_MEDIUM
        },
        "AT_RISK" : {
            "label"      : "At Risk",
            "emoji"      : "⚠️",
            "color"      : "orange",
            "description": "Warning signs present — intervention needed",
            "priority"   : PRIORITY_HIGH
        },
        "FAILING" : {
            "label"      : "Failing",
            "emoji"      : "🚨",
            "color"      : "red",
            "description": "High probability of failure — urgent action required",
            "priority"   : PRIORITY_URGENT
        },
        "Unknown" : {
            "label"      : "Under Review",
            "emoji"      : "🔍",
            "color"      : "gray",
            "description": "Insufficient data for complete assessment",
            "priority"   : PRIORITY_MEDIUM
        }
    }

    @staticmethod
    def determine_performance_level(results: dict) -> str:
        """
        Determines overall performance level
        from inference engine results.
        """
        # Check direct prediction first
        prediction = results.get("performance_prediction", "")
        if prediction == "FAILING":
            return "FAILING"
        if prediction == "EXCELLENT":
            return "EXCELLENT"

        # Check overall risk level
        risk = results.get("overall_risk_level", "")
        if risk == "CRITICAL":
            return "FAILING"
        if risk == "AT_RISK":
            return "AT_RISK"
        if risk == "HIGH":
            return "AT_RISK"
        if risk == "MEDIUM":
            return "AVERAGE"

        # Check academic status
        academic = results.get("academic_status", "")
        if academic == "EXCELLENT":
            return "EXCELLENT"
        if academic == "STRONG":
            return "EXCELLENT"
        if academic == "GOOD":
            return "GOOD"
        if academic == "PASSING":
            return "AVERAGE"

        # Check academic risk
        academic_risk = results.get("academic_risk_level", "")
        if academic_risk == "CRITICAL":
            return "FAILING"
        if academic_risk == "HIGH":
            return "AT_RISK"
        if academic_risk == "MEDIUM":
            return "AVERAGE"

        # Check attendance risk
        attendance_risk = results.get("attendance_risk_level", "")
        if attendance_risk == "CRITICAL":
            return "AT_RISK"
        if attendance_risk == "HIGH":
            return "AT_RISK"

        # Default
        return "AVERAGE"

    @staticmethod
    def calculate_risk_score(results: dict) -> int:
        """
        Calculates a 0-100 risk score from
        inference engine results.
        Higher = more at risk.
        """
        score = 0

        # Attendance risk contribution (max 30)
        att_risk = results.get("attendance_risk_level", "")
        if att_risk == "CRITICAL":
            score += 30
        elif att_risk == "HIGH":
            score += 22
        elif att_risk == "MEDIUM":
            score += 12
        elif att_risk == "BORDERLINE":
            score += 8

        # Academic risk contribution (max 40)
        acad_risk = results.get("academic_risk_level", "")
        if acad_risk == "CRITICAL":
            score += 40
        elif acad_risk == "HIGH":
            score += 30
        elif acad_risk == "MEDIUM":
            score += 18

        acad_pred = results.get("academic_performance_prediction", "")
        if acad_pred == "LIKELY_FAIL":
            score += 15

        # Study habit contribution (max 15)
        study_risk = results.get("study_habit_risk", "")
        if study_risk == "CRITICAL":
            score += 15
        elif study_risk == "HIGH":
            score += 10

        # External factors (max 15)
        ext = results.get("external_pressure", "")
        if ext == "HIGH":
            score += 10

        concern = results.get("concern_level", "")
        if concern == "URGENT":
            score += 15
        elif concern == "HIGH":
            score += 8

        # Cap at 100
        return min(score, 100)

    @staticmethod
    def identify_primary_risk_factors(results: dict) -> list:
        """
        Identifies the top risk factors from
        inference engine working memory results.
        Returns list of human-readable strings.
        """
        factors = []

        # Attendance factors
        att_risk = results.get("attendance_risk_level", "")
        if att_risk == "CRITICAL":
            factors.append("🔴 Critical attendance shortage (below 60%)")
        elif att_risk == "HIGH":
            factors.append("🟠 High attendance risk (60-75%)")
        elif att_risk == "MEDIUM":
            factors.append("🟡 Borderline attendance (75-85%)")

        att_pattern = results.get("attendance_pattern", "")
        if att_pattern == "CONCERNING":
            factors.append("🔴 Consecutive absences detected")

        # Academic factors
        acad_risk = results.get("academic_risk_level", "")
        if acad_risk == "CRITICAL":
            factors.append("🔴 Critical exam score (below 40%)")
        elif acad_risk == "HIGH":
            factors.append("🟠 Very low exam performance (40-50%)")
        elif acad_risk == "MEDIUM":
            factors.append("🟡 Below average exam score (50-60%)")

        assign_risk = results.get("assignment_risk", "")
        if assign_risk == "CRITICAL":
            factors.append("🔴 Very low assignment completion (below 40%)")
        elif assign_risk == "HIGH":
            factors.append("🟠 Low assignment completion (40-70%)")

        quiz_risk = results.get("quiz_risk", "")
        if quiz_risk == "HIGH":
            factors.append("🟠 Poor quiz performance (below 50%)")

        # Behavioral factors
        study_risk = results.get("study_habit_risk", "")
        if study_risk == "CRITICAL":
            factors.append("🔴 Critically low study hours (below 1 hr/day)")
        elif study_risk == "HIGH":
            factors.append("🟠 Insufficient study hours (1-2 hrs/day)")

        part_risk = results.get("participation_risk", "")
        if part_risk == "HIGH":
            factors.append("🟠 Very low class participation (below 30%)")

        # External factors
        time_risk = results.get("time_constraint_risk", "")
        if time_risk == "HIGH":
            factors.append("🟡 Part-time job limiting study time")

        ext_pressure = results.get("external_pressure", "")
        if ext_pressure == "HIGH":
            factors.append("🟡 Multiple external stressors present")

        fin_stress = results.get("financial_stress_factor", "")
        if fin_stress == "HIGH":
            factors.append("🟡 High financial stress reported")

        health = results.get("health_factor", "")
        if health == "PRESENT":
            factors.append("🟡 Health issues affecting performance")

        # Academic trajectory
        trajectory = results.get("academic_trajectory", "")
        if trajectory == "NEGATIVE":
            factors.append("🟠 Academic performance declining")

        concern = results.get("concern_level", "")
        if concern == "URGENT":
            factors.append("🔴 Sudden sharp drop in performance")

        # Return top 5 factors max
        return factors[:5] if factors else ["No significant risk factors identified"]

    @staticmethod
    def identify_strengths(results: dict) -> list:
        """
        Identifies positive factors from
        inference engine results.
        """
        strengths = []

        # Attendance strengths
        att_status = results.get("attendance_status", "")
        att_strength = results.get("attendance_strength", "")
        if att_strength == "EXCELLENT":
            strengths.append("✅ Excellent attendance (95%+)")
        elif att_status == "GOOD":
            strengths.append("✅ Good attendance (85%+)")

        att_traj = results.get("attendance_trajectory", "")
        if att_traj == "POSITIVE":
            strengths.append("✅ Attendance is improving")

        # Academic strengths
        acad_status = results.get("academic_status", "")
        if acad_status == "EXCELLENT":
            strengths.append("✅ Excellent exam performance (90%+)")
        elif acad_status == "STRONG":
            strengths.append("✅ Strong exam performance (80-90%)")
        elif acad_status == "GOOD":
            strengths.append("✅ Good exam performance (70-80%)")

        assign_status = results.get("assignment_status", "")
        if assign_status == "GOOD":
            strengths.append("✅ Good assignment completion (85%+)")

        quiz_status = results.get("quiz_status", "")
        if quiz_status == "GOOD":
            strengths.append("✅ Consistent quiz performance (75%+)")

        # Behavioral strengths
        study_status = results.get("study_habit_status", "")
        if study_status == "EXCELLENT":
            strengths.append("✅ Excellent study hours (5+/day)")
        elif study_status == "GOOD":
            strengths.append("✅ Good daily study habits (3-5 hrs)")

        part_status = results.get("participation_status", "")
        if part_status == "GOOD":
            strengths.append("✅ Good class participation (70%+)")

        # Positive indicators
        acad_strength = results.get("academic_strength", "")
        if acad_strength == "MULTIPLE":
            strengths.append("✅ Consistent strength across all academic metrics")

        resilience = results.get("resilience_factor", "")
        if resilience == "HIGH":
            strengths.append("✅ Showing resilience despite external challenges")

        recovery = results.get("recovery_potential", "")
        if recovery == "YES":
            strengths.append("✅ Showing improvement — recovery possible")

        return strengths if strengths else ["Keep working — strengths will develop"]

    @classmethod
    def process(cls, engine_results: dict, student_name: str = "") -> dict:
        """
        Main processing function.
        Takes raw inference engine results and
        returns a clean structured recommendation object.
        """
        # Determine performance level
        perf_level = cls.determine_performance_level(engine_results)
        level_info = cls.PERFORMANCE_LEVELS.get(
            perf_level,
            cls.PERFORMANCE_LEVELS["Unknown"]
        )

        # Calculate risk score
        risk_score = cls.calculate_risk_score(engine_results)

        # Get raw recommendations from working memory
        raw_recs = engine_results.get("recommendations", [])

        # Get primary risk factors
        risk_factors = cls.identify_primary_risk_factors(engine_results)

        # Get strengths
        strengths = cls.identify_strengths(engine_results)

        # Get reasoning trace
        reasoning = engine_results.get("reasoning_trace", [])

        # Build final structured output
        processed = {
            "student_name"      : student_name,
            "performance_level" : perf_level,
            "performance_label" : level_info["label"],
            "performance_emoji" : level_info["emoji"],
            "performance_desc"  : level_info["description"],
            "intervention_priority": level_info["priority"],
            "risk_score"        : risk_score,
            "risk_factors"      : risk_factors,
            "strengths"         : strengths,
            "recommendations"   : raw_recs,
            "reasoning_trace"   : reasoning,
            "rules_fired_count" : engine_results.get("fired_rules_count", 0),
            "rules_fired"       : engine_results.get("fired_rules", []),
            "confidence"        : engine_results.get("confidence", 0.0),
        }

        return processed


# ============================================
# QUICK TEST
# ============================================

if __name__ == "__main__":
    print("Testing RecommendationProcessor...")

    # Simulate inference engine results
    sample_results = {
        "attendance_risk_level"  : "HIGH",
        "academic_risk_level"    : "MEDIUM",
        "study_habit_risk"       : "HIGH",
        "participation_risk"     : "HIGH",
        "overall_risk_level"     : "AT_RISK",
        "academic_status"        : "PASSING",
        "assignment_status"      : "GOOD",
        "fired_rules_count"      : 12,
        "fired_rules"            : ["Rule1", "Rule2"],
        "recommendations"        : [
            "1. Schedule meeting with academic advisor this week",
            "2. Increase daily study to 3+ hours",
            "3. Attend every class",
        ],
        "reasoning_trace"        : [
            {"step": 1, "rule": "Attendance-High-Risk",
             "description": "Attendance 60-75%",
             "conclusion": "HIGH risk",
             "cf_percent": "85%"}
        ]
    }

    result = RecommendationProcessor.process(
        sample_results, "Test Student"
    )

    print(f"\n  Student         : {result['student_name']}")
    print(f"  Performance     : {result['performance_emoji']} {result['performance_label']}")
    print(f"  Risk Score      : {result['risk_score']}/100")
    print(f"  Priority        : {result['intervention_priority']}")
    print(f"\n  Risk Factors ({len(result['risk_factors'])}):")
    for f in result['risk_factors']:
        print(f"    {f}")
    print(f"\n  Strengths ({len(result['strengths'])}):")
    for s in result['strengths']:
        print(f"    {s}")
    print(f"\n  Recommendations ({len(result['recommendations'])}):")
    for r in result['recommendations']:
        print(f"    {r}")

    print(f"\n✅ RecommendationProcessor working perfectly!")