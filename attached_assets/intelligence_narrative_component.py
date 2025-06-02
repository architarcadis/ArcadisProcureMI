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
        
        # Use the intelligence dashboard if available, otherwise show basic comparison
        if self.intelligence_dashboard:
            self.intelligence_dashboard.render_market_intelligence_tab()
        else:
            self._render_basic_comparison(analysis)
    
    def _render_basic_comparison(self, analysis: Dict[str, Any]):
        """Render basic supplier comparison when dashboard not available"""
        segments = analysis.get("market_segments", {})
        all_suppliers = []
        
        for segment_data in segments.values():
            all_suppliers.extend(segment_data.get("suppliers", []))
        
        if all_suppliers:
            # Performance metrics comparison
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🎯 Relevance Leaders")
                top_relevance = sorted(all_suppliers, key=lambda x: x.get("relevance_score", 0), reverse=True)[:3]
                for i, supplier in enumerate(top_relevance, 1):
                    st.markdown(f"{i}. {supplier.get('company_name', 'Unknown')} ({supplier.get('relevance_score', 0):.1f}/10)")
            
            with col2:
                st.markdown("### 🚀 Innovation Leaders")
                top_innovation = sorted(all_suppliers, key=lambda x: x.get("innovation_index", 0), reverse=True)[:3]
                for i, supplier in enumerate(top_innovation, 1):
                    st.markdown(f"{i}. {supplier.get('company_name', 'Unknown')} ({supplier.get('innovation_index', 0):.1f}/10)")
            
            with col3:
                st.markdown("### 🌱 ESG Leaders")
                top_esg = sorted(all_suppliers, key=lambda x: x.get("esg_rating", 0), reverse=True)[:3]
                for i, supplier in enumerate(top_esg, 1):
                    st.markdown(f"{i}. {supplier.get('company_name', 'Unknown')} ({supplier.get('esg_rating', 0):.1f}/10)")
        else:
            st.info("🔄 Comparison analytics will appear here as supplier data is gathered")
    
    def _render_question_what_to_do(self, analysis: Dict[str, Any], company_name: str):
        """💡 What Should We Do? - Strategic Recommendations"""
        st.markdown("# 💡 What Should We Do?")
        
        # The Strategic Question
        st.markdown("## 🎯 The Strategic Question")
        st.info("**Based on our web intelligence gathering, what are the actionable next steps?**")
        
        # The Answer - Strategic Recommendations
        st.markdown("## 📊 The Answer")
        
        segments = analysis.get("market_segments", {})
        all_suppliers = []
        for segment_data in segments.values():
            all_suppliers.extend(segment_data.get("suppliers", []))
        
        if all_suppliers:
            # Priority Actions
            st.markdown("### 🎯 Priority Actions")
            
            # Find top performers
            top_relevance = max(all_suppliers, key=lambda x: x.get("relevance_score", 0))
            top_innovation = max(all_suppliers, key=lambda x: x.get("innovation_index", 0))
            top_esg = max(all_suppliers, key=lambda x: x.get("esg_rating", 0))
            
            action_items = [
                f"**1. Immediate Partnership Discussion**: Contact {top_relevance.get('company_name')} (Highest relevance: {top_relevance.get('relevance_score', 0):.1f}/10)",
                f"**2. Innovation Collaboration**: Explore R&D partnership with {top_innovation.get('company_name')} (Innovation leader: {top_innovation.get('innovation_index', 0):.1f}/10)",
                f"**3. ESG Alignment**: Consider sustainability partnership with {top_esg.get('company_name')} (ESG rating: {top_esg.get('esg_rating', 0):.1f}/10)",
                f"**4. Market Coverage**: Our analysis covers {len(segments)} market segments with {len(all_suppliers)} suppliers total"
            ]
            
            for action in action_items:
                st.markdown(action)
            
            # Next Steps
            st.markdown("### 🚀 Next Steps")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Immediate Actions (This Week)")
                immediate_actions = [
                    "Download and review detailed supplier profiles",
                    "Initiate contact with top 3 strategic suppliers",
                    "Schedule supplier capability assessments"
                ]
                for action in immediate_actions:
                    st.markdown(f"• {action}")
            
            with col2:
                st.markdown("#### Strategic Actions (Next Month)")
                strategic_actions = [
                    "Conduct deeper due diligence on key suppliers",
                    "Develop partnership framework and criteria",
                    "Re-run analysis to track market changes"
                ]
                for action in strategic_actions:
                    st.markdown(f"• {action}")
            
            # Export and Follow-up
            st.markdown("### 📤 Take Action")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Export Full Report"):
                    if self.database_service and hasattr(self.database_service, 'export_company_data_csv'):
                        csv_data = self.database_service.export_company_data_csv(company_name)
                        if csv_data:
                            st.download_button(
                                "Download Intelligence Report",
                                csv_data,
                                f"{company_name}_market_intelligence.csv",
                                "text/csv"
                            )
                    else:
                        st.info("Export functionality requires database service integration")
            
            with col2:
                if st.button("🔄 Update Analysis"):
                    st.info("Run a fresh analysis to capture latest market intelligence")
            
            with col3:
                if st.button("📧 Generate Summary"):
                    executive_summary = analysis.get("executive_summary", "")
                    if executive_summary:
                        st.text_area("Executive Summary for Sharing:", executive_summary, height=100)
        else:
            st.info("🔄 Strategic recommendations will appear here once web intelligence gathering is complete")


# Example usage function
def create_intelligence_narrative(database_service=None, intelligence_dashboard=None):
    """
    Factory function to create an Intelligence Narrative Component
    
    Args:
        database_service: Optional database service for data persistence
        intelligence_dashboard: Optional dashboard component for analytics
    
    Returns:
        IntelligenceNarrativeComponent: Ready-to-use narrative component
    """
    return IntelligenceNarrativeComponent(database_service, intelligence_dashboard)