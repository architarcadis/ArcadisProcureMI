"""
Elegant Market Intelligence Alert System
Simple, effective alerts from real web data
"""

import streamlit as st
import requests
from datetime import datetime
import sqlite3
from googleapiclient.discovery import build

def create_alerts_database():
    """Create simple alerts database"""
    conn = sqlite3.connect('market_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intelligence_alerts (
            id INTEGER PRIMARY KEY,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            source_url TEXT,
            date_found TEXT,
            category TEXT,
            entity_name TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def gather_supplier_alerts(suppliers):
    """Gather real supplier intelligence alerts"""
    google_api_key = st.session_state.get('google_api_key')
    google_cse_id = st.session_state.get('google_cse_id')
    
    if not google_api_key or not google_cse_id:
        st.error("Google API credentials required for intelligence gathering")
        return []
    
    alerts = []
    
    with st.spinner("Gathering intelligence alerts..."):
        progress = st.progress(0)
        
        for i, supplier in enumerate(suppliers):
            progress.progress((i + 1) / len(suppliers))
            
            # Search for supplier news and updates
            search_query = f"{supplier} financial news updates 2024"
            
            try:
                service = build("customsearch", "v1", developerKey=google_api_key)
                result = service.cse().list(q=search_query, cx=google_cse_id, num=3).execute()
                
                for item in result.get('items', []):
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    url = item.get('link', '')
                    
                    # Determine alert severity based on keywords
                    severity = determine_alert_severity(title + " " + snippet)
                    
                    alert = {
                        'alert_type': 'Supplier Intelligence',
                        'severity': severity,
                        'title': title,
                        'description': snippet[:200] + '...' if len(snippet) > 200 else snippet,
                        'source_url': url,
                        'date_found': datetime.now().strftime('%Y-%m-%d'),
                        'category': 'Supplier',
                        'entity_name': supplier
                    }
                    alerts.append(alert)
                    
            except Exception as e:
                st.warning(f"Could not gather data for {supplier}")
    
    return alerts

def determine_alert_severity(text):
    """Simple keyword-based severity detection"""
    text = text.lower()
    
    risk_keywords = ['bankruptcy', 'financial trouble', 'lawsuit', 'investigation', 'defaulted', 'crisis']
    warning_keywords = ['restructuring', 'changes', 'delays', 'issues', 'concerns', 'review']
    positive_keywords = ['growth', 'expansion', 'success', 'award', 'contract', 'investment']
    
    if any(keyword in text for keyword in risk_keywords):
        return 'High Risk'
    elif any(keyword in text for keyword in warning_keywords):
        return 'Medium Watch'
    elif any(keyword in text for keyword in positive_keywords):
        return 'Positive'
    else:
        return 'Neutral'

def display_supplier_alerts():
    """Display elegant supplier alert cards"""
    if 'supplier_alerts' not in st.session_state:
        st.info("Click 'Refresh Intelligence' to gather current supplier alerts")
        return
    
    alerts = st.session_state.supplier_alerts
    
    if not alerts:
        st.info("No alerts found. Try refreshing or check API credentials.")
        return
    
    # Group alerts by severity
    high_risk = [a for a in alerts if a['severity'] == 'High Risk']
    medium_watch = [a for a in alerts if a['severity'] == 'Medium Watch']
    positive = [a for a in alerts if a['severity'] == 'Positive']
    neutral = [a for a in alerts if a['severity'] == 'Neutral']
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 High Risk", len(high_risk))
    with col2:
        st.metric("🟡 Watch", len(medium_watch))
    with col3:
        st.metric("🟢 Positive", len(positive))
    with col4:
        st.metric("⚪ Neutral", len(neutral))
    
    # Display alert cards
    for alert_group, color, emoji in [
        (high_risk, "red", "🚨"),
        (medium_watch, "orange", "⚠️"),
        (positive, "green", "✅"),
        (neutral, "gray", "ℹ️")
    ]:
        if alert_group:
            st.subheader(f"{emoji} {alert_group[0]['severity']} Alerts")
            
            for alert in alert_group:
                with st.container():
                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding: 12px; margin: 8px 0; background-color: rgba(255,255,255,0.05);">
                        <h4 style="margin: 0 0 8px 0;">{alert['entity_name']}</h4>
                        <p style="margin: 0 0 8px 0; font-weight: bold;">{alert['title']}</p>
                        <p style="margin: 0 0 8px 0; color: #888;">{alert['description']}</p>
                        <small>Source: <a href="{alert['source_url']}" target="_blank">View Article</a> | {alert['date_found']}</small>
                    </div>
                    """, unsafe_allow_html=True)

def show_category_intelligence_alerts():
    """Category market trend alerts"""
    st.subheader("📊 Category Intelligence Alerts")
    
    categories = ['Water Treatment', 'Infrastructure', 'Engineering Services']
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Monitoring {len(categories)} categories for market trends")
    with col2:
        if st.button("Refresh Trends", type="primary"):
            gather_category_alerts(categories)
    
    display_category_alerts()

def gather_category_alerts(categories):
    """Gather category trend alerts"""
    # Similar implementation to supplier alerts but for market trends
    st.session_state.category_alerts = []  # Placeholder

def display_category_alerts():
    """Display category alert cards"""
    st.info("Category trend alerts will appear here")

def show_regulatory_alerts():
    """Regulatory monitoring alerts"""
    st.subheader("⚖️ Regulatory Alerts")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("Monitoring regulatory changes affecting procurement")
    with col2:
        if st.button("Check Regulations", type="primary"):
            gather_regulatory_alerts()
    
    display_regulatory_alerts()

def gather_regulatory_alerts():
    """Gather regulatory alerts"""
    st.session_state.regulatory_alerts = []  # Placeholder

def display_regulatory_alerts():
    """Display regulatory alert cards"""
    st.info("Regulatory alerts will appear here")

def show_economic_alerts():
    """Economic indicator alerts"""
    st.subheader("💰 Economic Alerts")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("Monitoring economic factors affecting procurement costs")
    with col2:
        if st.button("Update Economics", type="primary"):
            gather_economic_alerts()
    
    display_economic_alerts()

def gather_economic_alerts():
    """Gather economic indicator alerts"""
    st.session_state.economic_alerts = []  # Placeholder

def display_economic_alerts():
    """Display economic alert cards"""
    st.info("Economic impact alerts will appear here")

def show_supplier_discovery_alerts():
    """New supplier discovery alerts"""
    st.subheader("🔍 Supplier Discovery")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("Discovering new potential suppliers")
    with col2:
        if st.button("Find Suppliers", type="primary"):
            discover_new_suppliers()
    
    display_supplier_discovery()

def discover_new_suppliers():
    """Discover new potential suppliers"""
    st.session_state.supplier_discoveries = []  # Placeholder

def display_supplier_discovery():
    """Display supplier discovery cards"""
    st.info("New supplier opportunities will appear here")