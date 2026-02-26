import streamlit as st
import sys
import os
import datetime

sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="CareerPulse AI", 
    page_icon="🎯",
    layout="wide"
)

# ===== HEALTH CHECK ENDPOINT FOR UPTIMEROBOT =====
def health_check():
    """Simple health check endpoint to keep Render awake"""
    st.set_page_config(
        page_title="Health Check - CareerPulse AI",
        page_icon="✅",
        layout="centered"
    )
    
    st.markdown("""
    <h1 style='color: #00ff9d; text-align: center;'>✅ CareerPulse AI</h1>
    <h2 style='text-align: center;'>Server is Healthy</h2>
    <hr>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "🟢 Online")
    with col2:
        st.metric("Server Time", datetime.datetime.now().strftime("%H:%M:%S"))
    
    st.markdown("---")
    st.json({
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "service": "CareerPulse AI",
        "version": "1.0.0",
        "environment": "production"
    })
    
    st.caption("This endpoint is used by UptimeRobot to keep the server awake.")
    st.stop()

# Check for health parameter in query string
query_params = st.query_params
if "health" in query_params and query_params["health"] in ["1", "true", "yes"]:
    health_check()
# ==================================================

# Page routing
if 'page' not in st.session_state:
    st.session_state.page = "Login"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Navigation - ONLY 7 PAGES
if st.session_state.page == "Login":
    import frontend.Login as Login
    Login.show()
elif st.session_state.page == "Register":
    import frontend.Register as Register
    Register.show()
elif st.session_state.page == "Home":
    import frontend.Home as Home
    Home.show()
elif st.session_state.page == "Dashboard":
    import frontend.Dashboard as Dashboard
    Dashboard.show()
elif st.session_state.page == "SkillGap":
    import frontend.Skill_Gap as SkillGap
    SkillGap.show()
elif st.session_state.page == "CareerPath":
    import frontend.Career_Path as CareerPath
    CareerPath.show()
elif st.session_state.page == "Resume":
    import frontend.Resume as Resume
    Resume.show()