# ============================================
# Streamlit Web Interface
# Student Performance Prediction Advisor
# Complete UI for the Expert System
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from inference_engine.engine    import InferenceEngine
from knowledge_base.rules       import build_knowledge_base
from input_handler.student_profile  import StudentProfile
from input_handler.input_validator  import InputValidator
from output_handler.recommendation  import RecommendationProcessor
from output_handler.report_generator import ReportGenerator


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title = "Student Performance Advisor",
    page_icon  = "🎓",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)


# ============================================
# CUSTOM CSS STYLING
# ============================================

st.markdown("""
<style>
    /* Main background */
    .main { background-color: #f8fafc; }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #1e3a8a, #2563eb, #7c3aed);
        padding: 30px 40px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    .hero-banner h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-banner p {
        font-size: 1rem;
        opacity: 0.85;
        margin: 0;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        text-align: center;
    }

    /* Result cards */
    .result-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }

    /* Risk factor items */
    .risk-item {
        padding: 10px 15px;
        border-radius: 8px;
        margin: 6px 0;
        font-size: 14px;
    }

    /* Recommendation items */
    .rec-item {
        background: #f0f9ff;
        border-left: 4px solid #2563eb;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0;
        font-size: 14px;
    }

    /* Strength items */
    .strength-item {
        background: #f0fdf4;
        border-left: 4px solid #059669;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0;
        font-size: 14px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin: 20px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Verdict banner */
    .verdict-excellent { background: #d1fae5; border: 2px solid #059669;
                         border-radius: 12px; padding: 20px; text-align: center; }
    .verdict-good      { background: #dbeafe; border: 2px solid #2563eb;
                         border-radius: 12px; padding: 20px; text-align: center; }
    .verdict-average   { background: #fef3c7; border: 2px solid #d97706;
                         border-radius: 12px; padding: 20px; text-align: center; }
    .verdict-atrisk    { background: #ffedd5; border: 2px solid #ea580c;
                         border-radius: 12px; padding: 20px; text-align: center; }
    .verdict-failing   { background: #fee2e2; border: 2px solid #dc2626;
                         border-radius: 12px; padding: 20px; text-align: center; }

    /* Reasoning trace */
    .trace-item {
        background: #1e293b;
        color: #e2e8f0;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 6px 0;
        font-family: monospace;
        font-size: 13px;
    }

    /* Sidebar */
    .sidebar-info {
        background: #f1f5f9;
        padding: 12px;
        border-radius: 8px;
        font-size: 13px;
        margin: 8px 0;
    }

    /* Hide streamlit defaults */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================
# INITIALIZE SESSION STATE
# ============================================

if "kb" not in st.session_state:
    st.session_state.kb      = build_knowledge_base()
    st.session_state.engine  = InferenceEngine(st.session_state.kb)
    st.session_state.results = None
    st.session_state.analyzed = False


# ============================================
# HELPER FUNCTIONS
# ============================================

def create_gauge_chart(risk_score: int, color: str) -> go.Figure:
    """Creates a gauge chart for risk score"""
    fig = go.Figure(go.Indicator(
        mode  = "gauge+number",
        value = risk_score,
        title = {"text": "Risk Score", "font": {"size": 16}},
        gauge = {
            "axis"  : {"range": [0, 100], "tickwidth": 1},
            "bar"   : {"color": color},
            "steps" : [
                {"range": [0, 25],  "color": "#d1fae5"},
                {"range": [25, 50], "color": "#fef3c7"},
                {"range": [50, 75], "color": "#ffedd5"},
                {"range": [75, 100],"color": "#fee2e2"},
            ],
            "threshold": {
                "line" : {"color": "red", "width": 3},
                "thickness": 0.75,
                "value": 75
            }
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="white"
    )
    return fig


def create_radar_chart(student_data: dict) -> go.Figure:
    """Creates a radar chart of student metrics"""
    categories = [
        "Attendance",
        "Midterm Score",
        "Assignments",
        "Quiz Average",
        "Study Hours",
        "Participation"
    ]

    # Normalize study hours to 0-100 scale (max = 8 hrs)
    study_normalized = min(
        student_data.get("study_hours_per_day", 0) / 8 * 100, 100
    )

    values = [
        student_data.get("attendance", 0),
        student_data.get("midterm_score", 0),
        student_data.get("assignment_completion_rate", 0),
        student_data.get("quiz_average", 0),
        study_normalized,
        student_data.get("participation_level", 0),
    ]

    fig = go.Figure(go.Scatterpolar(
        r      = values + [values[0]],
        theta  = categories + [categories[0]],
        fill   = "toself",
        fillcolor = "rgba(37, 99, 235, 0.15)",
        line   = dict(color="#2563eb", width=2),
        name   = "Student Profile"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        height=320,
        margin=dict(t=30, b=30, l=40, r=40),
        paper_bgcolor="white"
    )
    return fig


def create_bar_chart(student_data: dict) -> go.Figure:
    """Creates a bar chart comparing all metrics"""
    metrics = [
        "Attendance",
        "Midterm",
        "Assignments",
        "Quizzes",
        "Participation",
        "Prev. Avg"
    ]

    values = [
        student_data.get("attendance", 0),
        student_data.get("midterm_score", 0),
        student_data.get("assignment_completion_rate", 0),
        student_data.get("quiz_average", 0),
        student_data.get("participation_level", 0),
        student_data.get("prev_semester_avg", 0),
    ]

    colors = [
        "#dc2626" if v < 60 else "#d97706" if v < 75 else "#059669"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x              = metrics,
        y              = values,
        marker_color   = colors,
        text           = [f"{v}%" for v in values],
        textposition   = "outside",
    ))

    fig.add_hline(
        y=60, line_dash="dash",
        line_color="red", opacity=0.5,
        annotation_text="Minimum (60%)"
    )
    fig.add_hline(
        y=75, line_dash="dash",
        line_color="orange", opacity=0.5,
        annotation_text="Target (75%)"
    )

    fig.update_layout(
        yaxis=dict(range=[0, 110], title="Score (%)"),
        xaxis=dict(title="Metric"),
        height=350,
        margin=dict(t=20, b=20, l=40, r=40),
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        showlegend=False
    )
    return fig


def get_verdict_class(level: str) -> str:
    """Returns CSS class for verdict banner"""
    mapping = {
        "EXCELLENT": "verdict-excellent",
        "GOOD"     : "verdict-good",
        "AVERAGE"  : "verdict-average",
        "AT_RISK"  : "verdict-atrisk",
        "FAILING"  : "verdict-failing",
    }
    return mapping.get(level, "verdict-average")


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## 🎓 About This System")
    st.markdown("""
    <div class="sidebar-info">
    <strong>Student Performance Prediction Advisor</strong><br><br>
    A rule-based Expert System that analyzes student academic data and provides:
    <ul>
    <li>Performance prediction</li>
    <li>Risk assessment</li>
    <li>Root cause analysis</li>
    <li>Personalized recommendations</li>
    <li>Explainable AI reasoning</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 System Stats")

    kb = st.session_state.kb
    st.metric("Total Rules", kb.get_rule_count())
    st.metric("Rule Categories", "5")
    st.metric("Inference Type", "Forward Chaining")
    st.metric("CF Method", "Certainty Factors")

    st.markdown("---")
    st.markdown("### 📁 Rule Categories")
    rule_data = {
        "Category"   : [
            "Attendance",
            "Academic",
            "Behavioral",
            "Composite",
            "Recommendations"
        ],
        "Rules" : [10, 18, 12, 18, 12]
    }
    df = pd.DataFrame(rule_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown("### ℹ️ Performance Levels")
    st.markdown("""
    - 🌟 **Excellent** — Outstanding
    - ✅ **Good** — Performing well
    - 📊 **Average** — Needs focus
    - ⚠️ **At Risk** — Intervention needed
    - 🚨 **Failing** — Urgent action
    """)

    st.markdown("---")
    st.caption("AI Course — BS CS 4th Semester")
    st.caption("Expert System Term Project")


# ============================================
# MAIN PAGE
# ============================================

# Hero Banner
st.markdown("""
<div class="hero-banner">
    <h1>🎓 Student Performance Prediction Advisor</h1>
    <p>Intelligent Rule-Based Expert System | Forward Chaining | Certainty Factors | Explainable AI</p>
</div>
""", unsafe_allow_html=True)


# ============================================
# TABS
# ============================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Enter Student Data",
    "📊 Analysis Results",
    "🧠 Reasoning Chain",
    "📋 Sample Profiles"
])


# ============================================
# TAB 1 — STUDENT DATA INPUT
# ============================================

with tab1:
    st.markdown("### Enter Student Information")
    st.info(
        "Fill in all fields below and click **Analyze Performance** "
        "to get the expert system prediction."
    )

    with st.form("student_form"):

        # ── Personal Information ──────────────
        st.markdown(
            '<div class="section-header">👤 Personal Information</div>',
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input(
                "Student Name *",
                placeholder="e.g. Ali Hassan"
            )
        with col2:
            student_id = st.text_input(
                "Student ID *",
                placeholder="e.g. F21-001"
            )
        with col3:
            semester = st.selectbox(
                "Current Semester *",
                options=list(range(1, 9)),
                index=3
            )

        st.markdown("---")

        # ── Academic Performance ──────────────
        st.markdown(
            '<div class="section-header">📚 Academic Performance</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            midterm_score = st.slider(
                "Midterm Exam Score (%)",
                min_value=0, max_value=100,
                value=65, step=1,
                help="Score obtained in midterm examination"
            )
        with col2:
            assignment_rate = st.slider(
                "Assignment Completion Rate (%)",
                min_value=0, max_value=100,
                value=75, step=1,
                help="Percentage of assignments submitted"
            )
        with col3:
            quiz_average = st.slider(
                "Quiz Average Score (%)",
                min_value=0, max_value=100,
                value=60, step=1,
                help="Average score across all quizzes"
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            lab_rate = st.slider(
                "Lab Work Completion (%)",
                min_value=0, max_value=100,
                value=70, step=1,
                help="Percentage of lab work completed"
            )
        with col2:
            prev_avg = st.slider(
                "Previous Semester Average (%)",
                min_value=0, max_value=100,
                value=65, step=1,
                help="Average score from last semester"
            )
        with col3:
            failed_count = st.number_input(
                "Failed Subjects (History)",
                min_value=0, max_value=10,
                value=0, step=1,
                help="Number of subjects previously failed"
            )

        col1, col2 = st.columns(2)
        with col1:
            academic_trend = st.selectbox(
                "Academic Performance Trend",
                options=["improving", "stable", "declining"],
                index=1,
                help="How grades have changed recently"
            )

        st.markdown("---")

        # ── Attendance ────────────────────────
        st.markdown(
            '<div class="section-header">📅 Attendance</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            attendance = st.slider(
                "Attendance Percentage (%)",
                min_value=0, max_value=100,
                value=80, step=1,
                help="Overall attendance percentage"
            )
        with col2:
            consec_absences = st.number_input(
                "Consecutive Days Absent",
                min_value=0, max_value=30,
                value=0, step=1,
                help="Maximum consecutive days absent"
            )
        with col3:
            attendance_trend = st.selectbox(
                "Attendance Trend",
                options=["improving", "stable", "declining"],
                index=1,
                help="How attendance has changed recently"
            )

        st.markdown("---")

        # ── Behavioral Factors ────────────────
        st.markdown(
            '<div class="section-header">🧍 Behavioral Factors</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            study_hours = st.slider(
                "Study Hours Per Day",
                min_value=0.0, max_value=12.0,
                value=2.0, step=0.5,
                help="Average hours spent studying daily"
            )
        with col2:
            participation = st.slider(
                "Class Participation Level (%)",
                min_value=0, max_value=100,
                value=50, step=5,
                help="How actively student participates"
            )
        with col3:
            has_job = st.checkbox(
                "Has Part-Time Job",
                value=False,
                help="Student works part-time alongside studies"
            )

        st.markdown("---")

        # ── Personal Factors ──────────────────
        st.markdown(
            '<div class="section-header">👤 Personal Factors</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            financial_stress = st.select_slider(
                "Financial Stress Level",
                options=[1, 2, 3, 4, 5],
                value=2,
                help="1 = No stress, 5 = Extreme stress"
            )
        with col2:
            health_issues = st.checkbox(
                "Has Health Issues",
                value=False,
                help="Student has ongoing health problems"
            )
        with col3:
            family_resp = st.select_slider(
                "Family Responsibilities",
                options=[0, 1, 2, 3, 4, 5],
                value=1,
                help="0 = None, 5 = Very high responsibilities"
            )

        st.markdown("---")

        # ── Submit Button ─────────────────────
        submitted = st.form_submit_button(
            "🔍 Analyze Performance",
            use_container_width=True,
            type="primary"
        )

    # ── Process Form Submission ───────────────
    if submitted:
        # Build student profile
        profile = StudentProfile()
        profile.name                        = name
        profile.student_id                  = student_id
        profile.semester                    = semester
        profile.midterm_score               = midterm_score
        profile.assignment_completion_rate  = assignment_rate
        profile.quiz_average                = quiz_average
        profile.lab_completion_rate         = lab_rate
        profile.prev_semester_avg           = prev_avg
        profile.failed_subjects_count       = int(failed_count)
        profile.academic_trend              = academic_trend
        profile.attendance                  = attendance
        profile.days_absent_consecutively   = int(consec_absences)
        profile.attendance_trend            = attendance_trend
        profile.study_hours_per_day         = study_hours
        profile.participation_level         = participation
        profile.has_part_time_job           = has_job
        profile.financial_stress_level      = financial_stress
        profile.health_issues               = health_issues
        profile.family_responsibilities     = family_resp
        profile.is_first_semester           = (semester == 1)

        # Validate
        validation = InputValidator.validate_profile(profile)

        if not validation.is_valid:
            st.error("❌ Please fix the following errors:")
            for err in validation.get_error_messages():
                st.error(f"• {err}")
        else:
            # Show warnings if any
            if validation.warnings:
                for warn in validation.get_warning_messages():
                    st.warning(f"⚠️ {warn}")

            # Run inference engine
            with st.spinner("🧠 Running Expert System Analysis..."):
                student_dict = profile.to_dict()
                engine_results = st.session_state.engine.run(student_dict)

                # Process results
                processed = RecommendationProcessor.process(
                    engine_results, name
                )
                st_data = ReportGenerator.generate_streamlit_data(
                    processed, student_dict
                )
                console_report = ReportGenerator.generate_console_report(
                    processed, student_dict
                )

                # Store in session state
                st.session_state.results        = st_data
                st.session_state.processed      = processed
                st.session_state.student_dict   = student_dict
                st.session_state.console_report = console_report
                st.session_state.analyzed       = True

            st.success(
                "✅ Analysis complete! Go to the "
                "**📊 Analysis Results** tab to see your results."
            )
            st.balloons()


# ============================================
# TAB 2 — ANALYSIS RESULTS
# ============================================

with tab2:
    if not st.session_state.analyzed:
        st.info(
            "👈 Please enter student data in the "
            "**📝 Enter Student Data** tab first."
        )
    else:
        data       = st.session_state.results
        processed  = st.session_state.processed
        student_dict = st.session_state.student_dict

        # ── Verdict Banner ────────────────────
        level      = data["performance_level"]
        verdict_cls = get_verdict_class(level)

        st.markdown(f"""
        <div class="{verdict_cls}">
            <h2 style="margin:0; font-size:2rem;">
                {data['performance_emoji']} {data['performance_label']}
            </h2>
            <p style="margin:8px 0 0 0; font-size:1rem;">
                {data['performance_desc']}
            </p>
            <p style="margin:4px 0 0 0; font-size:0.85rem; opacity:0.7;">
                Analysis for: <strong>{data['student_name']}</strong> |
                ID: {data['student_id']} |
                Semester: {data['semester']} |
                {data['generated_at']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Top Metrics Row ───────────────────
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            gauge_color = ReportGenerator.get_gauge_color(data["risk_score"])
            st.plotly_chart(
                create_gauge_chart(data["risk_score"], gauge_color),
                use_container_width=True
            )

        with col2:
            st.metric(
                "Attendance",
                f"{data['attendance']}%",
                delta=f"{'✅ Good' if data['attendance'] >= 85 else '⚠️ Low'}"
            )
            st.metric(
                "Midterm Score",
                f"{data['midterm_score']}%",
                delta=f"{'✅ Good' if data['midterm_score'] >= 70 else '⚠️ Low'}"
            )

        with col3:
            st.metric(
                "Assignments",
                f"{data['assignment_rate']}%",
                delta=f"{'✅ Good' if data['assignment_rate'] >= 80 else '⚠️ Low'}"
            )
            st.metric(
                "Quiz Average",
                f"{data['quiz_average']}%",
                delta=f"{'✅ Good' if data['quiz_average'] >= 70 else '⚠️ Low'}"
            )

        with col4:
            st.metric(
                "Study Hours",
                f"{data['study_hours']} hrs/day",
                delta=f"{'✅ Good' if data['study_hours'] >= 3 else '⚠️ Low'}"
            )
            st.metric(
                "Participation",
                f"{data['participation']}%",
                delta=f"{'✅ Good' if data['participation'] >= 70 else '⚠️ Low'}"
            )

        st.markdown("---")

        # ── Charts Row ────────────────────────
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div class="section-header">📡 Student Profile Radar</div>',
                unsafe_allow_html=True
            )
            st.plotly_chart(
                create_radar_chart(student_dict),
                use_container_width=True
            )

        with col2:
            st.markdown(
                '<div class="section-header">📊 Performance by Metric</div>',
                unsafe_allow_html=True
            )
            st.plotly_chart(
                create_bar_chart(student_dict),
                use_container_width=True
            )

        st.markdown("---")

        # ── Risk Factors and Strengths ────────
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div class="section-header">🔴 Primary Risk Factors</div>',
                unsafe_allow_html=True
            )
            if data["risk_factors"]:
                for factor in data["risk_factors"]:
                    st.markdown(
                        f'<div class="risk-item">{factor}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.success("No significant risk factors identified")

        with col2:
            st.markdown(
                '<div class="section-header">✅ Identified Strengths</div>',
                unsafe_allow_html=True
            )
            if data["strengths"]:
                for strength in data["strengths"]:
                    st.markdown(
                        f'<div class="strength-item">{strength}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("Keep working — strengths will develop")

        st.markdown("---")

        # ── Recommendations ───────────────────
        st.markdown(
            '<div class="section-header">💡 Personalized Recommendations</div>',
            unsafe_allow_html=True
        )

        priority = data["intervention_priority"]
        if priority == "URGENT":
            st.error(f"🚨 URGENT — Immediate action required")
        elif priority == "HIGH":
            st.warning(f"⚠️ HIGH PRIORITY — Act this week")
        elif priority == "MEDIUM":
            st.info(f"📋 MEDIUM PRIORITY — Address soon")
        else:
            st.success(f"✅ LOW PRIORITY — Keep up the good work")

        if data["recommendations"]:
            for rec in data["recommendations"]:
                st.markdown(
                    f'<div class="rec-item">💡 {rec}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.success("Continue current performance — you are doing great!")

        st.markdown("---")

        # ── Download Report ───────────────────
        st.markdown(
            '<div class="section-header">📥 Download Report</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            label      = "📄 Download Full Text Report",
            data       = st.session_state.console_report,
            file_name  = f"report_{data['student_id']}.txt",
            mime       = "text/plain",
            use_container_width=True
        )


# ============================================
# TAB 3 — REASONING CHAIN
# ============================================

with tab3:
    if not st.session_state.analyzed:
        st.info(
            "👈 Please enter student data in the "
            "**📝 Enter Student Data** tab first."
        )
    else:
        data = st.session_state.results
        trace = data["reasoning_trace"]

        st.markdown("### 🧠 Expert System Reasoning Chain")
        st.markdown(
            "This shows exactly how the expert system reached its conclusion — "
            "every rule that fired, every condition that was satisfied, "
            "and every confidence score assigned."
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rules Fired", data["rules_fired"])
        with col2:
            st.metric("Total Rules in KB", data["total_rules"])
        with col3:
            st.metric("Reasoning Steps", len(trace))

        st.markdown("---")

        if trace:
            for entry in trace:
                with st.expander(
                    f"Step {entry.get('step', '?')} — "
                    f"{entry.get('rule', 'Unknown')} "
                    f"[{entry.get('cf_percent', '?')} confidence]",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Rule Name:**")
                        st.code(entry.get("rule", ""), language="text")
                        st.markdown("**Condition Satisfied:**")
                        st.info(entry.get("description", ""))
                    with col2:
                        st.markdown("**Conclusion Reached:**")
                        st.success(entry.get("conclusion", ""))
                        st.markdown("**Confidence Level:**")
                        cf_val = entry.get("cf_percent", "0%")
                        cf_num = int(cf_val.replace("%", ""))
                        st.progress(cf_num / 100)
                        st.caption(
                            f"{cf_val} — "
                            f"{entry.get('cf_label', '')}"
                        )
        else:
            st.warning("No reasoning trace available for this analysis.")

        st.markdown("---")
        st.markdown("### 📌 How Forward Chaining Works")
        st.markdown("""
        1. **Load Facts** — Student data loaded into Working Memory
        2. **Match Rules** — Engine checks all 70 rules against facts
        3. **Conflict Set** — All satisfied rules collected
        4. **Resolve** — Highest priority + CF rule selected
        5. **Fire Rule** — Conclusion added to Working Memory
        6. **Repeat** — Until no more rules can fire
        7. **Output** — Final conclusions + reasoning chain returned
        """)


# ============================================
# TAB 4 — SAMPLE PROFILES
# ============================================

with tab4:
    st.markdown("### 📋 Test with Sample Student Profiles")
    st.markdown(
        "Click any profile below to instantly analyze "
        "a pre-built student scenario."
    )

    profiles = StudentProfile.create_sample_profiles()

    for profile_name, profile in profiles:
        with st.expander(f"👤 {profile_name}", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Academic**")
                st.write(f"Midterm: {profile.midterm_score}%")
                st.write(f"Assignments: {profile.assignment_completion_rate}%")
                st.write(f"Quiz Avg: {profile.quiz_average}%")

            with col2:
                st.markdown("**Attendance & Study**")
                st.write(f"Attendance: {profile.attendance}%")
                st.write(f"Study Hours: {profile.study_hours_per_day} hrs/day")
                st.write(f"Participation: {profile.participation_level}%")

            with col3:
                st.markdown("**Personal**")
                st.write(f"Part-time Job: {'Yes' if profile.has_part_time_job else 'No'}")
                st.write(f"Financial Stress: {profile.financial_stress_level}/5")
                st.write(f"Health Issues: {'Yes' if profile.health_issues else 'No'}")

            if st.button(
                f"🔍 Analyze {profile_name}",
                key=f"btn_{profile_name}"
            ):
                with st.spinner(f"Analyzing {profile_name}..."):
                    student_dict = profile.to_dict()
                    engine_results = st.session_state.engine.run(student_dict)

                    processed = RecommendationProcessor.process(
                        engine_results, profile.name
                    )
                    st_data = ReportGenerator.generate_streamlit_data(
                        processed, student_dict
                    )
                    console_report = ReportGenerator.generate_console_report(
                        processed, student_dict
                    )

                    st.session_state.results        = st_data
                    st.session_state.processed      = processed
                    st.session_state.student_dict   = student_dict
                    st.session_state.console_report = console_report
                    st.session_state.analyzed       = True

                st.success(
                    f"✅ {profile_name} analyzed! "
                    f"Go to **📊 Analysis Results** tab."
                )