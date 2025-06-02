"""
Reusable Question-Answer Intelligence Narrative Component
========================================================

A modular component that creates narrative-driven market intelligence through
real web crawling and AI analysis. Can be integrated into any Streamlit application.

Usage:
    from components.intelligence_narrative_component import IntelligenceNarrativeComponent
    
    narrative = IntelligenceNarrativeComponent(database_service)
    narrative.render_narrative_story(analysis_data, company_name)
"""

import streamlit as st
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class IntelligenceNarrativeComponent:
    """
    Reusable Question-Answer Intelligence Narrative Component
    
    Creates a 5-tab narrative structure that builds market intelligence
    through real web crawling and AI analysis:
    
    1. Who Are We Analyzing? - Strategic context and target definition
    2. What Technologies Matter? - Innovation landscape from web data
    3. Who Are The Key Players? - Supplier profiles from real websites
    4. How Do They Compare? - Competitive analytics and performance
    5. What Should We Do? - Actionable recommendations and next steps
    """
    
    def __init__(self, database_service=None, intelligence_dashboard=None):
        """
        Initialize the Intelligence Narrative Component
        
        Args:
            database_service: Service for data persistence (optional)
            intelligence_dashboard: Dashboard component for analytics (optional)
        """
        self.database_service = database_service
        self.intelligence_dashboard = intelligence_dashboard
    
    def render_narrative_story(self, analysis: Dict[str, Any], company_name: str):
        """
        Render the complete question-answer narrative as a flowing story
        
        Args:
            analysis: Complete analysis data with context and market segments
            company_name: Name of the target company being analyzed
        """
        # Single flowing narrative with 5 sections
        st.header(f"📊 Market Intelligence Story: {company_name}")
        
        # Section 1: Who Are We Analyzing?
        self._render_question_who_analyzing(analysis, company_name)
        st.divider()
        
        # Section 2: What Technologies Matter?
        self._render_question_what_technologies(analysis)
        st.divider()
        
        # Section 3: Who Are The Key Players?
        self._render_question_key_players(analysis)
        st.divider()
        
        # Section 4: How Do They Compare?
        self._render_question_how_compare(analysis)
        st.divider()
        
        # Section 5: What Should We Do?
        self._render_question_what_to_do(analysis, company_name)
    
    def _render_question_who_analyzing(self, analysis: Dict[str, Any], company_name: str):
        """❓ Who Are We Analyzing? - Target Company Intelligence Brief"""
        st.markdown("# ❓ Who Are We Analyzing?")
        
        context = analysis.get("context_analysis", {})
        industry = context.get("identified_industry", "Unknown Industry")
        
        # The Strategic Question
        st.markdown("## 🎯 The Strategic Question")
        st.info(f"**Who is {company_name} and what makes them strategically important in their market?**")
        
        # The Answer - Company Profile
        st.markdown("## 📊 The Answer")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### Company Profile: {company_name}")
            st.markdown(f"**Industry**: {industry}")
            
            # Strategic overview from context analysis
            overview = context.get("strategic_industry_overview", "")
            if overview:
                st.markdown("**Market Context**:")
                st.markdown(overview)
            
            # Market segments we're investigating
            segments = context.get("critical_supplier_market_segments", [])
            if segments:
                st.markdown("### 🔍 Critical Supplier Segments We're Investigating:")
                for i, segment in enumerate(segments, 1):
                    with st.expander(f"{i}. {segment.get('segment_name', 'Unknown Segment')}"):
                        st.markdown(f"**Why This Matters**: {segment.get('segment_definition_and_strategic_relevance', 'Strategic importance not defined')}")
                        keywords = segment.get('intelligence_gathering_keywords', [])
                        if keywords:
                            st.markdown("**Web Crawling Keywords**: " + ", ".join(keywords))
        
        with col2:
            st.markdown("### 📈 Analysis Scope")
            st.metric("Market Segments", len(segments) if segments else 0)
            
            # Data crawling status
            total_suppliers = 0
            segments_data = analysis.get("market_segments", {})
            for segment_data in segments_data.values():
                total_suppliers += len(segment_data.get("suppliers", []))
            
            st.metric("Suppliers Discovered", total_suppliers)
            
            if total_suppliers > 0:
                st.success("✅ Web crawling completed")
            else:
                st.warning("⏳ Ready for web intelligence gathering")
    
    def _render_question_what_technologies(self, analysis: Dict[str, Any]):
        """🔍 What Technologies Matter? - Technology Landscape Analysis"""
        st.markdown("# 🔍 What Technologies Matter?")
        
        # The Strategic Question
        st.markdown("## 🎯 The Strategic Question")
        st.info("**What are the critical technologies and innovation trends across the supplier ecosystem?**")
        
        # The Answer - Technology Analysis
        st.markdown("## 📊 The Answer")
        
        segments = analysis.get("market_segments", {})
        all_technologies = []
        innovation_by_segment = {}
        
        # Extract technology data from web-crawled supplier information
        for segment_name, segment_data in segments.items():
            suppliers = segment_data.get("suppliers", [])
            segment_technologies = []
            innovation_scores = []
            
            for supplier in suppliers:
                tech_diff = supplier.get("technological_differentiators", [])
                if isinstance(tech_diff, list):
                    all_technologies.extend(tech_diff)
                    segment_technologies.extend(tech_diff)
                
                innovation_score = supplier.get("innovation_index", 0)
                if innovation_score > 0:
                    innovation_scores.append(innovation_score)
            
            if innovation_scores:
                innovation_by_segment[segment_name] = {
                    'avg_innovation': sum(innovation_scores) / len(innovation_scores),
                    'technologies': segment_technologies,
                    'supplier_count': len(suppliers)
                }
        
        if all_technologies:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🚀 Technology Frequency Analysis")
                tech_counts = {}
                for tech in all_technologies:
                    tech_counts[tech] = tech_counts.get(tech, 0) + 1
                
                # Show top technologies discovered through web crawling
                sorted_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                
                for tech, count in sorted_tech:
                    st.markdown(f"**{tech}** - Found in {count} suppliers")
            
            with col2:
                st.markdown("### 📈 Innovation Index by Segment")
                for segment_name, data in innovation_by_segment.items():
                    avg_score = data['avg_innovation']
                    supplier_count = data['supplier_count']
                    st.metric(
                        f"{segment_name}", 
                        f"{avg_score:.1f}/10",
                        help=f"Based on {supplier_count} suppliers analyzed"
                    )
        else:
            st.info("🔄 Technology analysis will populate here as suppliers are discovered through web crawling")
    
    def _render_question_key_players(self, analysis: Dict[str, Any]):
        """🏢 Who Are The Key Players? - Supplier Profiles"""
        st.markdown("# 🏢 Who Are The Key Players?")
        
        # The Strategic Question
        st.markdown("## 🎯 The Strategic Question")
        st.info("**Who are the most strategic suppliers and what makes them valuable partners?**")
        
        # The Answer - Key Players Analysis
        st.markdown("## 📊 The Answer")
        
        segments = analysis.get("market_segments", {})
        all_suppliers = []
        
        # Compile all suppliers from web-crawled data
        for segment_name, segment_data in segments.items():
            suppliers = segment_data.get("suppliers", [])
            for supplier in suppliers:
                supplier["segment"] = segment_name
                all_suppliers.append(supplier)
        
        if all_suppliers:
            # Top Strategic Partners
            st.markdown("### 🌟 Top Strategic Partners (by Relevance Score)")
            
            top_suppliers = sorted(all_suppliers, 
                                 key=lambda x: x.get("relevance_score", 0), 
                                 reverse=True)[:5]
            
            for i, supplier in enumerate(top_suppliers):
                rank = i + 1
                name = supplier.get('company_name', 'Unknown Company')
                segment = supplier.get('segment', 'Unknown Segment')
                relevance = supplier.get('relevance_score', 0)
                innovation = supplier.get('innovation_index', 0)
                source_url = supplier.get('source_url', '')
                
                with st.expander(f"#{rank} {name} ({segment}) - Relevance: {relevance:.1f}/10"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Relevance Score", f"{relevance:.1f}/10")
                    with col2:
                        st.metric("Innovation Index", f"{innovation:.1f}/10")
                    with col3:
                        st.metric("ESG Rating", f"{supplier.get('esg_rating', 0):.1f}/10")
                    
                    # Web-crawled company overview
                    overview = supplier.get('overview', 'Overview not available from web crawling')
                    st.markdown(f"**Company Overview** (from web analysis): {overview}")
                    
                    # Source information
                    if source_url:
                        st.markdown(f"**Data Source**: [Company Website]({source_url})")
                    
                    # Key technologies (from web crawling)
                    tech_diff = supplier.get('technological_differentiators', [])
                    if tech_diff and isinstance(tech_diff, list):
                        st.markdown("**Key Technologies**: " + ", ".join(tech_diff))
            
            # Segment breakdown
            st.markdown("### 📊 Suppliers by Market Segment")
            for segment_name, segment_data in segments.items():
                suppliers = segment_data.get("suppliers", [])
                urls_processed = segment_data.get("total_urls_processed", 0)
                
                if suppliers:
                    with st.expander(f"{segment_name} - {len(suppliers)} suppliers ({urls_processed} URLs analyzed)"):
                        for supplier in suppliers:
                            name = supplier.get('company_name', 'Unknown')
                            domain = supplier.get('domain', 'Unknown domain')
                            st.markdown(f"• **{name}** ({domain})")
        else:
            st.info("🔄 Supplier profiles will appear here as web intelligence gathering discovers key players")
    
    def _render_question_how_compare(self, analysis: Dict[str, Any]):
        """📊 How Do They Compare? - Competitive Analysis"""
        st.markdown("# 📊 How Do They Compare?")
        
        # The Strategic Question
        st.markdown("## 🎯 The Strategic Question")
        st.info("**How do suppliers compare across key performance metrics and what patterns emerge?**")
        
        # The Answer - Comparative Analysis
        st.markdown("## 📊 The Answer")
        
        segments = analysis.get("market_segments", {})
        all_suppliers = []
        
        # Compile all suppliers for comparison
        for segment_name, segment_data in segments.items():
            suppliers = segment_data.get("suppliers", [])
            for supplier in suppliers:
                supplier["segment"] = segment_name
                all_suppliers.append(supplier)
        
        if all_suppliers and len(all_suppliers) >= 2:
            # Comparative metrics visualization
            import plotly.express as px
            import plotly.graph_objects as go
            import pandas as pd
            
            # Prepare comparison data
            comparison_data = []
            for supplier in all_suppliers:
                comparison_data.append({
                    'Company': supplier.get('company_name', 'Unknown')[:20],
                    'Segment': supplier.get('segment', 'Unknown'),
                    'Relevance': supplier.get('relevance_score', 0),
                    'Innovation': supplier.get('innovation_index', 0),
                    'ESG': supplier.get('esg_rating', 0),
                    'Tech_Count': len(supplier.get('technological_differentiators', [])),
                    'Overall_Score': (supplier.get('relevance_score', 0) + 
                                    supplier.get('innovation_index', 0) + 
                                    supplier.get('esg_rating', 0)) / 3
                })
            
            df = pd.DataFrame(comparison_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance comparison radar chart
                st.markdown("### 🎯 Performance Comparison Matrix")
                
                fig = px.scatter(
                    df,
                    x='Innovation',
                    y='ESG',
                    size='Relevance',
                    color='Segment',
                    hover_name='Company',
                    title="Innovation vs ESG Performance",
                    labels={'Innovation': 'Innovation Index', 'ESG': 'ESG Rating'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Overall rankings
                st.markdown("### 🏆 Overall Performance Rankings")
                
                top_performers = df.nlargest(10, 'Overall_Score')
                fig = px.bar(
                    top_performers,
                    x='Overall_Score',
                    y='Company',
                    color='Overall_Score',
                    orientation='h',
                    title="Top Performers (Overall Score)",
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Key insights from comparison
            st.markdown("### 💡 Key Competitive Insights")
            
            # Calculate insights
            avg_innovation = df['Innovation'].mean()
            avg_esg = df['ESG'].mean()
            innovation_leader = df.loc[df['Innovation'].idxmax()]
            esg_leader = df.loc[df['ESG'].idxmax()]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🚀 Innovation Leaders**")
                high_innovation = df[df['Innovation'] >= avg_innovation]
                for _, supplier in high_innovation.head(3).iterrows():
                    st.markdown(f"• {supplier['Company']} ({supplier['Innovation']:.1f}/10)")
            
            with col2:
                st.markdown("**🌱 ESG Champions**")
                high_esg = df[df['ESG'] >= avg_esg]
                for _, supplier in high_esg.head(3).iterrows():
                    st.markdown(f"• {supplier['Company']} ({supplier['ESG']:.1f}/10)")
            
            with col3:
                st.markdown("**⚖️ Balanced Performers**")
                balanced = df[(df['Innovation'] >= avg_innovation) & (df['ESG'] >= avg_esg)]
                for _, supplier in balanced.head(3).iterrows():
                    st.markdown(f"• {supplier['Company']} (Balanced)")
        
        else:
            st.info("🔄 Comparative analysis will show here when multiple suppliers are analyzed")
    
    def _render_question_what_to_do(self, analysis: Dict[str, Any], company_name: str):
        """💼 What Should We Do? - Strategic Recommendations"""
        st.markdown("# 💼 What Should We Do?")
        
        # The Strategic Question
        st.markdown("## 🎯 The Strategic Question")
        st.info(f"**What are the immediate next steps and strategic recommendations for {company_name}'s supplier strategy?**")
        
        # The Answer - Strategic Recommendations
        st.markdown("## 📊 The Answer")
        
        # Get executive summary if available
        executive_summary = analysis.get("executive_summary", "")
        
        if executive_summary:
            st.markdown("### 📋 Executive Summary & Recommendations")
            st.markdown(executive_summary)
        
        # Generate tactical recommendations based on analysis
        segments = analysis.get("market_segments", {})
        all_suppliers = []
        
        for segment_data in segments.values():
            all_suppliers.extend(segment_data.get("suppliers", []))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Immediate Actions")
            
            if all_suppliers:
                # Find top performers
                top_suppliers = sorted(all_suppliers, 
                                     key=lambda x: x.get("relevance_score", 0), 
                                     reverse=True)[:3]
                
                st.markdown("**1. Priority Supplier Engagement**")
                for supplier in top_suppliers:
                    name = supplier.get('company_name', 'Unknown')
                    score = supplier.get('relevance_score', 0)
                    st.markdown(f"• Contact {name} (Relevance: {score:.1f}/10)")
                
                # Technology focus areas
                all_tech = []
                for supplier in all_suppliers:
                    all_tech.extend(supplier.get('technological_differentiators', []))
                
                if all_tech:
                    from collections import Counter
                    top_tech = Counter(all_tech).most_common(3)
                    
                    st.markdown("**2. Technology Focus Areas**")
                    for tech, count in top_tech:
                        st.markdown(f"• {tech} ({count} suppliers)")
            else:
                st.markdown("**1. Begin Supplier Discovery**")
                st.markdown("• Execute web intelligence gathering")
                st.markdown("• Analyze market segments identified")
                st.markdown("• Build supplier database")
        
        with col2:
            st.markdown("### 📈 Strategic Initiatives")
            
            st.markdown("**1. Supplier Portfolio Optimization**")
            st.markdown("• Diversify across market segments")
            st.markdown("• Balance innovation vs stability")
            st.markdown("• Enhance ESG compliance")
            
            st.markdown("**2. Technology Roadmap Alignment**")
            st.markdown("• Map supplier capabilities to needs")
            st.markdown("• Identify innovation partners")
            st.markdown("• Plan technology adoption timeline")
            
            st.markdown("**3. Risk Management**")
            st.markdown("• Assess supplier dependencies")
            st.markdown("• Develop backup alternatives")
            st.markdown("• Monitor market dynamics")
        
        # Next steps checklist
        st.markdown("### ✅ Next Steps Checklist")
        
        next_steps = [
            "Review and validate top supplier recommendations",
            "Initiate contact with priority suppliers",
            "Conduct detailed capability assessments",
            "Develop supplier evaluation framework",
            "Create supplier onboarding timeline",
            "Establish ongoing market monitoring"
        ]
        
        for i, step in enumerate(next_steps, 1):
            st.checkbox(f"{i}. {step}", key=f"step_{i}")