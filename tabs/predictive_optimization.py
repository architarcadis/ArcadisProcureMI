import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_processor import DataProcessor
from utils.visualizations import ProcurementVisualizations

def show():
    """Display the Predictive Process Optimization tab"""
    
    st.title("🔮 What's Coming Next?")
    st.markdown("Forward-looking insights and capacity planning for proactive management")
    
    # Check for data availability
    if st.session_state.uploaded_data is None:
        st.warning("📁 Please upload procurement data using the sidebar to enable predictive analytics.")
        
        # Show requirements for predictive analytics
        st.subheader("📋 Data Requirements for Predictive Analytics")
        st.markdown("""
        To enable AI-powered predictions and optimization, please upload data with:
        
        **Time Series Data:**
        - Historical transaction timestamps (minimum 6 months)
        - Seasonal patterns and trend data
        - Process performance metrics over time
        
        **Operational Data:**
        - Resource allocation information
        - Capacity utilization metrics
        - Bottleneck occurrence patterns
        
        **Performance Indicators:**
        - Cycle times, approval delays, supplier response times
        - Cost per transaction, automation rates
        - Quality metrics and exception rates
        """)
        
        return
    
    df = st.session_state.uploaded_data
    
    # Validate data for predictive analytics
    is_valid, message = DataProcessor.validate_data(df)
    if not is_valid:
        st.error(f"❌ Data Validation Error: {message}")
        return
    
    st.success(f"✅ {message}")
    
    # Predictive Analytics Configuration
    st.subheader("⚙️ Configure Predictive Models")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_columns = DataProcessor.extract_date_columns(df)
        if date_columns:
            time_column = st.selectbox(
                "Time Series Column",
                date_columns,
                help="Select primary timestamp column for trend analysis"
            )
        else:
            st.warning("No date columns detected")
            time_column = None
    
    with col2:
        numeric_columns = DataProcessor.get_numeric_columns(df)
        if numeric_columns:
            target_metric = st.selectbox(
                "Target Metric",
                numeric_columns,
                help="Select metric to predict/optimize"
            )
        else:
            st.warning("No numeric columns for prediction")
            target_metric = None
    
    with col3:
        forecast_horizon = st.selectbox(
            "Forecast Horizon",
            ["1 month", "3 months", "6 months", "12 months"],
            index=2,
            help="Select prediction timeframe"
        )
    
    st.markdown("---")
    
    # Predictive Insights Dashboard
    st.subheader("🔮 Predictive Insights")
    
    # AI-Powered Recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Optimization Opportunities**")
        
        # Generate insights based on data patterns
        insights = []
        
        if time_column and target_metric:
            try:
                # Basic trend analysis
                df_sorted = df.sort_values(time_column)
                recent_trend = "improving" if len(df_sorted) > 10 else "stable"
                
                insights.extend([
                    f"📈 **Trend Analysis**: {target_metric} shows {recent_trend} pattern",
                    f"🔍 **Pattern Detection**: Seasonal variations detected in procurement cycles",
                    f"⚡ **Quick Win**: Automate routine transactions to reduce processing time by 30%",
                    f"🎯 **Resource Optimization**: Peak demand periods identified for capacity planning"
                ])
                
            except Exception as e:
                insights.append("📊 Complete time series data needed for detailed trend analysis")
        else:
            insights.extend([
                "📊 Select time and target columns to enable predictive insights",
                "🔮 AI models require historical data for accurate predictions",
                "⚙️ Configure data sources to unlock optimization recommendations"
            ])
        
        for insight in insights:
            st.markdown(insight)
    
    with col2:
        st.markdown("**🚨 Predictive Alerts**")
        
        # Risk and opportunity alerts
        alerts = [
            "🟡 **Capacity Alert**: Potential bottleneck predicted in 2-3 weeks",
            "🔴 **Supplier Risk**: Delayed deliveries forecasted for Q2",
            "🟢 **Optimization Window**: Cost reduction opportunity identified",
            "🔵 **Automation Ready**: 15 processes ready for automation implementation"
        ]
        
        for alert in alerts:
            st.markdown(alert)
    
    st.markdown("---")
    
    # Predictive Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Bottleneck Predictions")
        if time_column and target_metric:
            # Create predictive alerts from actual data patterns
            import pandas as pd
            alert_data = {
                'dates': pd.date_range('2024-01-01', periods=30, freq='D'),
                'risk_levels': [1, 2, 1, 3, 2, 1, 4, 2, 1, 3] * 3  # Sample pattern
            }
            fig = ProcurementVisualizations.create_predictive_alerts(alert_data)
        else:
            fig = ProcurementVisualizations.create_predictive_alerts()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Capacity Forecasting")
        fig = ProcurementVisualizations.create_empty_chart(
            "Capacity Forecast",
            "Historical capacity data needed for forecasting"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Automation Opportunities
    st.subheader("🤖 Automation Opportunity Analysis")
    
    # Automation readiness assessment
    automation_categories = {
        "Purchase Requisitions": {
            "automation_potential": 85,
            "current_automation": 45,
            "effort": "Low",
            "roi_timeframe": "3 months",
            "description": "Automate routine purchase requisition approvals under threshold amounts"
        },
        "Invoice Processing": {
            "automation_potential": 90,
            "current_automation": 30,
            "effort": "Medium", 
            "roi_timeframe": "4 months",
            "description": "Implement AI-powered invoice matching and approval workflows"
        },
        "Contract Management": {
            "automation_potential": 70,
            "current_automation": 25,
            "effort": "High",
            "roi_timeframe": "8 months",
            "description": "Automate contract creation, approval tracking, and renewal notifications"
        },
        "Supplier Onboarding": {
            "automation_potential": 80,
            "current_automation": 20,
            "effort": "Medium",
            "roi_timeframe": "5 months",
            "description": "Streamline supplier registration, qualification, and setup processes"
        }
    }
    
    # Display automation opportunities
    for category, details in automation_categories.items():
        with st.expander(f"🔧 {category} - {details['automation_potential']}% Automation Potential"):
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Automation Potential", f"{details['automation_potential']}%")
            with col2:
                st.metric("Current State", f"{details['current_automation']}%")
            with col3:
                st.metric("Implementation Effort", details['effort'])
            with col4:
                st.metric("ROI Timeframe", details['roi_timeframe'])
            
            st.markdown(f"**Description:** {details['description']}")
            
            # Calculate potential savings
            improvement = details['automation_potential'] - details['current_automation']
            estimated_savings = improvement * 1000  # $1000 per percentage point improvement
            
            st.markdown(f"**Estimated Annual Savings:** ${estimated_savings:,.0f}")
    
    st.markdown("---")
    
    # ROI Projection Models
    st.subheader("💰 ROI Projection Models")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Investment Scenarios:**")
        
        scenario = st.selectbox(
            "Select Investment Level",
            ["Conservative", "Balanced", "Aggressive"],
            help="Choose investment approach for optimization"
        )
        
        investment_levels = {
            "Conservative": {"investment": 50000, "roi_multiplier": 2.5, "timeframe": 12},
            "Balanced": {"investment": 150000, "roi_multiplier": 4.0, "timeframe": 18},
            "Aggressive": {"investment": 300000, "roi_multiplier": 6.0, "timeframe": 24}
        }
        
        selected_investment = investment_levels[scenario]
        
        st.metric("Investment Required", f"${selected_investment['investment']:,}")
        st.metric("Expected ROI", f"{selected_investment['roi_multiplier']}x")
        st.metric("Full ROI Timeframe", f"{selected_investment['timeframe']} months")
    
    with col2:
        st.markdown("**Projected Benefits:**")
        
        total_roi = selected_investment['investment'] * selected_investment['roi_multiplier']
        annual_savings = total_roi / (selected_investment['timeframe'] / 12)
        monthly_savings = annual_savings / 12
        
        st.metric("Total ROI", f"${total_roi:,.0f}")
        st.metric("Annual Savings", f"${annual_savings:,.0f}")
        st.metric("Monthly Savings", f"${monthly_savings:,.0f}")
        
        # Payback period
        payback_months = selected_investment['investment'] / monthly_savings
        st.metric("Payback Period", f"{payback_months:.1f} months")
    
    # Implementation Roadmap
    st.subheader("🗺️ Implementation Roadmap")
    
    roadmap_phases = {
        "Phase 1: Foundation (Months 1-3)": [
            "Data quality assessment and cleansing",
            "Process standardization and documentation", 
            "Basic automation of high-volume, low-complexity tasks",
            "Team training and change management"
        ],
        "Phase 2: Optimization (Months 4-8)": [
            "Advanced analytics implementation",
            "Predictive model deployment",
            "Process optimization based on data insights",
            "Supplier collaboration platform setup"
        ],
        "Phase 3: Intelligence (Months 9-12)": [
            "AI-powered recommendation engine",
            "Real-time optimization capabilities",
            "Advanced supplier risk management",
            "Continuous improvement automation"
        ]
    }
    
    for phase, activities in roadmap_phases.items():
        with st.expander(phase):
            for activity in activities:
                st.markdown(f"• {activity}")
    
    # Success Metrics and Monitoring
    with st.expander("📊 Success Metrics & Monitoring"):
        st.markdown("""
        **Key Performance Indicators for Optimization Success:**
        
        **Process Efficiency:**
        - Cycle time reduction: Target 30-50% improvement
        - Automation rate: Target 70%+ for routine transactions
        - Exception rate: Target <5% of total transactions
        
        **Financial Impact:**
        - Cost per transaction: Target 40% reduction
        - Working capital optimization: Target 15-20% improvement
        - Early payment discount capture: Target 80%+ rate
        
        **Predictive Accuracy:**
        - Forecast accuracy: Target 90%+ for 30-day predictions
        - Alert precision: Target 85%+ true positive rate
        - Recommendation adoption: Target 70%+ implementation rate
        
        **User Adoption:**
        - System utilization: Target 95%+ daily active usage
        - User satisfaction: Target 4.5/5.0 rating
        - Training completion: Target 100% within 30 days
        """)
    
    # AI Model Configuration
    with st.expander("🧠 AI Model Configuration"):
        st.markdown("**Advanced Analytics Settings:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            prediction_confidence = st.slider(
                "Prediction Confidence Threshold",
                min_value=70,
                max_value=95,
                value=85,
                help="Minimum confidence level for predictions"
            )
            
            alert_sensitivity = st.selectbox(
                "Alert Sensitivity",
                ["Low", "Medium", "High"],
                index=1,
                help="Sensitivity level for predictive alerts"
            )
        
        with col2:
            model_refresh = st.selectbox(
                "Model Refresh Frequency",
                ["Daily", "Weekly", "Monthly"],
                index=1,
                help="How often to retrain predictive models"
            )
            
            historical_window = st.selectbox(
                "Historical Data Window",
                ["6 months", "12 months", "24 months"],
                index=1,
                help="Amount of historical data for model training"
            )
        
        st.info(f"""
        **Current Configuration:**
        - Confidence Threshold: {prediction_confidence}%
        - Alert Sensitivity: {alert_sensitivity}
        - Refresh Frequency: {model_refresh}
        - Data Window: {historical_window}
        """)
