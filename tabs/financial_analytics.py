import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.visualizations import ProcurementVisualizations

def show():
    """Display the Financial Impact Analytics tab"""
    
    st.title("💰 What's This Costing Me?")
    st.markdown("Quantify the financial impact of process delays and identify savings opportunities")
    
    # Check for data
    if st.session_state.uploaded_data is None:
        st.warning("📁 Please upload procurement data using the sidebar to view financial analytics.")
        
        # Show sample structure
        st.subheader("📋 Expected Financial Data Structure")
        st.markdown("""
        To enable financial impact analysis, please upload data with these columns:
        - **Invoice Date/Timestamp**: When invoices were received
        - **Payment Date**: When payments were made
        - **Payment Terms**: Contracted payment terms (e.g., Net 30)
        - **Invoice Amount**: Value of invoices
        - **Early Payment Discounts**: Available discount rates
        - **Supplier Information**: For supplier-based analysis
        """)
        
        return
    
    df = st.session_state.uploaded_data
    
    # Validate data
    is_valid, message = DataProcessor.validate_data(df)
    if not is_valid:
        st.error(f"❌ Data Validation Error: {message}")
        return
    
    st.success(f"✅ {message}")
    
    # Configuration Section
    st.subheader("⚙️ Configure Financial Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_columns = DataProcessor.extract_date_columns(df)
        numeric_columns = DataProcessor.get_numeric_columns(df)
        
        if date_columns:
            invoice_date_col = st.selectbox(
                "Invoice Date Column",
                date_columns,
                help="Select column with invoice dates"
            )
        else:
            st.warning("No date columns detected")
            invoice_date_col = None
    
    with col2:
        if date_columns:
            payment_date_col = st.selectbox(
                "Payment Date Column",
                ["None"] + date_columns,
                help="Select column with payment dates"
            )
            payment_date_col = None if payment_date_col == "None" else payment_date_col
        else:
            payment_date_col = None
    
    with col3:
        if numeric_columns:
            amount_col = st.selectbox(
                "Amount/Value Column",
                numeric_columns,
                help="Select column with transaction amounts"
            )
        else:
            st.warning("No numeric columns detected")
            amount_col = None
    
    st.markdown("---")
    
    # Financial KPIs
    st.subheader("💰 Financial Performance Indicators")
    
    if amount_col and amount_col in df.columns:
        total_value = df[amount_col].sum()
        avg_transaction = df[amount_col].mean()
        transaction_count = len(df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Transaction Value",
                f"${total_value:,.0f}",
                help="Sum of all transaction amounts"
            )
        
        with col2:
            st.metric(
                "Average Transaction",
                f"${avg_transaction:,.0f}",
                help="Average transaction value"
            )
        
        with col3:
            st.metric(
                "Transaction Count",
                f"{transaction_count:,}",
                help="Total number of transactions"
            )
        
        with col4:
            # Calculate estimated working capital impact
            estimated_wc_days = 45  # Default assumption
            working_capital = (total_value / 365) * estimated_wc_days
            st.metric(
                "Est. Working Capital",
                f"${working_capital:,.0f}",
                help="Estimated working capital tied up"
            )
    else:
        st.info("Select amount column to view financial KPIs")
    
    # Payment Analysis
    if invoice_date_col and payment_date_col:
        st.subheader("📅 Payment Cycle Analysis")
        
        try:
            payment_days = DataProcessor.calculate_cycle_times(df, invoice_date_col, payment_date_col)
            
            if payment_days is not None and len(payment_days) > 0:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_payment_days = payment_days.mean()
                    st.metric(
                        "Average Payment Days",
                        f"{avg_payment_days:.1f} days",
                        help="Average days from invoice to payment"
                    )
                
                with col2:
                    early_payments = (payment_days <= 10).sum()
                    early_payment_rate = (early_payments / len(payment_days)) * 100
                    st.metric(
                        "Early Payment Rate",
                        f"{early_payment_rate:.1f}%",
                        help="Percentage of payments made within 10 days"
                    )
                
                with col3:
                    late_payments = (payment_days > 45).sum()
                    late_payment_rate = (late_payments / len(payment_days)) * 100
                    st.metric(
                        "Late Payment Rate",
                        f"{late_payment_rate:.1f}%",
                        help="Percentage of payments made after 45 days"
                    )
        except Exception as e:
            st.error(f"Error calculating payment cycles: {str(e)}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💧 Payment Cycle Waterfall")
        if invoice_date_col and payment_date_col and payment_days is not None:
            # Create waterfall data from actual payment cycles
            waterfall_data = {
                'stages': ['Invoice Received', 'Approval', 'Processing', 'Payment'],
                'values': [payment_days.mean(), -5, -8, -12]  # Use actual average
            }
            fig = ProcurementVisualizations.create_payment_waterfall(waterfall_data)
        else:
            fig = ProcurementVisualizations.create_payment_waterfall()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Working Capital Impact")
        # Create a simple working capital visualization
        if amount_col:
            fig = ProcurementVisualizations.create_empty_chart(
                "Working Capital Trends",
                "Historical payment data needed for working capital analysis"
            )
        else:
            fig = ProcurementVisualizations.create_empty_chart(
                "Working Capital Trends",
                "Select amount column to enable working capital analysis"
            )
        st.plotly_chart(fig, use_container_width=True)
    
    # Savings Opportunities
    st.subheader("💡 Savings Opportunities")
    
    savings_opportunities = []
    
    if invoice_date_col and payment_date_col and amount_col:
        try:
            payment_days = DataProcessor.calculate_cycle_times(df, invoice_date_col, payment_date_col)
            
            if payment_days is not None:
                avg_days = payment_days.mean()
                total_value = df[amount_col].sum()
                
                # Early payment discount opportunity
                early_payment_savings = total_value * 0.02 * 0.3  # 2% discount on 30% of transactions
                savings_opportunities.append({
                    "opportunity": "Early Payment Discounts",
                    "description": "Capture 2% discounts on eligible payments",
                    "annual_savings": early_payment_savings,
                    "implementation": "Implement automated early payment workflows"
                })
                
                # Working capital optimization
                if avg_days > 30:
                    days_improvement = min(avg_days - 30, 15)
                    wc_savings = (total_value / 365) * days_improvement * 0.05  # 5% cost of capital
                    savings_opportunities.append({
                        "opportunity": "Working Capital Optimization",
                        "description": f"Reduce payment days by {days_improvement:.0f} days",
                        "annual_savings": wc_savings,
                        "implementation": "Streamline approval processes and payment automation"
                    })
                
                # Process cost reduction
                process_cost_savings = len(df) * 50  # $50 per transaction reduction
                savings_opportunities.append({
                    "opportunity": "Process Cost Reduction",
                    "description": "Automate manual invoice processing steps",
                    "annual_savings": process_cost_savings,
                    "implementation": "Deploy invoice automation and digital workflows"
                })
        
        except Exception as e:
            st.error(f"Error calculating savings opportunities: {str(e)}")
    
    if savings_opportunities:
        for i, opp in enumerate(savings_opportunities):
            with st.expander(f"💰 {opp['opportunity']} - ${opp['annual_savings']:,.0f} annual savings"):
                st.markdown(f"**Description:** {opp['description']}")
                st.markdown(f"**Implementation:** {opp['implementation']}")
                st.markdown(f"**Projected Annual Savings:** ${opp['annual_savings']:,.0f}")
    else:
        st.info("Complete payment cycle data needed to identify specific savings opportunities")
    
    # Supplier Analysis
    categorical_cols = DataProcessor.get_categorical_columns(df)
    supplier_cols = [col for col in categorical_cols if 'supplier' in col.lower() or 'vendor' in col.lower()]
    
    if supplier_cols and amount_col:
        st.subheader("🏢 Supplier Financial Analysis")
        
        supplier_col = st.selectbox("Select Supplier Column", supplier_cols)
        
        try:
            supplier_analysis = df.groupby(supplier_col)[amount_col].agg([
                'sum', 'count', 'mean'
            ]).round(2)
            supplier_analysis.columns = ['Total Value', 'Transaction Count', 'Avg Transaction']
            supplier_analysis = supplier_analysis.sort_values('Total Value', ascending=False).head(10)
            
            st.dataframe(supplier_analysis, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in supplier analysis: {str(e)}")
    
    # Cash Flow Forecasting
    with st.expander("📈 Cash Flow Forecasting"):
        st.markdown("""
        **Cash Flow Optimization Recommendations:**
        
        1. **Payment Timing Optimization**: Schedule payments to maximize cash flow benefits
        2. **Early Payment Programs**: Negotiate better discount terms with key suppliers
        3. **Payment Consolidation**: Group payments to reduce processing costs
        4. **Seasonal Planning**: Adjust payment cycles based on business seasonality
        
        *Note: Upload historical payment data spanning multiple periods for detailed cash flow forecasting.*
        """)
