"""
Advanced Market Context Engine
Comprehensive market intelligence with regulatory, economic, and competitive analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import sqlite3

@dataclass
class RegulatoryAlert:
    """Regulatory change alert"""
    title: str
    description: str
    impact_level: str  # 'high', 'medium', 'low'
    affected_categories: List[str]
    compliance_deadline: Optional[datetime]
    source: str
    date_published: datetime

@dataclass
class EconomicIndicator:
    """Economic indicator affecting procurement"""
    indicator_name: str
    current_value: float
    trend: str  # 'up', 'down', 'stable'
    impact_on_procurement: str
    affected_categories: List[str]
    confidence_level: float

@dataclass
class CompetitiveIntelligence:
    """Competitive supplier intelligence"""
    competitor_name: str
    market_share: float
    strengths: List[str]
    weaknesses: List[str]
    pricing_strategy: str
    threat_level: str  # 'high', 'medium', 'low'

@dataclass
class TechnologyTrend:
    """Technology trend affecting supply chain"""
    trend_name: str
    description: str
    maturity_level: str  # 'emerging', 'developing', 'mature'
    impact_timeline: str  # 'immediate', 'short-term', 'long-term'
    affected_suppliers: List[str]
    disruption_potential: float

class AdvancedMarketContext:
    """Advanced market context analysis engine"""
    
    def __init__(self, search_engine, ai_analyzer, web_crawler):
        self.search_engine = search_engine
        self.ai_analyzer = ai_analyzer
        self.web_crawler = web_crawler
        self.db_path = "advanced_market_intelligence.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize database for advanced market intelligence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Regulatory alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS regulatory_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                impact_level TEXT,
                affected_categories TEXT,
                compliance_deadline TEXT,
                source TEXT,
                date_published TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Economic indicators table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS economic_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_name TEXT,
                current_value REAL,
                trend TEXT,
                impact_description TEXT,
                affected_categories TEXT,
                confidence_level REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Technology trends table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technology_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trend_name TEXT,
                description TEXT,
                maturity_level TEXT,
                impact_timeline TEXT,
                affected_suppliers TEXT,
                disruption_potential REAL,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_regulatory_landscape(self, context: Dict[str, Any], progress_callback=None) -> List[RegulatoryAlert]:
        """Analyze regulatory changes affecting procurement categories"""
        categories = context.get('categories', [])
        alerts = []
        
        if progress_callback:
            progress_callback("Analyzing regulatory landscape for procurement categories...")
        
        for category in categories[:3]:
            queries = [
                f"{category} regulatory changes 2024 compliance requirements",
                f"{category} industry regulations procurement impact",
                f"{category} government policy changes supply chain"
            ]
            
            for query in queries:
                if progress_callback:
                    progress_callback(f"Searching regulatory updates: {query}")
                
                results = self.search_engine.search_market_data(query, 2)
                
                for result in results:
                    content = self.web_crawler.crawl_web_content(result['link'])
                    if content:
                        analysis = self.ai_analyzer.analyze_with_ai(content, {
                            **context,
                            'analysis_type': 'regulatory_analysis',
                            'category_focus': category
                        })
                        
                        impact_level = analysis.get('regulatory_impact', 'medium')
                        if impact_level in ['high', 'medium', 'low']:
                            alert = RegulatoryAlert(
                                title=result['title'][:100],
                                description=analysis.get('regulatory_summary', '')[:300],
                                impact_level=impact_level,
                                affected_categories=[category],
                                compliance_deadline=None,  # Would be extracted from content
                                source=result['source'],
                                date_published=datetime.now() - timedelta(days=len(alerts))
                            )
                            alerts.append(alert)
                        
                        if progress_callback:
                            progress_callback(f"Found regulatory alert: {impact_level} impact for {category}")
        
        # Save to database
        self._save_regulatory_alerts(alerts)
        return alerts[:5]
    
    def analyze_economic_indicators(self, context: Dict[str, Any], progress_callback=None) -> List[EconomicIndicator]:
        """Analyze economic indicators affecting procurement costs"""
        categories = context.get('categories', [])
        indicators = []
        
        if progress_callback:
            progress_callback("Analyzing economic indicators affecting procurement...")
        
        # Key economic indicators to monitor
        economic_queries = [
            "inflation rate impact procurement costs 2024",
            "supply chain inflation commodity prices",
            "interest rates business investment procurement",
            "currency exchange rates import costs",
            "labor costs impact service procurement"
        ]
        
        for query in economic_queries:
            if progress_callback:
                progress_callback(f"Analyzing: {query}")
            
            results = self.search_engine.search_market_data(query, 2)
            
            for result in results:
                content = self.web_crawler.crawl_web_content(result['link'])
                if content:
                    analysis = self.ai_analyzer.analyze_with_ai(content, {
                        **context,
                        'analysis_type': 'economic_analysis'
                    })
                    
                    indicator = EconomicIndicator(
                        indicator_name=query.split()[0].title(),
                        current_value=analysis.get('indicator_value', 0.0),
                        trend=analysis.get('trend', 'stable'),
                        impact_on_procurement=analysis.get('procurement_impact', 'moderate'),
                        affected_categories=categories,
                        confidence_level=analysis.get('confidence', 0.7)
                    )
                    indicators.append(indicator)
                    
                    if progress_callback:
                        progress_callback(f"Economic indicator: {indicator.indicator_name} - {indicator.trend} trend")
        
        return indicators[:6]
    
    def discover_alternative_suppliers(self, context: Dict[str, Any], progress_callback=None) -> List[CompetitiveIntelligence]:
        """Discover alternative suppliers and competitive intelligence"""
        current_suppliers = context.get('suppliers', [])
        categories = context.get('categories', [])
        competitive_intel = []
        
        if progress_callback:
            progress_callback("Discovering alternative suppliers and competitive landscape...")
        
        for category in categories[:2]:
            queries = [
                f"leading {category} suppliers market leaders 2024",
                f"emerging {category} companies competitive alternatives",
                f"{category} vendor comparison market analysis"
            ]
            
            for query in queries:
                if progress_callback:
                    progress_callback(f"Searching: {query}")
                
                results = self.search_engine.search_market_data(query, 3)
                
                for result in results:
                    content = self.web_crawler.crawl_web_content(result['link'])
                    if content:
                        analysis = self.ai_analyzer.analyze_with_ai(content, {
                            **context,
                            'analysis_type': 'competitive_analysis',
                            'current_suppliers': current_suppliers
                        })
                        
                        competitor_name = analysis.get('competitor_name', f"Alternative Supplier {len(competitive_intel) + 1}")
                        
                        # Skip if this is already a current supplier
                        if not any(supplier.lower() in competitor_name.lower() for supplier in current_suppliers):
                            intel = CompetitiveIntelligence(
                                competitor_name=competitor_name,
                                market_share=analysis.get('market_share', 15.0),
                                strengths=analysis.get('strengths', []),
                                weaknesses=analysis.get('weaknesses', []),
                                pricing_strategy=analysis.get('pricing_strategy', 'competitive'),
                                threat_level=analysis.get('threat_level', 'medium')
                            )
                            competitive_intel.append(intel)
                            
                            if progress_callback:
                                progress_callback(f"Found alternative: {competitor_name} - {intel.threat_level} threat level")
        
        return competitive_intel[:8]
    
    def analyze_technology_trends(self, context: Dict[str, Any], progress_callback=None) -> List[TechnologyTrend]:
        """Analyze technology trends impacting suppliers and supply chain"""
        categories = context.get('categories', [])
        suppliers = context.get('suppliers', [])
        trends = []
        
        if progress_callback:
            progress_callback("Analyzing technology trends affecting supply chain...")
        
        tech_queries = [
            "artificial intelligence supply chain automation trends",
            "blockchain procurement transparency technology",
            "IoT supply chain monitoring innovations",
            "sustainability technology green procurement",
            "digital transformation supplier capabilities"
        ]
        
        for query in tech_queries:
            if progress_callback:
                progress_callback(f"Analyzing: {query}")
            
            results = self.search_engine.search_market_data(query, 2)
            
            for result in results:
                content = self.web_crawler.crawl_web_content(result['link'])
                if content:
                    analysis = self.ai_analyzer.analyze_with_ai(content, {
                        **context,
                        'analysis_type': 'technology_analysis'
                    })
                    
                    trend = TechnologyTrend(
                        trend_name=analysis.get('technology_name', query.split()[0].title()),
                        description=analysis.get('technology_description', '')[:200],
                        maturity_level=analysis.get('maturity', 'developing'),
                        impact_timeline=analysis.get('timeline', 'short-term'),
                        affected_suppliers=suppliers[:3],
                        disruption_potential=analysis.get('disruption_score', 50.0)
                    )
                    trends.append(trend)
                    
                    if progress_callback:
                        progress_callback(f"Technology trend: {trend.trend_name} - {trend.maturity_level}")
        
        # Save to database
        self._save_technology_trends(trends)
        return trends[:6]
    
    def _save_regulatory_alerts(self, alerts: List[RegulatoryAlert]):
        """Save regulatory alerts to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for alert in alerts:
            cursor.execute('''
                INSERT INTO regulatory_alerts 
                (title, description, impact_level, affected_categories, source, date_published)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                alert.title,
                alert.description,
                alert.impact_level,
                json.dumps(alert.affected_categories),
                alert.source,
                alert.date_published
            ))
        
        conn.commit()
        conn.close()
    
    def _save_technology_trends(self, trends: List[TechnologyTrend]):
        """Save technology trends to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for trend in trends:
            cursor.execute('''
                INSERT INTO technology_trends 
                (trend_name, description, maturity_level, impact_timeline, 
                 affected_suppliers, disruption_potential)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                trend.trend_name,
                trend.description,
                trend.maturity_level,
                trend.impact_timeline,
                json.dumps(trend.affected_suppliers),
                trend.disruption_potential
            ))
        
        conn.commit()
        conn.close()

def render_advanced_market_context(context: Dict[str, Any], engine):
    """Render advanced market context analysis"""
    st.subheader("🌐 Advanced Market Context")
    
    # Initialize advanced context engine
    advanced_engine = AdvancedMarketContext(engine, engine, engine)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏛️ Regulatory Analysis", help="Analyze regulatory changes affecting your categories"):
            with st.spinner("Analyzing regulatory landscape..."):
                progress_placeholder = st.empty()
                
                def progress_callback(message):
                    progress_placeholder.info(message)
                
                alerts = advanced_engine.analyze_regulatory_landscape(context, progress_callback)
                progress_placeholder.empty()
                
                st.success(f"Found {len(alerts)} regulatory alerts")
                
                for alert in alerts:
                    with st.expander(f"⚠️ {alert.title[:50]}..."):
                        st.write(f"**Impact Level:** {alert.impact_level.title()}")
                        st.write(f"**Categories:** {', '.join(alert.affected_categories)}")
                        st.write(f"**Source:** {alert.source}")
                        st.write(f"**Description:** {alert.description}")
    
    with col2:
        if st.button("📊 Economic Indicators", help="Analyze economic factors affecting procurement"):
            with st.spinner("Analyzing economic indicators..."):
                progress_placeholder = st.empty()
                
                def progress_callback(message):
                    progress_placeholder.info(message)
                
                indicators = advanced_engine.analyze_economic_indicators(context, progress_callback)
                progress_placeholder.empty()
                
                st.success(f"Analyzed {len(indicators)} economic indicators")
                
                for indicator in indicators:
                    with st.expander(f"📈 {indicator.indicator_name}"):
                        st.write(f"**Trend:** {indicator.trend.title()}")
                        st.write(f"**Impact:** {indicator.impact_on_procurement}")
                        st.write(f"**Confidence:** {indicator.confidence_level:.1%}")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🔍 Alternative Suppliers", help="Discover competitive alternatives"):
            with st.spinner("Discovering alternative suppliers..."):
                progress_placeholder = st.empty()
                
                def progress_callback(message):
                    progress_placeholder.info(message)
                
                competitors = advanced_engine.discover_alternative_suppliers(context, progress_callback)
                progress_placeholder.empty()
                
                st.success(f"Discovered {len(competitors)} alternative suppliers")
                
                for competitor in competitors:
                    with st.expander(f"🏢 {competitor.competitor_name}"):
                        st.write(f"**Market Share:** {competitor.market_share:.1f}%")
                        st.write(f"**Threat Level:** {competitor.threat_level.title()}")
                        st.write(f"**Pricing Strategy:** {competitor.pricing_strategy}")
                        if competitor.strengths:
                            st.write(f"**Strengths:** {', '.join(competitor.strengths[:3])}")
    
    with col4:
        if st.button("🚀 Technology Trends", help="Analyze technology disruption trends"):
            with st.spinner("Analyzing technology trends..."):
                progress_placeholder = st.empty()
                
                def progress_callback(message):
                    progress_placeholder.info(message)
                
                trends = advanced_engine.analyze_technology_trends(context, progress_callback)
                progress_placeholder.empty()
                
                st.success(f"Analyzed {len(trends)} technology trends")
                
                for trend in trends:
                    with st.expander(f"💡 {trend.trend_name}"):
                        st.write(f"**Maturity:** {trend.maturity_level.title()}")
                        st.write(f"**Timeline:** {trend.impact_timeline}")
                        st.write(f"**Disruption Potential:** {trend.disruption_potential:.1f}%")
                        st.write(f"**Description:** {trend.description}")