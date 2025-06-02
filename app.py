import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sqlite3
import hashlib
import json
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
import io
import base64

# Page config
st.set_page_config(
    page_title="Procure Insights & Market Intelligence Tool",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

def format_currency_millions(value):
    """Format currency values in millions for UK display"""
    if pd.isna(value) or value == 0:
        return "£0.0M"
    millions = value / 1_000_000
    return f"£{millions:.1f}M"

def format_number_millions(value):
    """Format numbers in millions for better readability"""
    if pd.isna(value) or value == 0:
        return "0.0M"
    millions = value / 1_000_000
    return f"{millions:.1f}M"

def safe_get_column(df, possible_names, default_value=None):
    """Safely get column data with fallback options - handles various naming conventions"""
    for name in possible_names:
        if name in df.columns:
            return df[name]
    
    # Create a series with default values if no column found
    if default_value is not None:
        return pd.Series([default_value] * len(df), index=df.index)
    else:
        return pd.Series([None] * len(df), index=df.index)

def safe_calculate_metric(data, calculation_func, default_value="N/A"):
    """Safely calculate metrics with error handling"""
    try:
        result = calculation_func(data)
        return result if result is not None else default_value
    except Exception:
        return default_value

def create_unified_procurement_template():
    """Create unified template that matches exactly what mock data button generates"""
    
    # Enhanced supplier ecosystem for Thames Water AMP8
    suppliers = [
        # Tier 1 Water Infrastructure Partners
        'Thames Water Engineering Ltd', 'Balfour Beatty Living Places', 'Clancy Docwra Ltd',
        'Morrison Water Services', 'Dwr Cymru Utilities', 'Amey Infrastructure', 
        'Kier Water Services', 'Anglian Water Services', 'Veolia Water Projects',
        'Jacobs Engineering UK', 'Arup Infrastructure', 'Atkins Water Solutions',
        
        # Specialist Water Treatment & Technology
        'SUEZ Water Technologies', 'GE Water & Process Technologies', 'Grundfos Pumps Ltd',
        'Xylem Water Solutions', 'Pentair Water Treatment', 'Evoqua Water Technologies',
        'Siemens Water Technologies', 'ABB Water Solutions', 'Schneider Electric Water',
        
        # Construction & Civil Engineering
        'Skanska UK Building', 'Costain Group PLC', 'Laing O\'Rourke Construction',
        'Galliford Try Infrastructure', 'Morgan Sindall Infrastructure', 'BAM Nuttall Ltd',
        'VINCI Construction UK', 'Carillion Water (Administration)', 'Willmott Dixon Holdings',
        
        # Facilities & Professional Services
        'Capita Business Services', 'Serco Group PLC', 'Mitie Technical Services',
        'ISS Facility Services', 'Sodexo Government Services', 'Interserve Support Services'
    ]
    
    # Comprehensive category structure for water infrastructure
    categories = [
        # Core Water Infrastructure
        'Water Treatment Works', 'Sewage Treatment Works', 'Water Mains Replacement',
        'Sewer Network Upgrade', 'Pumping Station Construction', 'Reservoir Construction',
        'Water Storage Facilities', 'Distribution Network', 'Collection Network',
        
        # Technology & Equipment
        'SCADA Systems', 'Water Quality Monitoring', 'Leak Detection Systems',
        'Smart Meter Installation', 'Process Control Equipment', 'Laboratory Equipment',
        'Electrical & Instrumentation', 'Pumps & Valves', 'Chemical Dosing Systems',
        
        # Environmental & Compliance
        'Environmental Compliance', 'Discharge Permits', 'Environmental Monitoring',
        'Waste Management Services', 'Energy Efficiency Projects', 'Carbon Reduction',
        
        # Professional & Support Services
        'Engineering Consultancy', 'Project Management', 'Legal Services', 'Financial Services',
        'Health & Safety Consultancy', 'Training Services', 'Facilities Management'
    ]
    
    # Regional coverage for Thames Water operations
    regions = [
        'London Central', 'London North', 'London South', 'London East', 'London West',
        'Thames Valley', 'Buckinghamshire', 'Hertfordshire', 'Essex', 'Kent',
        'Surrey', 'Berkshire', 'Oxfordshire', 'Slough', 'Reading'
    ]
    
    # Generate realistic data
    np.random.seed(42)  # For reproducible results
    n_records = 300
    
    data = []
    for i in range(n_records):
        # Realistic date ranges for AMP8 period
        need_date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))
        
        # Realistic procurement timelines based on category
        category = np.random.choice(categories)
        if 'Construction' in category or 'Works' in category:
            cycle_days = np.random.randint(45, 120)  # Major infrastructure
        elif 'Equipment' in category or 'Systems' in category:
            cycle_days = np.random.randint(25, 60)   # Equipment procurement
        else:
            cycle_days = np.random.randint(15, 45)   # Services
        
        award_date = need_date + timedelta(days=cycle_days)
        payment_date = award_date + timedelta(days=np.random.randint(30, 90))
        
        # Realistic contract values based on category
        if 'Construction' in category or 'Works' in category:
            amount = np.random.lognormal(15, 1.2) * 100000  # £1M-£50M range
        elif 'Consultancy' in category or 'Services' in category:
            amount = np.random.lognormal(12, 1.0) * 10000   # £100K-£5M range
        else:
            amount = np.random.lognormal(13, 1.1) * 50000   # £500K-£10M range
        
        # Status distribution reflecting real procurement
        status_weights = [0.65, 0.20, 0.10, 0.05]
        status = np.random.choice(['Completed', 'In Progress', 'Awarded', 'Planning'], p=status_weights)
        
        record = {
            'Transaction_ID': f'TW-{2024}-{i+1:04d}',
            'Need_Identification_Date': need_date.strftime('%Y-%m-%d'),
            'Contract_Award_Date': award_date.strftime('%Y-%m-%d'),
            'Payment_Date': payment_date.strftime('%Y-%m-%d'),
            'Supplier_Name': np.random.choice(suppliers),
            'Category': category,
            'Region': np.random.choice(regions),
            'Amount': round(amount, 2),
            'Status': status,
            'Priority': np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.6, 0.2]),
            'Sourcing_Method': np.random.choice([
                'Open Tender', 'Restricted Tender', 'Framework Call-off', 'Direct Award'
            ], p=[0.3, 0.4, 0.25, 0.05]),
            'Department': np.random.choice([
                'Capital Delivery', 'Operations & Maintenance', 'Strategic Projects',
                'Environmental Compliance', 'Technology & Innovation', 'Customer Services'
            ]),
            'Exception_Type': np.random.choice(['None', 'Delayed Approval', 'Budget Exceeded', 'Supplier Issue'], p=[0.75, 0.1, 0.08, 0.07])
        }
        data.append(record)
    
    return pd.DataFrame(data)

def calculate_cycle_time(df, date_columns):
    """Calculate cycle time between two date columns with error handling"""
    try:
        start_col = None
        end_col = None
        
        # Find available date columns using flexible matching
        for col in date_columns:
            matched_col = safe_get_column(df, [col, col.lower(), col.replace('_', ' '), col.replace(' ', '_')])
            if matched_col is not None and not matched_col.isna().all():
                if start_col is None:
                    start_col = matched_col
                    start_col_name = col
                else:
                    end_col = matched_col
                    end_col_name = col
                    break
        
        if start_col is not None and end_col is not None:
            start_dates = pd.to_datetime(start_col, errors='coerce')
            end_dates = pd.to_datetime(end_col, errors='coerce')
            cycle_times = (end_dates - start_dates).dt.days
            valid_cycles = cycle_times.dropna()
            
            if len(valid_cycles) > 0:
                return valid_cycles.mean()  # Return numeric value
        
        return None  # Return None instead of "N/A"
    except Exception as e:
        return None

def show_welcome_tab():
    """Welcome tab explaining the platform modules and insights"""
    st.header("🏠 Welcome to Procure Insights")
    st.markdown("### Built Assets Procurement Intelligence Platform")
    
    # Platform overview
    st.markdown("""
    **Transform your built assets procurement data into strategic insights for construction, infrastructure, and facilities management.**
    
    Streamlined analytics designed specifically for the unique challenges of built environment procurement.
    """)
    
    st.markdown("---")
    
    # Module explanations
    st.subheader("📋 Platform Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📊 Portfolio Overview
        **Strategic Built Assets Dashboard**
        
        **Key Insights:**
        - Project portfolio performance tracking
        - Financial impact analysis
        - Resource allocation optimization
        - Risk and opportunity identification
        
        **Perfect for:** Executive teams needing high-level strategic oversight of procurement performance.
        """)
        
        st.markdown("""
        #### 🔄 Process Analytics
        **Workflow Performance Intelligence**
        
        **Key Insights:**
        - Cycle time analysis and bottleneck identification
        - Approval workflow efficiency
        - Exception handling patterns
        - Process improvement opportunities
        
        **Perfect for:** Operations managers optimizing procurement workflows and reducing delays.
        """)
    
    with col2:
        st.markdown("""
        #### 💰 Spend Analytics
        **Financial Performance Intelligence**
        
        **Key Insights:**
        - Supplier spend analysis and concentration
        - Category performance benchmarking
        - Cost optimization opportunities
        - Budget variance analysis
        
        **Perfect for:** Finance teams managing procurement budgets and supplier relationships.
        """)
        
        st.markdown("""
        #### 🔍 Market Intelligence
        **External Market Monitoring**
        
        **Key Insights:**
        - Real-time supplier market intelligence
        - Regulatory and economic impact alerts
        - New supplier discovery
        - Category trend monitoring
        
        **Perfect for:** Procurement professionals staying ahead of market changes and opportunities.
        """)
    
    st.markdown("---")
    
    # Getting started
    st.subheader("🚀 Getting Started")
    
    st.markdown("""
    1. **Upload Your Data:** Use the sidebar to upload your procurement data files
    2. **Load Mock Data:** Try the sample Thames Water AMP8 dataset to explore features
    3. **Explore Insights:** Navigate through the tabs to discover actionable insights
    4. **Configure Intelligence:** Set up market monitoring for ongoing intelligence
    """)
    
    # Key benefits
    st.markdown("---")
    st.subheader("💡 Key Benefits")
    
    benefit_col1, benefit_col2, benefit_col3 = st.columns(3)
    
    with benefit_col1:
        st.markdown("""
        **⚡ Instant Insights**
        - Dynamic data adaptation
        - Real-time performance tracking
        - Automated exception detection
        """)
    
    with benefit_col2:
        st.markdown("""
        **🎯 Actionable Intelligence**
        - Specific bottleneck identification
        - Cost optimization opportunities
        - Risk mitigation strategies
        """)
    
    with benefit_col3:
        st.markdown("""
        **🔮 Forward-Looking**
        - Market trend analysis
        - Predictive insights
        - Strategic planning support
        """)

def calculate_kpis(df):
    """Calculate key procurement KPIs from the data using dynamic column detection"""
    if df is None or df.empty:
        return {}
    
    kpis = {}
    
    # Basic metrics with dynamic amount detection
    amount_col = safe_get_column(df, ['Amount', 'amount', 'Contract_Value', 'contract_value', 'Total_Value', 'total_value', 'PO_Amount', 'Invoice_Amount', 'Cost', 'cost', 'Value', 'value'])
    if not amount_col.isna().all():
        numeric_amounts = pd.to_numeric(amount_col, errors='coerce').dropna()
        if len(numeric_amounts) > 0:
            kpis['total_spend'] = numeric_amounts.sum()
            kpis['avg_transaction_value'] = numeric_amounts.mean()
        else:
            kpis['total_spend'] = 0
            kpis['avg_transaction_value'] = 0
    else:
        kpis['total_spend'] = 0
        kpis['avg_transaction_value'] = 0
    
    kpis['total_transactions'] = len(df)
    
    # Cycle time analysis with dynamic date detection
    req_date_col = safe_get_column(df, ['Requisition_Date', 'requisition_date', 'req_date', 'Request_Date', 'request_date', 'Need_Identification_Date'])
    po_date_col = safe_get_column(df, ['PO_Issue_Date', 'po_issue_date', 'PO_Date', 'po_date', 'Order_Date', 'order_date', 'Payment_Date'])
    
    if not req_date_col.isna().all() and not po_date_col.isna().all():
        try:
            req_dates = pd.to_datetime(req_date_col, errors='coerce')
            po_dates = pd.to_datetime(po_date_col, errors='coerce')
            req_to_po_days = (po_dates - req_dates).dt.days
            valid_cycle_times = req_to_po_days.dropna()
            if len(valid_cycle_times) > 0:
                kpis['avg_req_to_po_days'] = valid_cycle_times.mean()
            else:
                kpis['avg_req_to_po_days'] = 0
        except Exception:
            kpis['avg_req_to_po_days'] = 0
    else:
        kpis['avg_req_to_po_days'] = 0
    
    return kpis

def show_executive_dashboard():
    """Executive Summary Dashboard"""
    st.header("📊 Portfolio Overview")
    st.markdown("### Strategic Built Assets Procurement Dashboard")
    
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("📁 Upload procurement data or load mock data from the sidebar to view analytics")
        st.info("💡 **Quick Start:** Use the 'Load Mock Data' button in the sidebar to explore with Thames Water AMP8 sample data")
        return
    
    df = st.session_state.data
    kpis = calculate_kpis(df)
    
    # Executive KPI Overview
    st.subheader("⚡ Executive KPI Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spend = kpis.get('total_spend', 0)
        st.metric(
            "Total Portfolio Value",
            format_currency_millions(total_spend),
            help="Total value of all procurement activities"
        )
    
    with col2:
        total_transactions = kpis.get('total_transactions', 0)
        st.metric(
            "Active Projects",
            f"{total_transactions:,}",
            help="Number of procurement transactions"
        )
    
    with col3:
        avg_value = kpis.get('avg_transaction_value', 0)
        st.metric(
            "Avg Project Value",
            format_currency_millions(avg_value),
            help="Average value per procurement"
        )
    
    with col4:
        avg_cycle = kpis.get('avg_req_to_po_days', 0)
        if avg_cycle > 0:
            st.metric(
                "Avg Cycle Time",
                f"{avg_cycle:.1f} days",
                help="Average procurement cycle time"
            )
        else:
            st.metric("Avg Cycle Time", "N/A")
    
    st.markdown("---")
    
    # Executive Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Suppliers by Spend
        if 'Supplier_Name' in df.columns and 'Amount' in df.columns:
            top_suppliers = df.groupby('Supplier_Name')['Amount'].sum().sort_values(ascending=False).head(8)
            fig = px.bar(
                x=top_suppliers.values,
                y=top_suppliers.index,
                orientation='h',
                title="🏢 Top Suppliers by Spend",
                labels={'x': 'Total Spend (£)', 'y': 'Supplier'},
                color=top_suppliers.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Spend by Department
        if 'Department' in df.columns and 'Amount' in df.columns:
            dept_spend = df.groupby('Department')['Amount'].sum().sort_values(ascending=True)
            fig = px.bar(
                x=dept_spend.values,
                y=dept_spend.index,
                orientation='h',
                title="🏛️ Spend by Department",
                labels={'x': 'Total Spend (£)', 'y': 'Department'},
                color=dept_spend.values,
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

def show_consolidated_process_analytics():
    """Consolidated Process Analytics - Complete Source-to-Pay workflow performance"""
    
    if st.session_state.data is None:
        st.warning("📊 Please upload data or load mock data from the sidebar to view analytics")
        return
    
    df = st.session_state.data
    
    st.header("🔄 Process Analytics")
    st.markdown("### Complete Source-to-Pay Workflow Performance")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_transactions = len(df)
        st.metric("Total Transactions", f"{total_transactions:,}")
    
    with col2:
        if 'Status' in df.columns:
            active_processes = len(df[df['Status'].isin(['Processing', 'In Progress'])])
            st.metric("Active Processes", f"{active_processes:,}")
        else:
            st.metric("Active Processes", "N/A")
    
    with col3:
        avg_cycle_time = calculate_cycle_time(df, ['Need_Identification_Date', 'Payment_Date'])
        if avg_cycle_time and isinstance(avg_cycle_time, (int, float)):
            st.metric("Avg Cycle Time", f"{avg_cycle_time:.1f} days")
        else:
            st.metric("Avg Cycle Time", "N/A")
    
    with col4:
        if 'Exception_Type' in df.columns:
            exception_rate = (len(df[df['Exception_Type'] != 'None']) / len(df)) * 100
            st.metric("Exception Rate", f"{exception_rate:.1f}%")
        else:
            st.metric("Exception Rate", "N/A")
    
    # Process performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        if 'Status' in df.columns:
            status_counts = df['Status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="📋 Process Status Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cycle time by category
        if 'Category' in df.columns:
            # Calculate cycle time for each category
            df_with_cycle = df.copy()
            cycle_times = []
            for _, row in df.iterrows():
                cycle_time = calculate_cycle_time(pd.DataFrame([row]), ['Need_Identification_Date', 'Payment_Date'])
                cycle_times.append(cycle_time if cycle_time else 0)
            
            df_with_cycle['cycle_time'] = cycle_times
            category_cycle = df_with_cycle.groupby('Category')['cycle_time'].mean().sort_values(ascending=True).head(10)
            
            fig = px.bar(
                x=category_cycle.values,
                y=category_cycle.index,
                orientation='h',
                title="⏱️ Avg Cycle Time by Category",
                labels={'x': 'Days', 'y': 'Category'}
            )
            st.plotly_chart(fig, use_container_width=True)

def show_financial_analysis():
    """Financial Impact Analysis"""
    st.header("💰 Spend Analytics")
    st.markdown("### Financial Performance Intelligence")
    
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("📊 Upload data to see financial insights")
        return
    
    data = st.session_state.data
    
    # Financial KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Amount' in data.columns:
            total_spend = data['Amount'].sum()
            st.metric("Total Spend", format_currency_millions(total_spend))
        else:
            st.metric("Total Spend", "N/A")
    
    with col2:
        if 'Amount' in data.columns:
            avg_transaction = data['Amount'].mean()
            st.metric("Avg Transaction", format_currency_millions(avg_transaction))
        else:
            st.metric("Avg Transaction", "N/A")
    
    with col3:
        if 'Supplier_Name' in data.columns:
            supplier_count = data['Supplier_Name'].nunique()
            st.metric("Active Suppliers", f"{supplier_count:,}")
        else:
            st.metric("Active Suppliers", "N/A")
    
    with col4:
        if 'Category' in data.columns:
            category_count = data['Category'].nunique()
            st.metric("Spend Categories", f"{category_count:,}")
        else:
            st.metric("Spend Categories", "N/A")
    
    # Financial charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Spend by category
        if 'Category' in data.columns and 'Amount' in data.columns:
            category_spend = data.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=category_spend.index,
                y=category_spend.values,
                title="💰 Spend by Category",
                labels={'x': 'Category', 'y': 'Total Spend (£)'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly spend trend
        if 'Need_Identification_Date' in data.columns and 'Amount' in data.columns:
            data['month'] = pd.to_datetime(data['Need_Identification_Date']).dt.to_period('M')
            monthly_spend = data.groupby('month')['Amount'].sum()
            fig = px.line(
                x=monthly_spend.index.astype(str),
                y=monthly_spend.values,
                title="📈 Monthly Spend Trend",
                labels={'x': 'Month', 'y': 'Total Spend (£)'}
            )
            st.plotly_chart(fig, use_container_width=True)

def show_market_research():
    """Market Research - MarketScan AI Intelligence"""
    st.header("🔍 Market Intelligence")
    st.markdown("### External Market Monitoring Dashboard")
    
    st.info("🚀 **Market Intelligence Features Coming Soon**")
    st.markdown("""
    This section will provide:
    - Real-time supplier market intelligence
    - Regulatory and economic impact alerts  
    - New supplier discovery
    - Category trend monitoring
    
    **Contact your administrator to enable market intelligence features.**
    """)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None

# Sidebar
with st.sidebar:
    st.header("📁 Data Management")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Procurement Data",
        type=['csv', 'xlsx'],
        help="Upload your procurement data in CSV or Excel format"
    )
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.data = df
            st.success(f"✅ Data loaded: {len(df)} records")
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    st.markdown("---")
    
    # Mock data option
    st.subheader("🔬 Mock Data")
    st.markdown("Load sample data for demonstration:")
    
    if st.button("Load Mock Data"):
        mock_data = create_unified_procurement_template()
        st.session_state.data = mock_data
        st.success("✅ Mock data loaded")
        st.info(f"📊 Combined dataset: {len(mock_data)} records with {len(mock_data.columns)} fields")
    
    st.markdown("---")

# Main content area with workflow-focused tabs
st.title("🚀 Procure Insights & Market Intelligence Tool")

# Main application tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Welcome",
    "📊 Portfolio Overview", 
    "🔄 Process Analytics",
    "💰 Spend Analytics",
    "🔍 Market Intelligence"
])

with tab1:
    show_welcome_tab()

with tab2:
    show_executive_dashboard()

with tab3:
    show_consolidated_process_analytics()

with tab4:
    show_financial_analysis()

with tab5:
    show_market_research()
