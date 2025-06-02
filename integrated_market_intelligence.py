"""
Integrated Market Intelligence for Source-to-Pay
Context-driven intelligence based on actual procurement data
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import os
import requests
from openai import OpenAI

class IntegratedMarketIntelligence:
    """Market intelligence integrated with S2P procurement data"""
    
    def __init__(self):
        self.google_api_key = os.environ.get('GOOGLE_API_KEY')
        self.google_cse_id = os.environ.get('GOOGLE_CSE_ID')
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def analyze_procurement_context(self, df: pd.DataFrame, data_type: str) -> Dict[str, Any]:
        """Extract procurement context from uploaded data"""
        
        context = {
            'suppliers': [],
            'categories': [],
            'spend_areas': [],
            'geographic_focus': [],
            'time_period': None,
            'key_relationships': []
        }
        
        # Extract suppliers
        supplier_columns = ['supplier', 'supplier_name', 'vendor', 'contractor', 'company']
        for col in df.columns:
            if any(term in col.lower() for term in supplier_columns):
                context['suppliers'] = df[col].dropna().unique().tolist()[:20]  # Top 20 suppliers
                break
        
        # Extract categories
        category_columns = ['category', 'commodity', 'service_type', 'product_type', 'classification']
        for col in df.columns:
            if any(term in col.lower() for term in category_columns):
                context['categories'] = df[col].dropna().unique().tolist()[:15]  # Top 15 categories
                break
        
        # Extract spend areas
        spend_columns = ['amount', 'value', 'cost', 'price', 'spend']
        for col in df.columns:
            if any(term in col.lower() for term in spend_columns):
                if df[col].dtype in ['int64', 'float64']:
                    # Identify high-spend areas
                    category_cols = [c for c in df.columns if 'category' in c.lower()]
                    if category_cols:
                        category_col = category_cols[0]
                        try:
                            spend_by_category = df.groupby(category_col)[col].sum().sort_values(ascending=False)
                            context['spend_areas'] = spend_by_category.head(10).to_dict()
                        except:
                            context['spend_areas'] = {}
                break
        
        # Extract geographic information
        location_columns = ['location', 'region', 'country', 'city', 'site']
        for col in df.columns:
            if any(term in col.lower() for term in location_columns):
                context['geographic_focus'] = df[col].dropna().unique().tolist()[:10]
                break
        
        # Determine time period
        date_columns = [col for col in df.columns if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower()]
        if date_columns:
            for col in date_columns:
                try:
                    date_series = pd.to_datetime(df[col], errors='coerce')
                    context['time_period'] = {
                        'start': date_series.min(),
                        'end': date_series.max(),
                        'span_months': (date_series.max() - date_series.min()).days / 30
                    }
                    break
                except:
                    continue
        
        return context
    
    def generate_intelligence_story(self, context: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Generate contextual intelligence story based on procurement data"""
        
        story_elements = {
            'executive_summary': self._create_executive_summary(context, data_type),
            'supplier_intelligence': self._analyze_supplier_landscape(context),
            'category_intelligence': self._analyze_category_dynamics(context),
            'market_opportunities': self._identify_market_opportunities(context),
            'risk_assessment': self._assess_market_risks(context),
            'strategic_recommendations': self._generate_strategic_actions(context, data_type)
        }
        
        return story_elements
    
    def _create_executive_summary(self, context: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Create executive summary of market intelligence findings"""
        
        summary = {
            'data_scope': f"{data_type.title()} data analysis",
            'supplier_count': len(context.get('suppliers', [])),
            'category_count': len(context.get('categories', [])),
            'geographic_reach': len(context.get('geographic_focus', [])),
            'time_span': context.get('time_period', {}).get('span_months', 0),
            'key_insights': []
        }
        
        # Generate contextual insights
        if context.get('suppliers'):
            summary['key_insights'].append(f"Analysis covers {len(context['suppliers'])} key suppliers across your procurement portfolio")
        
        if context.get('spend_areas'):
            top_category = max(context['spend_areas'], key=context['spend_areas'].get)
            summary['key_insights'].append(f"Highest spend concentration in {top_category} category")
        
        if context.get('time_period') and context['time_period'].get('span_months', 0) > 12:
            summary['key_insights'].append("Multi-year data enables trend analysis and forecasting")
        
        return summary
    
    def _analyze_supplier_landscape(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze supplier landscape based on actual procurement data"""
        
        supplier_analysis = {
            'total_suppliers': len(context.get('suppliers', [])),
            'supplier_intelligence': [],
            'market_positioning': {},
            'relationship_insights': []
        }
        
        # Analyze top suppliers if we have them
        if context.get('suppliers'):
            top_suppliers = context['suppliers'][:10]  # Focus on top 10
            
            for supplier in top_suppliers:
                # This would gather real intelligence about each supplier
                supplier_intel = {
                    'name': supplier,
                    'market_presence': 'Active in multiple categories' if len(context.get('categories', [])) > 1 else 'Specialized supplier',
                    'strategic_importance': 'High' if supplier in context['suppliers'][:5] else 'Medium',
                    'intelligence_gathering_needed': True
                }
                supplier_analysis['supplier_intelligence'].append(supplier_intel)
        
        return supplier_analysis
    
    def _analyze_category_dynamics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze category dynamics from procurement data"""
        
        category_analysis = {
            'total_categories': len(context.get('categories', [])),
            'category_insights': [],
            'spend_distribution': context.get('spend_areas', {}),
            'market_dynamics': {}
        }
        
        if context.get('categories'):
            spend_areas = context.get('spend_areas', {})
            # Convert spend_areas to dict if it's a list
            if isinstance(spend_areas, list):
                spend_areas = {}
            
            for category in context['categories'][:8]:  # Top 8 categories
                category_insight = {
                    'category': category,
                    'spend_level': spend_areas.get(category, 'Unknown'),
                    'supplier_count': 'Multiple suppliers' if len(context.get('suppliers', [])) > 3 else 'Limited suppliers',
                    'market_intelligence_priority': 'High' if category in list(spend_areas.keys())[:3] else 'Medium'
                }
                category_analysis['category_insights'].append(category_insight)
        
        return category_analysis
    
    def _identify_market_opportunities(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Identify market opportunities based on procurement patterns"""
        
        opportunities = {
            'supplier_diversification': [],
            'category_optimization': [],
            'geographic_expansion': [],
            'strategic_partnerships': []
        }
        
        # Supplier diversification opportunities
        if len(context.get('suppliers', [])) < 5:
            opportunities['supplier_diversification'].append("Limited supplier base - opportunity to diversify supply chain")
        
        # Category optimization
        if context.get('spend_areas'):
            high_spend_categories = [cat for cat, spend in context['spend_areas'].items() 
                                   if spend > sum(context['spend_areas'].values()) * 0.2]
            for category in high_spend_categories:
                opportunities['category_optimization'].append(f"High spend in {category} - potential for market intelligence and optimization")
        
        return opportunities
    
    def _assess_market_risks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market risks based on procurement data patterns"""
        
        risks = {
            'supplier_concentration': [],
            'category_risks': [],
            'geographic_risks': [],
            'market_volatility': []
        }
        
        # Supplier concentration risk
        if len(context.get('suppliers', [])) < 3:
            risks['supplier_concentration'].append("High supplier concentration risk - limited supplier diversity")
        
        # Category concentration risk
        if context.get('spend_areas'):
            total_spend = sum(context['spend_areas'].values())
            for category, spend in context['spend_areas'].items():
                if spend / total_spend > 0.5:
                    risks['category_risks'].append(f"High spend concentration in {category} - market risk exposure")
        
        return risks
    
    def _generate_strategic_actions(self, context: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Generate strategic recommendations based on procurement context"""
        
        actions = {
            'immediate_actions': [],
            'intelligence_priorities': [],
            'strategic_initiatives': []
        }
        
        # Immediate actions based on data type
        if data_type == 'sourcing':
            actions['immediate_actions'].extend([
                "Conduct market intelligence on active sourcing categories",
                "Analyze supplier performance and market positioning",
                "Assess competitive landscape for ongoing tenders"
            ])
        elif data_type == 'processing':
            actions['immediate_actions'].extend([
                "Review supplier performance against market benchmarks",
                "Identify optimization opportunities in high-spend categories",
                "Assess supply chain resilience and alternative suppliers"
            ])
        
        # Intelligence priorities based on suppliers and categories
        if context.get('suppliers'):
            actions['intelligence_priorities'].extend([
                f"Deep market analysis for top {min(5, len(context['suppliers']))} suppliers",
                "Competitive landscape mapping for key supplier relationships",
                "Supplier financial health and risk assessment"
            ])
        
        if context.get('categories'):
            spend_areas = context.get('spend_areas', {})
            # Convert spend_areas to dict if it's a list
            if isinstance(spend_areas, list):
                spend_areas = {}
            
            top_categories = list(spend_areas.keys())[:3] if spend_areas else context.get('categories', [])[:3]
            for category in top_categories:
                actions['intelligence_priorities'].append(f"Market intelligence for {category} category")
        
        return actions

def render_integrated_market_intelligence(df: pd.DataFrame, data_type: str):
    """Render integrated market intelligence based on procurement data"""
    
    st.markdown("## 🎯 Integrated Market Intelligence")
    st.markdown("*Contextual intelligence based on your procurement data*")
    
    # Initialize intelligence engine
    intel_engine = IntegratedMarketIntelligence()
    
    # Analyze procurement context
    with st.spinner("Analyzing your procurement data for intelligence context..."):
        context = intel_engine.analyze_procurement_context(df, data_type)
    
    # Generate intelligence story
    story = intel_engine.generate_intelligence_story(context, data_type)
    
    # Display executive summary
    st.markdown("### 📊 Executive Intelligence Summary")
    summary = story['executive_summary']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Suppliers", summary['supplier_count'])
    with col2:
        st.metric("Categories", summary['category_count'])
    with col3:
        st.metric("Locations", summary['geographic_reach'])
    with col4:
        st.metric("Time Span (months)", f"{summary['time_span']:.0f}")
    
    # Key insights
    st.markdown("**🔍 Key Intelligence Insights:**")
    for insight in summary['key_insights']:
        st.write(f"• {insight}")
    
    # Intelligence tabs based on actual data
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Supplier Intelligence", 
        "📦 Category Intelligence", 
        "🎯 Market Opportunities", 
        "🚨 Risk Assessment"
    ])
    
    with tab1:
        render_supplier_intelligence(story['supplier_intelligence'], context, intel_engine)
    
    with tab2:
        render_category_intelligence(story['category_intelligence'], context)
    
    with tab3:
        render_market_opportunities(story['market_opportunities'])
    
    with tab4:
        render_risk_assessment(story['risk_assessment'])
    
    # Strategic recommendations
    st.markdown("### 🎯 Strategic Intelligence Actions")
    render_strategic_recommendations(story['strategic_recommendations'])

def render_supplier_intelligence(supplier_analysis: Dict, context: Dict, intel_engine):
    """Render supplier intelligence based on actual procurement data"""
    
    st.markdown("### 🏢 Supplier Intelligence")
    
    if supplier_analysis['supplier_intelligence']:
        st.markdown("**Your Key Suppliers Analysis:**")
        
        # Create supplier intelligence table
        supplier_data = []
        for supplier in supplier_analysis['supplier_intelligence']:
            supplier_data.append({
                'Supplier': supplier['name'],
                'Market Presence': supplier['market_presence'],
                'Strategic Importance': supplier['strategic_importance'],
                'Intelligence Status': 'Pending Analysis' if supplier['intelligence_gathering_needed'] else 'Complete'
            })
        
        supplier_df = pd.DataFrame(supplier_data)
        st.dataframe(supplier_df, use_container_width=True)
        
        # Real-time intelligence gathering option
        if st.button("🔍 Gather Real-Time Supplier Intelligence", key="supplier_intel"):
            gather_supplier_intelligence(context['suppliers'][:5], intel_engine)
    else:
        st.info("Upload procurement data with supplier information to see supplier intelligence analysis")

def render_category_intelligence(category_analysis: Dict, context: Dict):
    """Render category intelligence based on procurement data"""
    
    st.markdown("### 📦 Category Intelligence")
    
    if category_analysis['category_insights']:
        # Spend distribution chart
        if category_analysis['spend_distribution']:
            st.markdown("**Spend Distribution Analysis:**")
            
            spend_df = pd.DataFrame([
                {'Category': cat, 'Spend': spend} 
                for cat, spend in category_analysis['spend_distribution'].items()
            ])
            
            fig = px.pie(spend_df, values='Spend', names='Category', 
                        title='Procurement Spend by Category')
            st.plotly_chart(fig, use_container_width=True)
        
        # Category intelligence table
        st.markdown("**Category Intelligence Priorities:**")
        category_data = []
        for category in category_analysis['category_insights']:
            category_data.append({
                'Category': category['category'],
                'Spend Level': category['spend_level'],
                'Supplier Diversity': category['supplier_count'],
                'Intel Priority': category['market_intelligence_priority']
            })
        
        category_df = pd.DataFrame(category_data)
        st.dataframe(category_df, use_container_width=True)
    else:
        st.info("Upload procurement data with category information to see category intelligence")

def render_market_opportunities(opportunities: Dict):
    """Render market opportunities based on procurement patterns"""
    
    st.markdown("### 🎯 Market Opportunities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔄 Supplier Diversification**")
        for opp in opportunities['supplier_diversification']:
            st.write(f"• {opp}")
        
        st.markdown("**📦 Category Optimization**")
        for opp in opportunities['category_optimization']:
            st.write(f"• {opp}")
    
    with col2:
        st.markdown("**🌍 Geographic Expansion**")
        if opportunities['geographic_expansion']:
            for opp in opportunities['geographic_expansion']:
                st.write(f"• {opp}")
        else:
            st.write("• Analyze geographic supplier distribution from data")
        
        st.markdown("**🤝 Strategic Partnerships**")
        if opportunities['strategic_partnerships']:
            for opp in opportunities['strategic_partnerships']:
                st.write(f"• {opp}")
        else:
            st.write("• Identify partnership opportunities based on supplier relationships")

def render_risk_assessment(risks: Dict):
    """Render risk assessment based on procurement data"""
    
    st.markdown("### 🚨 Risk Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏢 Supplier Risks**")
        for risk in risks['supplier_concentration']:
            st.error(f"⚠️ {risk}")
        
        st.markdown("**📦 Category Risks**")
        for risk in risks['category_risks']:
            st.warning(f"⚠️ {risk}")
    
    with col2:
        st.markdown("**🌍 Geographic Risks**")
        if risks['geographic_risks']:
            for risk in risks['geographic_risks']:
                st.error(f"⚠️ {risk}")
        else:
            st.info("Geographic risk analysis requires location data")
        
        st.markdown("**📈 Market Volatility**")
        if risks['market_volatility']:
            for risk in risks['market_volatility']:
                st.warning(f"⚠️ {risk}")
        else:
            st.info("Market volatility assessment based on category analysis")

def render_strategic_recommendations(recommendations: Dict):
    """Render strategic recommendations"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🚀 Immediate Actions**")
        for action in recommendations['immediate_actions']:
            st.write(f"• {action}")
    
    with col2:
        st.markdown("**🔍 Intelligence Priorities**")
        for priority in recommendations['intelligence_priorities']:
            st.write(f"• {priority}")
    
    with col3:
        st.markdown("**🎯 Strategic Initiatives**")
        for initiative in recommendations['strategic_initiatives']:
            st.write(f"• {initiative}")

def gather_comprehensive_market_intelligence(suppliers: List[str], categories: List[str], intel_engine):
    """Gather comprehensive market intelligence including macro factors"""
    
    if not intel_engine.google_api_key:
        st.error("API credentials required for comprehensive market intelligence")
        st.info("To enable real-time intelligence gathering, please provide:")
        st.code("GOOGLE_API_KEY=your_google_api_key\nGOOGLE_CSE_ID=your_custom_search_engine_id\nOPENAI_API_KEY=your_openai_api_key")
        return
    
    st.markdown("### 🌍 Comprehensive Intelligence Gathering")
    
    # Multi-dimensional intelligence collection
    intelligence_areas = {
        'supplier_intelligence': suppliers[:5],
        'macro_economic': ['UK GDP growth', 'inflation impact', 'interest rates', 'economic outlook'],
        'government_policy': ['government spending', 'regulatory changes', 'policy updates'],
        'market_dynamics': categories[:3] if categories else ['market trends']
    }
    
    results = {}
    total_searches = sum(len(items) for items in intelligence_areas.values())
    current_search = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for area, items in intelligence_areas.items():
        results[area] = []
        
        for item in items:
            current_search += 1
            status_text.text(f"Gathering {area.replace('_', ' ')}: {item}")
            
            # Customize queries based on intelligence area
            query = generate_contextual_query(item, area)
            
            try:
                intelligence_data = search_with_macro_context(query, area, intel_engine)
                if intelligence_data:
                    results[area].extend(intelligence_data)
                    st.write(f"✅ {item}: Found {len(intelligence_data)} sources")
                else:
                    st.write(f"⚠️ {item}: Limited data available")
                    
            except Exception as e:
                st.write(f"❌ {item}: Search error")
            
            progress_bar.progress(current_search / total_searches)
    
    return results

def generate_contextual_query(item: str, area: str) -> str:
    """Generate contextual search queries for different intelligence areas"""
    
    query_templates = {
        'supplier_intelligence': f"{item} company financial performance market position supplier analysis",
        'macro_economic': f"UK {item} economic indicators Bank of England ONS statistics 2024",
        'government_policy': f"UK government {item} policy framework legislation regulatory impact",
        'market_dynamics': f"{item} market trends industry analysis UK competitive landscape"
    }
    
    return query_templates.get(area, f"{item} market intelligence analysis")

def search_with_macro_context(query: str, area: str, intel_engine) -> List[Dict]:
    """Enhanced search with macro economic context"""
    
    # Site-specific searches for authoritative sources
    site_modifiers = {
        'macro_economic': ['site:bankofengland.co.uk', 'site:ons.gov.uk', 'site:hm-treasury.gov.uk'],
        'government_policy': ['site:gov.uk', 'site:parliament.uk', 'filetype:pdf government'],
        'supplier_intelligence': ['site:companieshouse.gov.uk', 'site:linkedin.com', 'financial statements'],
        'market_dynamics': ['market research', 'industry analysis', 'competitive intelligence']
    }
    
    modifiers = site_modifiers.get(area, [''])
    all_results = []
    
    for modifier in modifiers[:2]:  # Limit to prevent API overuse
        enhanced_query = f"{query} {modifier}".strip()
        
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'key': intel_engine.google_api_key,
                'cx': intel_engine.google_cse_id,
                'q': enhanced_query,
                'num': 3
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('items', [])
                
                for result in results:
                    intelligence_item = {
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'snippet': result.get('snippet', ''),
                        'source': result.get('displayLink', ''),
                        'intelligence_area': area,
                        'search_modifier': modifier,
                        'authority_score': calculate_source_authority(result, area),
                        'content_depth': len(result.get('snippet', '')) / 100
                    }
                    
                    # Enhanced analysis with LLM if available
                    if intel_engine.openai_api_key:
                        intelligence_item.update(analyze_with_llm(intelligence_item, intel_engine))
                    
                    all_results.append(intelligence_item)
                    
        except Exception as e:
            continue
    
    return all_results

def calculate_source_authority(result: Dict, area: str) -> float:
    """Calculate source authority based on domain and content type"""
    
    url = result.get('link', '').lower()
    domain = result.get('displayLink', '').lower()
    title = result.get('title', '').lower()
    
    authority_score = 0.5  # Base score
    
    # Government and official sources
    if any(gov in domain for gov in ['.gov.uk', 'bankofengland', 'ons.gov', 'parliament']):
        authority_score += 0.4
    
    # Academic and research institutions
    elif '.ac.uk' in domain or 'research' in title:
        authority_score += 0.3
    
    # Professional networks and company data
    elif area == 'supplier_intelligence' and ('linkedin' in domain or 'companieshouse' in domain):
        authority_score += 0.3
    
    # Established media for market intelligence
    elif any(media in domain for media in ['ft.com', 'reuters', 'bbc.co.uk']):
        authority_score += 0.2
    
    # Content depth indicators
    if any(indicator in title for indicator in ['report', 'analysis', 'statistics', 'data']):
        authority_score += 0.1
    
    return min(authority_score, 1.0)

def analyze_with_llm(intelligence_item: Dict, intel_engine) -> Dict:
    """Analyze intelligence data using LLM for deeper insights"""
    
    try:
        content = f"Area: {intelligence_item['intelligence_area']}\nTitle: {intelligence_item['title']}\nContent: {intelligence_item['snippet']}"
        
        prompt = f"""
        Analyze this market intelligence data:
        {content}
        
        Extract key information in JSON format:
        {{
            "strategic_value": 0-1,
            "key_metrics": ["metric1", "metric2", "metric3"],
            "insights": ["insight1", "insight2"],
            "decision_relevance": "high/medium/low",
            "data_type": "quantitative/qualitative/mixed",
            "time_sensitivity": "current/recent/historical"
        }}
        """
        
        response = intel_engine.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=300
        )
        
        import json
        return json.loads(response.choices[0].message.content)
        
    except:
        return {
            'strategic_value': 0.5,
            'decision_relevance': 'medium',
            'data_type': 'mixed'
        }

def gather_supplier_intelligence(suppliers: List[str], intel_engine):
    """Gather real-time intelligence for specific suppliers"""
    
    if not intel_engine.google_api_key:
        st.error("API credentials required for real-time supplier intelligence gathering")
        st.info("Please provide GOOGLE_API_KEY and GOOGLE_CSE_ID to access authentic market intelligence")
        return
    
    st.markdown("**🔍 Real-Time Supplier Intelligence Gathering:**")
    
    progress_bar = st.progress(0)
    
    for i, supplier in enumerate(suppliers):
        st.write(f"Analyzing: {supplier}")
        
        try:
            # Search for supplier intelligence
            query = f"{supplier} company profile financial performance market position"
            
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'key': intel_engine.google_api_key,
                'cx': intel_engine.google_cse_id,
                'q': query,
                'num': 3
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('items', [])
                
                if results:
                    st.success(f"✅ Found {len(results)} intelligence sources for {supplier}")
                    for result in results[:2]:
                        st.write(f"• **{result['title'][:60]}** - {result['displayLink']}")
                else:
                    st.warning(f"Limited public information found for {supplier}")
            
        except Exception as e:
            st.warning(f"Intelligence gathering error for {supplier}: {e}")
        
        progress_bar.progress((i + 1) / len(suppliers))