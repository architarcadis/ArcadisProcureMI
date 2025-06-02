"""
Market Intelligence Command Center
Comprehensive intelligence platform with intelligent crawling and additive data collection
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sqlite3
import json
import hashlib

class IntelligentCrawlingEngine:
    """Intelligent crawling engine that avoids duplicate information"""
    
    def __init__(self, db_path="intelligence_command_center.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize comprehensive intelligence database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for different intelligence types
        tables = {
            'supplier_intelligence': '''
                CREATE TABLE IF NOT EXISTS supplier_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_name TEXT,
                    content_hash TEXT UNIQUE,
                    intelligence_type TEXT,
                    title TEXT,
                    content TEXT,
                    analysis TEXT,
                    risk_score REAL,
                    confidence REAL,
                    source_url TEXT,
                    source_domain TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'category_intelligence': '''
                CREATE TABLE IF NOT EXISTS category_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT,
                    content_hash TEXT UNIQUE,
                    intelligence_type TEXT,
                    title TEXT,
                    content TEXT,
                    analysis TEXT,
                    trend_direction TEXT,
                    impact_score REAL,
                    source_url TEXT,
                    source_domain TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'regulatory_intelligence': '''
                CREATE TABLE IF NOT EXISTS regulatory_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    regulation_area TEXT,
                    content_hash TEXT UNIQUE,
                    title TEXT,
                    content TEXT,
                    analysis TEXT,
                    impact_level TEXT,
                    effective_date TEXT,
                    affected_categories TEXT,
                    source_url TEXT,
                    source_domain TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'innovation_intelligence': '''
                CREATE TABLE IF NOT EXISTS innovation_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    innovation_area TEXT,
                    content_hash TEXT UNIQUE,
                    title TEXT,
                    content TEXT,
                    analysis TEXT,
                    innovation_type TEXT,
                    maturity_level TEXT,
                    disruption_potential REAL,
                    source_url TEXT,
                    source_domain TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'market_entrants': '''
                CREATE TABLE IF NOT EXISTS market_entrants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT,
                    content_hash TEXT UNIQUE,
                    entry_type TEXT,
                    title TEXT,
                    content TEXT,
                    analysis TEXT,
                    market_category TEXT,
                    threat_level TEXT,
                    funding_amount REAL,
                    source_url TEXT,
                    source_domain TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        for table_sql in tables.values():
            cursor.execute(table_sql)
        
        conn.commit()
        conn.close()
    
    def _generate_content_hash(self, url: str, content: str) -> str:
        """Generate unique hash for content to avoid duplicates"""
        combined = f"{url}:{content[:500]}"  # Use URL and first 500 chars
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _is_duplicate_content(self, table: str, content_hash: str) -> bool:
        """Check if content already exists in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE content_hash = ?", (content_hash,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count > 0
    
    def crawl_supplier_intelligence(self, supplier: str, search_engine, progress_callback=None) -> List[Dict]:
        """Crawl supplier intelligence with duplicate detection"""
        intelligence_data = []
        
        # Define UK-focused supplier intelligence search queries
        queries = [
            f"{supplier} UK financial performance earnings report 2024 Companies House",
            f"{supplier} UK company risk assessment credit rating",
            f"{supplier} UK innovation R&D technology partnerships",
            f"{supplier} UK supply chain operations resilience",
            f"{supplier} UK regulatory compliance FCA cybersecurity"
        ]
        
        intelligence_types = ['financial', 'risk', 'innovation', 'operations', 'compliance']
        
        for query, intel_type in zip(queries, intelligence_types):
            if progress_callback:
                progress_callback(f"Searching {intel_type} intelligence for {supplier}")
            
            # Use slider value for number of sources
            num_sources = getattr(st.session_state, 'sources_per_query', 3)
            results = search_engine.search_market_data(query, num_sources)
            
            for result in results:
                content = search_engine.crawl_web_content(result['link'])
                if content and len(content) > 100:  # Ensure meaningful content
                    
                    content_hash = self._generate_content_hash(result['link'], content)
                    
                    # Skip if duplicate
                    if self._is_duplicate_content('supplier_intelligence', content_hash):
                        if progress_callback:
                            progress_callback(f"Skipping duplicate content from {result['source']}")
                        continue
                    
                    # Analyze with AI
                    analysis = search_engine.analyze_with_ai(content, {
                        'supplier_focus': supplier,
                        'intelligence_type': intel_type,
                        'analysis_depth': 'comprehensive'
                    })
                    
                    intelligence_item = {
                        'supplier_name': supplier,
                        'content_hash': content_hash,
                        'intelligence_type': intel_type,
                        'title': result['title'],
                        'content': content[:2000],  # Store first 2000 chars
                        'analysis': json.dumps(analysis),
                        'risk_score': analysis.get('risk_score', 50.0),
                        'confidence': analysis.get('confidence', 0.7),
                        'source_url': result['link'],
                        'source_domain': result['source']
                    }
                    
                    intelligence_data.append(intelligence_item)
                    
                    if progress_callback:
                        progress_callback(f"New intelligence: {intel_type} from {result['source']}")
        
        # Save to database
        self._save_supplier_intelligence(intelligence_data)
        return intelligence_data
    
    def crawl_category_intelligence(self, category: str, search_engine, progress_callback=None) -> List[Dict]:
        """Crawl category market intelligence"""
        intelligence_data = []
        
        queries = [
            f"{category} UK market trends pricing analysis 2024",
            f"{category} UK supply demand dynamics forecast",
            f"{category} UK technology innovation disruption",
            f"{category} UK sustainability requirements ESG",
            f"{category} UK quality standards regulatory changes"
        ]
        
        intelligence_types = ['pricing', 'supply_demand', 'technology', 'sustainability', 'standards']
        
        for query, intel_type in zip(queries, intelligence_types):
            if progress_callback:
                progress_callback(f"Analyzing {intel_type} trends for {category}")
            
            # Use slider value for number of sources
            num_sources = getattr(st.session_state, 'sources_per_query', 3)
            results = search_engine.search_market_data(query, num_sources)
            
            for result in results:
                content = search_engine.crawl_web_content(result['link'])
                if content and len(content) > 100:
                    
                    content_hash = self._generate_content_hash(result['link'], content)
                    
                    if self._is_duplicate_content('category_intelligence', content_hash):
                        continue
                    
                    analysis = search_engine.analyze_with_ai(content, {
                        'category_focus': category,
                        'intelligence_type': intel_type,
                        'analysis_depth': 'market_analysis'
                    })
                    
                    intelligence_item = {
                        'category_name': category,
                        'content_hash': content_hash,
                        'intelligence_type': intel_type,
                        'title': result['title'],
                        'content': content[:2000],
                        'analysis': json.dumps(analysis),
                        'trend_direction': analysis.get('trend', 'stable'),
                        'impact_score': analysis.get('impact_score', 50.0),
                        'source_url': result['link'],
                        'source_domain': result['source']
                    }
                    
                    intelligence_data.append(intelligence_item)
                    
                    if progress_callback:
                        progress_callback(f"New trend analysis: {intel_type} for {category}")
        
        self._save_category_intelligence(intelligence_data)
        return intelligence_data
    
    def crawl_regulatory_intelligence(self, categories: List[str], search_engine, progress_callback=None) -> List[Dict]:
        """Crawl regulatory changes affecting categories"""
        intelligence_data = []
        
        # Use slider value for number of categories
        max_categories = getattr(st.session_state, 'max_categories', 3)
        for category in categories[:max_categories]:
            queries = [
                f"{category} UK regulatory changes compliance requirements 2024",
                f"{category} UK environmental regulations ESG mandates HSE",
                f"{category} UK safety standards updates BSI approval",
                f"{category} UK trade regulations import export Brexit impact"
            ]
            
            for query in queries:
                if progress_callback:
                    progress_callback(f"Monitoring regulatory changes for {category}")
                
                # Use slider value for number of sources
                num_sources = getattr(st.session_state, 'sources_per_query', 2)
                results = search_engine.search_market_data(query, num_sources)
                
                for result in results:
                    content = search_engine.crawl_web_content(result['link'])
                    if content and len(content) > 100:
                        
                        content_hash = self._generate_content_hash(result['link'], content)
                        
                        if self._is_duplicate_content('regulatory_intelligence', content_hash):
                            continue
                        
                        analysis = search_engine.analyze_with_ai(content, {
                            'category_focus': category,
                            'analysis_type': 'regulatory_analysis'
                        })
                        
                        intelligence_item = {
                            'regulation_area': category,
                            'content_hash': content_hash,
                            'title': result['title'],
                            'content': content[:2000],
                            'analysis': json.dumps(analysis),
                            'impact_level': analysis.get('regulatory_impact', 'medium'),
                            'effective_date': analysis.get('effective_date', ''),
                            'affected_categories': json.dumps([category]),
                            'source_url': result['link'],
                            'source_domain': result['source']
                        }
                        
                        intelligence_data.append(intelligence_item)
        
        self._save_regulatory_intelligence(intelligence_data)
        return intelligence_data
    
    def crawl_innovation_intelligence(self, categories: List[str], search_engine, progress_callback=None) -> List[Dict]:
        """Crawl innovation and technology disruption intelligence"""
        intelligence_data = []
        
        innovation_areas = [
            "UK artificial intelligence automation supply chain",
            "UK blockchain procurement transparency",
            "UK IoT supply chain monitoring sensors",
            "UK sustainability green technology innovation",
            "UK digital transformation procurement platforms"
        ]
        
        for innovation_area in innovation_areas:
            if progress_callback:
                progress_callback(f"Tracking innovation: {innovation_area}")
            
            query = f"{innovation_area} 2024 market impact procurement UK"
            # Use slider value for number of sources
            num_sources = getattr(st.session_state, 'sources_per_query', 2)
            results = search_engine.search_market_data(query, num_sources)
            
            for result in results:
                content = search_engine.crawl_web_content(result['link'])
                if content and len(content) > 100:
                    
                    content_hash = self._generate_content_hash(result['link'], content)
                    
                    if self._is_duplicate_content('innovation_intelligence', content_hash):
                        continue
                    
                    analysis = search_engine.analyze_with_ai(content, {
                        'innovation_focus': innovation_area,
                        'analysis_type': 'innovation_analysis'
                    })
                    
                    intelligence_item = {
                        'innovation_area': innovation_area,
                        'content_hash': content_hash,
                        'title': result['title'],
                        'content': content[:2000],
                        'analysis': json.dumps(analysis),
                        'innovation_type': analysis.get('innovation_type', 'technology'),
                        'maturity_level': analysis.get('maturity', 'developing'),
                        'disruption_potential': analysis.get('disruption_score', 50.0),
                        'source_url': result['link'],
                        'source_domain': result['source']
                    }
                    
                    intelligence_data.append(intelligence_item)
        
        self._save_innovation_intelligence(intelligence_data)
        return intelligence_data
    
    def crawl_market_entrants(self, categories: List[str], search_engine, progress_callback=None) -> List[Dict]:
        """Crawl information about new market entrants"""
        intelligence_data = []
        
        # Use slider value for number of categories  
        max_categories = getattr(st.session_state, 'max_categories', 2)
        for category in categories[:max_categories]:
            queries = [
                f"new companies entering {category} UK market 2024",
                f"UK startup funding {category} supply chain disruption",
                f"UK merger acquisition {category} suppliers consolidation",
                f"international expansion {category} UK market entry"
            ]
            
            entry_types = ['new_company', 'startup_funding', 'merger_acquisition', 'international_expansion']
            
            for query, entry_type in zip(queries, entry_types):
                if progress_callback:
                    progress_callback(f"Identifying {entry_type} in {category}")
                
                # Use slider value for number of sources
                num_sources = getattr(st.session_state, 'sources_per_query', 2)
                results = search_engine.search_market_data(query, num_sources)
                
                for result in results:
                    content = search_engine.crawl_web_content(result['link'])
                    if content and len(content) > 100:
                        
                        content_hash = self._generate_content_hash(result['link'], content)
                        
                        if self._is_duplicate_content('market_entrants', content_hash):
                            continue
                        
                        analysis = search_engine.analyze_with_ai(content, {
                            'category_focus': category,
                            'analysis_type': 'market_entrant_analysis'
                        })
                        
                        intelligence_item = {
                            'company_name': analysis.get('company_name', 'New Market Entrant'),
                            'content_hash': content_hash,
                            'entry_type': entry_type,
                            'title': result['title'],
                            'content': content[:2000],
                            'analysis': json.dumps(analysis),
                            'market_category': category,
                            'threat_level': analysis.get('threat_level', 'medium'),
                            'funding_amount': analysis.get('funding_amount', 0.0),
                            'source_url': result['link'],
                            'source_domain': result['source']
                        }
                        
                        intelligence_data.append(intelligence_item)
        
        self._save_market_entrants(intelligence_data)
        return intelligence_data
    
    def _save_supplier_intelligence(self, data: List[Dict]):
        """Save supplier intelligence to database"""
        if not data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO supplier_intelligence 
                    (supplier_name, content_hash, intelligence_type, title, content, 
                     analysis, risk_score, confidence, source_url, source_domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['supplier_name'], item['content_hash'], item['intelligence_type'],
                    item['title'], item['content'], item['analysis'], 
                    item['risk_score'], item['confidence'], item['source_url'], item['source_domain']
                ))
            except Exception as e:
                st.error(f"Error saving supplier intelligence: {e}")
        
        conn.commit()
        conn.close()
    
    def _save_category_intelligence(self, data: List[Dict]):
        """Save category intelligence to database"""
        if not data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO category_intelligence 
                    (category_name, content_hash, intelligence_type, title, content, 
                     analysis, trend_direction, impact_score, source_url, source_domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['category_name'], item['content_hash'], item['intelligence_type'],
                    item['title'], item['content'], str(item.get('analysis', {})), 
                    item['trend_direction'], item['impact_score'], item['source_url'], item['source_domain']
                ))
            except Exception as e:
                st.error(f"Error saving category intelligence: {e}")
        
        conn.commit()
        conn.close()
    
    def _save_regulatory_intelligence(self, data: List[Dict]):
        """Save regulatory intelligence to database"""
        if not data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO regulatory_intelligence 
                    (regulation_area, content_hash, title, content, analysis, 
                     impact_level, effective_date, affected_categories, source_url, source_domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['regulation_area'], item['content_hash'], item['title'],
                    item['content'], item['analysis'], item['impact_level'], 
                    item['effective_date'], item['affected_categories'], item['source_url'], item['source_domain']
                ))
            except Exception as e:
                st.error(f"Error saving regulatory intelligence: {e}")
        
        conn.commit()
        conn.close()
    
    def _save_innovation_intelligence(self, data: List[Dict]):
        """Save innovation intelligence to database"""
        if not data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO innovation_intelligence 
                    (innovation_area, content_hash, title, content, analysis, 
                     innovation_type, maturity_level, disruption_potential, source_url, source_domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['innovation_area'], item['content_hash'], item['title'],
                    item['content'], item['analysis'], item['innovation_type'], 
                    item['maturity_level'], item['disruption_potential'], item['source_url'], item['source_domain']
                ))
            except Exception as e:
                st.error(f"Error saving innovation intelligence: {e}")
        
        conn.commit()
        conn.close()
    
    def _save_market_entrants(self, data: List[Dict]):
        """Save market entrants intelligence to database"""
        if not data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO market_entrants 
                    (company_name, content_hash, entry_type, title, content, analysis, 
                     market_category, threat_level, funding_amount, source_url, source_domain)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['company_name'], item['content_hash'], item['entry_type'],
                    item['title'], item['content'], item['analysis'], item['market_category'],
                    item['threat_level'], item['funding_amount'], item['source_url'], item['source_domain']
                ))
            except Exception as e:
                st.error(f"Error saving market entrants: {e}")
        
        conn.commit()
        conn.close()
    
    def get_database_summary(self) -> Dict[str, Any]:
        """Get comprehensive database summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        summary = {}
        
        tables = ['supplier_intelligence', 'category_intelligence', 'regulatory_intelligence', 
                 'innovation_intelligence', 'market_entrants']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT COUNT(DISTINCT source_domain) FROM {table}")
            unique_sources = cursor.fetchone()[0]
            
            summary[table] = {
                'total_records': count,
                'unique_sources': unique_sources
            }
        
        conn.close()
        return summary

def render_market_intelligence_command_center():
    """Render the Market Intelligence Command Center"""
    st.header("🎯 Market Intelligence Command Center")
    st.caption("Comprehensive intelligence platform with intelligent crawling and real-time monitoring")
    
    # Check for data from other tabs
    df = None
    if 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
    elif 'df' in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
    elif hasattr(st.session_state, 'data') and st.session_state.data is not None:
        df = st.session_state.data
    
    if df is None:
        st.info("No procurement data detected. Please upload data in one of the other tabs first to enable market intelligence analysis.")
        return
    
    # Check API keys from environment variables
    import os
    required_keys = ['OPENAI_API_KEY', 'GOOGLE_API_KEY', 'GOOGLE_CSE_ID']
    missing_keys = [key for key in required_keys if not os.environ.get(key)]
    
    if missing_keys:
        st.error(f"Missing required API keys: {', '.join(missing_keys)}")
        st.info("Please provide the necessary API keys to enable real market data crawling.")
        return
    
    # Initialize engines
    if 'crawling_engine' not in st.session_state:
        st.session_state.crawling_engine = IntelligentCrawlingEngine()
    
    if 'enhanced_intel_engine' not in st.session_state:
        from enhanced_market_intelligence import EnhancedMarketIntelligence
        st.session_state.enhanced_intel_engine = EnhancedMarketIntelligence()
    
    crawling_engine = st.session_state.crawling_engine
    search_engine = st.session_state.enhanced_intel_engine
    
    # Extract context from data
    context = extract_procurement_context(df)
    
    # Show detected data summary
    if context['suppliers'] or context['categories']:
        st.success(f"Data detected: {len(context['suppliers'])} suppliers, {len(context['categories'])} categories from {len(df):,} records")
        
        # Quick preview
        with st.expander("📋 Detected Suppliers & Categories"):
            col1, col2 = st.columns(2)
            with col1:
                if context['suppliers']:
                    st.write("**Suppliers:**")
                    for supplier in context['suppliers'][:5]:
                        st.write(f"• {supplier}")
                    if len(context['suppliers']) > 5:
                        st.write(f"... and {len(context['suppliers']) - 5} more")
            with col2:
                if context['categories']:
                    st.write("**Categories:**")
                    for category in context['categories'][:5]:
                        st.write(f"• {category}")
                    if len(context['categories']) > 5:
                        st.write(f"... and {len(context['categories']) - 5} more")
    else:
        st.warning("Could not identify suppliers or categories in your data. Please ensure your data contains supplier/vendor and category/type columns.")
    
    # Intelligence Controls
    st.subheader("⚙️ Intelligence Controls")
    col1, col2 = st.columns(2)
    
    with col1:
        sources_per_query = st.slider(
            "Sources per search query",
            min_value=1,
            max_value=10,
            value=3,
            key="sources_per_query_slider",
            help="Number of web sources to analyze for each intelligence query. Higher = more comprehensive but slower."
        )
    
    with col2:
        max_categories = st.slider(
            "Categories to analyze",
            min_value=1,
            max_value=6,
            value=3,
            key="max_categories_slider",
            help="Maximum number of procurement categories to analyze. Higher = broader coverage but slower."
        )
    
    # Store in session state for use across functions
    st.session_state.sources_per_query = sources_per_query
    st.session_state.max_categories = max_categories
    
    # One-click intelligence gathering
    st.subheader("🚀 One-Click Intelligence Gathering")
    
    # Auto-start option
    auto_start = st.checkbox("Auto-start intelligence gathering", help="Automatically begin crawling when data is detected")
    
    # Single comprehensive button
    if st.button("🔍 Start Complete Market Intelligence Scan", type="primary", use_container_width=True):
        launch_comprehensive_scan(context, crawling_engine, search_engine)
    
    # Auto-start functionality
    if auto_start and 'auto_scan_completed' not in st.session_state:
        st.info("Auto-starting comprehensive intelligence scan...")
        st.session_state.auto_scan_completed = True
        launch_comprehensive_scan(context, crawling_engine, search_engine)
    
    # Intelligence sub-tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏢 Supplier Intelligence",
        "📊 Category Market Intelligence", 
        "⚖️ Regulatory Monitoring",
        "🚀 Innovation & Technology",
        "🌟 New Market Entrants",
        "🗄️ Intelligence Database"
    ])
    
    with tab1:
        render_supplier_intelligence_results(context)
    
    with tab2:
        render_category_intelligence_results(context)
    
    with tab3:
        render_regulatory_monitoring_results(context)
    
    with tab4:
        render_innovation_intelligence_results(context)
    
    with tab5:
        render_market_entrants_results(context)
    
    with tab6:
        render_intelligence_database_viewer(crawling_engine)

def extract_procurement_context(df: pd.DataFrame) -> Dict[str, Any]:
    """Extract procurement context from uploaded data"""
    context = {'suppliers': [], 'categories': []}
    
    # Extract top 5 suppliers by spend or transaction count
    supplier_columns = ['supplier', 'vendor', 'supplier_name', 'vendor_name', 'company']
    for col in df.columns:
        if any(term in col.lower() for term in supplier_columns):
            # Filter out date-like entries and invalid supplier names
            def is_valid_supplier(value):
                if pd.isna(value) or str(value).strip() == '' or str(value) == 'nan':
                    return False
                
                str_val = str(value).strip()
                
                # Filter out date patterns (YYYY-MM-DD, DD/MM/YYYY, etc.)
                import re
                date_patterns = [
                    r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
                    r'^\d{2}/\d{2}/\d{4}$',  # DD/MM/YYYY or MM/DD/YYYY
                    r'^\d{2}-\d{2}-\d{4}$',  # DD-MM-YYYY
                    r'^\d{1,2}/\d{1,2}/\d{2,4}$',  # Flexible date formats
                    r'^\d+$'  # Pure numbers
                ]
                
                for pattern in date_patterns:
                    if re.match(pattern, str_val):
                        return False
                
                # Must be at least 2 characters and contain letters
                return len(str_val) >= 2 and any(c.isalpha() for c in str_val)
            
            # Try to rank by spend amount first
            amount_columns = [c for c in df.columns if any(term in c.lower() for term in ['amount', 'value', 'cost', 'price', 'spend'])]
            
            valid_suppliers = df[df[col].apply(is_valid_supplier)]
            
            if not valid_suppliers.empty and amount_columns:
                try:
                    # Rank suppliers by total spend
                    df_temp = valid_suppliers.copy()
                    df_temp[amount_columns[0]] = pd.to_numeric(df_temp[amount_columns[0]], errors='coerce')
                    top_suppliers = df_temp.groupby(col)[amount_columns[0]].sum().nlargest(5)
                    context['suppliers'] = [str(s) for s in top_suppliers.index]
                    break
                except:
                    pass
            
            # Fallback to transaction frequency ranking
            if not valid_suppliers.empty:
                top_suppliers = valid_suppliers[col].value_counts().head(5)
                context['suppliers'] = [str(s) for s in top_suppliers.index]
                break
    
    # If no valid suppliers found with standard column names, check all text columns
    if not context['suppliers']:
        for col in df.columns:
            if df[col].dtype == 'object':  # Text columns
                def is_valid_supplier(value):
                    if pd.isna(value) or str(value).strip() == '' or str(value) == 'nan':
                        return False
                    
                    str_val = str(value).strip()
                    
                    # Filter out date patterns
                    import re
                    date_patterns = [
                        r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
                        r'^\d{2}/\d{2}/\d{4}$',  # DD/MM/YYYY
                        r'^\d{2}-\d{2}-\d{4}$',  # DD-MM-YYYY
                        r'^\d{1,2}/\d{1,2}/\d{2,4}$',  # Flexible dates
                        r'^\d+$',  # Pure numbers
                        r'^\d+\.\d+$'  # Decimal numbers
                    ]
                    
                    for pattern in date_patterns:
                        if re.match(pattern, str_val):
                            return False
                    
                    # Must be at least 3 characters, contain letters, and look like a company name
                    return (len(str_val) >= 3 and 
                            any(c.isalpha() for c in str_val) and
                            not str_val.lower() in ['yes', 'no', 'true', 'false'])
                
                valid_suppliers = df[df[col].apply(is_valid_supplier)]
                if not valid_suppliers.empty and len(valid_suppliers[col].unique()) >= 2:
                    top_suppliers = valid_suppliers[col].value_counts().head(5)
                    context['suppliers'] = [str(s) for s in top_suppliers.index]
                    break
    
    # Extract top 5 categories by transaction count
    category_columns = ['category', 'product_category', 'service_category', 'type', 'classification']
    for col in df.columns:
        if any(term in col.lower() for term in category_columns):
            top_categories = df[col].value_counts().head(5)
            context['categories'] = [str(c) for c in top_categories.index if str(c).strip() != '' and str(c) != 'nan']
            break
    
    return context

def launch_comprehensive_scan(context: Dict[str, Any], crawling_engine, search_engine):
    """Launch comprehensive intelligence scan across all areas"""
    progress_bar = st.progress(0)
    status_container = st.container()
    live_updates = st.empty()
    
    updates = []
    total_steps = 5
    current_step = 0
    
    def update_progress(message):
        nonlocal current_step
        updates.append(f"• {message}")
        live_updates.text("\n".join(updates[-8:]))  # Show last 8 updates
    
    try:
        # Step 1: Supplier Intelligence
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        status_container.info("Step 1/5: Gathering supplier intelligence...")
        
        for supplier in context['suppliers'][:3]:
            supplier_data = crawling_engine.crawl_supplier_intelligence(supplier, search_engine, update_progress)
            update_progress(f"Collected {len(supplier_data)} intelligence items for {supplier}")
        
        # Step 2: Category Intelligence
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        status_container.info("Step 2/5: Analyzing category markets...")
        
        for category in context['categories'][:3]:
            category_data = crawling_engine.crawl_category_intelligence(category, search_engine, update_progress)
            update_progress(f"Analyzed {len(category_data)} market trends for {category}")
        
        # Step 3: Regulatory Intelligence
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        status_container.info("Step 3/5: Monitoring regulatory changes...")
        
        regulatory_data = crawling_engine.crawl_regulatory_intelligence(context['categories'], search_engine, update_progress)
        update_progress(f"Found {len(regulatory_data)} regulatory updates")
        
        # Step 4: Innovation Intelligence
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        status_container.info("Step 4/5: Tracking innovation trends...")
        
        innovation_data = crawling_engine.crawl_innovation_intelligence(context['categories'], search_engine, update_progress)
        update_progress(f"Identified {len(innovation_data)} innovation trends")
        
        # Step 5: Market Entrants
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        status_container.info("Step 5/5: Identifying new market entrants...")
        
        entrant_data = crawling_engine.crawl_market_entrants(context['categories'], search_engine, update_progress)
        update_progress(f"Discovered {len(entrant_data)} market entrants")
        
        # Complete
        progress_bar.progress(1.0)
        status_container.success("Comprehensive intelligence scan complete!")
        
        # Summary
        summary = crawling_engine.get_database_summary()
        total_intelligence = sum(summary[table]['total_records'] for table in summary)
        st.success(f"Intelligence gathering complete! Collected {total_intelligence} total intelligence items across all focus areas.")
        
        live_updates.empty()
        
    except Exception as e:
        st.error(f"Intelligence gathering encountered an issue: {str(e)}")
        st.info("This may be due to API rate limits or connectivity issues. Please try again or check your API keys.")

def render_supplier_intelligence_results(context):
    """Display supplier intelligence results with AI analysis and visuals"""
    st.subheader("🏢 Supplier Intelligence Hub")
    st.caption("AI-powered analysis of supplier performance, risk assessment, and strategic positioning")
    
    if context['suppliers']:
        # Check for mock data first, then real data
        db_path = None
        if 'mock_db_path' in st.session_state:
            db_path = st.session_state['mock_db_path']
        elif 'crawling_engine' in st.session_state:
            db_path = st.session_state.crawling_engine.db_path
        
        if db_path:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT COUNT(*) FROM supplier_intelligence")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    # Get all supplier intelligence data
                    cursor.execute("""
                        SELECT supplier_name, intelligence_type, title, source_domain, crawled_at
                        FROM supplier_intelligence 
                        ORDER BY crawled_at DESC
                    """)
                    raw_data = cursor.fetchall()
                    
                    # Use AI to analyze and visualize
                    analyze_supplier_intelligence_with_ai(raw_data, context['suppliers'])
                else:
                    st.info("Run the comprehensive scan to gather supplier intelligence")
            except Exception as e:
                st.warning("Intelligence database is being initialized. Run the comprehensive scan to begin data collection.")
            
            conn.close()
        else:
            st.info("Generate sample data from the sidebar to see how the intelligence analysis works")
    else:
        st.info("No suppliers identified in your data")

def analyze_supplier_intelligence_with_ai(raw_data, suppliers):
    """Use AI to analyze supplier intelligence and create strategic insights with visuals"""
    import os
    
    # Check for OpenAI API key
    if not os.environ.get('OPENAI_API_KEY'):
        st.error("OpenAI API key required for AI analysis")
        return
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        # Prepare data for AI analysis
        data_summary = {}
        for supplier, intel_type, title, source, date in raw_data:
            if supplier not in data_summary:
                data_summary[supplier] = []
            data_summary[supplier].append(f"{intel_type}: {title}")
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze the following supplier intelligence data and provide strategic business insights:
        
        Suppliers and Intelligence: {str(data_summary)}
        
        Provide analysis in JSON format:
        {{
            "executive_summary": "Strategic overview of supplier landscape",
            "supplier_assessments": [
                {{
                    "supplier": "name",
                    "risk_level": "Low/Medium/High",
                    "performance_rating": "Poor/Fair/Good/Excellent",
                    "financial_stability": "Weak/Stable/Strong",
                    "strategic_importance": "Low/Medium/High",
                    "key_strengths": ["strength1", "strength2"],
                    "risk_factors": ["risk1", "risk2"],
                    "recommendations": ["rec1", "rec2"]
                }}
            ],
            "market_insights": {{
                "supplier_concentration": "Low/Medium/High",
                "market_risks": ["risk1", "risk2"],
                "opportunities": ["opp1", "opp2"]
            }},
            "strategic_recommendations": ["rec1", "rec2", "rec3"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        
        # Display AI analysis with charts and insights
        display_supplier_intelligence_dashboard(analysis, data_summary)
        
    except Exception as e:
        st.error(f"AI analysis failed: {e}")
        # Display raw data as fallback
        display_raw_supplier_intelligence(data_summary)

def display_supplier_intelligence_dashboard(analysis, raw_data):
    """Display AI-analyzed supplier intelligence with strategic visuals"""
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    
    # Executive Summary
    st.success(f"**Strategic Analysis:** {analysis['executive_summary']}")
    
    # Key Metrics Dashboard
    st.subheader("📊 Supplier Portfolio Overview")
    
    # Create metrics from analysis
    supplier_df = pd.DataFrame(analysis['supplier_assessments'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_risk = len(supplier_df[supplier_df['risk_level'] == 'High'])
        st.metric("High Risk Suppliers", high_risk, delta=f"{high_risk/len(supplier_df)*100:.0f}%")
    with col2:
        excellent_perf = len(supplier_df[supplier_df['performance_rating'] == 'Excellent'])
        st.metric("Top Performers", excellent_perf)
    with col3:
        strategic_suppliers = len(supplier_df[supplier_df['strategic_importance'] == 'High'])
        st.metric("Strategic Suppliers", strategic_suppliers)
    with col4:
        stable_financial = len(supplier_df[supplier_df['financial_stability'] == 'Strong'])
        st.metric("Financially Strong", stable_financial)
    
    # Risk Assessment Matrix
    st.subheader("⚠️ Supplier Risk Assessment")
    
    # Create risk level mapping for visualization
    risk_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
    importance_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
    
    supplier_df['risk_score'] = supplier_df['risk_level'].map(risk_mapping)
    supplier_df['importance_score'] = supplier_df['strategic_importance'].map(importance_mapping)
    
    fig = px.scatter(supplier_df, x='risk_score', y='importance_score',
                     text='supplier', size_max=60,
                     color='financial_stability',
                     title="Supplier Risk vs Strategic Importance Matrix",
                     labels={'risk_score': 'Risk Level', 'importance_score': 'Strategic Importance'})
    
    fig.update_traces(textposition="top center")
    fig.update_xaxes(tickmode='array', tickvals=[1, 2, 3], ticktext=['Low Risk', 'Medium Risk', 'High Risk'])
    fig.update_yaxes(tickmode='array', tickvals=[1, 2, 3], ticktext=['Low Importance', 'Medium Importance', 'High Importance'])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Performance Distribution")
        perf_counts = supplier_df['performance_rating'].value_counts()
        fig_perf = px.pie(values=perf_counts.values, names=perf_counts.index,
                          title="Supplier Performance Ratings")
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        st.subheader("💰 Financial Stability")
        fin_counts = supplier_df['financial_stability'].value_counts()
        fig_fin = px.bar(x=fin_counts.index, y=fin_counts.values,
                         title="Financial Stability Distribution")
        st.plotly_chart(fig_fin, use_container_width=True)
    
    # Detailed Supplier Analysis
    st.subheader("🔍 Detailed Supplier Analysis")
    
    for supplier_data in analysis['supplier_assessments']:
        with st.expander(f"📋 {supplier_data['supplier']} - Strategic Assessment"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_color = "🔴" if supplier_data['risk_level'] == 'High' else "🟡" if supplier_data['risk_level'] == 'Medium' else "🟢"
                st.write(f"**Risk Level:** {risk_color} {supplier_data['risk_level']}")
                st.write(f"**Performance:** {supplier_data['performance_rating']}")
            
            with col2:
                st.write(f"**Financial Stability:** {supplier_data['financial_stability']}")
                st.write(f"**Strategic Importance:** {supplier_data['strategic_importance']}")
            
            with col3:
                intel_count = len(raw_data.get(supplier_data['supplier'], []))
                st.write(f"**Intelligence Items:** {intel_count}")
            
            if supplier_data['key_strengths']:
                st.write("**Key Strengths:**")
                for strength in supplier_data['key_strengths']:
                    st.success(f"✅ {strength}")
            
            if supplier_data['risk_factors']:
                st.write("**Risk Factors:**")
                for risk in supplier_data['risk_factors']:
                    st.error(f"⚠️ {risk}")
            
            if supplier_data['recommendations']:
                st.write("**Recommendations:**")
                for rec in supplier_data['recommendations']:
                    st.info(f"💡 {rec}")
    
    # Market-Level Insights
    st.subheader("🌍 Market Intelligence")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Market Risks:**")
        for risk in analysis['market_insights']['market_risks']:
            st.warning(f"⚠️ {risk}")
    
    with col2:
        st.write("**Market Opportunities:**")
        for opp in analysis['market_insights']['opportunities']:
            st.success(f"🎯 {opp}")
    
    # Strategic Recommendations
    st.subheader("📋 Strategic Action Plan")
    for i, rec in enumerate(analysis['strategic_recommendations'], 1):
        st.info(f"**Action {i}:** {rec}")

def display_raw_supplier_intelligence(data_summary):
    """Fallback display for raw supplier intelligence"""
    st.warning("Displaying raw intelligence data - AI analysis unavailable")
    
    for supplier, intel_items in data_summary.items():
        with st.expander(f"📊 {supplier} ({len(intel_items)} items)"):
            for item in intel_items:
                st.write(f"• {item}")
                st.divider()

def render_category_intelligence_results(context):
    """Display category intelligence with market analysis and strategic insights"""
    st.subheader("📊 Category Market Intelligence")
    st.caption("AI-powered market trends, pricing dynamics, and growth opportunities analysis")
    
    if context['categories']:
        # Check for mock data first, then real data
        db_path = None
        if 'mock_db_path' in st.session_state:
            db_path = st.session_state['mock_db_path']
        elif 'crawling_engine' in st.session_state:
            db_path = st.session_state.crawling_engine.db_path
        
        if db_path:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT COUNT(*) FROM category_intelligence")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    # Get all category intelligence data
                    cursor.execute("""
                        SELECT category_name, title, source_domain, crawled_at
                        FROM category_intelligence 
                        ORDER BY crawled_at DESC
                    """)
                    raw_data = cursor.fetchall()
                    
                    # Use AI to analyze and create market insights
                    analyze_category_intelligence_with_ai(raw_data, context['categories'])
                else:
                    st.info("Run the comprehensive scan to gather category market intelligence")
            except Exception as e:
                st.warning("Intelligence database is being initialized. Run the comprehensive scan to begin data collection.")
            
            conn.close()
        else:
            st.info("Generate mock data from the sidebar to see how the intelligence analysis works")
    else:
        st.info("No categories identified in your data")

def analyze_category_intelligence_with_ai(raw_data, categories):
    """Use AI to analyze category intelligence and create market insights with visuals"""
    import os
    
    # Check for OpenAI API key
    if not os.environ.get('OPENAI_API_KEY'):
        st.error("OpenAI API key required for AI market analysis")
        return
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        # Prepare data for AI analysis
        category_data = {}
        for category, title, source, date in raw_data:
            if category not in category_data:
                category_data[category] = []
            category_data[category].append(f"Market insight: {title}")
        
        # Create market analysis prompt
        analysis_prompt = f"""
        Analyze the following category market intelligence data and provide strategic market insights:
        
        Categories and Market Intelligence: {str(category_data)}
        
        Provide analysis in JSON format:
        {{
            "market_overview": {{
                "total_market_size_gbp": "estimated_value",
                "growth_outlook": "Positive/Stable/Declining",
                "key_trends": ["trend1", "trend2", "trend3"]
            }},
            "category_analysis": [
                {{
                    "category": "name",
                    "market_size_gbp": "estimated_value",
                    "growth_rate_percent": "percentage",
                    "competition_level": "Low/Medium/High",
                    "price_volatility": "Stable/Moderate/Volatile",
                    "innovation_potential": 0-100,
                    "strategic_priority": "High/Medium/Low",
                    "key_opportunities": ["opp1", "opp2"],
                    "market_risks": ["risk1", "risk2"]
                }}
            ],
            "strategic_insights": {{
                "fastest_growing": ["categories"],
                "highest_potential": ["categories"],
                "price_stable": ["categories"],
                "disruption_risk": ["categories"]
            }},
            "recommendations": ["rec1", "rec2", "rec3"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        
        # Display AI analysis with market charts
        display_category_intelligence_dashboard(analysis, category_data)
        
    except Exception as e:
        st.error(f"AI market analysis failed: {e}")
        # Display raw data as fallback
        display_raw_category_intelligence(category_data)

def display_category_intelligence_dashboard(analysis, raw_data):
    """Display AI-analyzed category intelligence with market visuals"""
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    
    # Market Overview
    st.success(f"**Market Overview:** Total market size: {analysis['market_overview']['total_market_size_gbp']} | Growth outlook: {analysis['market_overview']['growth_outlook']}")
    
    # Key Market Trends
    if analysis['market_overview']['key_trends']:
        st.info("**Key Market Trends:** " + " • ".join(analysis['market_overview']['key_trends']))
    
    # Market Metrics Dashboard
    st.subheader("📈 Market Performance Dashboard")
    
    category_df = pd.DataFrame(analysis['category_analysis'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_growth = len(category_df[category_df['growth_rate_percent'].str.replace('%', '').astype(float) >= 5])
        st.metric("High Growth Categories", high_growth)
    with col2:
        high_potential = len(category_df[category_df['innovation_potential'] >= 70])
        st.metric("High Innovation Potential", high_potential)
    with col3:
        stable_pricing = len(category_df[category_df['price_volatility'] == 'Stable'])
        st.metric("Price Stable Categories", stable_pricing)
    with col4:
        strategic_categories = len(category_df[category_df['strategic_priority'] == 'High'])
        st.metric("Strategic Priorities", strategic_categories)
    
    # Market Growth Radar Chart
    st.subheader("🎯 Market Growth & Opportunity Radar")
    
    # Create radar chart data
    radar_categories = category_df['category'].tolist()
    growth_rates = [float(x.replace('%', '')) for x in category_df['growth_rate_percent']]
    innovation_scores = category_df['innovation_potential'].tolist()
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=growth_rates,
        theta=radar_categories,
        fill='toself',
        name='Growth Rate %',
        line_color='blue'
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[x/20 for x in innovation_scores],  # Scale to match growth rates
        theta=radar_categories,
        fill='toself',
        name='Innovation Potential (scaled)',
        line_color='red'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(growth_rates) + 2])
        ),
        showlegend=True,
        title="Market Growth vs Innovation Potential by Category"
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Market Analysis Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Market Size Distribution")
        # Extract numeric values from market size strings
        market_sizes = []
        for size_str in category_df['market_size_gbp']:
            # Extract number from strings like "£500M" or "£2.3B"
            import re
            match = re.search(r'[\d.]+', size_str)
            if match:
                value = float(match.group())
                if 'B' in size_str:
                    value *= 1000  # Convert billions to millions
                market_sizes.append(value)
            else:
                market_sizes.append(100)  # Default value
        
        category_df['market_size_numeric'] = market_sizes
        
        fig_market = px.bar(category_df, x='category', y='market_size_numeric',
                           title="Market Size by Category (£M)",
                           color='strategic_priority',
                           color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
        fig_market.update_xaxes(tickangle=45)
        st.plotly_chart(fig_market, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Competition & Volatility Matrix")
        
        # Map competition levels to numeric values
        comp_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        vol_mapping = {'Stable': 1, 'Moderate': 2, 'Volatile': 3}
        
        category_df['comp_score'] = category_df['competition_level'].map(comp_mapping)
        category_df['vol_score'] = category_df['price_volatility'].map(vol_mapping)
        
        fig_matrix = px.scatter(category_df, x='comp_score', y='vol_score',
                               text='category', size='innovation_potential',
                               color='strategic_priority',
                               title="Competition vs Price Volatility",
                               labels={'comp_score': 'Competition Level', 'vol_score': 'Price Volatility'})
        
        fig_matrix.update_traces(textposition="top center")
        fig_matrix.update_xaxes(tickmode='array', tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High'])
        fig_matrix.update_yaxes(tickmode='array', tickvals=[1, 2, 3], ticktext=['Stable', 'Moderate', 'Volatile'])
        
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Strategic Category Prioritization
    st.subheader("🎯 Strategic Category Prioritization")
    
    # Sort by strategic priority and innovation potential
    priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
    category_df['priority_score'] = category_df['strategic_priority'].map(priority_order)
    sorted_categories = category_df.sort_values(['priority_score', 'innovation_potential'], ascending=False)
    
    for i, (_, cat_data) in enumerate(sorted_categories.iterrows(), 1):
        priority_color = "🔴" if cat_data['strategic_priority'] == 'High' else "🟡" if cat_data['strategic_priority'] == 'Medium' else "🟢"
        
        with st.expander(f"{priority_color} #{i} {cat_data['category']} - {cat_data['strategic_priority']} Priority"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Market Size", cat_data['market_size_gbp'])
                st.metric("Growth Rate", cat_data['growth_rate_percent'])
            
            with col2:
                st.metric("Innovation Potential", f"{cat_data['innovation_potential']}/100")
                st.metric("Competition Level", cat_data['competition_level'])
            
            with col3:
                intel_count = len(raw_data.get(cat_data['category'], []))
                st.metric("Intelligence Sources", intel_count)
                st.metric("Price Volatility", cat_data['price_volatility'])
            
            if cat_data['key_opportunities']:
                st.write("**Key Opportunities:**")
                for opp in cat_data['key_opportunities']:
                    st.success(f"💰 {opp}")
            
            if cat_data['market_risks']:
                st.write("**Market Risks:**")
                for risk in cat_data['market_risks']:
                    st.warning(f"⚠️ {risk}")
    
    # Strategic Insights Summary
    st.subheader("🧠 Strategic Market Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Fastest Growing Markets:**")
        for category in analysis['strategic_insights']['fastest_growing']:
            st.success(f"📈 {category}")
        
        st.write("**Price Stable Categories:**")
        for category in analysis['strategic_insights']['price_stable']:
            st.info(f"💰 {category}")
    
    with col2:
        st.write("**Highest Potential Categories:**")
        for category in analysis['strategic_insights']['highest_potential']:
            st.success(f"🚀 {category}")
        
        st.write("**Disruption Risk Areas:**")
        for category in analysis['strategic_insights']['disruption_risk']:
            st.error(f"⚠️ {category}")
    
    # Strategic Recommendations
    st.subheader("📋 Strategic Market Recommendations")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.info(f"**Recommendation {i}:** {rec}")

def display_raw_category_intelligence(category_data):
    """Fallback display for raw category intelligence"""
    st.warning("Displaying raw intelligence data - AI analysis unavailable")
    
    for category, intel_items in category_data.items():
        with st.expander(f"📊 {category} ({len(intel_items)} items)"):
            for item in intel_items:
                st.write(f"• {item}")
                st.divider()

def render_regulatory_monitoring_results(context):
    """Display regulatory monitoring results with visual analytics"""
    st.subheader("⚖️ Regulatory Monitoring Dashboard")
    st.caption("Compliance requirements, regulatory changes, and policy impacts with visual analytics")
    
    # Check if we have mock data or real data
    if 'mock_regulatory_data' in st.session_state:
        analyze_regulatory_intelligence_with_ai(st.session_state.mock_regulatory_data, context.get('categories', []))
        return
    
    if 'crawling_engine' in st.session_state:
        crawling_engine = st.session_state.crawling_engine
        try:
            data_summary = crawling_engine.get_database_summary()
            regulatory_data = data_summary.get('regulatory_intelligence', {})
            
            if regulatory_data:
                analyze_regulatory_intelligence_with_ai(regulatory_data, context.get('categories', []))
            else:
                st.info("Run the comprehensive scan to gather regulatory intelligence for visual analysis")
        except Exception as e:
            st.warning("Connect to external services to enable regulatory monitoring")
    else:
        st.info("Intelligence engine not initialized")

def analyze_regulatory_intelligence_with_ai(raw_data, categories):
    """Use AI to analyze regulatory intelligence and create compliance insights with visuals"""
    try:
        import os
        from openai import OpenAI
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        analysis_prompt = f"""
        Analyze this regulatory intelligence data for UK procurement categories: {categories}.
        Focus on compliance requirements, regulatory changes, and policy impacts.
        
        Raw regulatory data: {str(raw_data)[:2000]}
        
        Return a JSON object with this structure:
        {{
            "compliance_overview": {{
                "total_regulations": "number",
                "high_impact_changes": "number",
                "compliance_score": 0-100
            }},
            "regulatory_changes": [
                {{
                    "regulation": "name",
                    "impact_level": "High/Medium/Low",
                    "implementation_date": "date or pending",
                    "affected_categories": ["category1", "category2"],
                    "compliance_requirements": ["req1", "req2"],
                    "risk_level": 0-100,
                    "cost_impact": "High/Medium/Low"
                }}
            ],
            "compliance_matrix": {{
                "fully_compliant": ["categories"],
                "partial_compliance": ["categories"],
                "non_compliant": ["categories"],
                "pending_changes": ["categories"]
            }},
            "risk_assessment": {{
                "high_risk_areas": ["areas"],
                "compliance_gaps": ["gaps"],
                "urgent_actions": ["actions"]
            }},
            "recommendations": ["rec1", "rec2", "rec3"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        
        # Display AI analysis with regulatory charts
        display_regulatory_intelligence_dashboard(analysis, raw_data)
        
    except Exception as e:
        st.error(f"AI regulatory analysis failed: {e}")
        # Display raw data as fallback
        display_raw_regulatory_intelligence(raw_data)

def display_regulatory_intelligence_dashboard(analysis, raw_data):
    """Display AI-analyzed regulatory intelligence with compliance visuals"""
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    
    # Compliance Overview
    overview = analysis['compliance_overview']
    st.success(f"**Compliance Overview:** {overview['total_regulations']} regulations monitored | {overview['high_impact_changes']} high-impact changes | Compliance score: {overview['compliance_score']}%")
    
    # Compliance Metrics Dashboard
    st.subheader("📊 Compliance Status Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_impact = len([r for r in analysis['regulatory_changes'] if r['impact_level'] == 'High'])
        st.metric("High Impact Changes", high_impact)
    with col2:
        high_risk = len([r for r in analysis['regulatory_changes'] if r['risk_level'] >= 70])
        st.metric("High Risk Regulations", high_risk)
    with col3:
        fully_compliant = len(analysis['compliance_matrix']['fully_compliant'])
        st.metric("Fully Compliant Categories", fully_compliant)
    with col4:
        urgent_actions = len(analysis['risk_assessment']['urgent_actions'])
        st.metric("Urgent Actions Required", urgent_actions)
    
    # Compliance Matrix Visualization
    st.subheader("🎯 Compliance Matrix")
    
    compliance_data = {
        'Status': ['Fully Compliant', 'Partial Compliance', 'Non-Compliant', 'Pending Changes'],
        'Count': [
            len(analysis['compliance_matrix']['fully_compliant']),
            len(analysis['compliance_matrix']['partial_compliance']),
            len(analysis['compliance_matrix']['non_compliant']),
            len(analysis['compliance_matrix']['pending_changes'])
        ],
        'Color': ['green', 'orange', 'red', 'blue']
    }
    
    fig_compliance = px.pie(
        values=compliance_data['Count'],
        names=compliance_data['Status'],
        title="Compliance Status Distribution",
        color_discrete_sequence=['#28a745', '#fd7e14', '#dc3545', '#007bff']
    )
    st.plotly_chart(fig_compliance, use_container_width=True)
    
    # Regulatory Risk Timeline
    st.subheader("📅 Regulatory Risk Timeline")
    
    if analysis['regulatory_changes']:
        reg_df = pd.DataFrame(analysis['regulatory_changes'])
        
        # Risk level chart
        fig_risk = px.bar(
            reg_df,
            x='regulation',
            y='risk_level',
            color='impact_level',
            title="Regulatory Risk Assessment",
            labels={'risk_level': 'Risk Level (0-100)', 'regulation': 'Regulation'}
        )
        fig_risk.update_xaxis(tickangle=45)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Risk Assessment Summary
    st.subheader("⚠️ Risk Assessment & Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**High Risk Areas:**")
        for area in analysis['risk_assessment']['high_risk_areas']:
            st.error(f"🚨 {area}")
        
        st.write("**Compliance Gaps:**")
        for gap in analysis['risk_assessment']['compliance_gaps']:
            st.warning(f"⚠️ {gap}")
    
    with col2:
        st.write("**Urgent Actions Required:**")
        for action in analysis['risk_assessment']['urgent_actions']:
            st.info(f"🔥 {action}")
    
    # Strategic Recommendations
    st.subheader("📋 Regulatory Compliance Recommendations")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.info(f"**Recommendation {i}:** {rec}")

def display_raw_regulatory_intelligence(regulatory_data):
    """Fallback display for raw regulatory intelligence"""
    st.warning("Displaying raw intelligence data - AI analysis unavailable")
    
    for category, intel_items in regulatory_data.items():
        with st.expander(f"⚖️ {category} ({len(intel_items)} items)"):
            for item in intel_items:
                st.write(f"• {item}")
                st.divider()

def render_innovation_intelligence_results(context):
    """Display innovation intelligence results with visual analytics"""
    st.subheader("🚀 Innovation & Technology Dashboard")
    st.caption("Technology disruption, innovation trends, and future market dynamics with visual analytics")
    
    # Check if we have mock data or real data
    if 'mock_innovation_data' in st.session_state:
        analyze_innovation_intelligence_with_ai(st.session_state.mock_innovation_data, context.get('categories', []))
        return
    
    if 'crawling_engine' in st.session_state:
        crawling_engine = st.session_state.crawling_engine
        try:
            data_summary = crawling_engine.get_database_summary()
            innovation_data = data_summary.get('innovation_intelligence', {})
            
            if innovation_data:
                analyze_innovation_intelligence_with_ai(innovation_data, context.get('categories', []))
            else:
                st.info("Run the comprehensive scan to gather innovation intelligence for visual analysis")
        except Exception as e:
            st.warning("Connect to external services to enable innovation monitoring")
    else:
        st.info("Intelligence engine not initialized")

def analyze_innovation_intelligence_with_ai(raw_data, categories):
    """Use AI to analyze innovation intelligence and create technology insights with visuals"""
    try:
        import os
        from openai import OpenAI
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        analysis_prompt = f"""
        Analyze this innovation and technology intelligence data for UK procurement categories: {categories}.
        Focus on technology disruption, innovation trends, and future market dynamics.
        
        Raw innovation data: {str(raw_data)[:2000]}
        
        Return a JSON object with this structure:
        {{
            "innovation_overview": {{
                "total_technologies": "number",
                "disruptive_trends": "number",
                "innovation_score": 0-100
            }},
            "technology_trends": [
                {{
                    "technology": "name",
                    "maturity_level": "Emerging/Developing/Mature",
                    "disruption_potential": 0-100,
                    "implementation_timeline": "Immediate/Short-term/Long-term",
                    "affected_categories": ["category1", "category2"],
                    "adoption_barriers": ["barrier1", "barrier2"],
                    "market_impact": "High/Medium/Low"
                }}
            ],
            "innovation_matrix": {{
                "emerging_tech": ["technologies"],
                "developing_tech": ["technologies"],
                "mature_tech": ["technologies"],
                "disruptive_tech": ["technologies"]
            }},
            "strategic_implications": {{
                "automation_opportunities": ["opportunities"],
                "efficiency_gains": ["gains"],
                "investment_priorities": ["priorities"]
            }},
            "recommendations": ["rec1", "rec2", "rec3"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        
        # Display AI analysis with innovation charts
        display_innovation_intelligence_dashboard(analysis, raw_data)
        
    except Exception as e:
        st.error(f"AI innovation analysis failed: {e}")
        # Display raw data as fallback
        display_raw_innovation_intelligence(raw_data)

def display_innovation_intelligence_dashboard(analysis, raw_data):
    """Display AI-analyzed innovation intelligence with technology visuals"""
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    
    # Innovation Overview
    overview = analysis['innovation_overview']
    st.success(f"**Innovation Overview:** {overview['total_technologies']} technologies tracked | {overview['disruptive_trends']} disruptive trends | Innovation score: {overview['innovation_score']}%")
    
    # Innovation Metrics Dashboard
    st.subheader("📊 Technology Innovation Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_disruption = len([t for t in analysis['technology_trends'] if t['disruption_potential'] >= 70])
        st.metric("High Disruption Potential", high_disruption)
    with col2:
        emerging_tech = len(analysis['innovation_matrix']['emerging_tech'])
        st.metric("Emerging Technologies", emerging_tech)
    with col3:
        immediate_impact = len([t for t in analysis['technology_trends'] if t['implementation_timeline'] == 'Immediate'])
        st.metric("Immediate Impact Tech", immediate_impact)
    with col4:
        automation_ops = len(analysis['strategic_implications']['automation_opportunities'])
        st.metric("Automation Opportunities", automation_ops)
    
    # Technology Maturity vs Disruption Matrix
    st.subheader("🎯 Technology Disruption Matrix")
    
    if analysis['technology_trends']:
        tech_df = pd.DataFrame(analysis['technology_trends'])
        
        # Create bubble chart
        fig_bubble = px.scatter(
            tech_df,
            x='maturity_level',
            y='disruption_potential',
            size='disruption_potential',
            color='market_impact',
            hover_name='technology',
            title="Technology Maturity vs Disruption Potential",
            labels={'disruption_potential': 'Disruption Potential (0-100)', 'maturity_level': 'Maturity Level'}
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    # Innovation Timeline
    st.subheader("📅 Innovation Implementation Timeline")
    
    timeline_data = {
        'Timeline': ['Immediate', 'Short-term', 'Long-term'],
        'Count': [
            len([t for t in analysis['technology_trends'] if t['implementation_timeline'] == 'Immediate']),
            len([t for t in analysis['technology_trends'] if t['implementation_timeline'] == 'Short-term']),
            len([t for t in analysis['technology_trends'] if t['implementation_timeline'] == 'Long-term'])
        ]
    }
    
    fig_timeline = px.bar(
        x=timeline_data['Timeline'],
        y=timeline_data['Count'],
        title="Technology Implementation Timeline",
        labels={'x': 'Implementation Timeline', 'y': 'Number of Technologies'}
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Strategic Implications
    st.subheader("🚀 Strategic Technology Implications")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Automation Opportunities:**")
        for opp in analysis['strategic_implications']['automation_opportunities']:
            st.success(f"🤖 {opp}")
        
        st.write("**Efficiency Gains:**")
        for gain in analysis['strategic_implications']['efficiency_gains']:
            st.info(f"⚡ {gain}")
    
    with col2:
        st.write("**Investment Priorities:**")
        for priority in analysis['strategic_implications']['investment_priorities']:
            st.warning(f"💰 {priority}")
    
    # Strategic Recommendations
    st.subheader("📋 Innovation Strategy Recommendations")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.info(f"**Recommendation {i}:** {rec}")

def display_raw_innovation_intelligence(innovation_data):
    """Fallback display for raw innovation intelligence"""
    st.warning("Displaying raw intelligence data - AI analysis unavailable")
    
    for category, intel_items in innovation_data.items():
        with st.expander(f"🚀 {category} ({len(intel_items)} items)"):
            for item in intel_items:
                st.write(f"• {item}")
                st.divider()

def render_market_entrants_results(context):
    """Display market entrants results with visual analytics"""
    st.subheader("🌟 New Market Entrants Dashboard")
    st.caption("Emerging suppliers, market disruption, and competitive landscape changes with visual analytics")
    
    # Check if we have mock data or real data
    if 'mock_market_entrants_data' in st.session_state:
        analyze_market_entrants_with_ai(st.session_state.mock_market_entrants_data, context.get('categories', []))
        return
    
    if 'crawling_engine' in st.session_state:
        crawling_engine = st.session_state.crawling_engine
        try:
            data_summary = crawling_engine.get_database_summary()
            entrants_data = data_summary.get('market_entrants', {})
            
            if entrants_data:
                analyze_market_entrants_with_ai(entrants_data, context.get('categories', []))
            else:
                st.info("Run the comprehensive scan to gather market entrants intelligence for visual analysis")
        except Exception as e:
            st.warning("Connect to external services to enable market entrants monitoring")
    else:
        st.info("Intelligence engine not initialized")

def analyze_market_entrants_with_ai(raw_data, categories):
    """Use AI to analyze market entrants and create competitive landscape insights with visuals"""
    try:
        import os
        from openai import OpenAI
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        analysis_prompt = f"""
        Analyze this market entrants intelligence data for UK procurement categories: {categories}.
        Focus on emerging suppliers, competitive threats, and market disruption patterns.
        
        Raw market entrants data: {str(raw_data)[:2000]}
        
        Return a JSON object with this structure:
        {{
            "market_overview": {{
                "new_entrants": "number",
                "market_disruption_level": "High/Medium/Low",
                "competitive_intensity": 0-100
            }},
            "new_suppliers": [
                {{
                    "company": "name",
                    "entry_date": "date or recent",
                    "market_share": 0-100,
                    "growth_rate": "percentage",
                    "competitive_advantage": "description",
                    "threat_level": "High/Medium/Low",
                    "target_categories": ["category1", "category2"],
                    "financial_backing": "High/Medium/Low"
                }}
            ],
            "competitive_landscape": {{
                "high_threat": ["companies"],
                "emerging_players": ["companies"],
                "niche_specialists": ["companies"],
                "tech_disruptors": ["companies"]
            }},
            "market_impacts": {{
                "pricing_pressure": ["categories"],
                "innovation_drivers": ["categories"],
                "consolidation_risks": ["categories"]
            }},
            "recommendations": ["rec1", "rec2", "rec3"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        
        # Display AI analysis with market entrants charts
        display_market_entrants_dashboard(analysis, raw_data)
        
    except Exception as e:
        st.error(f"AI market entrants analysis failed: {e}")
        # Display raw data as fallback
        display_raw_market_entrants(raw_data)

def display_market_entrants_dashboard(analysis, raw_data):
    """Display AI-analyzed market entrants with competitive landscape visuals"""
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    
    # Market Overview
    overview = analysis['market_overview']
    st.success(f"**Market Overview:** {overview['new_entrants']} new entrants | Disruption level: {overview['market_disruption_level']} | Competitive intensity: {overview['competitive_intensity']}%")
    
    # Competitive Metrics Dashboard
    st.subheader("📊 Competitive Landscape Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_threat = len(analysis['competitive_landscape']['high_threat'])
        st.metric("High Threat Entrants", high_threat)
    with col2:
        emerging_players = len(analysis['competitive_landscape']['emerging_players'])
        st.metric("Emerging Players", emerging_players)
    with col3:
        tech_disruptors = len(analysis['competitive_landscape']['tech_disruptors'])
        st.metric("Technology Disruptors", tech_disruptors)
    with col4:
        pricing_pressure = len(analysis['market_impacts']['pricing_pressure'])
        st.metric("Categories Under Pressure", pricing_pressure)
    
    # Market Share vs Growth Analysis
    st.subheader("🎯 Competitive Positioning Matrix")
    
    if analysis['new_suppliers']:
        suppliers_df = pd.DataFrame(analysis['new_suppliers'])
        
        # Convert growth rate to numeric
        suppliers_df['growth_numeric'] = suppliers_df['growth_rate'].str.replace('%', '').astype(float)
        
        # Create scatter plot
        fig_competitive = px.scatter(
            suppliers_df,
            x='market_share',
            y='growth_numeric',
            size='market_share',
            color='threat_level',
            hover_name='company',
            title="Market Share vs Growth Rate Analysis",
            labels={'market_share': 'Market Share (%)', 'growth_numeric': 'Growth Rate (%)'}
        )
        st.plotly_chart(fig_competitive, use_container_width=True)
    
    # Threat Level Distribution
    st.subheader("⚠️ Competitive Threat Assessment")
    
    threat_data = {
        'Threat Level': ['High Threat', 'Emerging Players', 'Niche Specialists', 'Tech Disruptors'],
        'Count': [
            len(analysis['competitive_landscape']['high_threat']),
            len(analysis['competitive_landscape']['emerging_players']),
            len(analysis['competitive_landscape']['niche_specialists']),
            len(analysis['competitive_landscape']['tech_disruptors'])
        ]
    }
    
    fig_threats = px.pie(
        values=threat_data['Count'],
        names=threat_data['Threat Level'],
        title="Competitive Threat Distribution",
        color_discrete_sequence=['#dc3545', '#fd7e14', '#28a745', '#6f42c1']
    )
    st.plotly_chart(fig_threats, use_container_width=True)
    
    # Market Impact Analysis
    st.subheader("📈 Market Impact Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Categories Under Pricing Pressure:**")
        for category in analysis['market_impacts']['pricing_pressure']:
            st.error(f"💰 {category}")
        
        st.write("**Innovation Drivers:**")
        for driver in analysis['market_impacts']['innovation_drivers']:
            st.success(f"🚀 {driver}")
    
    with col2:
        st.write("**Consolidation Risks:**")
        for risk in analysis['market_impacts']['consolidation_risks']:
            st.warning(f"🔄 {risk}")
    
    # Strategic Recommendations
    st.subheader("📋 Competitive Strategy Recommendations")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.info(f"**Recommendation {i}:** {rec}")

def display_raw_market_entrants(entrants_data):
    """Fallback display for raw market entrants intelligence"""
    st.warning("Displaying raw intelligence data - AI analysis unavailable")
    
    for category, intel_items in entrants_data.items():
        with st.expander(f"🌟 {category} ({len(intel_items)} items)"):
            for item in intel_items:
                st.write(f"• {item}")
                st.divider()
    
    if 'crawling_engine' in st.session_state:
        crawling_engine = st.session_state.crawling_engine
        conn = sqlite3.connect(crawling_engine.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM market_entrants")
            count = cursor.fetchone()[0]
            
            if count > 0:
                st.success(f"Market entrants intelligence available for {count} records")
                
                cursor.execute("SELECT title, crawled_at FROM market_entrants ORDER BY crawled_at DESC LIMIT 10")
                results = cursor.fetchall()
                
                for result in results:
                    with st.expander(f"🌟 {result[0]}"):
                        st.write(f"**Collected:** {result[1]}")
            else:
                st.info("Run the comprehensive scan to gather market entrants intelligence")
        except Exception:
            st.warning("Database schema updating. Run the comprehensive scan to initialize properly.")
        
        conn.close()
    else:
        st.info("Intelligence engine not initialized")

def render_category_intelligence_tab(context, crawling_engine, search_engine):
    """Render category intelligence tab"""
    st.subheader("📊 Category Market Intelligence")
    st.caption("Price trends, supply-demand dynamics, and market evolution analysis")
    
    if context['categories']:
        st.write("**Your Categories:**")
        for category in context['categories']:
            st.write(f"• {category}")
        
        if st.button("📈 Analyze Category Markets", key="category_intel"):
            with st.spinner("Analyzing category markets..."):
                progress_placeholder = st.empty()
                
                for category in context['categories'][:3]:
                    def progress_callback(message):
                        progress_placeholder.info(message)
                    
                    data = crawling_engine.crawl_category_intelligence(category, search_engine, progress_callback)
                    st.success(f"Analyzed {len(data)} market trends for {category}")
                
                progress_placeholder.empty()
    else:
        st.info("No categories identified in your data. Please ensure your data contains category/type columns.")

def render_regulatory_monitoring_tab(context, crawling_engine, search_engine):
    """Render regulatory monitoring tab"""
    st.subheader("⚖️ Regulatory Change Monitoring")
    st.caption("Compliance requirements, environmental regulations, and trade policy impacts")
    
    if st.button("🔍 Monitor Regulatory Changes", key="regulatory_intel"):
        with st.spinner("Monitoring regulatory landscape..."):
            progress_placeholder = st.empty()
            
            def progress_callback(message):
                progress_placeholder.info(message)
            
            data = crawling_engine.crawl_regulatory_intelligence(context['categories'], search_engine, progress_callback)
            st.success(f"Found {len(data)} regulatory updates affecting your categories")
            
            progress_placeholder.empty()

def render_innovation_intelligence_tab(context, crawling_engine, search_engine):
    """Render innovation intelligence tab"""
    st.subheader("🚀 Innovation & Technology Disruption")
    st.caption("Emerging technologies, digital transformation, and supply chain innovations")
    
    if st.button("💡 Track Innovation Trends", key="innovation_intel"):
        with st.spinner("Tracking innovation trends..."):
            progress_placeholder = st.empty()
            
            def progress_callback(message):
                progress_placeholder.info(message)
            
            data = crawling_engine.crawl_innovation_intelligence(context['categories'], search_engine, progress_callback)
            st.success(f"Identified {len(data)} innovation trends affecting your supply chain")
            
            progress_placeholder.empty()

def render_market_entrants_tab(context, crawling_engine, search_engine):
    """Render market entrants tab"""
    st.subheader("🌟 New Market Entrants & Competitive Landscape")
    st.caption("Startup companies, market expansions, and competitive disruptions")
    
    if st.button("🔍 Discover Market Entrants", key="entrants_intel"):
        with st.spinner("Discovering new market entrants..."):
            progress_placeholder = st.empty()
            
            def progress_callback(message):
                progress_placeholder.info(message)
            
            data = crawling_engine.crawl_market_entrants(context['categories'], search_engine, progress_callback)
            st.success(f"Discovered {len(data)} new market entrants in your categories")
            
            progress_placeholder.empty()

def render_intelligence_database_viewer(crawling_engine):
    """Render comprehensive database viewer"""
    st.subheader("🗄️ Intelligence Database Viewer")
    st.caption("View all collected intelligence data with comprehensive analytics")
    
    summary = crawling_engine.get_database_summary()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_records = sum(summary[table]['total_records'] for table in summary)
        st.metric("Total Intelligence Items", total_records)
    with col2:
        total_sources = sum(summary[table]['unique_sources'] for table in summary)
        st.metric("Unique Sources", total_sources)
    with col3:
        intelligence_areas = len([table for table in summary if summary[table]['total_records'] > 0])
        st.metric("Active Intelligence Areas", intelligence_areas)
    with col4:
        coverage_percentage = (intelligence_areas / 5) * 100
        st.metric("Coverage", f"{coverage_percentage:.0f}%")
    
    # Detailed breakdown
    st.subheader("📊 Intelligence Breakdown")
    
    breakdown_data = []
    for table, data in summary.items():
        area_name = table.replace('_', ' ').title()
        breakdown_data.append({
            'Intelligence Area': area_name,
            'Records': data['total_records'],
            'Unique Sources': data['unique_sources']
        })
    
    if breakdown_data:
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True)
        
        # Visualization
        fig = px.bar(breakdown_df, x='Intelligence Area', y='Records', 
                     title="Intelligence Records by Area",
                     color='Records', color_continuous_scale='viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No intelligence data collected yet. Run the comprehensive scan to populate the database.")