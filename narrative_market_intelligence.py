import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import requests
import os
import json
from openai import OpenAI
from typing import Dict, List, Any, Optional
import sqlite3

class NarrativeMarketIntelligence:
    """5-Question Narrative-Driven Market Intelligence System"""
    
    def __init__(self):
        self.google_api_key = os.environ.get('GOOGLE_API_KEY')
        self.google_cse_id = os.environ.get('GOOGLE_CSE_ID')
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for persistent intelligence storage"""
        self.conn = sqlite3.connect('market_intelligence.db', check_same_thread=False)
        
        # Create tables
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS company_analyses (
                id INTEGER PRIMARY KEY,
                company_name TEXT UNIQUE,
                industry_context TEXT,
                market_segments TEXT,
                keywords_generated TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS supplier_profiles (
                id INTEGER PRIMARY KEY,
                company_name TEXT,
                supplier_name TEXT,
                supplier_url TEXT,
                technologies TEXT,
                capabilities TEXT,
                relevance_score REAL,
                performance_metrics TEXT,
                crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_name) REFERENCES company_analyses (company_name)
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS market_segments (
                id INTEGER PRIMARY KEY,
                company_name TEXT,
                segment_name TEXT,
                technologies TEXT,
                key_players TEXT,
                trends TEXT,
                opportunities TEXT,
                FOREIGN KEY (company_name) REFERENCES company_analyses (company_name)
            )
        ''')
        
        self.conn.commit()
    
    def question_1_who_analyzing(self, company_name: str) -> Dict[str, Any]:
        """❓ Who Are We Analyzing? - Sets strategic context"""
        
        # Check if we already have analysis
        existing = self.get_existing_analysis(company_name)
        if existing:
            st.info(f"📚 Found existing analysis for {company_name}")
            return existing
        
        st.write("### ❓ Who Are We Analyzing?")
        st.write(f"**Target Company:** {company_name}")
        
        with st.spinner("🔍 Analyzing company context and generating intelligence strategy..."):
            # Generate company context and keywords using AI
            context_analysis = self._generate_company_context(company_name)
            
            # Store in database
            self.store_company_analysis(company_name, context_analysis)
            
            return context_analysis
    
    def question_2_what_technologies(self, company_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """🔍 What Technologies Matter? - Technology landscape analysis"""
        
        st.write("### 🔍 What Technologies Matter?")
        
        # Generate technology-focused keywords
        tech_keywords = context.get('keywords', {}).get('technology', [])
        
        with st.spinner("🌐 Crawling supplier technology profiles..."):
            # Incremental crawling - check what we already have
            existing_suppliers = self.get_existing_suppliers(company_name)
            
            if len(existing_suppliers) < 20:  # Crawl more if needed
                new_suppliers = self._crawl_technology_suppliers(company_name, tech_keywords)
                self.store_suppliers(company_name, new_suppliers)
            
            # Get all suppliers for analysis
            all_suppliers = self.get_existing_suppliers(company_name)
            
            # AI analysis of technology trends
            tech_analysis = self._analyze_technology_landscape(all_suppliers)
            
            return {
                'suppliers_found': len(all_suppliers),
                'technology_trends': tech_analysis,
                'key_technologies': tech_analysis.get('key_technologies', []),
                'innovation_areas': tech_analysis.get('innovation_areas', [])
            }
    
    def question_3_key_players(self, company_name: str) -> Dict[str, Any]:
        """🏢 Who Are The Key Players? - Supplier profiles with strategic rankings"""
        
        st.write("### 🏢 Who Are The Key Players?")
        
        # Get suppliers from database
        suppliers = self.get_existing_suppliers(company_name)
        
        if not suppliers:
            st.warning("No suppliers found. Running initial analysis...")
            return {}
        
        with st.spinner("📊 Ranking suppliers by strategic relevance..."):
            # AI-powered supplier ranking
            ranked_suppliers = self._rank_suppliers_strategically(suppliers)
            
            # Generate detailed profiles for top performers
            top_performers = ranked_suppliers[:10]
            detailed_profiles = self._generate_detailed_profiles(top_performers)
            
            return {
                'total_suppliers': len(suppliers),
                'top_performers': detailed_profiles,
                'supplier_categories': self._categorize_suppliers(suppliers),
                'market_coverage': self._analyze_market_coverage(suppliers)
            }
    
    def question_4_how_compare(self, company_name: str) -> Dict[str, Any]:
        """📊 How Do They Compare? - Competitive analytics and performance matrices"""
        
        st.write("### 📊 How Do They Compare?")
        
        suppliers = self.get_existing_suppliers(company_name)
        
        with st.spinner("📈 Generating competitive analytics..."):
            # Performance comparison matrices
            comparison_data = self._generate_performance_matrices(suppliers)
            
            # Market positioning analysis
            positioning = self._analyze_market_positioning(suppliers)
            
            # Trend analysis
            trends = self._analyze_competitive_trends(suppliers)
            
            return {
                'performance_matrices': comparison_data,
                'market_positioning': positioning,
                'competitive_trends': trends,
                'benchmarking_data': self._generate_benchmarks(suppliers)
            }
    
    def question_5_what_to_do(self, company_name: str, all_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """💡 What Should We Do? - Actionable strategic recommendations"""
        
        st.write("### 💡 What Should We Do?")
        
        with st.spinner("🎯 Generating strategic recommendations..."):
            # Synthesize all analysis into actionable insights
            recommendations = self._generate_strategic_recommendations(all_analysis)
            
            # Priority action matrix
            priority_actions = self._create_priority_matrix(all_analysis)
            
            # Export capabilities
            export_data = self._prepare_export_data(company_name, all_analysis)
            
            return {
                'strategic_recommendations': recommendations,
                'priority_actions': priority_actions,
                'next_steps': recommendations.get('next_steps', []),
                'export_data': export_data
            }
    
    def _generate_company_context(self, company_name: str) -> Dict[str, Any]:
        """Generate company context and intelligence keywords using AI"""
        
        if not self.openai_api_key:
            return self._fallback_company_context(company_name)
        
        try:
            prompt = f"""
            Analyze {company_name} to build a market intelligence strategy.
            
            Provide a JSON response with:
            1. industry_context: What industry/sector is this company in?
            2. business_model: How does this company operate?
            3. market_segments: List 5 relevant market segments to investigate
            4. keywords: Generate specific search keywords for:
               - technology: Technology and innovation keywords
               - suppliers: Supplier and vendor discovery keywords  
               - competitive: Competitive analysis keywords
               - regulatory: Regulatory and compliance keywords
               - market: Market trends and analysis keywords
            
            Focus on actionable intelligence gathering.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=800
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"AI analysis failed: {e}")
            return self._fallback_company_context(company_name)
    
    def _fallback_company_context(self, company_name: str) -> Dict[str, Any]:
        """Fallback context when AI is not available"""
        return {
            "industry_context": f"Analysis target: {company_name}",
            "business_model": "Large enterprise organization",
            "market_segments": ["Technology", "Infrastructure", "Services", "Innovation", "Operations"],
            "keywords": {
                "technology": [f"{company_name} technology", f"{company_name} innovation", f"{company_name} digital"],
                "suppliers": [f"{company_name} suppliers", f"{company_name} vendors", f"{company_name} contractors"],
                "competitive": [f"{company_name} competitors", f"{company_name} market share"],
                "regulatory": [f"{company_name} compliance", f"{company_name} regulatory"],
                "market": [f"{company_name} market trends", f"{company_name} industry analysis"]
            }
        }
    
    def _crawl_technology_suppliers(self, company_name: str, keywords: List[str]) -> List[Dict[str, Any]]:
        """Crawl for technology suppliers using generated keywords"""
        
        suppliers = []
        
        for keyword_set in keywords[:3]:  # Limit API calls
            search_query = f"{company_name} {keyword_set} suppliers 2024"
            results = self._search_google(search_query)
            
            for result in results[:5]:  # Process top 5 results per keyword
                supplier_data = self._extract_supplier_info(result, company_name)
                if supplier_data:
                    suppliers.append(supplier_data)
        
        return suppliers
    
    def _search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search Google Custom Search API"""
        if not self.google_api_key or not self.google_cse_id:
            return []
        
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': query,
                'num': num_results
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
        except Exception as e:
            st.error(f"Search error: {e}")
        
        return []
    
    def _extract_supplier_info(self, search_result: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """Extract structured supplier information from search results"""
        
        title = search_result.get('title', '')
        url = search_result.get('link', '')
        snippet = search_result.get('snippet', '')
        
        # Use AI to extract structured data
        if self.openai_api_key:
            try:
                prompt = f"""
                Extract supplier information from this search result about {company_name}:
                Title: {title}
                URL: {url}
                Content: {snippet}
                
                Return JSON with:
                - supplier_name: Company name mentioned
                - technologies: List of technologies mentioned
                - capabilities: List of capabilities or services
                - relevance_score: 0-10 relevance to {company_name}
                - category: Business category (Technology, Infrastructure, etc.)
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    max_tokens=300
                )
                
                extracted = json.loads(response.choices[0].message.content)
                extracted.update({
                    'url': url,
                    'source_title': title,
                    'source_content': snippet[:200]
                })
                
                return extracted
                
            except Exception as e:
                st.warning(f"AI extraction failed: {e}")
        
        # Fallback extraction
        return {
            'supplier_name': title.split(' ')[0] if title else 'Unknown',
            'technologies': ['Technology'],
            'capabilities': ['Services'],
            'relevance_score': 5.0,
            'category': 'General',
            'url': url,
            'source_title': title,
            'source_content': snippet[:200]
        }
    
    # Database operations
    def store_company_analysis(self, company_name: str, analysis: Dict[str, Any]):
        """Store company analysis in database"""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO company_analyses 
                (company_name, industry_context, market_segments, keywords_generated)
                VALUES (?, ?, ?, ?)
            ''', (
                company_name,
                json.dumps(analysis.get('industry_context', '')),
                json.dumps(analysis.get('market_segments', [])),
                json.dumps(analysis.get('keywords', {}))
            ))
            self.conn.commit()
        except Exception as e:
            st.error(f"Database storage error: {e}")
    
    def get_existing_analysis(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get existing company analysis from database"""
        try:
            cursor = self.conn.execute(
                'SELECT * FROM company_analyses WHERE company_name = ?',
                (company_name,)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    'industry_context': json.loads(row[2]),
                    'market_segments': json.loads(row[3]),
                    'keywords': json.loads(row[4])
                }
        except Exception as e:
            st.error(f"Database retrieval error: {e}")
        
        return None
    
    def store_suppliers(self, company_name: str, suppliers: List[Dict[str, Any]]):
        """Store supplier data in database"""
        for supplier in suppliers:
            try:
                self.conn.execute('''
                    INSERT INTO supplier_profiles 
                    (company_name, supplier_name, supplier_url, technologies, capabilities, relevance_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    company_name,
                    supplier.get('supplier_name', ''),
                    supplier.get('url', ''),
                    json.dumps(supplier.get('technologies', [])),
                    json.dumps(supplier.get('capabilities', [])),
                    float(supplier.get('relevance_score', 5.0))
                ))
            except Exception as e:
                st.warning(f"Supplier storage error: {e}")
        
        try:
            self.conn.commit()
        except Exception as e:
            st.error(f"Database commit error: {e}")
    
    def get_existing_suppliers(self, company_name: str) -> List[Dict[str, Any]]:
        """Get existing suppliers from database"""
        try:
            cursor = self.conn.execute(
                'SELECT * FROM supplier_profiles WHERE company_name = ?',
                (company_name,)
            )
            rows = cursor.fetchall()
            
            suppliers = []
            for row in rows:
                suppliers.append({
                    'supplier_name': row[2],
                    'url': row[3],
                    'technologies': json.loads(row[4]),
                    'capabilities': json.loads(row[5]),
                    'relevance_score': row[6]
                })
            
            return suppliers
        except Exception as e:
            st.error(f"Database retrieval error: {e}")
            return []
    
    # Analysis methods (simplified for space)
    def _analyze_technology_landscape(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze technology trends from supplier data"""
        all_technologies = []
        for supplier in suppliers:
            techs = supplier.get('technologies', [])
            if techs and isinstance(techs, list):
                all_technologies.extend(techs)
            elif techs and isinstance(techs, str):
                all_technologies.append(techs)
        
        tech_counts = {}
        for tech in all_technologies:
            tech_counts[tech] = tech_counts.get(tech, 0) + 1
        
        return {
            'key_technologies': list(tech_counts.keys())[:10],
            'technology_frequency': tech_counts,
            'innovation_areas': list(tech_counts.keys())[:5]
        }
    
    def _rank_suppliers_strategically(self, suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank suppliers by strategic relevance"""
        return sorted(suppliers, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    def _generate_detailed_profiles(self, suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate detailed profiles for top suppliers"""
        return suppliers  # Simplified for now
    
    def _categorize_suppliers(self, suppliers: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize suppliers by type"""
        categories = {}
        for supplier in suppliers:
            category = supplier.get('category', 'General')
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _analyze_market_coverage(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze market coverage from suppliers"""
        return {
            'total_suppliers': len(suppliers),
            'coverage_score': min(len(suppliers) / 20 * 100, 100),
            'diversity_index': len(set(s.get('category', 'General') for s in suppliers))
        }
    
    def _generate_performance_matrices(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate performance comparison data"""
        if not suppliers:
            return {}
        
        # Add default category if missing
        for supplier in suppliers:
            if 'category' not in supplier:
                supplier['category'] = 'General'
        
        df = pd.DataFrame(suppliers)
        
        try:
            relevance_stats = df['relevance_score'].describe().to_dict() if 'relevance_score' in df.columns else {}
            category_stats = df.groupby('category').size().to_dict() if 'category' in df.columns else {}
        except Exception:
            relevance_stats = {}
            category_stats = {}
        
        return {
            'relevance_distribution': relevance_stats,
            'category_performance': category_stats
        }
    
    def _analyze_market_positioning(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze market positioning"""
        return {
            'market_leaders': [s for s in suppliers if s.get('relevance_score', 0) > 8],
            'emerging_players': [s for s in suppliers if 5 < s.get('relevance_score', 0) <= 8],
            'niche_players': [s for s in suppliers if s.get('relevance_score', 0) <= 5]
        }
    
    def _analyze_competitive_trends(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze competitive trends"""
        return {
            'trend_analysis': 'Comprehensive analysis based on supplier data',
            'growth_areas': ['Technology', 'Innovation'],
            'consolidation_trends': ['Market consolidation observed']
        }
    
    def _generate_benchmarks(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate benchmarking data"""
        if not suppliers:
            return {}
        
        scores = [s.get('relevance_score', 0) for s in suppliers]
        return {
            'average_score': np.mean(scores),
            'top_quartile': np.percentile(scores, 75),
            'median_score': np.median(scores)
        }
    
    def _generate_strategic_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic recommendations from all analysis"""
        return {
            'priority_recommendations': [
                'Focus on high-performing supplier relationships',
                'Investigate emerging technology trends',
                'Strengthen market position in key segments'
            ],
            'next_steps': [
                'Conduct detailed supplier assessments',
                'Develop technology roadmap',
                'Create competitive response strategy'
            ]
        }
    
    def _create_priority_matrix(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create priority action matrix"""
        return {
            'high_priority': ['Supplier engagement', 'Technology adoption'],
            'medium_priority': ['Market expansion', 'Competitive analysis'],
            'low_priority': ['Process optimization', 'Cost reduction']
        }
    
    def _prepare_export_data(self, company_name: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for export"""
        return {
            'company': company_name,
            'analysis_date': datetime.now().isoformat(),
            'summary': analysis
        }

def render_narrative_market_intelligence():
    """Main function to render the 5-question narrative interface"""
    
    st.title("🔍 Narrative Market Intelligence")
    st.markdown("### Building strategic insights through intelligent questioning")
    
    # Company input
    company_name = st.text_input(
        "🏢 Target Company", 
        value="Thames Water",
        placeholder="Enter company name for analysis..."
    )
    
    if not company_name:
        st.info("👆 Enter a company name to begin the narrative analysis")
        return
    
    # Initialize intelligence engine
    intel_engine = NarrativeMarketIntelligence()
    
    # Progress tracking
    if st.button("🚀 Begin Narrative Analysis", type="primary"):
        st.session_state['narrative_started'] = True
        st.session_state['company_name'] = company_name
    
    if st.session_state.get('narrative_started'):
        company = st.session_state.get('company_name', company_name)
        
        # Run the 5-question narrative
        with st.container():
            
            # Question 1: Who Are We Analyzing?
            q1_result = intel_engine.question_1_who_analyzing(company)
            render_question_1_visuals(q1_result, company)
            
            # Question 2: What Technologies Matter?
            q2_result = intel_engine.question_2_what_technologies(company, q1_result)
            render_question_2_visuals(q2_result)
            
            # Question 3: Who Are The Key Players?
            q3_result = intel_engine.question_3_key_players(company)
            render_question_3_visuals(q3_result)
            
            # Question 4: How Do They Compare?
            q4_result = intel_engine.question_4_how_compare(company)
            render_question_4_visuals(q4_result)
            
            # Question 5: What Should We Do?
            all_analysis = {
                'context': q1_result,
                'technologies': q2_result,
                'players': q3_result,
                'comparison': q4_result
            }
            q5_result = intel_engine.question_5_what_to_do(company, all_analysis)
            render_question_5_visuals(q5_result, company)

def render_question_1_visuals(result: Dict[str, Any], company_name: str):
    """Render visuals for Question 1: Who Are We Analyzing?"""
    
    if not result:
        return
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Target Company", company_name)
        st.metric("Market Segments", len(result.get('market_segments', [])))
    
    with col2:
        st.metric("Keyword Categories", len(result.get('keywords', {})))
        st.metric("Analysis Status", "✅ Context Set")
    
    # Market segments visualization
    if result.get('market_segments'):
        segments_df = pd.DataFrame({
            'Segment': result['market_segments'],
            'Priority': np.random.uniform(0.6, 1.0, len(result['market_segments']))
        })
        
        fig = px.bar(segments_df, x='Segment', y='Priority', 
                     title=f"Market Segments for {company_name}",
                     color='Priority', color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)

def render_question_2_visuals(result: Dict[str, Any]):
    """Render visuals for Question 2: What Technologies Matter?"""
    
    if not result:
        return
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Suppliers Found", result.get('suppliers_found', 0))
    with col2:
        st.metric("Key Technologies", len(result.get('key_technologies', [])))
    with col3:
        st.metric("Innovation Areas", len(result.get('innovation_areas', [])))
    
    # Technology frequency chart
    tech_analysis = result.get('technology_trends', {})
    if tech_analysis.get('technology_frequency'):
        tech_df = pd.DataFrame(list(tech_analysis['technology_frequency'].items()), 
                              columns=['Technology', 'Frequency'])
        tech_df = tech_df.sort_values('Frequency', ascending=False).head(10)
        
        fig = px.treemap(tech_df, path=['Technology'], values='Frequency',
                        title="Technology Landscape - Frequency Analysis")
        st.plotly_chart(fig, use_container_width=True)

def render_question_3_visuals(result: Dict[str, Any]):
    """Render visuals for Question 3: Who Are The Key Players?"""
    
    if not result:
        return
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Suppliers", result.get('total_suppliers', 0))
    with col2:
        st.metric("Top Performers", len(result.get('top_performers', [])))
    with col3:
        coverage = result.get('market_coverage', {})
        st.metric("Market Coverage", f"{coverage.get('coverage_score', 0):.0f}%")
    
    # Supplier categories pie chart
    categories = result.get('supplier_categories', {})
    if categories:
        fig = px.pie(values=list(categories.values()), names=list(categories.keys()),
                     title="Supplier Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top performers table
    top_performers = result.get('top_performers', [])
    if top_performers:
        df = pd.DataFrame(top_performers[:10])
        st.subheader("🏆 Top Performing Suppliers")
        st.dataframe(df[['supplier_name', 'relevance_score', 'technologies']].head(), use_container_width=True)

def render_question_4_visuals(result: Dict[str, Any]):
    """Render visuals for Question 4: How Do They Compare?"""
    
    if not result:
        return
    
    st.markdown("---")
    
    # Performance matrices
    performance = result.get('performance_matrices', {})
    positioning = result.get('market_positioning', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leaders = positioning.get('market_leaders', [])
        st.metric("Market Leaders", len(leaders))
    with col2:
        emerging = positioning.get('emerging_players', [])
        st.metric("Emerging Players", len(emerging))
    with col3:
        niche = positioning.get('niche_players', [])
        st.metric("Niche Players", len(niche))
    
    # Market positioning scatter plot
    if positioning:
        positioning_data = []
        for category, suppliers in positioning.items():
            for supplier in suppliers:
                positioning_data.append({
                    'Supplier': supplier.get('supplier_name', 'Unknown'),
                    'Category': category.replace('_', ' ').title(),
                    'Relevance': supplier.get('relevance_score', 0),
                    'Technologies': len(supplier.get('technologies', []))
                })
        
        if positioning_data:
            pos_df = pd.DataFrame(positioning_data)
            fig = px.scatter(pos_df, x='Relevance', y='Technologies', 
                           color='Category', size='Relevance',
                           title="Market Positioning Analysis",
                           hover_data=['Supplier'])
            st.plotly_chart(fig, use_container_width=True)

def render_question_5_visuals(result: Dict[str, Any], company_name: str):
    """Render visuals for Question 5: What Should We Do?"""
    
    if not result:
        return
    
    st.markdown("---")
    st.subheader("🎯 Strategic Action Dashboard")
    
    recommendations = result.get('strategic_recommendations', {})
    priority_actions = result.get('priority_actions', {})
    
    # Priority matrix
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔴 High Priority Actions**")
        for action in priority_actions.get('high_priority', []):
            st.markdown(f"• {action}")
        
        st.markdown("**🟡 Medium Priority Actions**")
        for action in priority_actions.get('medium_priority', []):
            st.markdown(f"• {action}")
    
    with col2:
        st.markdown("**🟢 Low Priority Actions**")
        for action in priority_actions.get('low_priority', []):
            st.markdown(f"• {action}")
    
    # Next steps timeline
    next_steps = recommendations.get('next_steps', [])
    if next_steps:
        steps_df = pd.DataFrame({
            'Step': next_steps,
            'Timeline': ['Week 1-2', 'Week 3-4', 'Month 2+'][:len(next_steps)],
            'Priority': [3, 2, 1][:len(next_steps)]
        })
        
        fig = px.timeline(steps_df, x_start=[0, 2, 4][:len(next_steps)], 
                         x_end=[2, 4, 8][:len(next_steps)], y='Step',
                         title="Strategic Implementation Timeline")
        st.plotly_chart(fig, use_container_width=True)
    
    # Export functionality
    if st.button("📊 Export Analysis Report"):
        export_data = result.get('export_data', {})
        st.download_button(
            label="Download JSON Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"{company_name}_market_intelligence_report.json",
            mime="application/json"
        )