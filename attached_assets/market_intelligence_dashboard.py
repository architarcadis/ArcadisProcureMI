import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from services.database_service import DatabaseService

logger = logging.getLogger(__name__)

class MarketIntelligenceDashboard:
    """Enhanced Market Intelligence Dashboard with incremental data visualization"""
    
    def __init__(self, database_service: DatabaseService):
        self.db = database_service
    
    def render_market_intelligence_tab(self):
        """Render the comprehensive Market Intelligence tab with incremental data"""
        st.header("🔍 Market Intelligence Analytics")
        
        # Get all historical data for trend analysis
        companies = self.db.list_analyzed_companies()
        
        if not companies:
            self._render_empty_state()
            return
        
        # Overview metrics
        self._render_overview_metrics()
        
        # Market trends over time
        self._render_market_trends()
        
        # Industry distribution and insights
        self._render_industry_analysis()
        
        # Supplier ecosystem evolution
        self._render_supplier_ecosystem()
        
        # Technology trends tracking
        self._render_technology_trends()
        
        # Competitive intelligence
        self._render_competitive_intelligence()
    
    def _render_empty_state(self):
        """Render empty state when no data is available"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ## 🎯 Market Intelligence Analytics
            
            ### Start Building Your Intelligence Story
            
            This dashboard will show comprehensive market intelligence trends and insights as you analyze companies.
            
            **What you'll see here:**
            - 📈 Market trends over time
            - 🏭 Industry distribution analysis  
            - 🤝 Supplier ecosystem evolution
            - 🚀 Technology innovation tracking
            - ⚔️ Competitive intelligence insights
            
            **Get Started:** Use the sidebar to analyze your first company and watch the intelligence story unfold!
            """)
    
    def _render_overview_metrics(self):
        """Render high-level overview metrics"""
        st.subheader("📊 Intelligence Overview")
        
        # Get comprehensive stats
        stats = self.db.get_storage_stats()
        
        # Calculate additional metrics
        session = self.db.get_session()
        try:
            # Get analysis dates for trend calculation
            from services.database_service import CompanyAnalysis, SupplierProfile
            
            analyses = session.query(CompanyAnalysis).all()
            suppliers = session.query(SupplierProfile).all()
            
            # Calculate metrics
            total_companies = len(analyses)
            total_suppliers = len(suppliers)
            avg_suppliers_per_company = total_suppliers / total_companies if total_companies > 0 else 0
            
            # Innovation metrics
            high_innovation_suppliers = sum(1 for s in suppliers if s.innovation_index and s.innovation_index >= 7)
            innovation_rate = (high_innovation_suppliers / total_suppliers * 100) if total_suppliers > 0 else 0
            
            # Recent activity
            recent_analyses = sum(1 for a in analyses 
                                if a.created_at and a.created_at >= datetime.utcnow() - timedelta(days=7))
            
        finally:
            session.close()
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Companies Analyzed",
                total_companies,
                delta=f"+{recent_analyses} this week" if recent_analyses > 0 else None,
                help="Total companies analyzed in the platform"
            )
        
        with col2:
            st.metric(
                "Suppliers Discovered",
                total_suppliers,
                help="Total supplier profiles generated"
            )
        
        with col3:
            st.metric(
                "Avg Suppliers/Company",
                f"{avg_suppliers_per_company:.1f}",
                help="Average number of suppliers discovered per company"
            )
        
        with col4:
            st.metric(
                "Innovation Rate",
                f"{innovation_rate:.1f}%",
                help="Percentage of suppliers with high innovation scores (7+)"
            )
        
        with col5:
            st.metric(
                "Database Type",
                "PostgreSQL",
                help="Professional database backend for reliable data storage"
            )
    
    def _render_market_trends(self):
        """Render market trends over time"""
        st.subheader("📈 Market Intelligence Trends")
        
        session = self.db.get_session()
        try:
            from services.database_service import CompanyAnalysis, SupplierProfile
            
            # Get analysis timeline data
            analyses = session.query(CompanyAnalysis).order_by(CompanyAnalysis.created_at).all()
            
            if len(analyses) < 2:
                st.info("Need at least 2 company analyses to show trends. Analyze more companies to see trend visualization.")
                return
            
            # Prepare timeline data
            timeline_data = []
            cumulative_companies = 0
            cumulative_suppliers = 0
            
            for analysis in analyses:
                cumulative_companies += 1
                
                # Count suppliers for this analysis
                suppliers_count = session.query(SupplierProfile).filter(
                    SupplierProfile.company_name == analysis.company_name
                ).count()
                cumulative_suppliers += suppliers_count
                
                timeline_data.append({
                    'Date': analysis.created_at,
                    'Company': analysis.company_name,
                    'Industry': analysis.industry or 'Unknown',
                    'Cumulative_Companies': cumulative_companies,
                    'Cumulative_Suppliers': cumulative_suppliers,
                    'Suppliers_This_Analysis': suppliers_count
                })
            
            df = pd.DataFrame(timeline_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Cumulative growth chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df['Cumulative_Companies'],
                    mode='lines+markers',
                    name='Companies Analyzed',
                    line=dict(color='#00d4aa', width=3),
                    yaxis='y1'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df['Cumulative_Suppliers'],
                    mode='lines+markers',
                    name='Suppliers Discovered',
                    line=dict(color='#ff6b6b', width=3),
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title="📊 Cumulative Intelligence Growth",
                    xaxis_title="Date",
                    yaxis=dict(title="Companies", side="left", color="#00d4aa"),
                    yaxis2=dict(title="Suppliers", side="right", overlaying="y", color="#ff6b6b"),
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Analysis velocity chart
                fig = px.bar(
                    df,
                    x='Company',
                    y='Suppliers_This_Analysis',
                    color='Industry',
                    title="🚀 Supplier Discovery per Analysis",
                    labels={'Suppliers_This_Analysis': 'Suppliers Discovered', 'Company': 'Company Analysis'}
                )
                fig.update_layout(height=400, xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        finally:
            session.close()
    
    def _render_industry_analysis(self):
        """Render industry distribution and insights"""
        st.subheader("🏭 Industry Intelligence Distribution")
        
        session = self.db.get_session()
        try:
            from services.database_service import CompanyAnalysis, SupplierProfile
            
            # Get industry distribution
            analyses = session.query(CompanyAnalysis).all()
            industry_data = {}
            
            for analysis in analyses:
                industry = analysis.industry or 'Unknown'
                if industry not in industry_data:
                    industry_data[industry] = {
                        'companies': 0,
                        'suppliers': 0,
                        'avg_innovation': 0,
                        'avg_relevance': 0
                    }
                
                industry_data[industry]['companies'] += 1
                
                # Get suppliers for this company
                suppliers = session.query(SupplierProfile).filter(
                    SupplierProfile.company_name == analysis.company_name
                ).all()
                
                industry_data[industry]['suppliers'] += len(suppliers)
                
                if suppliers:
                    innovation_scores = [s.innovation_index for s in suppliers if s.innovation_index]
                    relevance_scores = [s.relevance_score for s in suppliers if s.relevance_score]
                    
                    if innovation_scores:
                        industry_data[industry]['avg_innovation'] = sum(innovation_scores) / len(innovation_scores)
                    if relevance_scores:
                        industry_data[industry]['avg_relevance'] = sum(relevance_scores) / len(relevance_scores)
            
            if not industry_data:
                st.info("No industry data available yet.")
                return
            
            # Create industry analysis charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Industry distribution pie chart
                industries = list(industry_data.keys())
                company_counts = [industry_data[ind]['companies'] for ind in industries]
                
                fig = px.pie(
                    values=company_counts,
                    names=industries,
                    title="🌍 Industry Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Industry performance matrix
                industry_df = pd.DataFrame([
                    {
                        'Industry': industry,
                        'Companies': data['companies'],
                        'Avg_Suppliers': data['suppliers'] / data['companies'] if data['companies'] > 0 else 0,
                        'Innovation_Score': data['avg_innovation'],
                        'Relevance_Score': data['avg_relevance']
                    }
                    for industry, data in industry_data.items()
                ])
                
                fig = px.scatter(
                    industry_df,
                    x='Innovation_Score',
                    y='Relevance_Score',
                    size='Avg_Suppliers',
                    color='Industry',
                    hover_name='Industry',
                    title="⚡ Industry Performance Matrix",
                    labels={
                        'Innovation_Score': 'Average Innovation Score',
                        'Relevance_Score': 'Average Relevance Score'
                    }
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        finally:
            session.close()
    
    def _render_supplier_ecosystem(self):
        """Render supplier ecosystem evolution"""
        st.subheader("🤝 Supplier Ecosystem Evolution")
        
        session = self.db.get_session()
        try:
            from services.database_service import SupplierProfile, MarketSegment
            
            # Get all suppliers with their segments
            suppliers = session.query(SupplierProfile).all()
            
            if not suppliers:
                st.info("No supplier data available yet.")
                return
            
            # Analyze supplier ecosystem
            segment_analysis = {}
            excellence_distribution = {'Low (0-4)': 0, 'Medium (4-7)': 0, 'High (7-10)': 0}
            
            for supplier in suppliers:
                segment = supplier.segment_name
                if segment not in segment_analysis:
                    segment_analysis[segment] = {
                        'count': 0,
                        'avg_innovation': 0,
                        'avg_relevance': 0,
                        'avg_esg': 0,
                        'innovation_scores': [],
                        'relevance_scores': [],
                        'esg_scores': []
                    }
                
                segment_analysis[segment]['count'] += 1
                
                if supplier.innovation_index:
                    segment_analysis[segment]['innovation_scores'].append(supplier.innovation_index)
                if supplier.relevance_score:
                    segment_analysis[segment]['relevance_scores'].append(supplier.relevance_score)
                if supplier.esg_rating:
                    segment_analysis[segment]['esg_scores'].append(supplier.esg_rating)
                
                # Excellence distribution
                avg_score = 0
                score_count = 0
                if supplier.innovation_index:
                    avg_score += supplier.innovation_index
                    score_count += 1
                if supplier.relevance_score:
                    avg_score += supplier.relevance_score
                    score_count += 1
                if supplier.esg_rating:
                    avg_score += supplier.esg_rating
                    score_count += 1
                
                if score_count > 0:
                    avg_score /= score_count
                    if avg_score >= 7:
                        excellence_distribution['High (7-10)'] += 1
                    elif avg_score >= 4:
                        excellence_distribution['Medium (4-7)'] += 1
                    else:
                        excellence_distribution['Low (0-4)'] += 1
            
            # Calculate averages
            for segment_data in segment_analysis.values():
                if segment_data['innovation_scores']:
                    segment_data['avg_innovation'] = sum(segment_data['innovation_scores']) / len(segment_data['innovation_scores'])
                if segment_data['relevance_scores']:
                    segment_data['avg_relevance'] = sum(segment_data['relevance_scores']) / len(segment_data['relevance_scores'])
                if segment_data['esg_scores']:
                    segment_data['avg_esg'] = sum(segment_data['esg_scores']) / len(segment_data['esg_scores'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Supplier excellence distribution
                fig = px.bar(
                    x=list(excellence_distribution.keys()),
                    y=list(excellence_distribution.values()),
                    title="🏆 Supplier Excellence Distribution",
                    labels={'x': 'Excellence Level', 'y': 'Number of Suppliers'},
                    color=list(excellence_distribution.values()),
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Market segment performance
                if segment_analysis:
                    segment_df = pd.DataFrame([
                        {
                            'Segment': segment[:30] + '...' if len(segment) > 30 else segment,
                            'Supplier_Count': data['count'],
                            'Innovation': data['avg_innovation'],
                            'Relevance': data['avg_relevance'],
                            'ESG': data['avg_esg']
                        }
                        for segment, data in segment_analysis.items()
                    ])
                    
                    fig = px.scatter(
                        segment_df,
                        x='Innovation',
                        y='Relevance',
                        size='Supplier_Count',
                        color='ESG',
                        hover_name='Segment',
                        title="📊 Market Segment Performance",
                        color_continuous_scale='viridis'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        
        finally:
            session.close()
    
    def _render_technology_trends(self):
        """Render technology trends tracking"""
        st.subheader("🚀 Technology Innovation Tracking")
        
        session = self.db.get_session()
        try:
            from services.database_service import SupplierProfile
            
            suppliers = session.query(SupplierProfile).all()
            
            if not suppliers:
                st.info("No technology data available yet.")
                return
            
            # Extract and analyze technologies
            all_technologies = []
            tech_by_company = {}
            
            for supplier in suppliers:
                if supplier.technological_differentiators:
                    techs = supplier.technological_differentiators
                    all_technologies.extend(techs)
                    
                    company = supplier.company_name
                    if company not in tech_by_company:
                        tech_by_company[company] = []
                    tech_by_company[company].extend(techs)
            
            if not all_technologies:
                st.info("No technology data extracted yet.")
                return
            
            # Count technology frequencies
            from collections import Counter
            tech_counts = Counter(all_technologies)
            top_technologies = dict(tech_counts.most_common(15))
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Technology popularity
                tech_df = pd.DataFrame([
                    {'Technology': tech, 'Frequency': freq}
                    for tech, freq in top_technologies.items()
                ])
                
                fig = px.bar(
                    tech_df,
                    x='Frequency',
                    y='Technology',
                    orientation='h',
                    title="🔬 Most Mentioned Technologies",
                    color='Frequency',
                    color_continuous_scale='plasma'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Technology diversity by company
                company_tech_diversity = {
                    company: len(set(techs))
                    for company, techs in tech_by_company.items()
                }
                
                diversity_df = pd.DataFrame([
                    {'Company': company[:20] + '...' if len(company) > 20 else company, 
                     'Tech_Diversity': diversity}
                    for company, diversity in company_tech_diversity.items()
                ])
                
                fig = px.bar(
                    diversity_df.nlargest(10, 'Tech_Diversity'),
                    x='Tech_Diversity',
                    y='Company',
                    orientation='h',
                    title="🌟 Technology Diversity Leaders",
                    color='Tech_Diversity',
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        finally:
            session.close()
    
    def _render_competitive_intelligence(self):
        """Render competitive intelligence insights"""
        st.subheader("⚔️ Competitive Intelligence Insights")
        
        session = self.db.get_session()
        try:
            from services.database_service import SupplierProfile, CompanyAnalysis
            
            # Get top performing suppliers across all analyses
            suppliers = session.query(SupplierProfile).all()
            
            if not suppliers:
                st.info("No competitive intelligence data available yet.")
                return
            
            # Calculate composite scores and rankings
            supplier_rankings = []
            for supplier in suppliers:
                innovation = supplier.innovation_index or 0
                relevance = supplier.relevance_score or 0
                esg = supplier.esg_rating or 0
                
                composite_score = (innovation + relevance + esg) / 3
                
                supplier_rankings.append({
                    'Supplier': supplier.supplier_name,
                    'Company_Context': supplier.company_name,
                    'Segment': supplier.segment_name,
                    'Innovation': innovation,
                    'Relevance': relevance,
                    'ESG': esg,
                    'Composite_Score': composite_score,
                    'Domain': supplier.domain or ''
                })
            
            rankings_df = pd.DataFrame(supplier_rankings)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top performers global ranking
                top_performers = rankings_df.nlargest(15, 'Composite_Score')
                
                fig = px.bar(
                    top_performers,
                    x='Composite_Score',
                    y='Supplier',
                    orientation='h',
                    color='Composite_Score',
                    title="🏆 Global Supplier Excellence Rankings",
                    color_continuous_scale='viridis',
                    hover_data=['Company_Context', 'Segment']
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance distribution across dimensions
                performance_data = []
                for _, row in rankings_df.iterrows():
                    performance_data.extend([
                        {'Supplier': row['Supplier'], 'Metric': 'Innovation', 'Score': row['Innovation']},
                        {'Supplier': row['Supplier'], 'Metric': 'Relevance', 'Score': row['Relevance']},
                        {'Supplier': row['Supplier'], 'Metric': 'ESG', 'Score': row['ESG']}
                    ])
                
                performance_df = pd.DataFrame(performance_data)
                top_suppliers = rankings_df.nlargest(10, 'Composite_Score')['Supplier'].tolist()
                performance_filtered = performance_df[performance_df['Supplier'].isin(top_suppliers)]
                
                fig = px.box(
                    performance_filtered,
                    x='Metric',
                    y='Score',
                    title="📊 Top Performers Score Distribution",
                    color='Metric'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Intelligence summary
                st.markdown("### 🎯 Key Intelligence Insights")
                
                if not rankings_df.empty:
                    avg_innovation = rankings_df['Innovation'].mean()
                    avg_relevance = rankings_df['Relevance'].mean()
                    avg_esg = rankings_df['ESG'].mean()
                    top_performer = rankings_df.loc[rankings_df['Composite_Score'].idxmax()]
                    
                    st.markdown(f"""
                    - **Market Leader**: {top_performer['Supplier']} (Score: {top_performer['Composite_Score']:.1f})
                    - **Average Innovation**: {avg_innovation:.1f}/10
                    - **Average Relevance**: {avg_relevance:.1f}/10  
                    - **Average ESG**: {avg_esg:.1f}/10
                    - **Total Suppliers Analyzed**: {len(rankings_df)}
                    """)
        
        finally:
            session.close()