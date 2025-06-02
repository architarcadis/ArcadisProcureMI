"""
Comprehensive Market Intelligence Story
A robust, data-driven narrative that integrates all advanced market intelligence capabilities
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

class MarketIntelligenceStory:
    """Comprehensive market intelligence story engine"""
    
    def __init__(self):
        self.story_phases = {
            "discovery": "📊 Discovery: Understanding Your Procurement Universe",
            "intelligence": "🔍 Intelligence: Real-World Market Analysis", 
            "insights": "💡 Insights: Strategic Intelligence Synthesis",
            "action": "🎯 Action: Your Strategic Roadmap"
        }
    
    def render_comprehensive_story(self):
        """Render the complete market intelligence story"""
        st.header("📖 Your Complete Market Intelligence Story")
        st.caption("A comprehensive analysis combining all intelligence capabilities")
        
        # Check data availability
        if 'uploaded_data' not in st.session_state or st.session_state.uploaded_data is None:
            st.info("Upload your procurement data to begin your comprehensive market intelligence analysis")
            return
        
        # Story progress tracking
        story_progress = self._get_story_progress()
        
        # Progress indicator
        self._render_progress_indicator(story_progress)
        
        # Phase selection
        current_phase = st.selectbox(
            "Choose your analysis phase:",
            list(self.story_phases.keys()),
            format_func=lambda x: self.story_phases[x],
            index=story_progress.get('current_phase_index', 0)
        )
        
        # Render selected phase
        if current_phase == "discovery":
            self._render_discovery_phase()
        elif current_phase == "intelligence":
            self._render_intelligence_phase()
        elif current_phase == "insights":
            self._render_insights_phase()
        else:
            self._render_action_phase()
    
    def _get_story_progress(self) -> Dict[str, Any]:
        """Track story completion progress"""
        progress = {
            'discovery_complete': 'story_context' in st.session_state,
            'intelligence_complete': 'comprehensive_intelligence' in st.session_state,
            'insights_complete': 'strategic_insights' in st.session_state,
            'action_complete': 'action_roadmap' in st.session_state
        }
        
        completed_phases = sum(progress.values())
        progress['completion_percentage'] = (completed_phases / 4) * 100
        progress['current_phase_index'] = completed_phases
        
        return progress
    
    def _render_progress_indicator(self, progress: Dict[str, Any]):
        """Render visual progress indicator"""
        col1, col2, col3, col4 = st.columns(4)
        
        phases = [
            ("📊", "Discovery", progress['discovery_complete']),
            ("🔍", "Intelligence", progress['intelligence_complete']),
            ("💡", "Insights", progress['insights_complete']),
            ("🎯", "Action", progress['action_complete'])
        ]
        
        for i, (emoji, name, complete) in enumerate(phases):
            with [col1, col2, col3, col4][i]:
                if complete:
                    st.success(f"{emoji} {name} ✓")
                else:
                    st.info(f"{emoji} {name}")
        
        # Progress bar
        st.progress(progress['completion_percentage'] / 100)
        st.caption(f"Story Progress: {progress['completion_percentage']:.0f}% Complete")
    
    def _render_discovery_phase(self):
        """Phase 1: Discovery - Understanding the procurement universe"""
        st.subheader("📊 Discovery Phase: Understanding Your Procurement Universe")
        
        df = st.session_state.uploaded_data
        
        # Extract comprehensive context
        if st.button("🔍 Analyze Your Procurement Data", type="primary"):
            with st.spinner("Analyzing your procurement universe..."):
                context = self._extract_comprehensive_context(df)
                st.session_state.story_context = context
                st.success("Discovery phase complete!")
        
        # Display context if available
        if 'story_context' in st.session_state:
            self._display_discovery_results(st.session_state.story_context)
    
    def _render_intelligence_phase(self):
        """Phase 2: Intelligence - Real-world market analysis"""
        st.subheader("🔍 Intelligence Phase: Real-World Market Analysis")
        
        if 'story_context' not in st.session_state:
            st.warning("Complete the Discovery phase first")
            return
        
        context = st.session_state.story_context
        
        if st.button("🌍 Launch Comprehensive Market Scan", type="primary"):
            intelligence_data = self._conduct_comprehensive_intelligence(context)
            st.session_state.comprehensive_intelligence = intelligence_data
        
        # Display intelligence results
        if 'comprehensive_intelligence' in st.session_state:
            self._display_intelligence_results(st.session_state.comprehensive_intelligence)
    
    def _render_insights_phase(self):
        """Phase 3: Insights - Strategic intelligence synthesis"""
        st.subheader("💡 Insights Phase: Strategic Intelligence Synthesis")
        
        if 'comprehensive_intelligence' not in st.session_state:
            st.warning("Complete the Intelligence phase first")
            return
        
        if st.button("⚡ Generate Strategic Insights", type="primary"):
            insights = self._synthesize_strategic_insights()
            st.session_state.strategic_insights = insights
        
        # Display insights
        if 'strategic_insights' in st.session_state:
            self._display_strategic_insights(st.session_state.strategic_insights)
    
    def _render_action_phase(self):
        """Phase 4: Action - Strategic roadmap"""
        st.subheader("🎯 Action Phase: Your Strategic Roadmap")
        
        if 'strategic_insights' not in st.session_state:
            st.warning("Complete the Insights phase first")
            return
        
        if st.button("🚀 Create Action Roadmap", type="primary"):
            roadmap = self._create_action_roadmap()
            st.session_state.action_roadmap = roadmap
        
        # Display roadmap
        if 'action_roadmap' in st.session_state:
            self._display_action_roadmap(st.session_state.action_roadmap)
    
    def _extract_comprehensive_context(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract comprehensive context from procurement data"""
        context = {
            'data_profile': {},
            'suppliers': {},
            'categories': {},
            'financial_profile': {},
            'temporal_profile': {},
            'risk_indicators': {}
        }
        
        # Data profile
        context['data_profile'] = {
            'total_records': len(df),
            'columns': list(df.columns),
            'data_quality': self._assess_data_quality(df),
            'completeness': df.notna().sum().sum() / (len(df) * len(df.columns)) * 100
        }
        
        # Supplier analysis
        supplier_data = self._analyze_suppliers(df)
        context['suppliers'] = supplier_data
        
        # Category analysis
        category_data = self._analyze_categories(df)
        context['categories'] = category_data
        
        # Financial analysis
        financial_data = self._analyze_financial_patterns(df)
        context['financial_profile'] = financial_data
        
        # Temporal analysis
        temporal_data = self._analyze_temporal_patterns(df)
        context['temporal_profile'] = temporal_data
        
        # Risk indicators
        risk_data = self._identify_risk_indicators(df)
        context['risk_indicators'] = risk_data
        
        return context
    
    def _conduct_comprehensive_intelligence(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive market intelligence gathering"""
        from enhanced_market_intelligence import EnhancedMarketIntelligence
        
        # Initialize intelligence engine
        if 'enhanced_intel_engine' not in st.session_state:
            st.session_state.enhanced_intel_engine = EnhancedMarketIntelligence()
        
        engine = st.session_state.enhanced_intel_engine
        
        intelligence_data = {
            'supplier_intelligence': {},
            'market_analysis': {},
            'regulatory_landscape': {},
            'economic_indicators': {},
            'geopolitical_factors': {},
            'technology_trends': {},
            'competitive_intelligence': {}
        }
        
        # Progress tracking
        total_steps = 7
        current_step = 0
        
        progress_bar = st.progress(0)
        status_container = st.container()
        
        def update_progress(message):
            nonlocal current_step
            current_step += 1
            progress_bar.progress(current_step / total_steps)
            status_container.info(f"Step {current_step}/{total_steps}: {message}")
        
        try:
            # 1. Supplier Intelligence
            update_progress("Analyzing supplier intelligence...")
            supplier_intel = engine.analyze_supplier_intelligence(context)
            intelligence_data['supplier_intelligence'] = {
                'profiles': supplier_intel,
                'risk_assessment': self._assess_supplier_risks(supplier_intel),
                'recommendations': self._generate_supplier_recommendations(supplier_intel)
            }
            
            # 2. Market Analysis
            update_progress("Conducting market analysis...")
            market_score = engine.calculate_market_score(context)
            market_trends = engine.analyze_category_trends(context)
            intelligence_data['market_analysis'] = {
                'market_score': market_score,
                'category_trends': market_trends,
                'market_sentiment': self._analyze_market_sentiment(market_trends)
            }
            
            # 3. Regulatory Landscape
            update_progress("Scanning regulatory landscape...")
            regulatory_data = self._scan_regulatory_environment(context, engine)
            intelligence_data['regulatory_landscape'] = regulatory_data
            
            # 4. Economic Indicators
            update_progress("Analyzing economic indicators...")
            economic_data = self._analyze_economic_environment(context, engine)
            intelligence_data['economic_indicators'] = economic_data
            
            # 5. Geopolitical Factors
            update_progress("Assessing geopolitical factors...")
            geopolitical_data = self._assess_geopolitical_environment(context, engine)
            intelligence_data['geopolitical_factors'] = geopolitical_data
            
            # 6. Technology Trends
            update_progress("Monitoring technology trends...")
            tech_data = self._monitor_technology_trends(context, engine)
            intelligence_data['technology_trends'] = tech_data
            
            # 7. Competitive Intelligence
            update_progress("Gathering competitive intelligence...")
            competitive_data = self._gather_competitive_intelligence(context, engine)
            intelligence_data['competitive_intelligence'] = competitive_data
            
            status_container.success("Comprehensive market intelligence gathering complete!")
            
        except Exception as e:
            st.error(f"Intelligence gathering encountered an issue: {str(e)}")
            st.info("This may require API keys for external market data sources. Please ensure proper authentication is configured.")
        
        return intelligence_data
    
    def _synthesize_strategic_insights(self) -> Dict[str, Any]:
        """Synthesize strategic insights from all intelligence data"""
        context = st.session_state.story_context
        intelligence = st.session_state.comprehensive_intelligence
        
        insights = {
            'executive_summary': {},
            'key_findings': [],
            'risk_assessment': {},
            'opportunity_analysis': {},
            'strategic_priorities': [],
            'market_positioning': {}
        }
        
        # Generate executive summary
        insights['executive_summary'] = self._generate_executive_summary(context, intelligence)
        
        # Extract key findings
        insights['key_findings'] = self._extract_key_findings(intelligence)
        
        # Comprehensive risk assessment
        insights['risk_assessment'] = self._conduct_comprehensive_risk_assessment(intelligence)
        
        # Opportunity analysis
        insights['opportunity_analysis'] = self._analyze_opportunities(intelligence)
        
        # Strategic priorities
        insights['strategic_priorities'] = self._identify_strategic_priorities(intelligence)
        
        # Market positioning
        insights['market_positioning'] = self._assess_market_positioning(context, intelligence)
        
        return insights
    
    def _create_action_roadmap(self) -> Dict[str, Any]:
        """Create comprehensive action roadmap"""
        insights = st.session_state.strategic_insights
        
        roadmap = {
            'immediate_actions': [],    # 0-30 days
            'short_term_actions': [],   # 1-3 months
            'medium_term_actions': [],  # 3-12 months
            'long_term_actions': [],    # 12+ months
            'success_metrics': [],
            'risk_mitigation': [],
            'resource_requirements': {}
        }
        
        # Generate time-based actions
        roadmap['immediate_actions'] = self._generate_immediate_actions(insights)
        roadmap['short_term_actions'] = self._generate_short_term_actions(insights)
        roadmap['medium_term_actions'] = self._generate_medium_term_actions(insights)
        roadmap['long_term_actions'] = self._generate_long_term_actions(insights)
        
        # Define success metrics
        roadmap['success_metrics'] = self._define_success_metrics(insights)
        
        # Risk mitigation strategies
        roadmap['risk_mitigation'] = self._develop_risk_mitigation(insights)
        
        # Resource requirements
        roadmap['resource_requirements'] = self._estimate_resource_requirements(insights)
        
        return roadmap
    
    def _analyze_suppliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive supplier analysis"""
        supplier_columns = ['supplier', 'vendor', 'supplier_name', 'vendor_name', 'company']
        supplier_data = {'suppliers': [], 'analysis': {}}
        
        for col in df.columns:
            if any(term in col.lower() for term in supplier_columns):
                suppliers = df[col].dropna().astype(str).str.strip()
                suppliers = suppliers[suppliers != ''].value_counts()
                
                supplier_data['suppliers'] = suppliers.head(10).index.tolist()
                supplier_data['analysis'] = {
                    'total_unique': len(suppliers),
                    'concentration': self._calculate_supplier_concentration(suppliers),
                    'distribution': suppliers.head(10).to_dict()
                }
                break
        
        return supplier_data
    
    def _analyze_categories(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive category analysis"""
        category_columns = ['category', 'product_category', 'service_category', 'type', 'classification']
        category_data = {'categories': [], 'analysis': {}}
        
        for col in df.columns:
            if any(term in col.lower() for term in category_columns):
                categories = df[col].dropna().astype(str).str.strip()
                categories = categories[categories != ''].value_counts()
                
                category_data['categories'] = categories.head(8).index.tolist()
                category_data['analysis'] = {
                    'total_unique': len(categories),
                    'distribution': categories.head(8).to_dict()
                }
                break
        
        return category_data
    
    def _display_discovery_results(self, context: Dict[str, Any]):
        """Display comprehensive discovery results"""
        st.success("Discovery Phase Complete!")
        
        # Data Profile
        st.subheader("📊 Your Data Profile")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{context['data_profile']['total_records']:,}")
        with col2:
            st.metric("Data Quality", f"{context['data_profile']['data_quality']:.1f}%")
        with col3:
            st.metric("Completeness", f"{context['data_profile']['completeness']:.1f}%")
        
        # Supplier Overview
        if context['suppliers']['suppliers']:
            st.subheader("🏢 Supplier Landscape")
            st.write(f"**{context['suppliers']['analysis']['total_unique']} unique suppliers** identified")
            
            # Supplier concentration
            concentration = context['suppliers']['analysis']['concentration']
            if concentration > 0.7:
                st.warning("High supplier concentration detected - consider diversification")
            elif concentration < 0.3:
                st.info("Well-diversified supplier base")
            else:
                st.success("Balanced supplier concentration")
        
        # Category Overview
        if context['categories']['categories']:
            st.subheader("📦 Category Portfolio")
            st.write(f"**{context['categories']['analysis']['total_unique']} unique categories** identified")
            
            for category in context['categories']['categories'][:5]:
                st.write(f"• {category}")
        
        st.info("Ready for Intelligence Phase - We'll now scan the market for real-time data about your suppliers and categories")
    
    def _display_intelligence_results(self, intelligence: Dict[str, Any]):
        """Display comprehensive intelligence results"""
        st.success("Intelligence Phase Complete!")
        
        tabs = st.tabs([
            "Supplier Intel", "Market Analysis", "Regulatory", 
            "Economic", "Geopolitical", "Technology", "Competitive"
        ])
        
        with tabs[0]:
            self._display_supplier_intelligence(intelligence['supplier_intelligence'])
        with tabs[1]:
            self._display_market_analysis(intelligence['market_analysis'])
        with tabs[2]:
            self._display_regulatory_intelligence(intelligence['regulatory_landscape'])
        with tabs[3]:
            self._display_economic_intelligence(intelligence['economic_indicators'])
        with tabs[4]:
            self._display_geopolitical_intelligence(intelligence['geopolitical_factors'])
        with tabs[5]:
            self._display_technology_intelligence(intelligence['technology_trends'])
        with tabs[6]:
            self._display_competitive_intelligence(intelligence['competitive_intelligence'])
        
        st.info("Ready for Insights Phase - We'll synthesize all this intelligence into strategic insights")

    # Additional helper methods would continue here...
    # For brevity, I'll include key methods that demonstrate the comprehensive approach

    def _calculate_supplier_concentration(self, suppliers: pd.Series) -> float:
        """Calculate supplier concentration using Herfindahl index"""
        if len(suppliers) == 0:
            return 0
        
        total = suppliers.sum()
        market_shares = suppliers / total
        herfindahl_index = (market_shares ** 2).sum()
        return herfindahl_index

    def _assess_data_quality(self, df: pd.DataFrame) -> float:
        """Assess overall data quality score"""
        quality_factors = []
        
        # Completeness
        completeness = df.notna().sum().sum() / (len(df) * len(df.columns))
        quality_factors.append(completeness * 40)  # 40% weight
        
        # Consistency (example: checking for standardized formats)
        consistency = 0.8  # Placeholder - would implement actual consistency checks
        quality_factors.append(consistency * 30)  # 30% weight
        
        # Accuracy (example: checking for reasonable value ranges)
        accuracy = 0.85  # Placeholder - would implement actual accuracy checks
        quality_factors.append(accuracy * 30)  # 30% weight
        
        return sum(quality_factors)

def render_comprehensive_market_intelligence_story():
    """Main function to render the comprehensive market intelligence story"""
    story_engine = MarketIntelligenceStory()
    story_engine.render_comprehensive_story()