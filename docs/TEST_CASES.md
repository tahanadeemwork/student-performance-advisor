# Student Performance Advisor — Test Cases

This document describes the 10 student scenarios used by the project test suite. These scenarios are defined in `tests/test_scenarios.py` and are used to validate input handling, inference behavior, and recommendation output.

## Running the Test Suite

From the repository root:

```bash
python main.py test
```

The test runner performs validation and processes each scenario through the inference engine.

## Test Scenario List

1. **Excellent Student**
   - High midterm score (88)
   - Strong assignment, quiz, and lab completion
   - Excellent attendance and participation
   - Expected outcome: excellent performance with low risk

2. **Good Student**
   - Good academic scores (midterm 74)
   - High assignment completion
   - Stable attendance and behavior
   - Expected outcome: good performance with minor recommendations

3. **Average Student**
   - Moderate academic scores (midterm 62)
   - Average attendance and engagement
   - Expected outcome: average performance with targeted improvement areas

4. **At-Risk Student**
   - Low academic scores (midterm 48)
   - Poor attendance, declining trends, part-time job stress
   - Expected outcome: at-risk performance with urgent intervention

5. **Failing Student**
   - Very low academic scores (midterm 28)
   - Low completion rates, high stress, health issues
   - Expected outcome: failing performance with urgent corrective actions

6. **Conflict: Good Grades Poor Attendance**
   - Strong academic performance but attendance below 60%
   - Tests the system's ability to weigh attendance risk against academic strength
   - Expected outcome: risk flagged despite good scores

7. **Conflict: Good Attendance Poor Grades**
   - Excellent attendance but weak exam performance
   - Verifies detection of academic risk separate from attendance
   - Expected outcome: academic intervention recommended

8. **Improving Student**
   - Mid-level scores with improving academic and attendance trends
   - Expected outcome: positive trend recognized and risk moderated

9. **High External Pressure**
   - Moderate academic scores but high financial, health, and family stress
   - Part-time job and external pressures are included
   - Expected outcome: external risk factors highlighted with supportive recommendations

10. **First Semester Student**
    - First-semester profile with no prior average
    - Tests handling of new students with limited history
    - Expected outcome: adjusted risk assessment for early semester conditions

## What the Test Runner Checks

- Input validation success for valid scenario data
- No validation errors for accepted scenarios
- Inference engine execution without runtime errors
- Recommendation generation and risk scoring
- Rule firing counts and reasoning trace availability

## Notes

The scenarios are intentionally diverse to cover:

- strong academic cases
- attendance conflicts
- external and personal stressors
- failing and at-risk students
- improving and first-semester students

Use this file as a reference when extending the rule base or adding new student profiles.
