import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class SupplierProfileComponent:
    """Component for detailed supplier profile display and analysis"""
    
    def render_all_profiles(self, suppliers: List[Dict[str, Any]]):
        """Render detailed profiles for all suppliers"""
        if not suppliers:
            st.warning("No supplier profiles available")
            return
        
        st.subheader("🏢 Detailed Supplier Profiles")
        
        # Supplier selector
        supplier_names = [s.get("company_name", f"Supplier {i+1}") for i, s in enumerate(suppliers)]
        
        selected_supplier = st.selectbox(
            "Select Supplier for Detailed View:",
            supplier_names,
            key="supplier_profile_selector"
        )
        
        if selected_supplier:
            # Find selected supplier data
            supplier_data = None
            for supplier in suppliers:
                if supplier.get("company_name") == selected_supplier:
                    supplier_data = supplier
                    break
            
            if supplier_data:
                self.render_single_profile(supplier_data)
        
        # Comparative analysis
        st.divider()
        self._render_comparative_analysis(suppliers)
    
    def render_single_profile(self, supplier: Dict[str, Any]):
        """Render detailed profile for a single supplier"""
        company_name = supplier.get("company_name", "Unknown Company")
        
        # Header with key metrics
        self._render_profile_header(supplier)
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Overview", 
            "🔬 Technology", 
            "🤝 Market Traction", 
            "🌱 ESG Profile", 
            "📊 Analytics"
        ])
        
        with tab1:
            self._render_overview_tab(supplier)
        
        with tab2:
            self._render_technology_tab(supplier)
        
        with tab3:
            self._render_market_traction_tab(supplier)
        
        with tab4:
            self._render_esg_tab(supplier)
        
        with tab5:
            self._render_analytics_tab(supplier)
    
    def _render_profile_header(self, supplier: Dict[str, Any]):
        """Render profile header with key metrics"""
        company_name = supplier.get("company_name", "Unknown Company")
        
        # Company header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.title(f"🏢 {company_name}")
            
            # Key positioning
            positioning = supplier.get("market_positioning", "")
            if positioning:
                st.markdown(f"*{positioning}*")
            
            # Website link
            domain = supplier.get("domain", "")
            source_url = supplier.get("source_url", "")
            if source_url:
                st.markdown(f"🌐 **Website:** [{domain}]({source_url})")
        
        with col2:
            # Key metrics
            relevance = supplier.get("relevance_score", 0)
            innovation = supplier.get("innovation_index", 0)
            esg = supplier.get("esg_rating", 0)
            
            st.metric("Relevance Score", f"{relevance}/10")
            st.metric("Innovation Index", f"{innovation}/10")
            st.metric("ESG Rating", f"{esg}/10")
    
    def _render_overview_tab(self, supplier: Dict[str, Any]):
        """Render overview tab content"""
        # Company overview
        overview = supplier.get("overview", "")
        if overview:
            st.subheader("📝 Company Overview")
            st.write(overview)
        
        # Products and services
        products = supplier.get("products_services", [])
        if products:
            st.subheader("🛠️ Products & Services")
            for product in products:
                st.write(f"• {product}")
        
        # Market positioning
        positioning = supplier.get("market_positioning", "")
        if positioning:
            st.subheader("🎯 Market Positioning")
            st.write(positioning)
    
    def _render_technology_tab(self, supplier: Dict[str, Any]):
        """Render technology tab content"""
        # Technological differentiators
        tech_diff = supplier.get("technological_differentiators", [])
        if tech_diff:
            st.subheader("🔬 Key Technologies")
            
            # Display as cards
            cols = st.columns(min(3, len(tech_diff)))
            for i, tech in enumerate(tech_diff):
                with cols[i % 3]:
                    st.info(f"🔧 {tech}")
        
        # Innovation indicators
        innovation = supplier.get("innovation_indicators", {})
        if innovation:
            st.subheader("💡 Innovation Indicators")
            
            col1, col2 = st.columns(2)
            
            with col1:
                rd_focus = innovation.get("rd_focus", "")
                if rd_focus:
                    st.write("**R&D Focus:**")
                    st.write(rd_focus)
                
                new_products = innovation.get("new_products", "")
                if new_products:
                    st.write("**Recent Products:**")
                    st.write(new_products)
            
            with col2:
                patents = innovation.get("patents_mentioned", "")
                if patents:
                    st.write("**Patents & IP:**")
                    st.write(patents)
        
        # Technology visualization
        if tech_diff:
            self._render_technology_chart(tech_diff)
    
    def _render_technology_chart(self, technologies: List[str]):
        """Render technology capabilities chart"""
        if not technologies:
            return
        
        # Create a simple radar chart for technology areas
        categories = [tech[:20] + "..." if len(tech) > 20 else tech for tech in technologies[:6]]
        values = [8, 7, 9, 6, 8, 7][:len(categories)]  # Placeholder scores
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Technology Strength'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            title="Technology Capabilities Profile",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_market_traction_tab(self, supplier: Dict[str, Any]):
        """Render market traction tab content"""
        traction = supplier.get("market_traction", {})
        
        if not traction:
            st.info("No market traction data available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Key clients
            clients = traction.get("key_clients", [])
            if clients:
                st.subheader("🤝 Key Clients")
                for client in clients:
                    st.write(f"• {client}")
            
            # Partnerships
            partnerships = traction.get("partnerships", [])
            if partnerships:
                st.subheader("🤝 Strategic Partnerships")
                for partnership in partnerships:
                    st.write(f"• {partnership}")
        
        with col2:
            # Case studies
            case_studies = traction.get("case_studies", [])
            if case_studies:
                st.subheader("📚 Success Stories")
                for i, case_study in enumerate(case_studies):
                    with st.expander(f"Case Study {i+1}"):
                        st.write(case_study)
    
    def _render_esg_tab(self, supplier: Dict[str, Any]):
        """Render ESG profile tab content"""
        esg = supplier.get("esg_profile", {})
        
        if not esg:
            st.info("No ESG data available")
            return
        
        # ESG overview chart
        esg_scores = []
        esg_categories = []
        
        environmental = esg.get("environmental", "")
        social = esg.get("social", "")
        governance = esg.get("governance", "")
        
        if environmental:
            esg_scores.append(7)  # Placeholder score
            esg_categories.append("Environmental")
        
        if social:
            esg_scores.append(6)  # Placeholder score
            esg_categories.append("Social")
        
        if governance:
            esg_scores.append(8)  # Placeholder score
            esg_categories.append("Governance")
        
        if esg_scores:
            fig = px.bar(
                x=esg_categories,
                y=esg_scores,
                title="ESG Performance Profile",
                labels={"x": "ESG Category", "y": "Score (1-10)"},
                color=esg_scores,
                color_continuous_scale="viridis"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed ESG information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if environmental:
                st.subheader("🌱 Environmental")
                st.write(environmental)
        
        with col2:
            if social:
                st.subheader("👥 Social")
                st.write(social)
        
        with col3:
            if governance:
                st.subheader("⚖️ Governance")
                st.write(governance)
    
    def _render_analytics_tab(self, supplier: Dict[str, Any]):
        """Render analytics and insights tab"""
        st.subheader("📊 Supplier Analytics")
        
        # Score breakdown
        relevance = supplier.get("relevance_score", 0)
        innovation = supplier.get("innovation_index", 0)
        esg = supplier.get("esg_rating", 0)
        
        # Scores visualization
        scores_df = pd.DataFrame({
            'Metric': ['Relevance', 'Innovation', 'ESG'],
            'Score': [relevance, innovation, esg],
            'Max': [10, 10, 10]
        })
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            name='Score',
            x=scores_df['Metric'],
            y=scores_df['Score'],
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
        ))
        
        # Add max line
        fig.add_trace(go.Scatter(
            x=scores_df['Metric'],
            y=scores_df['Max'],
            mode='lines+markers',
            name='Maximum',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title="Performance Metrics",
            yaxis_title="Score",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Strengths and areas for improvement
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💪 Key Strengths")
            strengths = []
            
            if relevance >= 7:
                strengths.append("High market relevance")
            if innovation >= 7:
                strengths.append("Strong innovation profile")
            if esg >= 7:
                strengths.append("Good ESG practices")
            
            # Add based on available data
            if supplier.get("technological_differentiators"):
                strengths.append("Diverse technology portfolio")
            if supplier.get("market_traction", {}).get("key_clients"):
                strengths.append("Established client base")
            
            for strength in strengths:
                st.write(f"✅ {strength}")
        
        with col2:
            st.subheader("🎯 Areas to Explore")
            areas = []
            
            if relevance < 6:
                areas.append("Market relevance assessment")
            if innovation < 6:
                areas.append("Innovation capabilities")
            if esg < 6:
                areas.append("ESG practices and reporting")
            
            if not supplier.get("market_traction", {}).get("case_studies"):
                areas.append("Success stories and case studies")
            
            for area in areas:
                st.write(f"🔍 {area}")
    
    def _render_comparative_analysis(self, suppliers: List[Dict[str, Any]]):
        """Render comparative analysis across all suppliers"""
        if len(suppliers) < 2:
            return
        
        st.subheader("⚖️ Comparative Analysis")
        
        # Create comparison DataFrame
        comparison_data = []
        for supplier in suppliers:
            comparison_data.append({
                "Company": supplier.get("company_name", "Unknown")[:20],
                "Relevance": supplier.get("relevance_score", 0),
                "Innovation": supplier.get("innovation_index", 0),
                "ESG": supplier.get("esg_rating", 0),
                "Tech Count": len(supplier.get("technological_differentiators", [])),
                "Client Count": len(supplier.get("market_traction", {}).get("key_clients", []))
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Comparative charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Scores comparison
            fig = px.bar(
                df.melt(id_vars=["Company"], 
                       value_vars=["Relevance", "Innovation", "ESG"],
                       var_name="Metric", value_name="Score"),
                x="Company",
                y="Score",
                color="Metric",
                title="Supplier Scores Comparison",
                barmode="group"
            )
            fig.update_layout(height=400)
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Portfolio size comparison
            fig = px.scatter(
                df,
                x="Tech Count",
                y="Client Count",
                size="Relevance",
                hover_name="Company",
                title="Portfolio Size: Technologies vs Clients",
                labels={"Tech Count": "Technology Areas", "Client Count": "Key Clients"}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Ranking table
        st.subheader("🏆 Supplier Rankings")
        
        # Calculate composite score
        df["Composite Score"] = (df["Relevance"] + df["Innovation"] + df["ESG"]) / 3
        df_ranked = df.sort_values("Composite Score", ascending=False)
        
        st.dataframe(
            df_ranked[["Company", "Relevance", "Innovation", "ESG", "Composite Score"]].round(1),
            use_container_width=True,
            hide_index=True
        )
