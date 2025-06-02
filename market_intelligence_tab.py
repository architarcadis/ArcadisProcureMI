import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Google Custom Search and OpenAI integration
import requests
from openai import OpenAI

class MarketIntelligenceService:
    """Core service for market intelligence data collection and analysis"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
    def generate_intelligence_categories(self, company_name: str) -> List[str]:
        """Generate AI-powered intelligence categories focused on suppliers, risk, categories, regulation"""
        if not self.openai_api_key:
            return [
                "Supplier Risk Assessment",
                "Regulatory Compliance Landscape", 
                "Category Market Analysis",
                "Supply Chain Vulnerabilities"
            ]
        
        try:
            prompt = f"""
            Generate 6-8 specific market intelligence categories for analyzing: {company_name}
            
            Focus areas: Suppliers, Risk Assessment, Category Analysis, Regulatory Environment
            
            Return only a JSON array of category names. Categories should be:
            - Actionable and specific to procurement intelligence
            - Focused on supplier ecosystems and risk factors
            - Relevant to regulatory and compliance landscapes
            - Strategic for category management decisions
            
            Example format: ["Supplier Financial Stability Risk", "Regulatory Change Impact Analysis"]
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("categories", [])
            
        except Exception as e:
            st.error(f"AI category generation failed: {e}")
            return [
                "Supplier Risk Assessment",
                "Regulatory Compliance Landscape", 
                "Category Market Analysis",
                "Supply Chain Vulnerabilities"
            ]
    
    def search_market_intelligence(self, company_name: str, category: str, num_results: int = 10) -> List[Dict]:
        """Search for market intelligence using Google Custom Search API"""
        if not self.google_api_key or not self.google_cse_id:
            return []
        
        try:
            search_query = f"{company_name} {category} suppliers risk regulation compliance"
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': search_query,
                'num': min(num_results, 10)
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            results = []
            if 'items' in data:
                for item in data['items']:
                    results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'category': category,
                        'search_query': search_query
                    })
            
            return results
            
        except Exception as e:
            st.error(f"Search failed for {category}: {e}")
            return []
    
    def analyze_intelligence_data(self, company_name: str, search_results: List[Dict]) -> Dict:
        """Analyze collected intelligence data using AI"""
        if not self.openai_api_key or not search_results:
            return {"analysis": "Analysis requires OpenAI API key and search results"}
        
        try:
            # Combine search results for analysis
            combined_text = "\n".join([
                f"Source: {result['title']}\nContent: {result['snippet']}\nCategory: {result['category']}"
                for result in search_results[:5]  # Limit to prevent token overflow
            ])
            
            prompt = f"""
            Analyze this market intelligence data for {company_name}:
            
            {combined_text}
            
            Provide analysis in JSON format with these sections:
            - "supplier_insights": Key findings about supplier landscape
            - "risk_factors": Identified risks and vulnerabilities  
            - "regulatory_landscape": Compliance and regulatory insights
            - "category_trends": Market category analysis
            - "strategic_recommendations": 3-5 actionable recommendations
            - "confidence_score": Assessment confidence (0-100)
            
            Focus on actionable procurement intelligence.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"AI analysis failed: {e}")
            return {"analysis": "Analysis failed"}

class DataStorageManager:
    """Manage storage and retrieval of market intelligence data"""
    
    def __init__(self, storage_file: str = "market_intelligence_data.json"):
        self.storage_file = storage_file
        self.ensure_storage_exists()
    
    def ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"analyses": {}}, f)
    
    def save_analysis(self, company_name: str, analysis_data: Dict) -> bool:
        """Save analysis data to storage"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            data["analyses"][company_name] = {
                "timestamp": datetime.now().isoformat(),
                "data": analysis_data
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
            
        except Exception as e:
            st.error(f"Failed to save analysis: {e}")
            return False
    
    def load_analysis(self, company_name: str) -> Optional[Dict]:
        """Load analysis data from storage"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return data["analyses"].get(company_name)
            
        except Exception as e:
            st.error(f"Failed to load analysis: {e}")
            return None
    
    def list_companies(self) -> List[str]:
        """Get list of analyzed companies"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return list(data["analyses"].keys())
            
        except Exception:
            return []

def render_market_intelligence_tab():
    """Main function to render the Market Intelligence tab"""
    
    st.header("🔍 Market Intelligence")
    st.markdown("### Strategic Supplier, Risk & Regulatory Intelligence")
    
    # Initialize services
    intel_service = MarketIntelligenceService()
    storage_manager = DataStorageManager()
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("🎯 Intelligence Controls")
        
        # Company input
        company_name = st.text_input("Company Name", placeholder="Enter company to analyze...")
        
        # Load & Process button
        if st.button("🚀 Load & Process", type="primary", disabled=not company_name):
            if company_name:
                st.session_state['current_company'] = company_name
                st.session_state['categories_generated'] = True
                st.rerun()
        
        # Show generated categories if available
        if st.session_state.get('categories_generated') and company_name:
            st.subheader("📋 Intelligence Categories")
            
            if 'generated_categories' not in st.session_state:
                with st.spinner("Generating smart categories..."):
                    categories = intel_service.generate_intelligence_categories(company_name)
                    st.session_state['generated_categories'] = categories
            
            categories = st.session_state.get('generated_categories', [])
            selected_categories = st.multiselect(
                "Select Focus Areas:",
                categories,
                default=categories[:3] if len(categories) >= 3 else categories
            )
            
            # Analysis button
            if st.button("📊 Run Analysis", disabled=not selected_categories):
                if selected_categories:
                    st.session_state['selected_categories'] = selected_categories
                    st.session_state['run_analysis'] = True
                    st.rerun()
        
        # Storage management
        st.subheader("💾 Previous Analyses")
        stored_companies = storage_manager.list_companies()
        if stored_companies:
            selected_stored = st.selectbox("Load Previous Analysis:", 
                                         [""] + stored_companies)
            if selected_stored:
                stored_data = storage_manager.load_analysis(selected_stored)
                if stored_data:
                    st.session_state['loaded_analysis'] = stored_data
                    st.session_state['current_company'] = selected_stored
                    st.success(f"Loaded analysis for {selected_stored}")
    
    # Main content area
    if not st.session_state.get('current_company'):
        # Welcome screen
        st.info("👆 Enter a company name in the sidebar to begin market intelligence analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏢 Focus Area", "Suppliers")
        with col2:
            st.metric("⚠️ Focus Area", "Risk Assessment")
        with col3:
            st.metric("📂 Focus Area", "Categories")
        with col4:
            st.metric("📋 Focus Area", "Regulation")
        
        st.markdown("""
        **This intelligence platform provides:**
        - Real-time supplier ecosystem analysis
        - Risk factor identification and assessment
        - Category market intelligence gathering
        - Regulatory landscape monitoring
        - AI-powered strategic recommendations
        """)
    
    else:
        # Show analysis results
        company = st.session_state['current_company']
        st.subheader(f"📊 Intelligence Analysis: {company}")
        
        # Check if we need to run new analysis
        if st.session_state.get('run_analysis'):
            selected_categories = st.session_state.get('selected_categories', [])
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_results = []
            analysis_data = {}
            
            # Collect data for each category
            for i, category in enumerate(selected_categories):
                status_text.text(f"Gathering intelligence for: {category}")
                progress_bar.progress((i + 1) / (len(selected_categories) + 1))
                
                search_results = intel_service.search_market_intelligence(company, category)
                all_results.extend(search_results)
                analysis_data[category] = search_results
            
            # AI analysis
            status_text.text("Generating AI insights...")
            ai_analysis = intel_service.analyze_intelligence_data(company, all_results)
            analysis_data['ai_insights'] = ai_analysis
            analysis_data['categories'] = selected_categories
            
            # Save to storage
            storage_manager.save_analysis(company, analysis_data)
            
            # Store in session
            st.session_state['current_analysis'] = analysis_data
            st.session_state['run_analysis'] = False
            
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            
            st.rerun()
        
        # Display analysis if available
        analysis = st.session_state.get('current_analysis') or st.session_state.get('loaded_analysis', {}).get('data')
        
        if analysis:
            render_analysis_dashboard(company, analysis)

def render_analysis_dashboard(company_name: str, analysis_data: Dict):
    """Render the complete analysis dashboard with story-driven tabs"""
    
    # Create story-driven tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Company Context",
        "🔍 Market Landscape", 
        "🏢 Key Intelligence",
        "📈 Risk & Insights",
        "💡 Strategic Actions"
    ])
    
    ai_insights = analysis_data.get('ai_insights', {})
    categories = analysis_data.get('categories', [])
    
    with tab1:
        render_company_context(company_name, analysis_data)
    
    with tab2:
        render_market_landscape(analysis_data)
    
    with tab3:
        render_key_intelligence(analysis_data)
    
    with tab4:
        render_risk_insights(ai_insights)
    
    with tab5:
        render_strategic_actions(ai_insights)

def render_company_context(company_name: str, analysis_data: Dict):
    """Render company context and analysis overview"""
    st.subheader(f"📊 {company_name} - Intelligence Overview")
    
    categories = analysis_data.get('categories', [])
    ai_insights = analysis_data.get('ai_insights', {})
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Categories Analyzed", len(categories))
    with col2:
        total_sources = sum(len(analysis_data.get(cat, [])) for cat in categories)
        st.metric("Intelligence Sources", total_sources)
    with col3:
        confidence = ai_insights.get('confidence_score', 'N/A')
        st.metric("Analysis Confidence", f"{confidence}%" if isinstance(confidence, (int, float)) else confidence)
    with col4:
        st.metric("Analysis Date", datetime.now().strftime("%Y-%m-%d"))
    
    # Categories overview
    st.subheader("🎯 Analysis Categories")
    for category in categories:
        sources_count = len(analysis_data.get(category, []))
        st.info(f"**{category}**: {sources_count} sources analyzed")

def render_market_landscape(analysis_data: Dict):
    """Render market landscape analysis"""
    st.subheader("🔍 Market Intelligence Landscape")
    
    categories = analysis_data.get('categories', [])
    
    # Create data for visualization
    landscape_data = []
    for category in categories:
        sources = analysis_data.get(category, [])
        landscape_data.append({
            'Category': category,
            'Sources': len(sources),
            'Intelligence_Depth': min(len(sources) * 10, 100)
        })
    
    if landscape_data:
        df = pd.DataFrame(landscape_data)
        
        # Sources by category chart
        fig = px.bar(df, x='Category', y='Sources', 
                    title="Intelligence Sources by Category",
                    color='Intelligence_Depth',
                    color_continuous_scale='Blues')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Intelligence depth radar chart
        if len(df) > 2:
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=df['Intelligence_Depth'],
                theta=df['Category'],
                fill='toself',
                name='Intelligence Coverage'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="Intelligence Coverage Depth"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

def render_key_intelligence(analysis_data: Dict):
    """Render key intelligence findings"""
    st.subheader("🏢 Key Intelligence Findings")
    
    categories = analysis_data.get('categories', [])
    ai_insights = analysis_data.get('ai_insights', {})
    
    # Supplier insights
    supplier_insights = ai_insights.get('supplier_insights', 'No supplier insights available')
    st.subheader("🏭 Supplier Landscape")
    st.write(supplier_insights)
    
    # Category trends
    category_trends = ai_insights.get('category_trends', 'No category trends available')
    st.subheader("📂 Category Analysis")
    st.write(category_trends)
    
    # Regulatory landscape
    regulatory_info = ai_insights.get('regulatory_landscape', 'No regulatory information available')
    st.subheader("📋 Regulatory Environment")
    st.write(regulatory_info)

def render_risk_insights(ai_insights: Dict):
    """Render risk assessment and insights"""
    st.subheader("📈 Risk Assessment & Strategic Insights")
    
    # Risk factors
    risk_factors = ai_insights.get('risk_factors', 'No risk factors identified')
    st.subheader("⚠️ Identified Risk Factors")
    
    if isinstance(risk_factors, list):
        for i, risk in enumerate(risk_factors, 1):
            st.warning(f"**Risk {i}:** {risk}")
    else:
        st.write(risk_factors)
    
    # Confidence assessment
    confidence = ai_insights.get('confidence_score', 0)
    st.subheader("🎯 Analysis Confidence")
    
    if isinstance(confidence, (int, float)):
        # Create confidence gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Analysis Confidence"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Confidence: {confidence}")

def render_strategic_actions(ai_insights: Dict):
    """Render strategic recommendations and actions"""
    st.subheader("💡 Strategic Recommendations")
    
    recommendations = ai_insights.get('strategic_recommendations', [])
    
    if isinstance(recommendations, list) and recommendations:
        st.subheader("🎯 Recommended Actions")
        for i, rec in enumerate(recommendations, 1):
            st.success(f"**Recommendation {i}:** {rec}")
    else:
        st.write("No specific recommendations available from current analysis.")
    
    # Action planning section
    st.subheader("📋 Next Steps Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Immediate Actions (0-30 days):**")
        st.write("- Review identified risk factors")
        st.write("- Validate supplier intelligence")
        st.write("- Assess regulatory compliance gaps")
    
    with col2:
        st.write("**Strategic Actions (30-90 days):**")
        st.write("- Develop supplier diversification plan")
        st.write("- Implement risk monitoring systems")
        st.write("- Update category strategies")
    
    # Export options
    st.subheader("📊 Export & Share")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Summary"):
            st.info("Summary export functionality would be implemented here")
    
    with col2:
        if st.button("📊 Export Data"):
            st.info("Data export functionality would be implemented here")
    
    with col3:
        if st.button("📧 Share Report"):
            st.info("Report sharing functionality would be implemented here")

# Initialize session state
if 'categories_generated' not in st.session_state:
    st.session_state['categories_generated'] = False
if 'current_company' not in st.session_state:
    st.session_state['current_company'] = None