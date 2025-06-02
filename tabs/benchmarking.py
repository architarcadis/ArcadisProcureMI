import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.visualizations import ProcurementVisualizations

def show():
    """Display the Benchmarking Intelligence tab"""
    
    st.title("📊 Benchmarking Intelligence")
    st.markdown("Industry comparison and performance target setting")
    
    # Industry Benchmarks (these would typically come from external databases)
    industry_benchmarks = {
        "Manufacturing": {
            "avg_cycle_time": 28,
            "process_efficiency": 78,
            "cost_per_transaction": 120,
            "automation_rate": 65,
            "supplier_performance": 82
        },
        "Healthcare": {
            "avg_cycle_time": 35,
            "process_efficiency": 72,
            "cost_per_transaction": 180,
            "automation_rate": 45,
            "supplier_performance": 79
        },
        "Financial Services": {
            "avg_cycle_time": 22,
            "process_efficiency": 85,
            "cost_per_transaction": 95,
            "automation_rate": 78,
            "supplier_performance": 88
        },
        "Government": {
            "avg_cycle_time": 45,
            "process_efficiency": 68,
            "cost_per_transaction": 220,
            "automation_rate": 35,
            "supplier_performance": 75
        },
        "Technology": {
            "avg_cycle_time": 18,
            "process_efficiency": 92,
            "cost_per_transaction": 75,
            "automation_rate": 85,
            "supplier_performance": 91
        }
    }
    
    # Industry Selection
    st.subheader("🏭 Industry Context")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_industry = st.selectbox(
            "Select Your Industry",
            list(industry_benchmarks.keys()),
            help="Choose your industry for relevant benchmarking"
        )
    
    with col2:
        st.info(f"""
        **Industry Selected: {selected_industry}**
        
        Benchmarks are based on data from leading procurement organizations 
        within the {selected_industry.lower()} sector.
        """)
    
    current_benchmarks = industry_benchmarks[selected_industry]
    
    st.markdown("---")
    
    # Performance Assessment
    st.subheader("📈 Current Performance Assessment")
    
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        # Calculate current performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Configure Performance Metrics:**")
            
            date_columns = DataProcessor.extract_date_columns(df)
            numeric_columns = DataProcessor.get_numeric_columns(df)
            
            if date_columns and len(date_columns) >= 2:
                start_col = st.selectbox("Process Start Column", date_columns)
                end_col = st.selectbox("Process End Column", date_columns, index=1)
                
                # Calculate current cycle time
                cycle_times = DataProcessor.calculate_cycle_times(df, start_col, end_col)
                if cycle_times is not None:
                    current_cycle_time = cycle_times.mean()
                else:
                    current_cycle_time = None
            else:
                current_cycle_time = None
                st.warning("Need at least 2 date columns for cycle time analysis")
            
            if numeric_columns:
                cost_col = st.selectbox("Cost/Amount Column", ["Estimate"] + numeric_columns)
                if cost_col != "Estimate":
                    avg_transaction_cost = df[cost_col].mean()
                else:
                    avg_transaction_cost = None
            else:
                avg_transaction_cost = None
        
        with col2:
            st.markdown("**Performance Comparison:**")
            
            # Current vs Benchmark metrics
            metrics_comparison = []
            
            if current_cycle_time:
                cycle_performance = (current_benchmarks["avg_cycle_time"] / current_cycle_time) * 100
                metrics_comparison.append({
                    "metric": "Cycle Time",
                    "current": f"{current_cycle_time:.1f} days",
                    "benchmark": f"{current_benchmarks['avg_cycle_time']} days",
                    "performance": f"{cycle_performance:.0f}%"
                })
            
            # Estimated metrics (when data is incomplete)
            est_efficiency = 75  # Default estimate
            est_automation = 50  # Default estimate
            
            efficiency_performance = (est_efficiency / current_benchmarks["process_efficiency"]) * 100
            automation_performance = (est_automation / current_benchmarks["automation_rate"]) * 100
            
            metrics_comparison.extend([
                {
                    "metric": "Process Efficiency",
                    "current": f"{est_efficiency}%",
                    "benchmark": f"{current_benchmarks['process_efficiency']}%",
                    "performance": f"{efficiency_performance:.0f}%"
                },
                {
                    "metric": "Automation Rate",
                    "current": f"{est_automation}%",
                    "benchmark": f"{current_benchmarks['automation_rate']}%",
                    "performance": f"{automation_performance:.0f}%"
                }
            ])
            
            # Display comparison table
            comparison_df = pd.DataFrame(metrics_comparison)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    else:
        st.warning("📁 Upload procurement data to compare against industry benchmarks")
        
        # Show benchmark standards
        st.subheader("📊 Industry Standards")
        benchmark_df = pd.DataFrame.from_dict(current_benchmarks, orient='index', columns=['Benchmark Value'])
        benchmark_df.index.name = 'Metric'
        st.dataframe(benchmark_df, use_container_width=True)
    
    st.markdown("---")
    
    # Benchmark Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Performance Radar Chart")
        if st.session_state.uploaded_data is not None and current_cycle_time:
            # Create radar data from actual performance vs benchmarks
            radar_data = {
                'categories': ['Cycle Time', 'Cost Efficiency', 'Quality', 'Automation', 'Compliance'],
                'current': [cycle_performance, efficiency_performance, 85, automation_performance, 90],
                'benchmark': [100, 100, 80, 100, 85]
            }
            fig = ProcurementVisualizations.create_benchmark_radar(radar_data)
        else:
            fig = ProcurementVisualizations.create_benchmark_radar()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Industry Comparison")
        # Create a simple comparison chart
        fig = ProcurementVisualizations.create_empty_chart(
            "Industry Ranking",
            "Upload performance data to see industry ranking"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Maturity Assessment
    st.subheader("🎯 Procurement Maturity Assessment")
    
    maturity_areas = {
        "Process Standardization": {
            "description": "Standardized procurement processes across organization",
            "levels": ["Ad-hoc", "Defined", "Managed", "Optimized", "Best-in-class"]
        },
        "Digital Automation": {
            "description": "Level of automation in procurement workflows",
            "levels": ["Manual", "Basic Tools", "Integrated Systems", "AI-Enhanced", "Fully Autonomous"]
        },
        "Data Analytics": {
            "description": "Use of data analytics for procurement decisions",
            "levels": ["None", "Basic Reporting", "Advanced Analytics", "Predictive Models", "AI-Driven Insights"]
        },
        "Supplier Management": {
            "description": "Sophistication of supplier relationship management",
            "levels": ["Transactional", "Collaborative", "Strategic", "Integrated", "Ecosystem Partner"]
        }
    }
    
    maturity_scores = {}
    
    for area, details in maturity_areas.items():
        with st.expander(f"📋 {area}"):
            st.markdown(f"*{details['description']}*")
            
            score = st.select_slider(
                f"Current Level - {area}",
                options=details['levels'],
                value=details['levels'][2],  # Default to middle level
                key=f"maturity_{area}"
            )
            
            # Convert to numeric score
            maturity_scores[area] = details['levels'].index(score) + 1
    
    # Calculate overall maturity score
    if maturity_scores:
        overall_score = sum(maturity_scores.values()) / len(maturity_scores)
        maturity_percentage = (overall_score / 5) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Overall Maturity Score",
                f"{overall_score:.1f}/5.0",
                help="Average score across all maturity areas"
            )
        
        with col2:
            st.metric(
                "Maturity Percentage",
                f"{maturity_percentage:.0f}%",
                help="Procurement maturity as percentage"
            )
        
        with col3:
            if maturity_percentage < 40:
                maturity_level = "Developing"
            elif maturity_percentage < 60:
                maturity_level = "Intermediate"
            elif maturity_percentage < 80:
                maturity_level = "Advanced"
            else:
                maturity_level = "Leading"
            
            st.metric(
                "Maturity Level",
                maturity_level,
                help="Overall procurement maturity classification"
            )
    
    st.markdown("---")
    
    # Gap Analysis and Recommendations
    st.subheader("🎯 Gap Analysis & Recommendations")
    
    if st.session_state.uploaded_data is not None and maturity_scores:
        # Priority improvement areas
        low_scoring_areas = [area for area, score in maturity_scores.items() if score <= 2]
        medium_scoring_areas = [area for area, score in maturity_scores.items() if 2 < score <= 3]
        
        if low_scoring_areas:
            st.markdown("**🔴 High Priority Improvement Areas:**")
            for area in low_scoring_areas:
                st.markdown(f"- **{area}**: Focus on establishing foundational capabilities")
        
        if medium_scoring_areas:
            st.markdown("**🟡 Medium Priority Enhancement Areas:**")
            for area in medium_scoring_areas:
                st.markdown(f"- **{area}**: Advance from defined to optimized practices")
        
        # Industry-specific recommendations
        st.markdown(f"**📊 {selected_industry} Industry Recommendations:**")
        
        if selected_industry == "Technology":
            recommendations = [
                "Leverage AI and machine learning for demand forecasting",
                "Implement real-time supplier collaboration platforms",
                "Focus on innovation partnerships with strategic suppliers"
            ]
        elif selected_industry == "Healthcare":
            recommendations = [
                "Prioritize regulatory compliance in procurement processes",
                "Implement specialized supplier qualification programs",
                "Focus on total cost of ownership for medical equipment"
            ]
        elif selected_industry == "Manufacturing":
            recommendations = [
                "Integrate procurement with production planning systems",
                "Implement supplier risk management for supply chain resilience",
                "Focus on sustainability and circular economy principles"
            ]
        elif selected_industry == "Financial Services":
            recommendations = [
                "Emphasize security and compliance in vendor selection",
                "Implement sophisticated contract management systems",
                "Focus on operational risk management with suppliers"
            ]
        else:  # Government
            recommendations = [
                "Ensure transparency and audit-ready documentation",
                "Implement competitive bidding process optimization",
                "Focus on value for money and public accountability"
            ]
        
        for rec in recommendations:
            st.markdown(f"• {rec}")
    
    else:
        st.info("Complete the maturity assessment and upload data for personalized gap analysis")
    
    # Best Practices Repository
    with st.expander("📚 Industry Best Practices"):
        st.markdown(f"""
        **Leading Practices in {selected_industry} Procurement:**
        
        **Process Excellence:**
        - Standardized procurement workflows with clear approval thresholds
        - Exception-based management for routine transactions
        - Continuous process improvement based on performance metrics
        
        **Technology Enablement:**
        - Integrated procurement platforms with ERP systems
        - Mobile-enabled approval workflows for faster decision-making
        - AI-powered spend analysis and supplier recommendations
        
        **Supplier Relationship Management:**
        - Strategic supplier segmentation and differentiated management
        - Regular business reviews with key suppliers
        - Collaborative innovation programs with strategic partners
        
        **Performance Management:**
        - Real-time dashboards for procurement KPI monitoring
        - Predictive analytics for demand forecasting
        - Benchmarking against industry standards and best-in-class performers
        """)
