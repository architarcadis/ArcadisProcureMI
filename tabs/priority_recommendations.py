import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.visualizations import ProcurementVisualizations

def show():
    """Display the Priority Recommendations tab - What should I fix first?"""
    
    st.title("🎯 What Should I Fix First?")
    st.markdown("Priority-ranked improvement opportunities based on your data")
    
    # Check for data
    if st.session_state.uploaded_data is None:
        st.warning("📁 Please upload procurement data or load mock data to see priority recommendations.")
        
        st.subheader("🔧 How This Works")
        st.markdown("""
        This module analyzes your actual procurement data to automatically identify:
        
        **From your transaction data, we calculate:**
        - Cycle time patterns to find approval bottlenecks
        - Payment timing to identify discount capture opportunities  
        - Volume patterns to spot automation candidates
        - Supplier performance to find consolidation opportunities
        
        **The tool generates prioritized recommendations with:**
        - Estimated financial impact based on your actual spend
        - Implementation effort assessment
        - Timeline for expected results
        - Specific next steps to get started
        """)
        return
    
    df = st.session_state.uploaded_data
    
    # Validate data
    is_valid, message = DataProcessor.validate_data(df)
    if not is_valid:
        st.error(f"❌ Data Validation Error: {message}")
        return
    
    st.success(f"✅ {message}")
    
    # Priority Recommendations Analysis
    recommendations = []
    
    # Analyze cycle times for quick wins
    date_columns = DataProcessor.extract_date_columns(df)
    if len(date_columns) >= 2:
        cycle_times = DataProcessor.calculate_cycle_times(df, date_columns[0], date_columns[1])
        if cycle_times is not None:
            avg_cycle = cycle_times.mean()
            if avg_cycle > 30:
                potential_savings = len(df) * 100 * (avg_cycle - 25) / avg_cycle  # $100 per day saved per transaction
                recommendations.append({
                    'priority': 'High',
                    'category': 'Quick Win',
                    'title': 'Reduce Approval Cycle Times',
                    'impact': f'${potential_savings:,.0f} annual savings',
                    'effort': 'Medium',
                    'timeframe': '1-3 months',
                    'description': f'Average cycle time is {avg_cycle:.1f} days. Target 25 days to unlock significant savings.',
                    'next_steps': ['Review approval workflows', 'Implement parallel approvals', 'Set approval time limits']
                })
    
    # Analyze payment terms for financial opportunities
    if 'Payment_Terms' in df.columns and 'Invoice_Amount' in df.columns:
        total_amount = df['Invoice_Amount'].sum()
        early_discount_opportunity = total_amount * 0.02 * 0.3  # 2% discount on 30% of spend
        recommendations.append({
            'priority': 'High',
            'category': 'Quick Win',
            'title': 'Capture Early Payment Discounts',
            'impact': f'${early_discount_opportunity:,.0f} annual opportunity',
            'effort': 'Low',
            'timeframe': '0-30 days',
            'description': 'Optimize payment timing to capture available early payment discounts.',
            'next_steps': ['Identify suppliers offering discounts', 'Implement automated payment scheduling', 'Track discount capture rate']
        })
    
    # Analyze automation opportunities
    if 'Amount' in df.columns:
        small_transactions = df[df['Amount'] < 5000]
        if len(small_transactions) > 50:
            automation_savings = len(small_transactions) * 50  # $50 savings per automated transaction
            recommendations.append({
                'priority': 'Medium',
                'category': 'Strategic Improvement',
                'title': 'Automate Small Value Transactions',
                'impact': f'${automation_savings:,.0f} annual savings',
                'effort': 'High',
                'timeframe': '3-6 months',
                'description': f'{len(small_transactions)} transactions under $5K could be automated.',
                'next_steps': ['Define automation thresholds', 'Implement e-procurement system', 'Train users on new process']
            })
    
    # Analyze supplier performance
    if 'Supplier_Name' in df.columns and 'Amount' in df.columns:
        supplier_analysis = df.groupby('Supplier_Name')['Amount'].agg(['sum', 'count']).sort_values('sum', ascending=False)
        top_suppliers = supplier_analysis.head(5)
        consolidation_opportunity = top_suppliers['sum'].sum() * 0.05  # 5% savings through consolidation
        recommendations.append({
            'priority': 'Medium',
            'category': 'Strategic Improvement',
            'title': 'Optimize Supplier Portfolio',
            'impact': f'${consolidation_opportunity:,.0f} potential savings',
            'effort': 'Medium',
            'timeframe': '2-4 months',
            'description': f'Top 5 suppliers represent {top_suppliers["sum"].sum()/df["Amount"].sum()*100:.0f}% of spend.',
            'next_steps': ['Negotiate volume discounts', 'Consolidate similar suppliers', 'Implement preferred supplier programs']
        })
    
    # Add default recommendations if data is limited
    if len(recommendations) < 3:
        recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Process Improvement',
                'title': 'Implement Spend Analytics',
                'impact': '10-15% cost reduction',
                'effort': 'Medium',
                'timeframe': '2-3 months',
                'description': 'Better data visibility leads to improved decision making.',
                'next_steps': ['Standardize data collection', 'Implement reporting dashboards', 'Train team on analytics']
            },
            {
                'priority': 'Low',
                'category': 'Long-term Initiative',
                'title': 'Digital Transformation',
                'impact': '20-30% efficiency gains',
                'effort': 'High',
                'timeframe': '6-12 months',
                'description': 'Comprehensive digitization of procurement processes.',
                'next_steps': ['Assess current technology', 'Define digital strategy', 'Plan phased implementation']
            }
        ])
    
    # Display recommendations by priority
    st.subheader("🚀 Priority Action Plan")
    
    # Quick Wins
    quick_wins = [r for r in recommendations if r['category'] == 'Quick Win']
    if quick_wins:
        st.markdown("### ⚡ Quick Wins (0-30 days)")
        for rec in quick_wins:
            with st.expander(f"🟢 {rec['title']} - {rec['impact']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Impact", rec['impact'])
                with col2:
                    st.metric("Effort", rec['effort'])
                with col3:
                    st.metric("Timeframe", rec['timeframe'])
                
                st.markdown(f"**Description:** {rec['description']}")
                st.markdown("**Next Steps:**")
                for step in rec['next_steps']:
                    st.markdown(f"• {step}")
    
    # Strategic Improvements
    strategic = [r for r in recommendations if r['category'] == 'Strategic Improvement']
    if strategic:
        st.markdown("### 🎯 Strategic Improvements (1-6 months)")
        for rec in strategic:
            with st.expander(f"🟡 {rec['title']} - {rec['impact']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Impact", rec['impact'])
                with col2:
                    st.metric("Effort", rec['effort'])
                with col3:
                    st.metric("Timeframe", rec['timeframe'])
                
                st.markdown(f"**Description:** {rec['description']}")
                st.markdown("**Next Steps:**")
                for step in rec['next_steps']:
                    st.markdown(f"• {step}")
    
    # Long-term Initiatives
    long_term = [r for r in recommendations if r['category'] in ['Process Improvement', 'Long-term Initiative']]
    if long_term:
        st.markdown("### 🏗️ Long-term Initiatives (6+ months)")
        for rec in long_term:
            with st.expander(f"🔵 {rec['title']} - {rec['impact']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Impact", rec['impact'])
                with col2:
                    st.metric("Effort", rec['effort'])
                with col3:
                    st.metric("Timeframe", rec['timeframe'])
                
                st.markdown(f"**Description:** {rec['description']}")
                st.markdown("**Next Steps:**")
                for step in rec['next_steps']:
                    st.markdown(f"• {step}")
    
    # ROI Summary
    st.markdown("---")
    st.subheader("💰 Investment Priorities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🟢 Start Immediately**")
        st.markdown("• Early payment discounts")
        st.markdown("• Process bottleneck removal")
        st.markdown("• Approval workflow optimization")
    
    with col2:
        st.markdown("**🟡 Plan for Next Quarter**")
        st.markdown("• Automation implementation")
        st.markdown("• Supplier consolidation")
        st.markdown("• Technology upgrades")
    
    with col3:
        st.markdown("**🔵 Strategic Planning**")
        st.markdown("• Digital transformation")
        st.markdown("• Organizational restructure")
        st.markdown("• Advanced analytics")
    
    st.info("""
    💡 **Implementation Tip:** Focus on quick wins first to build momentum and fund larger strategic initiatives.
    """)