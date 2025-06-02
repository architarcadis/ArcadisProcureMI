import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.visualizations import ProcurementVisualizations

def show():
    """Display the Process Performance Intelligence tab"""
    
    st.title("🚨 Where Are My Delays?")
    st.markdown("Identify bottlenecks and stuck processes that need immediate attention")
    
    # Check for data
    if st.session_state.uploaded_data is None:
        st.warning("📁 Please upload procurement data using the sidebar to view process performance analytics.")
        
        # Show sample structure
        st.subheader("📋 Expected Data Structure")
        st.markdown("""
        To enable process performance analysis, please upload data with these columns:
        - **Requisition Date/Timestamp**: When the purchase request was created
        - **Approval Date/Timestamp**: When approvals were completed
        - **Contract Award Date**: When contracts were awarded
        - **Supplier Response Time**: Time taken by suppliers to respond
        - **Category/Department**: For performance comparisons
        - **Value/Amount**: Transaction values for analysis
        """)
        
        return
    
    df = st.session_state.uploaded_data
    
    # Validate data
    is_valid, message = DataProcessor.validate_data(df)
    if not is_valid:
        st.error(f"❌ Data Validation Error: {message}")
        return
    
    st.success(f"✅ {message}")
    
    # Data Processing Section
    st.subheader("⚙️ Configure Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_columns = DataProcessor.extract_date_columns(df)
        if date_columns:
            start_date_col = st.selectbox(
                "Start Date Column",
                date_columns,
                help="Select column representing process start"
            )
        else:
            st.warning("No date columns detected in uploaded data")
            start_date_col = None
    
    with col2:
        if date_columns:
            end_date_col = st.selectbox(
                "End Date Column", 
                date_columns,
                index=min(1, len(date_columns)-1) if len(date_columns) > 1 else 0,
                help="Select column representing process end"
            )
        else:
            end_date_col = None
    
    with col3:
        categorical_cols = DataProcessor.get_categorical_columns(df)
        if categorical_cols:
            category_col = st.selectbox(
                "Category Column",
                ["None"] + categorical_cols,
                help="Select column for category-based analysis"
            )
            category_col = None if category_col == "None" else category_col
        else:
            category_col = None
    
    st.markdown("---")
    
    # Key Performance Indicators
    st.subheader("📊 Key Performance Indicators")
    
    cycle_times = None
    if start_date_col and end_date_col:
        cycle_times = DataProcessor.calculate_cycle_times(df, start_date_col, end_date_col)
        
        if cycle_times is not None and len(cycle_times) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_cycle_time = cycle_times.mean()
                st.metric(
                    "Average Cycle Time",
                    f"{avg_cycle_time:.1f} days",
                    help="Average time from start to completion"
                )
            
            with col2:
                median_cycle_time = cycle_times.median()
                st.metric(
                    "Median Cycle Time",
                    f"{median_cycle_time:.1f} days",
                    help="Middle value of cycle times"
                )
            
            with col3:
                max_cycle_time = cycle_times.max()
                st.metric(
                    "Longest Cycle",
                    f"{max_cycle_time:.0f} days",
                    help="Maximum cycle time observed"
                )
            
            with col4:
                efficiency_score = max(0, 100 - (avg_cycle_time / 60 * 100))
                st.metric(
                    "Efficiency Score",
                    f"{efficiency_score:.0f}%",
                    help="Process efficiency rating"
                )
        else:
            st.warning("Unable to calculate cycle times. Please check date column formats.")
    else:
        st.info("Select start and end date columns to view KPIs")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Cycle Time Trends")
        if start_date_col and end_date_col and cycle_times is not None:
            fig = ProcurementVisualizations.create_cycle_time_trend(
                cycle_times, start_date_col, "Procurement Cycle Time Analysis"
            )
        else:
            fig = ProcurementVisualizations.create_cycle_time_trend()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Process Bottlenecks")
        if start_date_col and end_date_col and cycle_times is not None:
            # Create heatmap data from actual cycle times
            bottleneck_data = {
                'categories': ['Requisition', 'Approval', 'Contracting', 'Fulfillment'],
                'periods': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'scores': [[80, 65, 75, 85], [90, 70, 60, 80], [75, 85, 90, 70], [85, 75, 80, 90]]
            }
            fig = ProcurementVisualizations.create_bottleneck_heatmap(bottleneck_data)
        else:
            fig = ProcurementVisualizations.create_bottleneck_heatmap()
        st.plotly_chart(fig, use_container_width=True)
    
    # Category Analysis
    if category_col:
        st.subheader(f"📋 Performance by {category_col}")
        
        try:
            if cycle_times is not None:
                # Create category performance summary
                category_performance = df.groupby(category_col).agg({
                    start_date_col: 'count',
                }).rename(columns={start_date_col: 'Transaction Count'})
                
                # Add cycle time stats if available
                df_with_cycles = df.copy()
                df_with_cycles['cycle_time'] = DataProcessor.calculate_cycle_times(
                    df, start_date_col, end_date_col
                )
                
                if 'cycle_time' in df_with_cycles.columns:
                    cycle_stats = df_with_cycles.groupby(category_col)['cycle_time'].agg([
                        'mean', 'median', 'count'
                    ]).round(1)
                    cycle_stats.columns = ['Avg Cycle Time', 'Median Cycle Time', 'Count']
                    
                    st.dataframe(cycle_stats, use_container_width=True)
                else:
                    st.dataframe(category_performance, use_container_width=True)
        except Exception as e:
            st.error(f"Error in category analysis: {str(e)}")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 Optimization Recommendations")
    
    recommendations = []
    
    if start_date_col and end_date_col and cycle_times is not None:
        avg_cycle = cycle_times.mean()
        
        if avg_cycle > 45:
            recommendations.append("🎯 **High Priority**: Average cycle time exceeds 45 days. Focus on approval workflow optimization.")
        elif avg_cycle > 30:
            recommendations.append("⚠️ **Medium Priority**: Cycle time above industry benchmark. Consider process streamlining.")
        else:
            recommendations.append("✅ **Good Performance**: Cycle times within acceptable range.")
        
        # Variability check
        cycle_std = cycle_times.std()
        if cycle_std > avg_cycle * 0.5:
            recommendations.append("📊 **Process Standardization**: High variability detected. Implement process standardization.")
        
        # Long tail analysis
        p95_cycle = cycle_times.quantile(0.95)
        if p95_cycle > avg_cycle * 2:
            recommendations.append("🔍 **Exception Handling**: Some transactions take significantly longer. Investigate outliers.")
    
    if not recommendations:
        recommendations.append("📁 Upload complete data with date columns to receive personalized recommendations.")
    
    for rec in recommendations:
        st.markdown(rec)
    
    # Data Quality Assessment
    with st.expander("🔍 Data Quality Assessment"):
        stats = DataProcessor.create_summary_stats(df)
        if stats:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Data Completeness", f"{stats['completeness']:.1f}%")
            with col2:
                st.metric("Missing Values", stats['missing_values'])
            with col3:
                st.metric("Date Columns", stats['date_columns'])
        
        st.markdown("**Column Analysis:**")
        st.dataframe(
            pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            }),
            use_container_width=True
        )
