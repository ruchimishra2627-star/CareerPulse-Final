import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def show():
    st.set_page_config(
        page_title="CareerPulse AI - Analytics", 
        page_icon="📊",
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
    
    st.markdown("<h1 style='text-align: center;'>📊 Analytics</h1>", unsafe_allow_html=True)
    
    # Generate sample data if history empty
    if 'history_data' not in st.session_state or len(st.session_state.history_data) == 0:
        # Create sample data
        domains = ["Software Developer", "Data Scientist", "Web Developer", "Business Analyst", "Cyber Security"]
        sample_data = []
        
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            prob = random.randint(45, 95)
            if prob >= 70:
                risk = "Low Risk"
            elif prob >= 40:
                risk = "Medium Risk"
            else:
                risk = "High Risk"
            
            sample_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "domain": random.choice(domains),
                "probability": prob,
                "risk": risk
            })
        
        df = pd.DataFrame(sample_data)
    else:
        df = pd.DataFrame(st.session_state.history_data)
    
    # Basic stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = df['probability'].mean()
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    with col2:
        max_score = df['probability'].max()
        st.metric("Highest Score", f"{max_score:.1f}%")
    
    with col3:
        min_score = df['probability'].min()
        st.metric("Lowest Score", f"{min_score:.1f}%")
    
    with col4:
        total = len(df)
        st.metric("Total Analyses", total)
    
    # Simple line chart
    st.markdown("### 📈 Score Trend")
    fig = px.line(df, x=df.index, y='probability', 
                  title='Your Progress Over Time',
                  markers=True)
    fig.update_traces(line_color='#00ff9d')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Domain distribution
    col1, col2 = st.columns(2)
    
    with col1:
        domain_counts = df['domain'].value_counts()
        fig = px.pie(values=domain_counts.values, names=domain_counts.index,
                     title='Analyses by Domain')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        risk_counts = df['risk'].value_counts()
        fig = px.bar(x=risk_counts.index, y=risk_counts.values,
                     title='Risk Distribution',
                     color=risk_counts.index,
                     color_discrete_map={
                         'Low Risk': '#00ff9d',
                         'Medium Risk': '#ffbb33',
                         'High Risk': '#ff4444'
                     })
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Back button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()