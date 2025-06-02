import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Dict, Any, List, Optional
from services.openai_service import OpenAIService
from services.serpapi_service import SerpAPIService
from services.web_scraper import WebScraper
from services.segment_template_service import SegmentTemplateService
from components.supplier_profile import SupplierProfileComponent
from components.market_intelligence_story import MarketIntelligenceStoryComponent
from components.market_intelligence_dashboard import MarketIntelligenceDashboard as MIDashboard
from utils.helpers import format_timestamp, calculate_analysis_progress
import time

logger = logging.getLogger(__name__)

class MarketIntelligenceDashboard:
    """Main dashboard component for Market Intelligence application"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.supplier_profile = SupplierProfileComponent()
        self.story_component = MarketIntelligenceStoryComponent()
        self.template_service = SegmentTemplateService()
        self.intelligence_dashboard = MIDashboard(data_manager)
        
        # Initialize services
        try:
            self.openai_service = OpenAIService()
            self.serpapi_service = SerpAPIService()
            self.web_scraper = WebScraper()
        except ValueError as e:
            st.error(f"Service initialization error: {e}")
            st.error("Please ensure API keys are properly configured in Replit Secrets.")
            st.stop()
    
    def render(self):
        """Render the main dashboard"""
        # Header
        st.title("🔍 Market Intelligence Platform")
        st.markdown("### Strategic Insights for Supplier Ecosystem Analysis")
        
        # Sidebar
        self._render_sidebar()
        
        # Main content area - Show question-answer narrative when company is selected
        if 'current_analysis' in st.session_state and st.session_state.current_analysis:
            self._render_analysis_dashboard()
        else:
            # Show available companies or welcome screen
            companies = self.data_manager.list_analyzed_companies()
            if companies:
                st.info("👆 Select a company from the sidebar to see the question-answer intelligence narrative")
                
                # Show preview of available analyses
                st.subheader("📊 Available Intelligence Reports")
                for company in companies:
                    if st.button(f"🔍 View {company} Analysis", key=f"view_{company}"):
                        analysis = self.data_manager.get_company_analysis(company)
                        if analysis:
                            st.session_state.current_analysis = analysis
                            st.rerun()
            else:
                self._render_welcome_screen()
    
    def _render_sidebar(self):
        """Render sidebar with controls and company analysis"""
        with st.sidebar:
            st.header("🎯 Analysis Control")
            
            # Company input
            company_name = st.text_input(
                "Enter Context Company Name:",
                placeholder="e.g., Thames Water, Microsoft, Tesla",
                help="Enter the name of the company you want to analyze"
            )
            
            # Analysis settings
            with st.expander("⚙️ Analysis Settings"):
                num_results = st.selectbox(
                    "Search Results per Keyword:",
                    [10, 20, 30, 50],
                    index=1,
                    help="Number of search results to process per keyword"
                )
                
                analysis_depth = st.selectbox(
                    "Analysis Depth:",
                    ["Standard", "Deep"],
                    help="Standard: Basic analysis, Deep: Extended scraping and analysis"
                )
            
            # Generate report button
            if st.button("🚀 Generate Comprehensive Market Intelligence Report", type="primary"):
                if company_name.strip():
                    self._start_analysis(company_name.strip(), num_results, analysis_depth)
                else:
                    st.error("Please enter a company name")
            
            # Display current analysis info
            if 'current_analysis' in st.session_state and st.session_state.current_analysis:
                st.divider()
                self._render_analysis_summary()
            
            # Previous analyses
            self._render_previous_analyses()
            
            # Sample data generation (for demonstration)
            st.divider()
            st.subheader("🎯 Demo Features")
            if st.button("Generate Sample Data", help="Create sample analyses to see dashboard features"):
                self._generate_sample_data()
    
    def _render_analysis_summary(self):
        """Render current analysis summary in sidebar"""
        analysis = st.session_state.current_analysis
        
        st.subheader("📊 Current Analysis")
        
        # Company info
        context = analysis.get("context_analysis", {})
        if context:
            st.write(f"**Company:** {context.get('context_company_name', 'Unknown')}")
            st.write(f"**Industry:** {context.get('identified_industry', 'Unknown')}")
            
            # Analysis timestamp
            timestamp = analysis.get("analysis_timestamp")
            if timestamp:
                st.write(f"**Generated:** {format_timestamp(timestamp)}")
        
        # Progress indicator
        progress = calculate_analysis_progress(analysis)
        st.progress(progress, text=f"Analysis {int(progress * 100)}% complete")
    
    def _render_previous_analyses(self):
        """Render list of previous analyses"""
        companies = self.data_manager.list_analyzed_companies()
        
        if companies:
            st.divider()
            st.subheader("📂 Previous Analyses")
            
            selected_company = st.selectbox(
                "Load Previous Analysis:",
                [""] + companies,
                format_func=lambda x: "Select..." if x == "" else x
            )
            
            if selected_company and selected_company != "":
                if st.button(f"Load {selected_company}", key=f"load_{selected_company}"):
                    self._load_previous_analysis(selected_company)
    
    def _render_welcome_screen(self):
        """Render welcome screen when no analysis is loaded"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ## Welcome to Market Intelligence Platform
            
            ### 🎯 What This Platform Does:
            
            **🔍 Company Context Analysis**
            - Identifies industry and market segments
            - Analyzes strategic supplier requirements
            
            **🌐 Intelligence Gathering**
            - Automated web research via advanced search
            - Discovers potential suppliers and key players
            
            **🤖 AI-Powered Analysis**
            - Comprehensive supplier profiling
            - ESG and innovation assessment
            - Market trend analysis
            
            **📊 Interactive Dashboard**
            - Professional data visualization
            - Detailed supplier comparisons
            - Export capabilities
            
            ### 🚀 Get Started:
            Enter a company name in the sidebar to begin your comprehensive market intelligence analysis.
            """)
        
        # Display storage statistics
        self._render_storage_stats()
    
    def _render_storage_stats(self):
        """Render storage statistics"""
        stats = self.data_manager.get_storage_stats()
        
        if "error" not in stats:
            st.divider()
            st.subheader("📈 Platform Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Companies Analyzed", stats.get("total_companies", 0))
            
            with col2:
                st.metric("Market Segments", stats.get("total_market_segments", 0))
            
            with col3:
                st.metric("Suppliers Profiled", stats.get("total_suppliers", 0))
            
            with col4:
                st.metric("Data Size (MB)", stats.get("file_size_mb", 0))
    
    def _start_analysis(self, company_name: str, num_results: int, analysis_depth: str):
        """Start comprehensive market intelligence analysis"""
        # Check if analysis already exists
        existing_analysis = self.data_manager.get_company_analysis(company_name)
        if existing_analysis:
            if st.sidebar.checkbox(f"Analysis for {company_name} exists. Overwrite?"):
                pass
            else:
                st.session_state.current_analysis = existing_analysis
                st.rerun()
                return
        
        # Initialize progress tracking
        progress_bar = st.sidebar.progress(0, text="Starting analysis...")
        status_text = st.sidebar.empty()
        
        try:
            # Phase 1: Company Context Analysis
            status_text.text("Phase 1: Analyzing company context...")
            progress_bar.progress(0.1, text="Analyzing company context...")
            
            context_analysis = self.openai_service.analyze_company_context(company_name, self.template_service)
            if not context_analysis:
                st.error("Failed to analyze company context. Please check your OpenAI API key and try again.")
                return
            
            # Initialize analysis data structure
            analysis_data = {
                "context_analysis": context_analysis,
                "market_segments": {},
                "executive_summary": "",
                "analysis_settings": {
                    "num_results": num_results,
                    "analysis_depth": analysis_depth
                }
            }
            
            # Phase 2 & 3: Process each market segment
            segments = context_analysis.get("critical_supplier_market_segments", [])
            total_segments = len(segments)
            
            for i, segment in enumerate(segments):
                segment_name = segment.get("segment_name", f"Segment {i+1}")
                
                # Update progress
                base_progress = 0.1 + (i / total_segments) * 0.7
                progress_bar.progress(base_progress, text=f"Processing {segment_name}...")
                status_text.text(f"Phase 2-3: Processing {segment_name} ({i+1}/{total_segments})")
                
                # Process segment
                segment_data = self._process_market_segment(
                    segment, num_results, analysis_depth == "Deep", progress_bar, base_progress
                )
                
                analysis_data["market_segments"][segment_name] = segment_data
            
            # Phase 4: Generate Executive Summary
            status_text.text("Phase 4: Generating executive summary...")
            progress_bar.progress(0.9, text="Generating executive summary...")
            
            executive_summary = self.openai_service.generate_executive_summary(analysis_data)
            analysis_data["executive_summary"] = executive_summary
            
            # Phase 5: Save and Display
            status_text.text("Phase 5: Saving analysis...")
            progress_bar.progress(0.95, text="Saving analysis...")
            
            # Save analysis
            if self.data_manager.save_company_analysis(company_name, analysis_data):
                st.session_state.current_analysis = analysis_data
                
                progress_bar.progress(1.0, text="Analysis complete!")
                status_text.text("✅ Analysis completed successfully!")
                
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to save analysis data")
        
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            st.error(f"Analysis failed: {str(e)}")
        finally:
            # Clean up progress indicators
            time.sleep(2)
            progress_bar.empty()
            status_text.empty()
    
    def _process_market_segment(self, segment: Dict[str, Any], num_results: int, 
                              deep_analysis: bool, progress_bar, base_progress: float) -> Dict[str, Any]:
        """Process individual market segment"""
        segment_name = segment.get("segment_name", "Unknown Segment")
        keywords = segment.get("intelligence_gathering_keywords", [])
        
        segment_data = {
            "segment_info": segment,
            "search_results": [],
            "suppliers": [],
            "market_insights": [],
            "total_urls_processed": 0,
            "processing_timestamp": time.time()
        }
        
        try:
            # Phase 2: Web Intelligence Gathering
            search_results = self.serpapi_service.search_market_intelligence(keywords, num_results)
            high_quality_results = self.serpapi_service.filter_high_quality_results(search_results)
            
            segment_data["search_results"] = high_quality_results
            
            # Phase 3: Content Analysis
            max_urls = 15 if deep_analysis else 8
            processed_count = 0
            
            for result in high_quality_results[:max_urls]:
                try:
                    # Update progress within segment
                    segment_progress = base_progress + (processed_count / max_urls) * 0.05
                    progress_bar.progress(segment_progress, text=f"Analyzing content from {result.get('source', 'unknown')}...")
                    
                    # Scrape content
                    if result.get('result_type') == 'company_website':
                        content_data = self.web_scraper.scrape_company_subpages(result['link'], 2 if deep_analysis else 1)
                        if content_data and content_data.get('pages'):
                            # Combine content from all pages
                            combined_content = ""
                            for page_content in content_data['pages'].values():
                                combined_content += page_content.get('content', '') + "\n\n"
                            
                            # AI analysis for supplier
                            supplier_profile = self.openai_service.analyze_supplier_content(
                                combined_content, segment_name
                            )
                            if supplier_profile:
                                supplier_profile['source_url'] = result['link']
                                supplier_profile['domain'] = result.get('source', '')
                                segment_data["suppliers"].append(supplier_profile)
                    else:
                        # Regular content scraping for market insights
                        content_data = self.web_scraper.scrape_url_content(result['link'])
                        if content_data:
                            market_insight = self.openai_service.analyze_market_content(
                                content_data['content'], segment_name
                            )
                            if market_insight:
                                market_insight['source_url'] = result['link']
                                market_insight['source_title'] = result.get('title', '')
                                segment_data["market_insights"].append(market_insight)
                    
                    processed_count += 1
                    segment_data["total_urls_processed"] = processed_count
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error processing URL {result.get('link', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Processed segment '{segment_name}': {len(segment_data['suppliers'])} suppliers, {len(segment_data['market_insights'])} insights")
            
        except Exception as e:
            logger.error(f"Error processing market segment '{segment_name}': {e}")
        
        return segment_data
    
    def _load_previous_analysis(self, company_name: str):
        """Load previous analysis from storage"""
        analysis = self.data_manager.get_company_analysis(company_name)
        if analysis:
            st.session_state.current_analysis = analysis
            st.sidebar.success(f"Loaded analysis for {company_name}")
            st.rerun()
        else:
            st.sidebar.error(f"Failed to load analysis for {company_name}")
    
    def _render_analysis_dashboard(self):
        """Render the main analysis dashboard"""
        analysis = st.session_state.current_analysis
        context = analysis.get("context_analysis", {})
        
        # Dashboard header
        company_name = context.get("context_company_name", "Unknown Company")
        st.header(f"📊 Market Intelligence Report: {company_name}")
        
        # Create question-answer narrative tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "❓ Who Are We Analyzing?", 
            "🔍 What Technologies Matter?", 
            "🏢 Who Are The Key Players?", 
            "📊 How Do They Compare?", 
            "💡 What Should We Do?"
        ])
        
        with tab1:
            # Single flowing narrative with 5 sections
            self._render_question_who_analyzing(analysis, company_name)
            st.divider()
            self._render_question_what_technologies(analysis)
            st.divider()
            self._render_question_key_players(analysis)
            st.divider()
            self._render_question_how_compare(analysis)
            st.divider()
            self._render_question_what_to_do(analysis, company_name)
        
        with tab2:
            # Technology Ecosystem - Innovation Landscape & Tech Trends
            self._render_question_what_technologies(analysis)
        
        with tab3:
            # Supplier Landscape - Company Profiles & Market Positioning
            self._render_question_key_players(analysis)
        
        with tab4:
            # Market Intelligence - Data Analytics & Competitive Intelligence
            self._render_question_how_compare(analysis)
        
        with tab5:
            # Strategic Insights - Executive Summary & Actionable Intelligence
            self._render_question_what_to_do(analysis, company_name)
    
    def _render_market_intelligence_overview(self):
        """Render the Market Intelligence overview tab"""
        # Render the comprehensive Market Intelligence dashboard without duplicate header
        self.intelligence_dashboard.render_market_intelligence_tab()
    
    def _generate_sample_data(self):
        """Generate sample data for demonstration"""
        try:
            from utils.mock_data_generator import MockDataGenerator
            generator = MockDataGenerator(self.data_manager)
            
            with st.spinner("Generating sample market intelligence data..."):
                success = generator.generate_mock_data()
            
            if success:
                st.success("✅ Sample data generated successfully! The Market Intelligence dashboard is now populated with demo data.")
                st.info("🔄 Refresh the page to see the Market Intelligence tab with visual analytics.")
                st.rerun()
            else:
                st.error("Failed to generate sample data.")
                
        except Exception as e:
            st.error(f"Error generating sample data: {str(e)}")
            logger.error(f"Sample data generation error: {e}")
    
    def _render_question_who_analyzing(self, analysis: Dict[str, Any], company_name: str):
        """❓ Who Are We Analyzing? - Target Company Intelligence Brief"""
        st.markdown("# ❓ Who Are We Analyzing?")
        
        context = analysis.get("context_analysis", {})
        industry = context.get("identified_industry", "Unknown Industry")
        
        # The Question
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
        
        # The Question
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
        
        # The Question
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
        
        # The Question
        st.markdown("## 🎯 The Strategic Question")
        st.info("**How do suppliers compare across key performance metrics and what patterns emerge?**")
        
        # The Answer - Comparative Analysis
        st.markdown("## 📊 The Answer")
        
        # Use the existing market intelligence dashboard for comparative analytics
        self.intelligence_dashboard.render_market_intelligence_tab()
    
    def _render_question_what_to_do(self, analysis: Dict[str, Any], company_name: str):
        """💡 What Should We Do? - Strategic Recommendations"""
        st.markdown("# 💡 What Should We Do?")
        
        # The Question
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
                    csv_data = self.data_manager.export_company_data_csv(company_name)
                    if csv_data:
                        st.download_button(
                            "Download Intelligence Report",
                            csv_data,
                            f"{company_name}_market_intelligence.csv",
                            "text/csv"
                        )
            
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
    
    def _render_mission_overview(self, analysis: Dict[str, Any], company_name: str):
        """Mission Overview - Company Context & Strategic Goals"""
        st.subheader(f"🚀 Mission Overview: {company_name}")
        
        context = analysis.get("context_analysis", {})
        industry = context.get("identified_industry", "Unknown Industry")
        
        # Company Intelligence Brief
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Strategic Intelligence Mission")
            st.info(f"""
            **Target Company**: {company_name}  
            **Industry Focus**: {industry}  
            **Mission**: Identify and analyze critical supplier ecosystem to enhance competitive positioning and strategic partnerships.
            """)
            
            # Strategic Questions this analysis will answer
            st.markdown("### 🔍 Key Intelligence Questions")
            questions = [
                "Who are the most innovative suppliers in each technology segment?",
                "What emerging technologies are reshaping the supplier landscape?", 
                "Which suppliers offer the best strategic partnership opportunities?",
                "How do supplier capabilities align with our growth objectives?"
            ]
            for q in questions:
                st.markdown(f"• {q}")
        
        with col2:
            # Analysis scope and segments
            segments = context.get("critical_supplier_market_segments", [])
            if segments:
                st.markdown("### 📊 Analysis Scope")
                st.metric("Market Segments", len(segments))
                
                with st.expander("View Market Segments"):
                    for segment in segments:
                        st.markdown(f"**{segment.get('segment_name', 'Unknown')}**")
                        st.caption(segment.get('segment_definition_and_strategic_relevance', ''))
    
    def _render_technology_ecosystem(self, analysis: Dict[str, Any]):
        """Technology Ecosystem - Innovation Landscape & Tech Trends"""
        st.subheader("🔧 Technology Ecosystem Analysis")
        
        # Technology Innovation Dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚀 Innovation Trends")
            # Extract technology trends from all segments
            segments = analysis.get("market_segments", {})
            all_technologies = []
            
            for segment_name, segment_data in segments.items():
                suppliers = segment_data.get("suppliers", [])
                for supplier in suppliers:
                    tech_diff = supplier.get("technological_differentiators", [])
                    if isinstance(tech_diff, list):
                        all_technologies.extend(tech_diff)
            
            # Technology frequency analysis
            if all_technologies:
                tech_counts = {}
                for tech in all_technologies:
                    tech_counts[tech] = tech_counts.get(tech, 0) + 1
                
                # Show top technologies
                sorted_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                
                for tech, count in sorted_tech:
                    st.markdown(f"**{tech}** - {count} suppliers")
            else:
                st.info("Technology analysis will appear here as supplier data is gathered")
        
        with col2:
            st.markdown("### 📈 Innovation Metrics")
            # Innovation scoring across segments
            segments = analysis.get("market_segments", {})
            innovation_scores = []
            
            for segment_name, segment_data in segments.items():
                suppliers = segment_data.get("suppliers", [])
                segment_avg = 0
                if suppliers:
                    scores = [s.get("innovation_index", 0) for s in suppliers if s.get("innovation_index")]
                    segment_avg = sum(scores) / len(scores) if scores else 0
                
                if segment_avg > 0:
                    st.metric(f"{segment_name}", f"{segment_avg:.1f}/10")
                    innovation_scores.append(segment_avg)
            
            if innovation_scores:
                overall_innovation = sum(innovation_scores) / len(innovation_scores)
                st.metric("Overall Innovation Index", f"{overall_innovation:.1f}/10")
    
    def _render_supplier_landscape(self, analysis: Dict[str, Any]):
        """Supplier Landscape - Company Profiles & Market Positioning"""
        st.subheader("🏭 Supplier Landscape Analysis")
        
        segments = analysis.get("market_segments", {})
        
        # Supplier Excellence Matrix
        all_suppliers = []
        for segment_name, segment_data in segments.items():
            suppliers = segment_data.get("suppliers", [])
            for supplier in suppliers:
                supplier["segment"] = segment_name
                all_suppliers.append(supplier)
        
        if all_suppliers:
            # Top performers across all segments
            st.markdown("### 🌟 Top Performing Suppliers")
            
            # Sort by relevance score
            top_suppliers = sorted(all_suppliers, 
                                 key=lambda x: x.get("relevance_score", 0), 
                                 reverse=True)[:5]
            
            for i, supplier in enumerate(top_suppliers):
                with st.expander(f"#{i+1} {supplier.get('company_name', 'Unknown')} - {supplier.get('segment', '')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Relevance Score", f"{supplier.get('relevance_score', 0):.1f}")
                    with col2:
                        st.metric("Innovation Index", f"{supplier.get('innovation_index', 0):.1f}")
                    with col3:
                        st.metric("ESG Rating", f"{supplier.get('esg_rating', 0):.1f}")
                    
                    st.markdown(f"**Overview**: {supplier.get('overview', 'No overview available')}")
            
            # Segment-by-segment analysis
            st.markdown("### 📊 Segment Analysis")
            
            for segment_name, segment_data in segments.items():
                suppliers = segment_data.get("suppliers", [])
                if suppliers:
                    with st.expander(f"{segment_name} - {len(suppliers)} suppliers"):
                        self.supplier_profile.render_all_profiles(suppliers)
        else:
            st.info("Supplier profiles will appear here as market intelligence is gathered")
    
    def _render_strategic_insights(self, analysis: Dict[str, Any], company_name: str):
        """Strategic Insights - Executive Summary & Actionable Intelligence"""
        st.subheader("💼 Strategic Intelligence Report")
        
        # Executive Summary
        executive_summary = analysis.get("executive_summary", "")
        if executive_summary:
            st.markdown("### 📋 Executive Summary")
            st.markdown(executive_summary)
        
        # Key Recommendations
        st.markdown("### 🎯 Strategic Recommendations")
        
        segments = analysis.get("market_segments", {})
        all_suppliers = []
        for segment_data in segments.values():
            all_suppliers.extend(segment_data.get("suppliers", []))
        
        if all_suppliers:
            # Generate strategic insights based on analysis
            top_innovation = max(all_suppliers, key=lambda x: x.get("innovation_index", 0))
            top_relevance = max(all_suppliers, key=lambda x: x.get("relevance_score", 0))
            
            recommendations = [
                f"**Partnership Priority**: {top_relevance.get('company_name')} shows highest strategic relevance ({top_relevance.get('relevance_score', 0):.1f}/10)",
                f"**Innovation Leader**: {top_innovation.get('company_name')} leads in innovation capabilities ({top_innovation.get('innovation_index', 0):.1f}/10)",
                f"**Market Coverage**: Analysis covers {len(segments)} critical market segments with {len(all_suppliers)} total suppliers",
                "**Next Steps**: Initiate contact with top-tier suppliers for partnership discussions"
            ]
            
            for rec in recommendations:
                st.markdown(f"• {rec}")
        
        # Export capabilities
        st.markdown("### 📤 Intelligence Export")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export Analysis"):
                csv_data = self.data_manager.export_company_data_csv(company_name)
                if csv_data:
                    st.download_button(
                        "Download CSV Report",
                        csv_data,
                        f"{company_name}_intelligence_report.csv",
                        "text/csv"
                    )
        
        with col2:
            if st.button("🔄 Update Analysis"):
                st.info("Re-run analysis to gather fresh market intelligence")
    
    def _render_executive_summary(self, analysis: Dict[str, Any]):
        """Render executive summary section"""
        st.subheader("🎯 Executive Summary")
        
        context = analysis.get("context_analysis", {})
        
        # Industry overview
        with st.expander("📈 Industry Context", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Industry:** {context.get('identified_industry', 'Unknown')}")
                st.write(context.get('strategic_industry_overview', 'No overview available'))
            
            with col2:
                # Analysis metadata
                timestamp = analysis.get("analysis_timestamp")
                if timestamp:
                    st.write(f"**Generated:** {format_timestamp(timestamp)}")
                
                settings = analysis.get("analysis_settings", {})
                if settings:
                    st.write(f"**Depth:** {settings.get('analysis_depth', 'Standard')}")
                    st.write(f"**Results per Keyword:** {settings.get('num_results', 20)}")
        
        # AI-generated summary
        summary = analysis.get("executive_summary", "")
        if summary:
            st.markdown("### 🧠 Strategic Insights")
            st.markdown(summary)
        else:
            st.info("Executive summary not available for this analysis.")
    
    def _render_market_segments(self, analysis: Dict[str, Any]):
        """Render market segments analysis"""
        segments = analysis.get("market_segments", {})
        
        if not segments:
            st.warning("No market segments analyzed")
            return
        
        st.subheader("🎯 Market Segment Analysis")
        
        # Segment selector
        segment_names = list(segments.keys())
        selected_segment = st.selectbox(
            "Select Market Segment:",
            segment_names,
            key="segment_selector"
        )
        
        if selected_segment:
            segment_data = segments[selected_segment]
            self._render_segment_detail(selected_segment, segment_data)
    
    def _render_segment_detail(self, segment_name: str, segment_data: Dict[str, Any]):
        """Render detailed view of a market segment"""
        segment_info = segment_data.get("segment_info", {})
        suppliers = segment_data.get("suppliers", [])
        market_insights = segment_data.get("market_insights", [])
        
        # Segment overview
        with st.expander("📋 Segment Overview", expanded=True):
            st.write(f"**Segment:** {segment_name}")
            st.write(segment_info.get("segment_definition_and_strategic_relevance", "No description available"))
            
            # Processing stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Suppliers Found", len(suppliers))
            with col2:
                st.metric("Market Insights", len(market_insights))
            with col3:
                st.metric("URLs Processed", segment_data.get("total_urls_processed", 0))
        
        # Suppliers analysis
        if suppliers:
            self._render_suppliers_table(suppliers)
        
        # Market insights
        if market_insights:
            self._render_market_insights(market_insights)
    
    def _render_suppliers_table(self, suppliers: List[Dict[str, Any]]):
        """Render interactive suppliers table"""
        st.subheader("🏢 Key Players & Potential Suppliers")
        
        # Create DataFrame for table
        table_data = []
        for supplier in suppliers:
            table_data.append({
                "Company": supplier.get("company_name", "Unknown"),
                "Relevance": supplier.get("relevance_score", 0),
                "Innovation": supplier.get("innovation_index", 0),
                "ESG Rating": supplier.get("esg_rating", 0),
                "Domain": supplier.get("domain", ""),
                "Key Technologies": ", ".join(supplier.get("technological_differentiators", [])[:3])
            })
        
        if table_data:
            df = pd.DataFrame(table_data)
            
            # Interactive table with sorting
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Relevance": st.column_config.ProgressColumn(
                        "Relevance Score",
                        help="AI-assessed relevance to segment",
                        min_value=0,
                        max_value=10,
                    ),
                    "Innovation": st.column_config.ProgressColumn(
                        "Innovation Index",
                        help="AI-assessed innovation level",
                        min_value=0,
                        max_value=10,
                    ),
                    "ESG Rating": st.column_config.ProgressColumn(
                        "ESG Rating",
                        help="AI-assessed ESG profile",
                        min_value=0,
                        max_value=10,
                    ),
                    "Domain": st.column_config.LinkColumn(
                        "Website",
                        help="Company website",
                    ),
                }
            )
            
            # Detailed supplier profiles
            if st.button("📊 View Detailed Supplier Profiles"):
                self.supplier_profile.render_all_profiles(suppliers)
        
        # Visualizations
        self._render_supplier_visualizations(suppliers)
    
    def _render_supplier_visualizations(self, suppliers: List[Dict[str, Any]]):
        """Render supplier data visualizations"""
        if not suppliers:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Relevance vs Innovation scatter plot
            df = pd.DataFrame([
                {
                    "Company": s.get("company_name", "Unknown"),
                    "Relevance": s.get("relevance_score", 0),
                    "Innovation": s.get("innovation_index", 0),
                    "ESG": s.get("esg_rating", 0)
                }
                for s in suppliers
            ])
            
            fig = px.scatter(
                df, 
                x="Relevance", 
                y="Innovation",
                size="ESG",
                hover_name="Company",
                title="Supplier Positioning: Relevance vs Innovation",
                labels={"Relevance": "Relevance Score", "Innovation": "Innovation Index"}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top technologies bar chart
            all_techs = []
            for supplier in suppliers:
                techs = supplier.get("technological_differentiators", [])
                all_techs.extend(techs[:3])  # Top 3 per supplier
            
            if all_techs:
                tech_counts = pd.Series(all_techs).value_counts().head(10)
                
                fig = px.bar(
                    x=tech_counts.values,
                    y=tech_counts.index,
                    orientation='h',
                    title="Most Common Technologies",
                    labels={"x": "Frequency", "y": "Technology"}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_market_insights(self, insights: List[Dict[str, Any]]):
        """Render market insights section"""
        st.subheader("📰 Market Intelligence & Trends")
        
        for i, insight in enumerate(insights[:5]):  # Show top 5 insights
            with st.expander(f"Insight {i+1}: {insight.get('source_title', 'Market Analysis')[:60]}..."):
                
                # Overview
                overview = insight.get("segment_overview", "")
                if overview:
                    st.write("**Market Overview:**")
                    st.write(overview)
                
                # Trends
                trends = insight.get("market_trends", [])
                if trends:
                    st.write("**Key Trends:**")
                    for trend in trends[:3]:
                        st.write(f"• {trend}")
                
                # Future outlook
                outlook = insight.get("future_outlook", "")
                if outlook:
                    st.write("**Future Outlook:**")
                    st.write(outlook)
                
                # Source
                source_url = insight.get("source_url", "")
                if source_url:
                    st.write(f"**Source:** [{source_url}]({source_url})")
    
    def _render_export_section(self, company_name: str):
        """Render data export and management section"""
        st.divider()
        st.subheader("📤 Export & Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export Supplier Data (CSV)"):
                csv_data = self.data_manager.export_company_data_csv(company_name)
                if csv_data:
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"{company_name}_suppliers.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("Failed to export data")
        
        with col2:
            if st.button("🔄 Refresh Analysis"):
                if st.checkbox("Confirm refresh (this will overwrite current data)"):
                    # Clear current analysis and trigger new one
                    if 'current_analysis' in st.session_state:
                        del st.session_state.current_analysis
                    st.rerun()
        
        with col3:
            if st.button("🗑️ Delete Analysis"):
                if st.checkbox("Confirm deletion"):
                    self.data_manager.delete_company_analysis(company_name)
                    if 'current_analysis' in st.session_state:
                        del st.session_state.current_analysis
                    st.success("Analysis deleted")
                    st.rerun()
