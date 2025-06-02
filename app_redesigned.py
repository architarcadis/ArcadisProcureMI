import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# Configure page
st.set_page_config(
    page_title="Strategic Procurement Analytics",
    page_icon="📊",
    layout="wide"
)

def create_comprehensive_template():
    """Create comprehensive procurement data template for strategic analytics"""
    
    import numpy as np
    from datetime import datetime, timedelta
    
    # Generate 200 realistic procurement records
    n_records = 200
    start_date = datetime(2024, 1, 1)
    
    # Generate IDs
    req_ids = [f'REQ-{str(i+1).zfill(4)}' for i in range(n_records)]
    po_ids = [f'PO-{str(i+1).zfill(4)}' for i in range(n_records)]
    invoice_ids = [f'INV-{str(i+1).zfill(4)}' for i in range(n_records)]
    
    # Strategic categories and realistic suppliers
    categories = ['Technology & Software', 'Professional Services', 'Facilities & Utilities', 'Marketing & Communications', 
                 'Operations & Maintenance', 'HR & Training', 'Finance & Legal', 'R&D & Innovation']
    departments = ['IT', 'Operations', 'Finance', 'Marketing', 'HR', 'Facilities', 'Legal', 'R&D']
    suppliers = ['TechCorp Solutions', 'Global Services Ltd', 'Premier Consulting', 'Infrastructure Partners', 
                'Innovation Labs', 'Quality Vendors', 'Strategic Suppliers', 'Excellence Group']
    
    # Date progression with realistic delays
    req_dates = [start_date + timedelta(days=i*2 + np.random.randint(0, 3)) for i in range(n_records)]
    approval_dates = [req_date + timedelta(days=np.random.randint(1, 14)) for req_date in req_dates]
    po_dates = [app_date + timedelta(days=np.random.randint(1, 10)) for app_date in approval_dates]
    delivery_dates = [po_date + timedelta(days=np.random.randint(5, 30)) for po_date in po_dates]
    invoice_dates = [del_date + timedelta(days=np.random.randint(1, 7)) for del_date in delivery_dates]
    payment_dates = [inv_date + timedelta(days=np.random.randint(15, 45)) for inv_date in invoice_dates]
    
    # Realistic amount distribution
    amounts = np.random.lognormal(mean=9.5, sigma=1.2, size=n_records).astype(int)
    amounts = np.clip(amounts, 500, 750000)
    
    # Comprehensive template with strategic data
    template_df = pd.DataFrame({
        # Core Transaction Data
        'Requisition_ID': req_ids,
        'PO_Number': po_ids,
        'Invoice_Number': invoice_ids,
        'Requisition_Date': [d.strftime('%Y-%m-%d') for d in req_dates],
        'Approval_Date': [d.strftime('%Y-%m-%d') for d in approval_dates],
        'PO_Issue_Date': [d.strftime('%Y-%m-%d') for d in po_dates],
        'Expected_Delivery_Date': [d.strftime('%Y-%m-%d') for d in delivery_dates],
        'Actual_Delivery_Date': [(d + timedelta(days=np.random.randint(-3, 7))).strftime('%Y-%m-%d') for d in delivery_dates],
        'Invoice_Date': [d.strftime('%Y-%m-%d') for d in invoice_dates],
        'Payment_Date': [d.strftime('%Y-%m-%d') for d in payment_dates],
        
        # Financial Data
        'Amount': amounts,
        'Currency': ['USD'] * n_records,
        'Payment_Terms': np.random.choice(['Net 15', 'Net 30', 'Net 45', '2/10 Net 30'], n_records),
        'Early_Discount_Rate': np.random.choice([0, 1, 2, 2.5], n_records, p=[0.6, 0.15, 0.15, 0.1]),
        'Discount_Captured': np.random.choice(['Yes', 'No'], n_records, p=[0.25, 0.75]),
        'Late_Fee_Incurred': np.random.uniform(0, 200, n_records).round(2),
        
        # Supplier & Category Data
        'Supplier_Name': np.random.choice(suppliers, n_records),
        'Supplier_Rating': np.random.choice([3, 4, 5], n_records, p=[0.2, 0.5, 0.3]),
        'Category': np.random.choice(categories, n_records),
        'Department': np.random.choice(departments, n_records),
        'Requestor': [f'Employee_{np.random.randint(1, 50)}' for _ in range(n_records)],
        
        # Process & Performance Data
        'Priority': np.random.choice(['Low', 'Medium', 'High', 'Urgent'], n_records, p=[0.4, 0.35, 0.2, 0.05]),
        'Approval_Level': np.random.choice(['Level 1', 'Level 2', 'Level 3', 'Executive'], n_records, p=[0.5, 0.3, 0.15, 0.05]),
        'Approver': [f'Manager_{np.random.randint(1, 15)}' for _ in range(n_records)],
        'Status': np.random.choice(['Completed', 'In Progress', 'Delayed', 'Cancelled'], n_records, p=[0.7, 0.15, 0.1, 0.05]),
        'Contract_Type': np.random.choice(['One-time', 'Annual', 'Multi-year', 'Framework'], n_records),
        'Delivery_Performance': np.random.choice(['On Time', 'Early', 'Late'], n_records, p=[0.7, 0.1, 0.2]),
        'Quality_Rating': np.random.randint(3, 6, n_records),
        
        # Budget & Planning Data
        'Budget_Code': [f'B{np.random.randint(1000, 9999)}' for _ in range(n_records)],
        'Annual_Budget': np.random.randint(50000, 1000000, n_records),
        'Spend_to_Date': np.random.randint(10000, 800000, n_records),
        'Contract_Start_Date': [d.strftime('%Y-%m-%d') for d in po_dates],
        'Contract_End_Date': [(po_date + timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d') for po_date in po_dates],
        
        # Risk & Compliance
        'Risk_Level': np.random.choice(['Low', 'Medium', 'High'], n_records, p=[0.6, 0.3, 0.1]),
        'Compliance_Check': np.random.choice(['Passed', 'Failed', 'Pending'], n_records, p=[0.8, 0.05, 0.15]),
        'SOX_Required': np.random.choice(['Yes', 'No'], n_records, p=[0.3, 0.7])
    })
    
    return template_df

def calculate_kpis(df):
    """Calculate key procurement KPIs from the data"""
    if df is None or len(df) == 0:
        return {}
    
    # Convert date columns
    date_cols = ['Requisition_Date', 'Approval_Date', 'PO_Issue_Date', 'Invoice_Date', 'Payment_Date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    kpis = {}
    
    # Basic metrics
    kpis['total_spend'] = df['Amount'].sum() if 'Amount' in df.columns else 0
    kpis['total_transactions'] = len(df)
    kpis['avg_transaction_value'] = df['Amount'].mean() if 'Amount' in df.columns else 0
    
    # Cycle time analysis
    if 'Requisition_Date' in df.columns and 'PO_Issue_Date' in df.columns:
        df['req_to_po_days'] = (df['PO_Issue_Date'] - df['Requisition_Date']).dt.days
        kpis['avg_req_to_po_days'] = df['req_to_po_days'].mean()
    
    if 'Invoice_Date' in df.columns and 'Payment_Date' in df.columns:
        df['invoice_to_payment_days'] = (df['Payment_Date'] - df['Invoice_Date']).dt.days
        kpis['avg_payment_days'] = df['invoice_to_payment_days'].mean()
    
    # Financial efficiency
    if 'Discount_Captured' in df.columns:
        kpis['discount_capture_rate'] = (df['Discount_Captured'] == 'Yes').mean() * 100
    
    if 'Late_Fee_Incurred' in df.columns:
        kpis['total_late_fees'] = df['Late_Fee_Incurred'].sum()
    
    # Supplier performance
    if 'Delivery_Performance' in df.columns:
        kpis['on_time_delivery_rate'] = (df['Delivery_Performance'] == 'On Time').mean() * 100
    
    # Process efficiency
    if 'Status' in df.columns:
        kpis['completion_rate'] = (df['Status'] == 'Completed').mean() * 100
    
    return kpis

def show_executive_dashboard():
    """Executive Summary Dashboard"""
    st.title("📊 Executive Dashboard")
    st.markdown("### Strategic Procurement Health at a Glance")
    
    if st.session_state.get('data') is None:
        st.warning("Upload procurement data to see your executive dashboard")
        return
    
    df = st.session_state.data
    kpis = calculate_kpis(df)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Spend", 
            f"${kpis.get('total_spend', 0):,.0f}",
            delta=f"{kpis.get('total_transactions', 0)} transactions"
        )
    
    with col2:
        st.metric(
            "Avg Cycle Time", 
            f"{kpis.get('avg_req_to_po_days', 0):.1f} days",
            delta="Req to PO"
        )
    
    with col3:
        st.metric(
            "Payment Performance", 
            f"{kpis.get('avg_payment_days', 0):.1f} days",
            delta="Invoice to Payment"
        )
    
    with col4:
        st.metric(
            "Process Efficiency", 
            f"{kpis.get('completion_rate', 0):.1f}%",
            delta="Completion Rate"
        )
    
    # Key Insights
    st.markdown("### 🎯 Key Strategic Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Spend by Category
        if 'Category' in df.columns and 'Amount' in df.columns:
            spend_by_category = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
            fig = px.pie(
                values=spend_by_category.values, 
                names=spend_by_category.index,
                title="Spend Distribution by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly Spend Trend
        if 'Requisition_Date' in df.columns and 'Amount' in df.columns:
            df['Month'] = pd.to_datetime(df['Requisition_Date']).dt.strftime('%Y-%m')
            monthly_spend = df.groupby('Month')['Amount'].sum()
            fig = px.line(
                x=monthly_spend.index, 
                y=monthly_spend.values,
                title="Monthly Spend Trend",
                labels={'x': 'Month', 'y': 'Amount ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)

def show_process_analysis():
    """Process Performance Analysis"""
    st.title("🔍 Process Analysis")
    st.markdown("### Where Are Your Process Bottlenecks?")
    
    if st.session_state.get('data') is None:
        st.warning("Upload procurement data to analyze process performance")
        return
    
    df = st.session_state.data
    
    # Cycle Time Analysis
    st.subheader("⏱️ Cycle Time Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Requisition_Date' in df.columns and 'Approval_Date' in df.columns:
            df['approval_cycle'] = (pd.to_datetime(df['Approval_Date']) - pd.to_datetime(df['Requisition_Date'])).dt.days
            fig = px.histogram(df, x='approval_cycle', title="Approval Cycle Time Distribution", nbins=20)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Department' in df.columns and 'approval_cycle' in df.columns:
            dept_performance = df.groupby('Department')['approval_cycle'].mean().sort_values(ascending=False)
            fig = px.bar(x=dept_performance.values, y=dept_performance.index, 
                        title="Average Approval Time by Department", orientation='h')
            st.plotly_chart(fig, use_container_width=True)
    
    # Bottleneck Identification
    st.subheader("🚧 Bottleneck Identification")
    
    if 'Status' in df.columns:
        status_counts = df['Status'].value_counts()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            delayed_pct = (status_counts.get('Delayed', 0) / len(df)) * 100
            st.metric("Delayed Transactions", f"{delayed_pct:.1f}%", delta=f"{status_counts.get('Delayed', 0)} items")
        
        with col2:
            in_progress_pct = (status_counts.get('In Progress', 0) / len(df)) * 100
            st.metric("In Progress", f"{in_progress_pct:.1f}%", delta=f"{status_counts.get('In Progress', 0)} items")
        
        with col3:
            completed_pct = (status_counts.get('Completed', 0) / len(df)) * 100
            st.metric("Completed", f"{completed_pct:.1f}%", delta=f"{status_counts.get('Completed', 0)} items")

def show_financial_analysis():
    """Financial Impact Analysis"""
    st.title("💰 Financial Analysis")
    st.markdown("### What Are Your Process Inefficiencies Costing?")
    
    if st.session_state.get('data') is None:
        st.warning("Upload procurement data to analyze financial impact")
        return
    
    df = st.session_state.data
    
    # Financial Efficiency Metrics
    st.subheader("💡 Financial Efficiency")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Discount_Captured' in df.columns and 'Amount' in df.columns:
            missed_discounts = df[df['Discount_Captured'] == 'No']
            if len(missed_discounts) > 0 and 'Early_Discount_Rate' in df.columns:
                potential_savings = (missed_discounts['Amount'] * missed_discounts['Early_Discount_Rate'] / 100).sum()
                st.metric("Missed Discount Savings", f"${potential_savings:,.0f}")
    
    with col2:
        if 'Late_Fee_Incurred' in df.columns:
            total_late_fees = df['Late_Fee_Incurred'].sum()
            st.metric("Late Fees Incurred", f"${total_late_fees:,.0f}")
    
    with col3:
        if 'Invoice_Date' in df.columns and 'Payment_Date' in df.columns:
            df['payment_delay'] = (pd.to_datetime(df['Payment_Date']) - pd.to_datetime(df['Invoice_Date'])).dt.days
            avg_delay = df['payment_delay'].mean()
            st.metric("Avg Payment Delay", f"{avg_delay:.1f} days")
    
    with col4:
        if 'Amount' in df.columns:
            avg_transaction = df['Amount'].mean()
            st.metric("Avg Transaction Value", f"${avg_transaction:,.0f}")

def show_strategic_opportunities():
    """Strategic Improvement Opportunities"""
    st.title("🎯 Strategic Opportunities")
    st.markdown("### Priority-Ranked Improvement Roadmap")
    
    if st.session_state.get('data') is None:
        st.warning("Upload procurement data to identify strategic opportunities")
        return
    
    df = st.session_state.data
    
    # Generate strategic recommendations based on data analysis
    recommendations = []
    
    # Analyze cycle times
    if 'Requisition_Date' in df.columns and 'Approval_Date' in df.columns:
        df['approval_cycle'] = (pd.to_datetime(df['Approval_Date']) - pd.to_datetime(df['Requisition_Date'])).dt.days
        avg_cycle = df['approval_cycle'].mean()
        if avg_cycle > 7:
            impact = len(df) * 50 * (avg_cycle - 5)  # $50 per day per transaction
            recommendations.append({
                'title': 'Streamline Approval Process',
                'impact': f'${impact:,.0f} annual savings',
                'effort': 'Medium',
                'timeframe': '2-3 months',
                'category': 'Process Optimization'
            })
    
    # Analyze payment performance
    if 'Discount_Captured' in df.columns:
        missed_rate = (df['Discount_Captured'] == 'No').mean()
        if missed_rate > 0.5:
            recommendations.append({
                'title': 'Improve Early Payment Capture',
                'impact': f'{(1-missed_rate)*100:.0f}% discount capture improvement',
                'effort': 'Low',
                'timeframe': '1 month',
                'category': 'Financial Optimization'
            })
    
    # Display recommendations
    for i, rec in enumerate(recommendations):
        with st.expander(f"🎯 Opportunity {i+1}: {rec['title']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expected Impact", rec['impact'])
            with col2:
                st.metric("Implementation Effort", rec['effort'])
            with col3:
                st.metric("Timeframe", rec['timeframe'])
            
            st.markdown(f"**Category:** {rec['category']}")

def show_forward_planning():
    """Forward Planning & Capacity Analysis"""
    st.title("📈 Forward Planning")
    st.markdown("### Capacity Planning & Future Insights")
    
    if st.session_state.get('data') is None:
        st.warning("Upload procurement data for forward planning analysis")
        return
    
    df = st.session_state.data
    
    # Volume forecasting
    st.subheader("📊 Volume Forecasting")
    
    if 'Requisition_Date' in df.columns:
        df['Month'] = pd.to_datetime(df['Requisition_Date']).dt.strftime('%Y-%m')
        monthly_volume = df.groupby('Month').size()
        
        # Simple trend analysis
        fig = px.line(x=monthly_volume.index, y=monthly_volume.values,
                     title="Monthly Transaction Volume Trend")
        st.plotly_chart(fig, use_container_width=True)
        
        # Capacity recommendations
        avg_monthly_volume = monthly_volume.mean()
        peak_volume = monthly_volume.max()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Monthly Volume", f"{avg_monthly_volume:.0f} transactions")
        with col2:
            st.metric("Peak Monthly Volume", f"{peak_volume:.0f} transactions")

def main():
    """Main application"""
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    # Sidebar for data management
    with st.sidebar:
        st.title("📊 Data Management")
        
        # Template download
        st.subheader("📋 Download Template")
        template_df = create_comprehensive_template()
        csv_buffer = io.StringIO()
        template_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Procurement Template",
            data=csv_data,
            file_name="Strategic_Procurement_Template.csv",
            mime="text/csv"
        )
        
        st.markdown(f"**Template includes:** {len(template_df.columns)} strategic data fields")
        
        # File upload
        st.subheader("📤 Upload Data")
        uploaded_file = st.file_uploader("Upload your procurement data", type=['csv'])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df
            st.success(f"✅ Data loaded: {len(df)} records")
        
        # Demo data
        st.subheader("🔬 Demo Data")
        if st.button("Load Demo Data"):
            st.session_state.data = create_comprehensive_template()
            st.success("✅ Demo data loaded")
    
    # Main content area with strategic tabs
    st.title("🚀 Strategic Procurement Analytics")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Dashboard",
        "🔍 Process Analysis", 
        "💰 Financial Analysis",
        "🎯 Strategic Opportunities",
        "📈 Forward Planning"
    ])
    
    with tab1:
        show_executive_dashboard()
    
    with tab2:
        show_process_analysis()
    
    with tab3:
        show_financial_analysis()
    
    with tab4:
        show_strategic_opportunities()
    
    with tab5:
        show_forward_planning()

if __name__ == "__main__":
    main()