"""
Clean wireframes with no mock data - only authentic data structures
"""
import streamlit as st

def show_supplier_wireframe():
    """Empty supplier wireframe showing only authentic data structure"""
    st.subheader("🏭 Supplier Intelligence")
    st.info("This section will populate with authentic supplier data after web crawling")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Financial Health Analysis**")
        st.caption("Real credit ratings and financial data")
    with col2:
        st.markdown("**Risk Assessment**")
        st.caption("Operational and market risk analysis")
    with col3:
        st.markdown("**Market Position**")
        st.caption("Revenue and market share data")

def show_category_wireframe():
    """Empty category wireframe showing only authentic data structure"""
    st.subheader("📈 Category Intelligence")
    st.info("This section will populate with authentic category market data after web crawling")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Market Share Distribution**")
        st.caption("Real market sizing data")
    with col2:
        st.markdown("**Growth Rate Analysis**")
        st.caption("Historical trend analysis")

def show_regulatory_wireframe():
    """Empty regulatory wireframe showing only authentic data structure"""
    st.subheader("⚖️ Regulatory Monitoring")
    st.info("This section will populate with authentic regulatory data after web crawling")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Impact Distribution**")
        st.caption("Regulatory impact analysis")
    with col2:
        st.markdown("**Regional Compliance**")
        st.caption("Geographic regulatory mapping")

def show_potential_suppliers_wireframe():
    """Empty potential suppliers wireframe showing only authentic data structure"""
    st.subheader("🆕 Potential New Suppliers")
    st.info("This section will populate with authentic supplier discovery data after web crawling")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Innovation vs Reliability**")
        st.caption("Supplier capability analysis")
    with col2:
        st.markdown("**Geographic Distribution**")
        st.caption("Regional supplier mapping")

def show_economic_wireframe():
    """Empty economic wireframe showing only authentic data structure"""
    st.subheader("💹 Economic Indicators")
    st.info("This section will populate with authentic economic data after web crawling")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Economic Trends**")
        st.caption("Key economic indicators")
    with col2:
        st.markdown("**Procurement Impact**")
        st.caption("Economic impact on procurement")