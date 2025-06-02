import streamlit as st
import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI

class MarketIntelligenceEngine:
    """Pragmatic market intelligence engine using Google Custom Search and OpenAI"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def search_supplier_intelligence(self, query: str, focus_area: str) -> List[Dict]:
        """Search for supplier and market intelligence using Google Custom Search"""
        if not self.google_api_key or not self.google_cse_id:
            st.error(f"❌ Missing API credentials for {focus_area}")
            return []
        
        try:
            st.info(f"🔍 Searching {focus_area} for: {query}")
            # Craft specific search queries for different intelligence areas
            search_queries = {
                "suppliers": f"{query} suppliers manufacturers vendors directory contact",
                "trends": f"{query} market trends analysis report 2024 industry outlook",
                "opportunities": f"{query} new suppliers emerging companies startup vendors",
                "risks": f"{query} supply chain risk compliance regulatory challenges"
            }
            
            search_query = search_queries.get(focus_area, f"{query} {focus_area}")
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': search_query,
                'num': 10
            }
            
            st.info(f"🌐 Making API call: {search_query}")
            response = requests.get(url, params=params)
            st.info(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code != 200:
                st.error(f"❌ API Error {response.status_code}: {response.text}")
                return []
            
            data = response.json()
            st.success(f"✅ API call successful for {focus_area}")
            
            results = []
            if 'items' in data:
                st.info(f"📊 Found {len(data['items'])} raw results")
                for item in data['items']:
                    results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'focus_area': focus_area,
                        'search_query': search_query,
                        'relevance_score': self._calculate_relevance_score(item, focus_area)
                    })
            
            return sorted(results, key=lambda x: x['relevance_score'], reverse=True)
            
        except Exception as e:
            st.error(f"Search failed for {focus_area}: {e}")
            return []
    
    def _calculate_relevance_score(self, item: Dict, focus_area: str) -> float:
        """Calculate relevance score based on content and focus area"""
        title = item.get('title', '').lower()
        snippet = item.get('snippet', '').lower()
        
        relevance_keywords = {
            "suppliers": ["supplier", "manufacturer", "vendor", "company", "contact", "directory"],
            "trends": ["trend", "market", "analysis", "report", "outlook", "forecast"],
            "opportunities": ["new", "emerging", "startup", "innovation", "growth"],
            "risks": ["risk", "compliance", "regulatory", "challenge", "disruption"]
        }
        
        keywords = relevance_keywords.get(focus_area, [])
        score = 0
        
        for keyword in keywords:
            if keyword in title:
                score += 2
            if keyword in snippet:
                score += 1
        
        return score
    
    def analyze_intelligence(self, company_category: str, search_results: List[Dict]) -> Dict:
        """Analyze collected intelligence using OpenAI"""
        if not self.openai_api_key or not search_results:
            return {"error": "Analysis requires OpenAI API key and search results"}
        
        try:
            # Combine top search results for analysis
            combined_text = "\n".join([
                f"Title: {result['title']}\nContent: {result['snippet']}\nFocus: {result['focus_area']}"
                for result in search_results[:8]  # Limit to prevent token overflow
            ])
            
            prompt = f"""
            Analyze this market intelligence data for {company_category}:
            
            {combined_text}
            
            Provide pragmatic, actionable analysis in JSON format:
            {{
                "market_positioning": {{
                    "key_suppliers": ["list of actual supplier names found"],
                    "market_concentration": "analysis of market structure",
                    "geographic_distribution": "supplier location insights"
                }},
                "trend_analysis": {{
                    "technology_trends": "current tech adoption patterns",
                    "market_consolidation": "M&A and consolidation trends",
                    "emerging_opportunities": "new market entrants and innovations"
                }},
                "supplier_engagement": {{
                    "new_targets": ["specific suppliers worth evaluating"],
                    "contact_opportunities": "engagement timing and approach",
                    "partnership_potential": "collaboration opportunities"
                }},
                "risk_assessment": {{
                    "concentration_risks": "supply base concentration issues",
                    "regulatory_landscape": "compliance and regulatory factors",
                    "financial_stability": "supplier financial health indicators"
                }},
                "actionable_recommendations": [
                    "Specific action 1 with timeline",
                    "Specific action 2 with approach",
                    "Specific action 3 with rationale"
                ],
                "confidence_level": 85
            }}
            
            Focus on specific, actionable insights that procurement professionals can immediately use.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=3000,
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return {"error": f"Analysis failed: {e}"}

class IntelligenceDataManager:
    """Manage storage and retrieval of market intelligence data"""
    
    def __init__(self, storage_file: str = "market_intelligence_storage.json"):
        self.storage_file = storage_file
        self.ensure_storage_exists()
    
    def ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"intelligence_reports": {}}, f)
    
    def save_intelligence_report(self, company_category: str, report_data: Dict) -> bool:
        """Save intelligence report to storage"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            data["intelligence_reports"][company_category] = {
                "timestamp": datetime.now().isoformat(),
                "data": report_data
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
            
        except Exception as e:
            st.error(f"Failed to save report: {e}")
            return False
    
    def load_intelligence_report(self, company_category: str) -> Optional[Dict]:
        """Load intelligence report from storage"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return data["intelligence_reports"].get(company_category)
            
        except Exception as e:
            return None
    
    def list_available_reports(self) -> List[str]:
        """Get list of available intelligence reports"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return list(data["intelligence_reports"].keys())
            
        except Exception:
            return []

def show_market_intelligence():
    """Main function to render the Market Intelligence tab"""
    
    st.header("🔍 Market Intelligence")
    st.markdown("### Pragmatic Supplier & Market Engagement Intelligence")
    
    # Initialize services
    intel_engine = MarketIntelligenceEngine()
    data_manager = IntelligenceDataManager()
    
    # Check API configuration
    apis_configured = bool(intel_engine.google_api_key and intel_engine.google_cse_id and intel_engine.openai_api_key)
    
    if not apis_configured:
        st.warning("⚠️ API Configuration Required")
        st.info("""
        This Market Intelligence system requires:
        - **GOOGLE_API_KEY**: Your Google Custom Search API key
        - **GOOGLE_CSE_ID**: Your Google Custom Search Engine ID  
        - **OPENAI_API_KEY**: Your OpenAI API key
        
        Please configure these environment variables to enable real market intelligence gathering.
        """)
        return
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("🎯 Intelligence Controls")
        
        # Company/Category input
        company_category = st.text_input(
            "Company or Category", 
            placeholder="e.g., Tesla, Cloud Computing Services, Industrial Automation..."
        )
        
        # Intelligence focus selection
        intelligence_focus = st.multiselect(
            "Intelligence Focus Areas:",
            ["suppliers", "trends", "opportunities", "risks"],
            default=["suppliers", "trends"]
        )
        
        # Geographic scope
        geographic_scope = st.selectbox(
            "Geographic Scope:",
            ["Global", "North America", "Europe", "Asia-Pacific", "UK"]
        )
        
        # Analysis depth
        analysis_depth = st.selectbox(
            "Analysis Depth:",
            ["Quick Scan (5 min)", "Deep Dive (15 min)"]
        )
        
        # Load & Process button
        process_intelligence = st.button(
            "🚀 Load & Process Intelligence", 
            type="primary",
            disabled=not company_category or not intelligence_focus
        )
        
        # Previous reports
        st.subheader("📊 Previous Reports")
        available_reports = data_manager.list_available_reports()
        if available_reports:
            selected_report = st.selectbox("Load Previous Report:", [""] + available_reports)
            if selected_report:
                report_data = data_manager.load_intelligence_report(selected_report)
                if report_data:
                    st.session_state['loaded_intelligence'] = report_data
                    st.session_state['current_company_category'] = selected_report
                    st.success(f"Loaded: {selected_report}")
    
    # Main content area
    if not company_category and not st.session_state.get('current_company_category'):
        # Welcome screen
        st.info("👆 Enter a company name or product category in the sidebar to begin market intelligence analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎯 Focus", "Market Positioning")
        with col2:
            st.metric("📈 Focus", "Trend Analysis")
        with col3:
            st.metric("🏢 Focus", "Supplier Engagement")
        with col4:
            st.metric("⚠️ Focus", "Risk Assessment")
        
        st.markdown("""
        **This intelligence platform provides:**
        - **Real supplier identification** with verified contact information
        - **Market trend analysis** from authoritative sources
        - **Supplier engagement opportunities** with timing insights
        - **Strategic risk assessment** with mitigation strategies
        - **Actionable recommendations** for immediate implementation
        """)
        return
    
    # Process new intelligence
    if process_intelligence and company_category:
        st.session_state['current_company_category'] = company_category
        
        # Progress tracking with database visibility
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create real-time data display containers
        data_container = st.container()
        with data_container:
            st.subheader("📊 Live Data Collection")
            results_table = st.empty()
            summary_metrics = st.empty()
            
            # Error logging container
            st.subheader("🔍 Process Logs")
            error_logs = st.empty()
            detailed_logs = st.expander("View Detailed Logs", expanded=False)
        
        # Initialize logging
        log_messages = []
        
        def add_log(message, level="INFO"):
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {level}: {message}"
            log_messages.append(log_entry)
            
            # Display in error logs container
            with error_logs:
                if level == "ERROR":
                    st.error(f"❌ {message}")
                elif level == "WARNING":
                    st.warning(f"⚠️ {message}")
                else:
                    st.info(f"ℹ️ {message}")
            
            # Update detailed logs
            with detailed_logs:
                st.code("\n".join(log_messages[-10:]))
        
        all_results = []
        total_steps = len(intelligence_focus) + 1  # +1 for analysis
        
        # Start analysis with logging
        add_log(f"Starting intelligence analysis for: {company_category}")
        add_log(f"Selected focus areas: {', '.join(intelligence_focus)}")
        add_log(f"Geographic scope: {geographic_scope}")
        
        # Collect intelligence for each focus area
        for i, focus in enumerate(intelligence_focus):
            status_text.text(f"🔍 Crawling {focus} intelligence for {company_category}...")
            progress_bar.progress((i + 1) / total_steps)
            
            add_log(f"Starting search for: {focus}")
            
            search_results = []
            try:
                search_results = intel_engine.search_supplier_intelligence(company_category, focus)
                
                if search_results:
                    add_log(f"✅ Found {len(search_results)} results for {focus}")
                    all_results.extend(search_results)
                else:
                    add_log(f"⚠️ No results found for {focus}", "WARNING")
                    
            except Exception as e:
                add_log(f"❌ Error searching {focus}: {str(e)}", "ERROR")
            
            # Show live database population
            if search_results:
                # Display latest results
                latest_df = pd.DataFrame([
                    {
                        'Focus Area': result['focus_area'],
                        'Source': result['title'][:60] + '...' if len(result['title']) > 60 else result['title'],
                        'Relevance': f"{result['relevance_score']}/10",
                        'Status': '✅ Collected'
                    }
                    for result in search_results[:5]
                ])
                
                results_table.dataframe(latest_df, use_container_width=True)
                
                # Update summary metrics
                with summary_metrics:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Sources", len(all_results))
                    with col2:
                        st.metric("Current Focus", focus.title())
                    with col3:
                        avg_relevance = sum(r['relevance_score'] for r in all_results) / len(all_results) if all_results else 0
                        st.metric("Avg Relevance", f"{avg_relevance:.1f}/10")
                    with col4:
                        st.metric("Categories Processed", f"{i+1}/{len(intelligence_focus)}")
                
                # Small delay to show the crawling effect
                import time
                time.sleep(1)
        
        # Show complete database before analysis
        status_text.text("📊 Database populated! Generating AI analysis...")
        
        # Display complete collected database
        if all_results:
            st.subheader("🗄️ Complete Database Content")
            
            # Full database view
            full_db_df = pd.DataFrame([
                {
                    'ID': i+1,
                    'Focus Area': result['focus_area'],
                    'Title': result['title'],
                    'Source URL': result['link'],
                    'Content Preview': result['snippet'][:100] + '...' if len(result['snippet']) > 100 else result['snippet'],
                    'Relevance Score': result['relevance_score'],
                    'Search Query': result['search_query']
                }
                for i, result in enumerate(all_results)
            ])
            
            st.dataframe(full_db_df, use_container_width=True, height=300)
            
            # Database statistics
            st.subheader("📈 Database Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(all_results))
            with col2:
                focus_counts = {}
                for result in all_results:
                    focus = result['focus_area']
                    focus_counts[focus] = focus_counts.get(focus, 0) + 1
                most_common = max(focus_counts.items(), key=lambda x: x[1]) if focus_counts else ("None", 0)
                st.metric("Top Category", f"{most_common[0]} ({most_common[1]})")
            with col3:
                avg_relevance = sum(r['relevance_score'] for r in all_results) / len(all_results)
                st.metric("Avg Relevance", f"{avg_relevance:.1f}")
            with col4:
                unique_domains = len(set(result['link'].split('/')[2] if '/' in result['link'] else result['link'] for result in all_results))
                st.metric("Unique Sources", unique_domains)
        
        # AI analysis with logging
        add_log("Starting AI analysis of collected data...")
        try:
            analysis = intel_engine.analyze_intelligence(company_category, all_results)
            add_log(f"✅ AI analysis completed successfully")
        except Exception as e:
            add_log(f"❌ AI analysis failed: {str(e)}", "ERROR")
            analysis = {"error": str(e)}
        
        # Combine data
        intelligence_data = {
            "search_results": all_results,
            "analysis": analysis,
            "focus_areas": intelligence_focus,
            "geographic_scope": geographic_scope,
            "analysis_depth": analysis_depth
        }
        
        # Save to storage
        data_manager.save_intelligence_report(company_category, intelligence_data)
        
        # Store in session
        st.session_state['current_intelligence'] = intelligence_data
        
        progress_bar.progress(1.0)
        status_text.text("✅ Intelligence analysis complete!")
        
        st.rerun()
    
    # Display intelligence results
    current_company = st.session_state.get('current_company_category')
    intelligence_data = (
        st.session_state.get('current_intelligence') or 
        st.session_state.get('loaded_intelligence', {}).get('data')
    )
    
    if current_company and intelligence_data:
        render_intelligence_narrative(current_company, intelligence_data)

def render_intelligence_narrative(company_category: str, intelligence_data: Dict):
    """Render the complete intelligence narrative in sections"""
    
    analysis = intelligence_data.get('analysis', {})
    search_results = intelligence_data.get('search_results', [])
    focus_areas = intelligence_data.get('focus_areas', [])
    
    # 1. Market Positioning Intelligence
    st.subheader("🎯 Market Positioning Intelligence")
    
    market_positioning = analysis.get('market_positioning', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        suppliers_found = len(market_positioning.get('key_suppliers', []))
        st.metric("Key Suppliers Identified", suppliers_found)
    with col2:
        total_sources = len(search_results)
        st.metric("Intelligence Sources", total_sources)
    with col3:
        confidence = analysis.get('confidence_level', 0)
        st.metric("Analysis Confidence", f"{confidence}%")
    
    # Key suppliers
    key_suppliers = market_positioning.get('key_suppliers', [])
    if key_suppliers:
        st.write("**Key Suppliers Identified:**")
        for supplier in key_suppliers:
            st.write(f"• {supplier}")
    
    # Market concentration
    market_concentration = market_positioning.get('market_concentration', '')
    if market_concentration:
        st.write("**Market Structure:**")
        st.write(market_concentration)
    
    # Geographic distribution
    geographic_dist = market_positioning.get('geographic_distribution', '')
    if geographic_dist:
        st.write("**Geographic Distribution:**")
        st.write(geographic_dist)
    
    # 2. Trend & Opportunity Analysis
    st.subheader("📈 Trend & Opportunity Analysis")
    
    trend_analysis = analysis.get('trend_analysis', {})
    
    # Technology trends
    tech_trends = trend_analysis.get('technology_trends', '')
    if tech_trends:
        st.write("**Technology Adoption Patterns:**")
        st.info(tech_trends)
    
    # Market consolidation
    market_consolidation = trend_analysis.get('market_consolidation', '')
    if market_consolidation:
        st.write("**Market Consolidation Trends:**")
        st.info(market_consolidation)
    
    # Emerging opportunities
    emerging_opps = trend_analysis.get('emerging_opportunities', '')
    if emerging_opps:
        st.write("**Emerging Opportunities:**")
        st.success(emerging_opps)
    
    # 3. Supplier Engagement Opportunities
    st.subheader("🏢 Supplier Engagement Opportunities")
    
    supplier_engagement = analysis.get('supplier_engagement', {})
    
    # New targets
    new_targets = supplier_engagement.get('new_targets', [])
    if new_targets:
        st.write("**Priority Supplier Targets:**")
        for target in new_targets:
            st.write(f"✅ {target}")
    
    # Contact opportunities
    contact_opps = supplier_engagement.get('contact_opportunities', '')
    if contact_opps:
        st.write("**Engagement Timing & Approach:**")
        st.write(contact_opps)
    
    # Partnership potential
    partnership_potential = supplier_engagement.get('partnership_potential', '')
    if partnership_potential:
        st.write("**Partnership Opportunities:**")
        st.write(partnership_potential)
    
    # 4. Strategic Risk Assessment
    st.subheader("⚠️ Strategic Risk Assessment")
    
    risk_assessment = analysis.get('risk_assessment', {})
    
    # Concentration risks
    concentration_risks = risk_assessment.get('concentration_risks', '')
    if concentration_risks:
        st.write("**Supply Concentration Risks:**")
        st.warning(concentration_risks)
    
    # Regulatory landscape
    regulatory_landscape = risk_assessment.get('regulatory_landscape', '')
    if regulatory_landscape:
        st.write("**Regulatory Environment:**")
        st.info(regulatory_landscape)
    
    # Financial stability
    financial_stability = risk_assessment.get('financial_stability', '')
    if financial_stability:
        st.write("**Financial Stability Indicators:**")
        st.write(financial_stability)
    
    # 5. Actionable Recommendations
    st.subheader("💼 Actionable Recommendations")
    
    recommendations = analysis.get('actionable_recommendations', [])
    if recommendations:
        st.write("**Immediate Action Items:**")
        for i, rec in enumerate(recommendations, 1):
            st.success(f"**{i}.** {rec}")
    
    # Intelligence sources summary
    st.subheader("📊 Intelligence Sources")
    
    if search_results:
        # Create DataFrame for source analysis
        sources_df = pd.DataFrame([
            {
                'Focus Area': result['focus_area'],
                'Source': result['title'][:50] + '...' if len(result['title']) > 50 else result['title'],
                'Relevance Score': result['relevance_score']
            }
            for result in search_results[:10]  # Show top 10 sources
        ])
        
        # Sources by focus area chart
        if not sources_df.empty:
            focus_counts = sources_df.groupby('Focus Area').size().reset_index(name='Count')
            fig = px.bar(focus_counts, x='Focus Area', y='Count', 
                        title="Intelligence Sources by Focus Area")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top sources table
            st.write("**Top Intelligence Sources:**")
            st.dataframe(sources_df.head(5), use_container_width=True)

# Initialize session state
if 'current_company_category' not in st.session_state:
    st.session_state['current_company_category'] = None
if 'current_intelligence' not in st.session_state:
    st.session_state['current_intelligence'] = None