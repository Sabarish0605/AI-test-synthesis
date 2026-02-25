import streamlit as st
import json
import os
from requirement_engine import extract_requirement, compare_requirements
from test_engine import generate_test_cases, TestArtifactGenerator
from metrics import calculate_coverage

# Page Config
st.set_page_config(
    page_title="AI QA Architect • Premium Dashboard",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Enterprise Glass-morphism CSS
st.markdown("""
<style>
    /* Dark Mode Global Overrides */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0D1117;
        color: #E5E7EB;
    }
    
    .stApp {
        background-color: #0D1117;
    }
    
    /* Fade-in Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-container {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Glassmorphism Panel */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .glass-card:hover {
        transform: translateY(-4px) scale(1.005);
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(76, 139, 245, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Left-accented Card */
    .accent-card {
        border-left: 4px solid #4C8BF5;
    }
    
    /* Header Typography */
    .dashboard-header {
        text-align: center;
        padding: 40px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 40px;
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #F8FAFC 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }
    
    .header-subtitle {
        font-size: 1rem;
        font-weight: 400;
        color: #94A3B8;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    /* Modern Navigation Pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        justify-content: center;
        margin-bottom: 30px;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 24px !important;
        padding: 0 24px !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(76, 139, 245, 0.1) !important;
        color: #4C8BF5 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4C8BF5 !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(76, 139, 245, 0.4) !important;
    }
    
    /* Section Headers */
    .section-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .section-head span {
        width: 4px;
        height: 24px;
        background: #4C8BF5;
        border-radius: 2px;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #F8FAFC;
    }
    
    /* Metric Stripe Dashboard */
    .stat-box {
        background: rgba(255, 255, 255, 0.02);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.2s ease;
    }
    
    .stat-box:hover {
        transform: scale(1.02);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 4px;
    }
    
    /* Indicators */
    .indicator { opacity: 0.8; margin-right: 8px; font-size: 0.8rem; }
    .status-add { color: #10B981; }
    .status-rem { color: #EF4444; }
    .status-mod { color: #FACC15; }
    .status-risk { color: #F97316; }

    /* Hide redundant Streamlit UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Input Styling */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #E5E7EB !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #4C8BF5, #22D3EE) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(76, 139, 245, 0.5) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Dashboard Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Top Premium Header
st.markdown("""
<div class="dashboard-header">
    <div class="header-subtitle">Enterprise QA Platform</div>
    <div class="header-title">AI QA ARCHITECT</div>
</div>
""", unsafe_allow_html=True)

# Session State Persistence
if 'structured_data' not in st.session_state: st.session_state.structured_data = None
if 'test_cases' not in st.session_state: st.session_state.test_cases = None
if 'automation_script' not in st.session_state: st.session_state.automation_script = None
if 'traceability' not in st.session_state: st.session_state.traceability = None
if 'metrics' not in st.session_state: st.session_state.metrics = None
if 'diff' not in st.session_state: st.session_state.diff = None

# Custom Modern Navigation
tabs = st.tabs(["REQUIREMENT ANALYSIS", "TEST DESIGN", "AUTOMATION", "CHANGE IMPACT", "INTELLIGENCE DASHBOARD"])

# --- TAB 1: REQUIREMENT ANALYSIS ---
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-head"><span></span><div class="section-title">Input Specification</div></div>', unsafe_allow_html=True)
    req_input = st.text_area("Enter raw requirement text for deep synthesis...", height=180, label_visibility="collapsed")
    
    if st.button("RUN SYNTHESIS ENGINE", use_container_width=True):
        if req_input:
            with st.spinner("SYTHESIZING QA INTELLIGENCE..."):
                data = extract_requirement(req_input)
                st.session_state.structured_data = data
                
                engine_data = {
                    "feature": data.get("feature_name", "Unknown"),
                    "functional_fields": data.get("functional_fields", []),
                    "validations": data.get("validations", {}),
                    "roles": data.get("actors", []),
                    "edge_cases": data.get("edge_cases", []),
                    "risk_analysis": data.get("risk_analysis", {})
                }
                
                st.session_state.test_cases = generate_test_cases(engine_data)
                generator = TestArtifactGenerator()
                st.session_state.automation_script = generator.generate_selenium_java(engine_data)
                st.session_state.traceability = generator.create_traceability_matrix(engine_data, st.session_state.test_cases)
                st.session_state.metrics = calculate_coverage(data, st.session_state.test_cases)
                st.rerun()
        else:
            st.error("Input required for synthesis.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.structured_data:
        data = st.session_state.structured_data
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div class="glass-card accent-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-head"><span></span><div class="section-title">Functional Schema</div></div>', unsafe_allow_html=True)
            st.markdown(f"**Identified Feature:** `{data.get('feature_name') or 'N/A'}`")
            st.markdown("**User Persona (Actors):**")
            for a in data.get('actors', []): st.write(f"▪ {a}")
            st.markdown("**Field Discovery:**")
            for f in data.get('functional_fields', []): st.markdown(f"<span style='color:#4C8BF5'>▣</span> {f}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-head"><span></span><div class="section-title">Validation Protocol</div></div>', unsafe_allow_html=True)
            with st.container(height=300, border=False):
                st.json(data.get('validations', {}))
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-head"><span></span><div class="section-title">Critical Insight Matrix</div></div>', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("<p class='status-risk'>HIGH RISK AREAS</p>", unsafe_allow_html=True)
            for h in data.get('risk_analysis', {}).get('high_risk_areas', []): st.write(f"▪ {h}")
            st.markdown("<p style='color:#94A3B8; margin-top:20px;'>AMBIGUITIES DETECTED</p>", unsafe_allow_html=True)
            for a in data.get('risk_analysis', {}).get('ambiguities', []): st.write(f"▪ {a}")
        with r2:
            st.markdown("<p style='color:#22D3EE'>EDGE CASES</p>", unsafe_allow_html=True)
            for e in data.get('edge_cases', []): st.write(f"▪ {e}")
            st.markdown("<p style='color:#EF4444; margin-top:20px;'>MISSING SPECIFICATIONS</p>", unsafe_allow_html=True)
            for m in data.get('risk_analysis', {}).get('missing_requirements', []): st.write(f"▪ {m}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: TEST DESIGN ---
with tabs[1]:
    if st.session_state.test_cases:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-head"><span></span><div class="section-title">Synthesized Test Suite</div></div>', unsafe_allow_html=True)
        for tc in st.session_state.test_cases:
            t_type = tc.get('type', 'Positive')
            accent_color = "#10B981" if t_type == "Positive" else "#EF4444" if t_type == "Negative" else "#FACC15"
            with st.expander(f"▪ {tc.get('tc_id')}: {tc.get('title')}"):
                st.markdown(f"<span style='color:{accent_color}; font-weight:600;'>{t_type.upper()}</span> | PRIORITY: `{tc.get('priority')}`", unsafe_allow_html=True)
                st.markdown("**Execution Steps:**")
                for i, s in enumerate(tc.get('steps', [])): st.write(f"{i+1}. {s}")
                st.markdown(f"**Expected Outcome:** <span style='color:#10B981'>{tc.get('expected_result')}</span>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("DOWNLOAD TEST JSON", json.dumps(st.session_state.test_cases, indent=2), "test_suite.json", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Initiate synthesis to generate test design artifacts.")

# --- TAB 3: AUTOMATION ---
with tabs[2]:
    if st.session_state.automation_script:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-head"><span></span><div class="section-title">Automation Scaffolding (Java/POM)</div></div>', unsafe_allow_html=True)
        st.markdown("Raw Selenium source generated via Senior Architect protocols.")
        st.code(st.session_state.automation_script, language="java")
        st.download_button("EXPORT JAVA CLASS", st.session_state.automation_script, "QABundle.java", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Automation scripts will be generated post-synthesis.")

# --- TAB 4: CHANGE IMPACT ---
with tabs[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-head"><span></span><div class="section-title">Baseline Comparison</div></div>', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    old = colA.text_area("Baseline Specification (V1)", height=150, placeholder="Reference text...")
    new = colB.text_area("Current Document (V2)", height=150, placeholder="Updated text...")
    if st.button("CALCULATE IMPACT DELTA", use_container_width=True):
        if old and new:
            st.session_state.diff = compare_requirements(old, new)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.diff:
        diff = st.session_state.diff
        st.markdown('<div class="glass-card accent-card">', unsafe_allow_html=True)
        st.markdown(f"#### IMPACT ANALYSIS: {diff.get('impact_analysis_summary') or 'Calculation Complete'}")
        st.markdown("---")
        dA, dB = st.columns(2)
        with dA:
            st.markdown("<p class='status-add'>▣ ADDED FIELDS</p>", unsafe_allow_html=True)
            for f in diff.get('added_fields', []): st.write(f"▪ {f}")
            st.markdown("<p class='status-mod' style='margin-top:20px;'>▣ MODIFIED RULES</p>", unsafe_allow_html=True)
            for r in diff.get('modified_rules', []): st.write(f"▪ {r}")
        with dB:
            st.markdown("<p class='status-rem'>▣ DEPRECATED FIELDS</p>", unsafe_allow_html=True)
            for f in diff.get('removed_fields', []): st.write(f"▪ {f}")
            st.markdown("<p class='status-risk' style='margin-top:20px;'>▣ RISK VECTOR INCREASE</p>", unsafe_allow_html=True)
            for r in diff.get('risk_increase', []): st.write(f"▪ {r}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 5: INTELLIGENCE DASHBOARD ---
with tabs[4]:
    if st.session_state.metrics:
        m = st.session_state.metrics
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-head"><span></span><div class="section-title">Operational Health Metrics</div></div>', unsafe_allow_html=True)
        
        m_cols = st.columns(4)
        with m_cols[0]:
            st.markdown(f'<div class="stat-box"><div class="stat-label">Total Test Cases</div><div class="stat-value">{m.get("total_test_cases")}</div></div>', unsafe_allow_html=True)
        with m_cols[1]:
            st.markdown(f'<div class="stat-box"><div class="stat-label">Coverage Index</div><div class="stat-value">{m.get("requirement_coverage_score")}/10</div></div>', unsafe_allow_html=True)
        with m_cols[2]:
            st.markdown(f'<div class="stat-box"><div class="stat-label">Risk Guard Score</div><div class="stat-value">{m.get("quality_score")}%</div></div>', unsafe_allow_html=True)
        with m_cols[3]:
            auto_ready = "OPERATIONAL" if m.get("automation_ready") else "PENDING"
            st.markdown(f'<div class="stat-box"><div class="stat-label">Automation Pipeline</div><div class="stat-value">{auto_ready}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-head"><span></span><div class="section-title">Traceability Mapping</div></div>', unsafe_allow_html=True)
        if st.session_state.traceability:
            # Clean display for traceability
            t_data = st.session_state.traceability.get("requirements_to_testcases", [])
            st.table(t_data)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Operational data is computed during the synthesis phase.")

st.markdown('</div>', unsafe_allow_html=True) # End main-container
