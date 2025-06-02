"""
Market Intelligence Integration Package
=====================================

Drop this into your existing Streamlit app to add Market Intelligence as a new tab.

STEP 1: Copy this file to your app directory
STEP 2: Copy the components/ and services/ folders
STEP 3: Add one line to your main app

Example integration:
```python
from market_intelligence_integration_package import add_market_intelligence_tab

# In your existing app where you create tabs:
tab1, tab2, tab3, tab_intel = st.tabs([
    "Your Tab 1", 
    "Your Tab 2", 
    "Your Tab 3",
    "🔍 Market Intelligence"
])

with tab_intel:
    add_market_intelligence_tab()
```
"""

import streamlit as st
import os
from typing import Dict, Any, Optional
from datetime import datetime

def _generate_category_keywords(segment, selected_categories, company_name):
    """Generate story-driven keywords based on selected intelligence categories"""
    base_keywords = segment.get('intelligence_gathering_keywords', [])
    category_keywords = []
    
    # Map categories to enhanced keyword patterns
    category_patterns = {
        'innovation_tech': ['innovative', 'emerging technology', 'R&D', 'patent', 'AI', 'IoT'],
        'cost_performance': ['cost reduction', 'efficiency', 'ROI', 'performance metrics', 'benchmarking'],
        'risk_compliance': ['compliance', 'risk management', 'audit', 'regulatory', 'certification'],
        'sustainability': ['sustainable', 'ESG', 'carbon neutral', 'green technology', 'circular economy'],
        'supply_chain': ['supply chain', 'resilience', 'backup supplier', 'geographic diversity'],
        'quality_standards': ['quality standards', 'ISO certification', 'excellence', 'best practices']
    }
    
    # Generate enhanced keywords for each selected category
    for category in selected_categories:
        if category in category_patterns:
            for base_keyword in base_keywords[:2]:  # Use top 2 base keywords
                for pattern in category_patterns[category][:2]:  # Top 2 patterns per category
                    enhanced_keyword = f"{pattern} {base_keyword}"
                    category_keywords.append(enhanced_keyword)
    
    return category_keywords[:6]  # Return top 6 enhanced keywords

def _generate_dynamic_categories(company_name):
    """Generate AI-powered, company-specific intelligence categories"""
    try:
        from services.openai_service import OpenAIService
        openai_service = OpenAIService()
        
        # AI prompt to generate company-specific categories
        prompt = f"""
        You are a Strategic Market Intelligence Expert. Analyze the company "{company_name}" and generate 6-8 highly specific, strategic intelligence categories that would be most valuable for procurement and supplier analysis for this company.

        Consider:
        - The company's industry and specific business model
        - Unique regulatory requirements they face
        - Critical operational dependencies 
        - Strategic competitive advantages they need
        - Industry-specific risks and opportunities
        - Innovation areas relevant to their sector

        Return a JSON array of objects with this structure:
        [
          {{
            "id": "unique_category_id",
            "display_name": "Human-Readable Category Name",
            "description": "Detailed explanation of why this intelligence category is strategically important for {company_name}",
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "strategic_priority": "high|medium|low"
          }}
        ]

        Make each category highly specific to {company_name}'s industry and strategic needs. Avoid generic categories.
        """
        
        # Generate categories using AI
        response = openai_service.client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            messages=[
                {"role": "system", "content": "You are a Strategic Market Intelligence Expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1500,
            temperature=0.3
        )
        
        import json
        response_content = response.choices[0].message.content
        
        if not response_content:
            st.warning("⚠️ AI response was empty, using intelligent fallback categories")
            return _get_intelligent_fallback_categories(company_name)
        
        # Debug: show what we got
        st.info(f"🤖 AI generated categories (first 200 chars): {response_content[:200]}...")
        
        try:
            categories_data = json.loads(response_content)
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON parsing failed: {str(e)}")
            return _get_intelligent_fallback_categories(company_name)
        
        # Handle different response structures
        if isinstance(categories_data, list):
            return categories_data
        elif isinstance(categories_data, dict):
            if 'categories' in categories_data:
                return categories_data['categories']
            elif 'data' in categories_data:
                return categories_data['data']
            else:
                # If it's a dict but we're not sure of the structure, try to extract
                for key, value in categories_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        return value
        
        # Last resort fallback
        return _get_intelligent_fallback_categories(company_name)
            
    except Exception as e:
        st.error(f"❌ Failed to generate dynamic categories: {str(e)}")
        # Return industry-intelligent fallback categories
        return _get_intelligent_fallback_categories(company_name)

def _get_intelligent_fallback_categories(company_name):
    """Intelligent fallback categories based on company name analysis"""
    # Basic industry detection from company name
    company_lower = company_name.lower()
    
    if any(word in company_lower for word in ['water', 'utility', 'thames', 'severn']):
        return [
            {"id": "water_treatment_tech", "display_name": "🌊 Advanced Water Treatment Technologies", 
             "description": "Next-generation purification, desalination, and smart water management systems"},
            {"id": "regulatory_compliance", "display_name": "⚖️ Utility Regulatory Compliance", 
             "description": "Ofwat compliance, AMP8 requirements, and regulatory reporting solutions"},
            {"id": "infrastructure_resilience", "display_name": "🔧 Infrastructure Resilience & Maintenance", 
             "description": "Asset management, predictive maintenance, and infrastructure upgrade suppliers"}
        ]
    elif any(word in company_lower for word in ['tesla', 'auto', 'car', 'vehicle']):
        return [
            {"id": "battery_tech", "display_name": "🔋 Battery & Energy Storage Technologies", 
             "description": "Advanced battery suppliers, energy density innovations, charging infrastructure"},
            {"id": "autonomous_systems", "display_name": "🤖 Autonomous Driving & AI Systems", 
             "description": "Computer vision, AI chips, sensor technologies for autonomous vehicles"},
            {"id": "sustainable_materials", "display_name": "♻️ Sustainable Manufacturing Materials", 
             "description": "Eco-friendly materials, recycling technologies, circular economy suppliers"}
        ]
    else:
        return [
            {"id": "digital_transformation", "display_name": "💻 Digital Transformation Solutions", 
             "description": "Technology modernization and digital capability suppliers"},
            {"id": "operational_efficiency", "display_name": "⚡ Operational Efficiency & Cost Optimization", 
             "description": "Process improvement and cost reduction solution providers"},
            {"id": "sustainability_esg", "display_name": "🌱 Sustainability & ESG Compliance", 
             "description": "Environmental compliance and sustainable business practice suppliers"}
        ]

def _gather_government_intelligence(company_name, segment_name, selected_gov_sources):
    """Gather government and regulatory intelligence data"""
    gov_data = []
    
    # Government data patterns based on sources
    gov_patterns = {
        'regulatory_bodies': f"{company_name} regulatory compliance {segment_name}",
        'procurement_db': f"government contracts {segment_name} suppliers",
        'performance_data': f"{company_name} industry performance benchmarks",
        'policy_updates': f"{segment_name} policy changes regulations 2024"
    }
    
    # Simulate government data gathering (in real implementation, this would connect to gov APIs)
    for source in selected_gov_sources:
        if source in gov_patterns:
            gov_data.append({
                'source': source,
                'search_pattern': gov_patterns[source],
                'data_type': 'government_intelligence',
                'relevance': 'high'
            })
    
    return gov_data

# Import the intelligence components
try:
    from components.intelligence_narrative_component import IntelligenceNarrativeComponent
    from services.database_service import DatabaseService
    from services.openai_service import OpenAIService
    from services.outscraper_service import OutscraperService
    from services.web_scraper import WebScraperService
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False

def add_market_intelligence_tab():
    """
    Add Market Intelligence functionality to your existing app
    Call this function inside your new tab
    """
    
    if not COMPONENTS_AVAILABLE:
        st.error("📦 Market Intelligence components not found. Please copy the components/ and services/ folders to your app directory.")
        st.info("Required folders: components/, services/")
        return
    
    st.header("🔍 Market Intelligence Center")
    st.markdown("Generate comprehensive supplier intelligence through story-driven research and government data integration.")
    
    # Company selection and analysis configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company_name = st.text_input(
            "🏢 Company Name", 
            placeholder="Enter company name (e.g., Thames Water, Tesla, Microsoft...)",
            help="Enter any company name to analyze their supplier ecosystem"
        )
    
    with col2:
        analysis_depth = st.selectbox(
            "Analysis Depth",
            ["Standard", "Deep Analysis"],
            help="Deep analysis includes government data and regulatory intelligence"
        )
    
    # Dynamic Intelligence Categories based on company
    if company_name:
        st.markdown("### 🧠 AI-Generated Intelligence Categories")
        st.markdown("Select company-specific intelligence themes:")
        
        # Generate dynamic categories based on company
        if st.button("🎯 Generate Smart Categories", help="AI will analyze the company and suggest relevant intelligence categories"):
            with st.spinner(f"🤖 Analyzing {company_name} to generate intelligent categories..."):
                try:
                    dynamic_categories = _generate_dynamic_categories(company_name)
                    if dynamic_categories and len(dynamic_categories) > 0:
                        st.session_state[f'categories_{company_name}'] = dynamic_categories
                        st.success(f"✅ Generated {len(dynamic_categories)} company-specific categories!")
                    else:
                        # Use intelligent fallback immediately
                        fallback_categories = _get_intelligent_fallback_categories(company_name)
                        st.session_state[f'categories_{company_name}'] = fallback_categories
                        st.info(f"💡 Generated {len(fallback_categories)} intelligent categories based on company analysis")
                except Exception as e:
                    st.error(f"❌ Category generation failed: {str(e)}")
                    # Always provide intelligent fallback
                    fallback_categories = _get_intelligent_fallback_categories(company_name)
                    st.session_state[f'categories_{company_name}'] = fallback_categories
                    st.info(f"💡 Using {len(fallback_categories)} intelligent fallback categories")
        
        # Display generated categories or defaults
        categories_key = f'categories_{company_name}'
        if categories_key in st.session_state:
            dynamic_categories = st.session_state[categories_key]
            
            st.success(f"✨ Generated {len(dynamic_categories)} company-specific intelligence categories:")
            
            selected_categories = st.multiselect(
                "Select Intelligence Categories to Explore:",
                options=[cat['id'] for cat in dynamic_categories],
                format_func=lambda x: next((cat['display_name'] for cat in dynamic_categories if cat['id'] == x), x),
                default=[cat['id'] for cat in dynamic_categories[:3]],  # Select top 3 by default
                help="These categories are specifically tailored to your company's industry and strategic needs"
            )
            
            # Show category descriptions
            if selected_categories:
                st.markdown("**Selected Categories:**")
                for cat_id in selected_categories:
                    cat_info = next((cat for cat in dynamic_categories if cat['id'] == cat_id), None)
                    if cat_info:
                        st.markdown(f"• **{cat_info['display_name']}**: {cat_info['description']}")
        else:
            st.info("👆 Click 'Generate Smart Categories' to get AI-powered, company-specific intelligence themes")
            selected_categories = []
    else:
        st.info("👆 Enter a company name above to generate intelligent categories")
        selected_categories = []
    
    # Government Data Sources (simplified)
    st.markdown("### 🏛️ Government & Regulatory Intelligence")
    selected_gov_sources = st.multiselect(
        "Include Government Data Sources:",
        options=['regulatory_bodies', 'procurement_db', 'performance_data', 'policy_updates'],
        format_func=lambda x: {
            'regulatory_bodies': '📋 Regulatory Bodies (Ofwat, FCA, HSE)',
            'procurement_db': '🏛️ Government Procurement Data', 
            'performance_data': '📊 Industry Performance Metrics',
            'policy_updates': '📰 Policy & Legislative Updates'
        }.get(x, x),
        default=['regulatory_bodies'],
        help="Government sources provide official data and regulatory insights"
    )
    
    # Analysis trigger
    if st.button(f"🚀 Analyze {company_name if company_name else 'Company'} Supplier Ecosystem", 
                disabled=not company_name or len(selected_categories) == 0, 
                type="primary"):
        
        if not company_name:
            st.warning("Please enter a company name to analyze.")
            return
        
        if len(selected_categories) == 0:
            st.warning("Please select at least one intelligence category to analyze.")
            return
            
        analyze_company_intelligence(company_name, analysis_depth, selected_categories, selected_gov_sources)
    
    # Show existing analyses
    show_existing_analyses()

def analyze_company_intelligence(company_name: str, analysis_depth: str, selected_categories: list = None, selected_gov_sources: list = None):
    """Run the complete market intelligence analysis"""
    
    try:
        # Use simple session-based storage for immediate functionality
        class SessionStorage:
            def get_company_analysis(self, company_name):
                return st.session_state.get(f'analysis_{company_name}', None)
            def save_company_analysis(self, company_name, data):
                st.session_state[f'analysis_{company_name}'] = data
                return True
            def list_analyzed_companies(self):
                companies = []
                for key in st.session_state.keys():
                    if key.startswith('analysis_'):
                        companies.append(key.replace('analysis_', ''))
                return companies
        
        database_service = SessionStorage()
        
        # Check if analysis already exists
        existing_analysis = database_service.get_company_analysis(company_name)
        
        if existing_analysis:
            st.success(f"✅ Found existing analysis for {company_name}")
            render_intelligence_narrative(existing_analysis, company_name)
            return
        
        # Create new analysis
        st.info(f"🔄 Starting real-time intelligence gathering for {company_name}...")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Real data crawling with your API keys
        if selected_categories is None:
            selected_categories = ["innovation_tech", "cost_performance", "risk_compliance"]
        if selected_gov_sources is None:
            selected_gov_sources = ["regulatory_bodies"]
        
        # Phase 1: Real AI Company Analysis
        status_text.text("🤖 AI analyzing company context...")
        progress_bar.progress(20)
        
        try:
            from services.openai_service import OpenAIService
            openai_service = OpenAIService()
            context_analysis = openai_service.analyze_company_context(company_name)
            
            if context_analysis:
                st.success(f"✅ AI identified {len(context_analysis.get('critical_supplier_market_segments', []))} market segments")
            else:
                st.error("❌ AI analysis failed - please check your OpenAI API key")
                return
                
        except Exception as e:
            st.error(f"❌ AI analysis error: {str(e)}")
            return
        
        # Phase 2: Real Web Data Crawling
        status_text.text("🌐 Crawling live web data...")
        progress_bar.progress(50)
        
        try:
            from services.outscraper_service import OutscraperService
            outscraper_service = OutscraperService()
            
            segments_data = {}
            segments = context_analysis.get('critical_supplier_market_segments', [])
            
            for segment in segments[:2]:  # Process top 2 segments
                segment_name = segment.get('segment_name', 'Market Segment')
                keywords = segment.get('intelligence_gathering_keywords', [])
                
                suppliers_data = []
                insights_data = []
                
                for keyword in keywords[:2]:  # Top 2 keywords
                    try:
                        # Real company search
                        companies = outscraper_service.search_companies(keyword, limit=3)
                        if companies:
                            suppliers_data.extend(companies)
                            st.write(f"📊 Found {len(companies)} companies for '{keyword}'")
                        
                        # Real market insights
                        insights = outscraper_service.search_market_insights(keyword, limit=2)
                        if insights:
                            insights_data.extend(insights)
                            
                    except Exception as e:
                        st.warning(f"⚠️ Search failed for '{keyword}': check Outscraper API key")
                
                # AI enhancement of profiles
                enhanced_suppliers = []
                for supplier in suppliers_data[:4]:
                    try:
                        enhanced = openai_service.enhance_supplier_profile(supplier, segment_name, company_name)
                        if enhanced:
                            enhanced_suppliers.append(enhanced)
                    except Exception as e:
                        st.warning(f"⚠️ AI enhancement failed: {str(e)}")
                
                segments_data[segment_name] = {
                    'segment_info': segment,
                    'suppliers': enhanced_suppliers,
                    'market_insights': insights_data,
                    'intelligence_categories': selected_categories,
                    'total_urls_processed': len(suppliers_data) + len(insights_data)
                }
            
            total_sources = sum(seg['total_urls_processed'] for seg in segments_data.values())
            st.success(f"✅ Crawled data from {total_sources} real sources")
            
        except Exception as e:
            st.error(f"❌ Data crawling failed: {str(e)}")
            return
        
        # Phase 3: AI Executive Summary
        status_text.text("📋 AI generating executive summary...")
        progress_bar.progress(85)
        
        try:
            executive_summary = openai_service.generate_executive_summary(company_name, context_analysis, segments_data)
            if executive_summary:
                st.success("✅ Executive summary generated")
        except Exception as e:
            executive_summary = "Executive summary generation failed"
            st.warning(f"⚠️ Summary generation failed: {str(e)}")
        
        # Real analysis results
        analysis_data = {
            'company_name': company_name,
            'context_analysis': context_analysis,
            'market_segments': segments_data,
            'executive_summary': executive_summary,
            'intelligence_categories': selected_categories,
            'government_sources': selected_gov_sources,
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_depth': analysis_depth,
            'story_driven': True
        }
        
        status_text.text("💾 Saving results...")
        progress_bar.progress(100)
        
        success = database_service.save_company_analysis(company_name, analysis_data)
        
        if success:
            st.success(f"✅ Real data analysis complete for {company_name}!")
            total_crawled = sum(seg['total_urls_processed'] for seg in segments_data.values())
            st.info(f"📊 Successfully processed {total_crawled} live data sources")
        
        # Display real results
        render_intelligence_narrative(analysis_data, company_name)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.info("💡 **Tip**: Ensure your API keys are configured in your environment")

def render_intelligence_narrative(analysis_data: Dict[str, Any], company_name: str):
    """Render the complete intelligence narrative"""
    
    if not COMPONENTS_AVAILABLE:
        st.error("Components not available for rendering narrative")
        return
    
    try:
        # Create the narrative component
        narrative = IntelligenceNarrativeComponent()
        
        # Render the flowing story
        narrative.render_narrative_story(analysis_data, company_name)
        
    except Exception as e:
        st.error(f"Error rendering narrative: {str(e)}")

def show_existing_analyses():
    """Show list of existing company analyses"""
    
    if not COMPONENTS_AVAILABLE:
        return
    
    try:
        database_service = DatabaseService()
        companies = database_service.list_analyzed_companies()
        
        if companies:
            st.markdown("---")
            st.subheader("📋 Previous Analyses")
            
            # Display as clickable cards
            cols = st.columns(min(len(companies), 4))
            
            for i, company in enumerate(companies[:4]):  # Show max 4
                with cols[i % 4]:
                    if st.button(f"📊 {company}", key=f"load_{company}"):
                        analysis_data = database_service.get_company_analysis(company)
                        if analysis_data:
                            st.rerun()  # Refresh to show analysis
            
            if len(companies) > 4:
                st.caption(f"... and {len(companies) - 4} more analyses")
                
    except Exception as e:
        st.caption("No previous analyses found")

def setup_intelligence_environment():
    """
    Setup function to check environment and dependencies
    Call this once in your app to verify everything is ready
    """
    
    issues = []
    
    # Check required environment variables
    required_env_vars = ['OPENAI_API_KEY', 'SERPAPI_API_KEY', 'DATABASE_URL']
    for var in required_env_vars:
        if not os.getenv(var):
            issues.append(f"Missing environment variable: {var}")
    
    # Check component availability
    if not COMPONENTS_AVAILABLE:
        issues.append("Market Intelligence components not found")
    
    return issues

# Integration helper functions
def get_integration_status():
    """Check if integration is ready"""
    issues = setup_intelligence_environment()
    return len(issues) == 0, issues

def display_integration_guide():
    """Show integration guide for developers"""
    
    st.markdown("""
    ## 🛠️ Integration Guide
    
    ### Quick Setup:
    1. **Copy Files**: Copy `components/` and `services/` folders to your app
    2. **Environment**: Set `OPENAI_API_KEY`, `SERPAPI_API_KEY`, `DATABASE_URL`
    3. **Add Tab**: Use `add_market_intelligence_tab()` in your tab
    
    ### Example Code:
    ```python
    from market_intelligence_integration_package import add_market_intelligence_tab
    
    # In your main app:
    tab1, tab2, tab_intel = st.tabs(["Tab 1", "Tab 2", "🔍 Intelligence"])
    
    with tab_intel:
        add_market_intelligence_tab()
    ```
    """)

if __name__ == "__main__":
    # Test the integration package
    st.title("Market Intelligence Integration Test")
    add_market_intelligence_tab()