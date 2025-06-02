import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MarketIntelligenceStoryComponent:
    """Component for creating elegant visual narratives of market intelligence data"""
    
    def render_intelligence_story(self, analysis_data: Dict[str, Any]):
        """Render the complete market intelligence story with elegant visuals"""
        if not analysis_data:
            st.warning("No analysis data available for story visualization")
            return
        
        context = analysis_data.get("context_analysis", {})
        company_name = context.get("context_company_name", "Unknown Company")
        
        # Story Header
        st.markdown(f"""
        # 📊 Market Intelligence Story: {company_name}
        ### *Strategic Insights & Supplier Ecosystem Analysis*
        """)
        
        # Executive Dashboard Overview
        self._render_executive_overview(analysis_data)
        
        # Market Landscape Visualization
        self._render_market_landscape(analysis_data)
        
        # Supplier Excellence Analysis
        self._render_supplier_excellence_story(analysis_data)
        
        # Innovation & Technology Trends
        self._render_innovation_trends(analysis_data)
        
        # Strategic Opportunities Dashboard
        self._render_strategic_opportunities(analysis_data)
        
        # Market Intelligence Timeline
        self._render_intelligence_timeline(analysis_data)
    
    def _render_executive_overview(self, analysis_data: Dict[str, Any]):
        """Render executive overview with key metrics"""
        st.subheader("🎯 Executive Intelligence Overview")
        
        # Extract key metrics
        market_segments = analysis_data.get("market_segments", {})
        total_suppliers = sum(len(segment.get("suppliers", [])) for segment in market_segments.values())
        total_insights = sum(len(segment.get("market_insights", [])) for segment in market_segments.values())
        
        # Calculate quality scores
        avg_relevance = 0
        avg_innovation = 0
        avg_esg = 0
        supplier_count = 0
        
        for segment in market_segments.values():
            for supplier in segment.get("suppliers", []):
                avg_relevance += supplier.get("relevance_score", 0)
                avg_innovation += supplier.get("innovation_index", 0)
                avg_esg += supplier.get("esg_rating", 0)
                supplier_count += 1
        
        if supplier_count > 0:
            avg_relevance /= supplier_count
            avg_innovation /= supplier_count
            avg_esg /= supplier_count
        
        # Key metrics display
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Market Segments Analyzed",
                len(market_segments),
                help="Number of strategic supplier segments identified"
            )
        
        with col2:
            st.metric(
                "Suppliers Profiled",
                total_suppliers,
                help="Total potential suppliers discovered and analyzed"
            )
        
        with col3:
            st.metric(
                "Market Insights",
                total_insights,
                help="Number of market intelligence insights gathered"
            )
        
        with col4:
            st.metric(
                "Avg. Relevance Score",
                f"{avg_relevance:.1f}/10",
                help="Average relevance score across all suppliers"
            )
        
        with col5:
            st.metric(
                "Innovation Index",
                f"{avg_innovation:.1f}/10",
                help="Average innovation rating of discovered suppliers"
            )
    
    def _render_market_landscape(self, analysis_data: Dict[str, Any]):
        """Render market landscape visualization"""
        st.subheader("🌍 Market Landscape Overview")
        
        market_segments = analysis_data.get("market_segments", {})
        
        if not market_segments:
            st.info("No market segment data available")
            return
        
        # Prepare data for visualization
        segment_data = []
        for segment_name, segment_info in market_segments.items():
            suppliers = segment_info.get("suppliers", [])
            insights = segment_info.get("market_insights", [])
            
            # Calculate segment metrics
            if suppliers:
                avg_relevance = sum(s.get("relevance_score", 0) for s in suppliers) / len(suppliers)
                avg_innovation = sum(s.get("innovation_index", 0) for s in suppliers) / len(suppliers)
                avg_esg = sum(s.get("esg_rating", 0) for s in suppliers) / len(suppliers)
            else:
                avg_relevance = avg_innovation = avg_esg = 0
            
            segment_data.append({
                "Segment": segment_name[:30] + "..." if len(segment_name) > 30 else segment_name,
                "Suppliers": len(suppliers),
                "Market Insights": len(insights),
                "Avg Relevance": avg_relevance,
                "Avg Innovation": avg_innovation,
                "Avg ESG": avg_esg,
                "Total Score": (avg_relevance + avg_innovation + avg_esg) / 3
            })
        
        df = pd.DataFrame(segment_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Market segment activity bubble chart
            fig = px.scatter(
                df,
                x="Suppliers",
                y="Market Insights",
                size="Total Score",
                color="Avg Innovation",
                hover_name="Segment",
                title="Market Segment Activity Overview",
                labels={
                    "Suppliers": "Number of Suppliers",
                    "Market Insights": "Market Intelligence Points",
                    "Avg Innovation": "Innovation Score"
                },
                color_continuous_scale="viridis"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Segment performance radar
            if len(df) > 0:
                fig = go.Figure()
                
                for _, row in df.iterrows():
                    fig.add_trace(go.Scatterpolar(
                        r=[row["Avg Relevance"], row["Avg Innovation"], row["Avg ESG"]],
                        theta=["Relevance", "Innovation", "ESG"],
                        fill='toself',
                        name=row["Segment"][:20],
                        opacity=0.6
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 10]
                        )),
                    title="Segment Performance Profile",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_supplier_excellence_story(self, analysis_data: Dict[str, Any]):
        """Render supplier excellence analysis"""
        st.subheader("🏆 Supplier Excellence Analysis")
        
        market_segments = analysis_data.get("market_segments", {})
        
        # Collect all suppliers
        all_suppliers = []
        for segment_name, segment_info in market_segments.items():
            for supplier in segment_info.get("suppliers", []):
                supplier_copy = supplier.copy()
                supplier_copy["segment"] = segment_name
                all_suppliers.append(supplier_copy)
        
        if not all_suppliers:
            st.info("No supplier data available for analysis")
            return
        
        # Create supplier excellence DataFrame
        supplier_df = pd.DataFrame([{
            "Company": s.get("company_name", "Unknown")[:25],
            "Segment": s.get("segment", "")[:20],
            "Relevance": s.get("relevance_score", 0),
            "Innovation": s.get("innovation_index", 0),
            "ESG": s.get("esg_rating", 0),
            "Excellence Score": (s.get("relevance_score", 0) + s.get("innovation_index", 0) + s.get("esg_rating", 0)) / 3,
            "Technologies": len(s.get("technological_differentiators", [])),
            "Clients": len(s.get("market_traction", {}).get("key_clients", []))
        } for s in all_suppliers])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top performers
            top_suppliers = supplier_df.nlargest(10, "Excellence Score")
            
            fig = px.bar(
                top_suppliers,
                x="Excellence Score",
                y="Company",
                color="Excellence Score",
                orientation="h",
                title="🌟 Top 10 Supplier Excellence Rankings",
                color_continuous_scale="viridis"
            )
            fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Excellence distribution
            fig = px.histogram(
                supplier_df,
                x="Excellence Score",
                nbins=20,
                title="Supplier Excellence Score Distribution",
                labels={"Excellence Score": "Excellence Score (0-10)", "count": "Number of Suppliers"}
            )
            fig.add_vline(x=supplier_df["Excellence Score"].mean(), line_dash="dash", 
                         annotation_text=f"Average: {supplier_df['Excellence Score'].mean():.1f}")
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance matrix
            fig = px.scatter(
                supplier_df,
                x="Innovation",
                y="ESG",
                size="Relevance",
                color="Segment",
                hover_name="Company",
                title="Innovation vs ESG Performance Matrix",
                labels={"Innovation": "Innovation Index", "ESG": "ESG Rating"}
            )
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_innovation_trends(self, analysis_data: Dict[str, Any]):
        """Render innovation and technology trends"""
        st.subheader("🚀 Innovation & Technology Trends")
        
        market_segments = analysis_data.get("market_segments", {})
        
        # Extract technology keywords
        all_technologies = []
        tech_by_segment = {}
        
        for segment_name, segment_info in market_segments.items():
            segment_techs = []
            for supplier in segment_info.get("suppliers", []):
                techs = supplier.get("technological_differentiators", [])
                all_technologies.extend(techs)
                segment_techs.extend(techs)
            tech_by_segment[segment_name] = segment_techs
        
        if all_technologies:
            # Count technology frequencies
            from collections import Counter
            tech_counts = Counter(all_technologies)
            top_technologies = dict(tech_counts.most_common(15))
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Technology frequency chart
                tech_df = pd.DataFrame([{"Technology": tech, "Frequency": freq} for tech, freq in top_technologies.items()])
                
                fig = px.bar(
                    tech_df,
                    x="Frequency",
                    y="Technology",
                    orientation="h",
                    title="🔬 Most Mentioned Technologies",
                    color="Frequency",
                    color_continuous_scale="plasma"
                )
                fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Technology distribution by segment
                segment_tech_data = []
                for segment, techs in tech_by_segment.items():
                    tech_count = Counter(techs)
                    for tech, count in tech_count.most_common(5):
                        segment_tech_data.append({
                            "Segment": segment[:20],
                            "Technology": tech[:30],
                            "Count": count
                        })
                
                if segment_tech_data:
                    seg_tech_df = pd.DataFrame(segment_tech_data)
                    
                    fig = px.sunburst(
                        seg_tech_df,
                        path=["Segment", "Technology"],
                        values="Count",
                        title="Technology Distribution by Market Segment"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No technology data available for trend analysis")
    
    def _render_strategic_opportunities(self, analysis_data: Dict[str, Any]):
        """Render strategic opportunities dashboard"""
        st.subheader("💡 Strategic Opportunities Dashboard")
        
        market_segments = analysis_data.get("market_segments", {})
        
        # Calculate opportunity metrics
        opportunities = []
        for segment_name, segment_info in market_segments.items():
            suppliers = segment_info.get("suppliers", [])
            insights = segment_info.get("market_insights", [])
            
            if suppliers:
                high_innovation = sum(1 for s in suppliers if s.get("innovation_index", 0) >= 7)
                high_relevance = sum(1 for s in suppliers if s.get("relevance_score", 0) >= 7)
                strong_esg = sum(1 for s in suppliers if s.get("esg_rating", 0) >= 7)
                
                opportunity_score = (high_innovation + high_relevance + strong_esg) / len(suppliers) * 10
                
                opportunities.append({
                    "Segment": segment_name,
                    "Opportunity Score": opportunity_score,
                    "High Innovation Suppliers": high_innovation,
                    "High Relevance Suppliers": high_relevance,
                    "Strong ESG Suppliers": strong_esg,
                    "Total Suppliers": len(suppliers),
                    "Market Insights": len(insights)
                })
        
        if opportunities:
            opp_df = pd.DataFrame(opportunities)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Opportunity matrix
                fig = px.scatter(
                    opp_df,
                    x="Total Suppliers",
                    y="Opportunity Score",
                    size="Market Insights",
                    color="High Innovation Suppliers",
                    hover_name="Segment",
                    title="📈 Strategic Opportunity Matrix",
                    labels={
                        "Total Suppliers": "Market Depth (Supplier Count)",
                        "Opportunity Score": "Opportunity Score (0-10)",
                        "High Innovation Suppliers": "Innovation Leaders"
                    }
                )
                fig.add_hline(y=opp_df["Opportunity Score"].mean(), line_dash="dash", 
                             annotation_text="Average Opportunity")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Opportunity ranking
                opp_ranked = opp_df.nlargest(len(opp_df), "Opportunity Score")
                
                fig = px.bar(
                    opp_ranked,
                    x="Opportunity Score",
                    y="Segment",
                    orientation="h",
                    title="🎯 Market Segment Opportunity Ranking",
                    color="Opportunity Score",
                    color_continuous_scale="viridis"
                )
                fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_intelligence_timeline(self, analysis_data: Dict[str, Any]):
        """Render market intelligence timeline and insights"""
        st.subheader("📅 Market Intelligence Timeline")
        
        # Analysis metadata
        analysis_timestamp = analysis_data.get("analysis_timestamp")
        context = analysis_data.get("context_analysis", {})
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create a timeline visualization
            if analysis_timestamp:
                analysis_date = datetime.fromisoformat(analysis_timestamp.replace('Z', '+00:00'))
                
                # Create timeline data
                timeline_data = [
                    {"Phase": "Context Analysis", "Start": analysis_date, "Duration": 2},
                    {"Phase": "Market Research", "Start": analysis_date + timedelta(minutes=2), "Duration": 15},
                    {"Phase": "Content Analysis", "Start": analysis_date + timedelta(minutes=17), "Duration": 20},
                    {"Phase": "AI Processing", "Start": analysis_date + timedelta(minutes=37), "Duration": 8},
                    {"Phase": "Report Generation", "Start": analysis_date + timedelta(minutes=45), "Duration": 3}
                ]
                
                fig = go.Figure()
                
                for i, phase in enumerate(timeline_data):
                    fig.add_trace(go.Scatter(
                        x=[phase["Start"], phase["Start"] + timedelta(minutes=phase["Duration"])],
                        y=[i, i],
                        mode='lines+markers',
                        name=phase["Phase"],
                        line=dict(width=10),
                        marker=dict(size=8)
                    ))
                
                fig.update_layout(
                    title="Analysis Processing Timeline",
                    xaxis_title="Time",
                    yaxis_title="Processing Phase",
                    yaxis=dict(tickmode='array', tickvals=list(range(len(timeline_data))), 
                              ticktext=[p["Phase"] for p in timeline_data]),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Analysis summary stats
            st.markdown("### 📊 Analysis Summary")
            
            if analysis_timestamp:
                st.write(f"**Generated:** {analysis_timestamp[:19]}")
            
            industry = context.get("identified_industry", "Unknown")
            st.write(f"**Industry:** {industry}")
            
            segments_count = len(analysis_data.get("market_segments", {}))
            st.write(f"**Segments:** {segments_count}")
            
            total_suppliers = sum(len(s.get("suppliers", [])) for s in analysis_data.get("market_segments", {}).values())
            st.write(f"**Suppliers:** {total_suppliers}")
            
            # Data freshness indicator
            if analysis_timestamp:
                age = datetime.now() - datetime.fromisoformat(analysis_timestamp.replace('Z', '+00:00'))
                if age.days == 0:
                    freshness = "🟢 Fresh (Today)"
                elif age.days <= 7:
                    freshness = f"🟡 Recent ({age.days} days old)"
                else:
                    freshness = f"🔴 Aging ({age.days} days old)"
                st.write(f"**Data Freshness:** {freshness}")