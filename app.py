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
    st.markdown("""
    <h1 style='color: #00ff9d;'>✅ CareerPulse AI - Healthy</h1>
    <p>Server is running properly!</p>
    """, unsafe_allow_html=True)
    
    # Show server stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "🟢 Online")
    with col2:
        st.metric("Timestamp", datetime.datetime.now().strftime("%H:%M:%S"))
    
    st.json({
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "service": "CareerPulse AI",
        "version": "1.0.0"
    })

# Health check route - Render ke liye
if st.query_params.get("health") == "1" or st.query_params.get("health") == "true":
    health_check()
    st.stop()
# ==================================================

# Page routing
if 'page' not in st.session_state:
    st.session_state.page = "Login"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Navigation
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
elif st.session_state.page == "History":
    import frontend.History as History
    History.show()
elif st.session_state.page == "Profile":
    import frontend.Profile as Profile
    Profile.show()
elif st.session_state.page == "About":
    import frontend.About as About
    About.show()
elif st.session_state.page == "Analytics":
    import frontend.Analytics as Analytics
    Analytics.show()