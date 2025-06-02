import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ProcurementVisualizations:
    """Utility class for creating procurement analytics visualizations"""
    
    @staticmethod
    def create_empty_chart(title, message="No data available"):
        """Create an empty chart with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=title,
            showlegend=False,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_cycle_time_trend(data=None, date_col=None, title="Procurement Cycle Time Trends"):
        """Create cycle time trend chart"""
        if data is None or len(data) == 0:
            return ProcurementVisualizations.create_empty_chart(
                title, "Upload procurement data to view cycle time trends"
            )
        
        fig = go.Figure()
        
        if date_col and date_col in data.index:
            # Use actual dates if available
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data.values,
                mode='lines+markers',
                name='Cycle Time (Days)',
                line=dict(color='#FF6B35', width=3),
                marker=dict(size=8)
            ))
            xaxis_title = "Date"
        else:
            # Use sequence if no dates
            fig.add_trace(go.Scatter(
                x=list(range(len(data))),
                y=data,
                mode='lines+markers',
                name='Cycle Time (Days)',
                line=dict(color='#FF6B35', width=3),
                marker=dict(size=8)
            ))
            xaxis_title = "Transaction Sequence"
        
        # Add trend line
        if len(data) > 2:
            z = np.polyfit(range(len(data)), data.values if hasattr(data, 'values') else data, 1)
            trend_line = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=list(range(len(data))),
                y=trend_line(range(len(data))),
                mode='lines',
                name='Trend',
                line=dict(color='rgba(255, 107, 53, 0.4)', dash='dash'),
                showlegend=True
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title="Days",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        return fig
    
    @staticmethod
    def create_bottleneck_heatmap(data=None, title="Process Bottleneck Analysis"):
        """Create bottleneck heatmap"""
        if data is None:
            return ProcurementVisualizations.create_empty_chart(
                title, "Upload workflow data to identify process bottlenecks"
            )
        
        # Create sample heatmap data based on actual data patterns
        categories = data.get('categories', ['Requisition', 'Approval', 'Contracting', 'Fulfillment'])
        time_periods = data.get('periods', ['Week 1', 'Week 2', 'Week 3', 'Week 4'])
        bottleneck_scores = data.get('scores', np.random.uniform(20, 100, (len(categories), len(time_periods))))
        
        fig = go.Figure(data=go.Heatmap(
            z=bottleneck_scores,
            x=time_periods,
            y=categories,
            colorscale='RdYlGn_r',
            colorbar=dict(title="Bottleneck Score"),
            text=[[f"{val:.0f}" for val in row] for row in bottleneck_scores],
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time Period",
            yaxis_title="Process Stage",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_payment_waterfall(data=None, title="Payment Cycle Waterfall"):
        """Create payment cycle waterfall chart"""
        if data is None:
            return ProcurementVisualizations.create_empty_chart(
                title, "Upload payment data to view waterfall analysis"
            )
        
        # Create waterfall chart from payment data
        stages = data.get('stages', ['Invoice Received', 'Approval', 'Processing', 'Payment'])
        values = data.get('values', [30, -5, -8, -12])  # Days at each stage
        cumulative = np.cumsum([0] + values[:-1])
        
        fig = go.Figure()
        
        # Add bars for each stage
        for i, (stage, value) in enumerate(zip(stages, values)):
            fig.add_trace(go.Bar(
                name=stage,
                x=[stage],
                y=[abs(value)],
                base=[cumulative[i] if value > 0 else cumulative[i] + value],
                marker_color='#FF6B35' if value > 0 else '#1f77b4',
                text=[f"{value} days"],
                textposition='auto'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Payment Process Stage",
            yaxis_title="Days",
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_benchmark_radar(data=None, title="Performance Benchmark Radar"):
        """Create benchmark radar chart"""
        if data is None:
            return ProcurementVisualizations.create_empty_chart(
                title, "Upload benchmark data to compare performance"
            )
        
        # Create radar chart from benchmark data
        categories = data.get('categories', ['Cycle Time', 'Cost Efficiency', 'Quality', 'Automation', 'Compliance'])
        current_scores = data.get('current', [75, 80, 85, 60, 90])
        benchmark_scores = data.get('benchmark', [85, 75, 80, 70, 85])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=current_scores + [current_scores[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            name='Current Performance',
            line_color='#FF6B35',
            fillcolor='rgba(255, 107, 53, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=benchmark_scores + [benchmark_scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Industry Benchmark',
            line_color='#1f77b4',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=title,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=500
        )
        return fig
    
    @staticmethod
    def create_predictive_alerts(data=None, title="Predictive Bottleneck Alerts"):
        """Create predictive alerts visualization"""
        if data is None:
            return ProcurementVisualizations.create_empty_chart(
                title, "Historical data required for predictive analysis"
            )
        
        # Create timeline chart with alert levels
        dates = data.get('dates', pd.date_range('2024-01-01', periods=30, freq='D'))
        risk_levels = data.get('risk_levels', np.random.choice([1, 2, 3, 4], size=30, p=[0.4, 0.3, 0.2, 0.1]))
        
        colors = {1: 'green', 2: 'yellow', 3: 'orange', 4: 'red'}
        risk_names = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Critical'}
        
        fig = go.Figure()
        
        for risk_level in [1, 2, 3, 4]:
            mask = risk_levels == risk_level
            if np.any(mask):
                fig.add_trace(go.Scatter(
                    x=dates[mask],
                    y=[risk_level] * np.sum(mask),
                    mode='markers',
                    name=f'{risk_names[risk_level]} Risk',
                    marker=dict(color=colors[risk_level], size=12),
                    text=[f'Risk Level: {risk_names[risk_level]}' for _ in range(np.sum(mask))],
                    hovertemplate='%{text}<br>Date: %{x}<extra></extra>'
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Risk Level",
            yaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4], ticktext=['Low', 'Medium', 'High', 'Critical']),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_roi_calculator_chart(savings_scenarios):
        """Create ROI calculator visualization"""
        if not savings_scenarios:
            return ProcurementVisualizations.create_empty_chart(
                "ROI Projections", "Configure scenarios to view ROI projections"
            )
        
        scenarios = list(savings_scenarios.keys())
        values = list(savings_scenarios.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=scenarios,
                y=values,
                marker_color='#FF6B35',
                text=[f"${v:,.0f}" for v in values],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Projected Annual Savings by Scenario",
            xaxis_title="Improvement Scenario",
            yaxis_title="Annual Savings ($)",
            showlegend=False
        )
        
        return fig
