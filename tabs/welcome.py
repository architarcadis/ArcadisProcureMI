import streamlit as st
import plotly.graph_objects as go
from utils.visualizations import ProcurementVisualizations

def show():
    """Display the welcome tab content"""
    
    # Hero Section
    st.title("🚀 Procurement Analytics - Essential Questions")
    st.markdown("""
    ### Get Answers to the Questions That Matter Most
    
    Built around the four critical questions every procurement professional asks daily.
    """)
    
    st.markdown("---")
    
    # Essential Questions Overview
    st.subheader("🎯 Four Essential Questions")
    
    # Question 1: Where are my delays?
    st.markdown("### 🚨 Where are my delays?")
    st.markdown("""
    **What you'll discover:**
    - Specific bottlenecks slowing down your processes
    - Which approvals are stuck and for how long
    - Department and category performance comparisons
    - Root causes of cycle time variations
    - Real-time status of pending transactions
    
    **Action you can take:** Immediately identify and resolve process bottlenecks that are costing time and money.
    """)
    
    st.markdown("---")
    
    # Question 2: What's this costing me?
    st.markdown("### 💰 What's this costing me?")
    st.markdown("""
    **What you'll discover:**
    - Working capital tied up in slow processes
    - Missed early payment discount opportunities
    - Late payment fees and penalties you're incurring
    - Cost of delayed implementations and projects
    - Cash flow impact of payment timing
    
    **Action you can take:** Quantify the business case for improvements and capture immediate savings opportunities.
    """)
    
    st.markdown("---")
    
    # Question 3: What should I fix first?
    st.markdown("### 🎯 What should I fix first?")
    st.markdown("""
    **What you'll discover:**
    - Quick wins with immediate impact (0-30 days)
    - Strategic improvements with strong ROI (1-6 months)
    - Long-term initiatives for sustainable change (6+ months)
    - Resource requirements and implementation timelines
    - Expected financial benefits of each improvement
    
    **Action you can take:** Focus your efforts on the highest-value improvements with clear implementation roadmaps.
    """)
    
    st.markdown("---")
    
    # Question 4: What's coming next?
    st.markdown("### 🔮 What's coming next?")
    st.markdown("""
    **What you'll discover:**
    - Upcoming capacity constraints and resource needs
    - Seasonal patterns affecting your procurement volumes
    - Early warning signals for potential bottlenecks
    - Automation opportunities with clear business cases
    - Trends that will impact future performance
    
    **Action you can take:** Shift from reactive to proactive management with forward-looking insights.
    """)
    
    st.markdown("---")
    
    # Getting Started
    st.info("""
    🚀 **Ready to get answers?** Upload your procurement data or load Thames Water example data from the sidebar to see these insights in action.
    """)
