import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def show():
    st.set_page_config(
        page_title="CareerPulse AI - History", 
        page_icon="📋",
        layout="wide"
    )
    
    # Check authentication
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning("⚠️ Please login first!")
        st.session_state.page = "Login"
        st.rerun()
    
    # Simple CSS
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        h1, h2, h3 {
            color: white !important;
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>📋 Analysis History</h1>", unsafe_allow_html=True)
    
    # Create sample data if empty
    if 'history_data' not in st.session_state or len(st.session_state.history_data) == 0:
        st.session_state.history_data = []
        domains = ["Software Developer", "Data Scientist", "Web Developer", "Business Analyst", "Cyber Security"]
        
        for i in range(20):
            date = datetime.now() - timedelta(days=i)
            prob = random.randint(45, 98)
            if prob >= 70:
                risk = "Low Risk"
            elif prob >= 40:
                risk = "Medium Risk"
            else:
                risk = "High Risk"
            
            st.session_state.history_data.append({
                "date": date.strftime("%d %b %Y"),
                "domain": random.choice(domains),
                "probability": prob,
                "risk": risk
            })
    
    df = pd.DataFrame(st.session_state.history_data)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        domain_filter = st.selectbox("Domain", ["All"] + list(df['domain'].unique()))
    with col2:
        risk_filter = st.selectbox("Risk Level", ["All"] + list(df['risk'].unique()))
    with col3:
        sort_by = st.selectbox("Sort By", ["Newest", "Oldest", "Highest Score", "Lowest Score"])
    
    # Apply filters
    filtered_df = df.copy()
    if domain_filter != "All":
        filtered_df = filtered_df[filtered_df['domain'] == domain_filter]
    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df['risk'] == risk_filter]
    
    # Apply sorting
    if sort_by == "Newest":
        filtered_df = filtered_df.sort_values('date', ascending=False)
    elif sort_by == "Oldest":
        filtered_df = filtered_df.sort_values('date', ascending=True)
    elif sort_by == "Highest Score":
        filtered_df = filtered_df.sort_values('probability', ascending=False)
    elif sort_by == "Lowest Score":
        filtered_df = filtered_df.sort_values('probability', ascending=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average", f"{filtered_df['probability'].mean():.1f}%")
    with col2:
        st.metric("Highest", f"{filtered_df['probability'].max():.1f}%")
    with col3:
        st.metric("Lowest", f"{filtered_df['probability'].min():.1f}%")
    with col4:
        st.metric("Total", len(filtered_df))
    
    # Chart
    fig = px.line(filtered_df, x=filtered_df.index, y='probability', 
                  title='Score Trend', markers=True)
    fig.update_traces(line_color='#00ff9d')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # History table
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.1); padding:15px; margin:10px 0; border-radius:10px;">
            <div style="display:flex; justify-content:space-between;">
                <span style="color:white;">{row['domain']}</span>
                <span style="color:#00ff9d;">{row['probability']}%</span>
            </div>
            <div style="color:gray;">{row['date']} | {row['risk']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()