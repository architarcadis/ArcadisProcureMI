"""
Interactive Geopolitical Impact Visualizer
Real-time analysis of geopolitical events affecting supply chain and procurement
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import sqlite3
import pycountry

@dataclass
class GeopoliticalEvent:
    """Geopolitical event affecting supply chain"""
    event_id: str
    title: str
    description: str
    country: str
    region: str
    event_type: str  # 'conflict', 'sanctions', 'trade_dispute', 'regulatory', 'natural_disaster'
    severity: str  # 'low', 'medium', 'high', 'critical'
    start_date: datetime
    affected_industries: List[str]
    supply_chain_impact: float  # 0-100 scale
    confidence_level: float
    source: str

@dataclass
class SupplierRiskProfile:
    """Supplier risk profile based on geopolitical factors"""
    supplier_name: str
    primary_country: str
    secondary_countries: List[str]
    current_risk_score: float
    risk_factors: List[str]
    affected_events: List[GeopoliticalEvent]
    mitigation_recommendations: List[str]

class GeopoliticalImpactAnalyzer:
    """Analyze geopolitical impacts on supply chain"""
    
    def __init__(self, search_engine, ai_analyzer, web_crawler):
        self.search_engine = search_engine
        self.ai_analyzer = ai_analyzer
        self.web_crawler = web_crawler
        self.db_path = "geopolitical_intelligence.db"
        self._init_database()
        self._init_country_data()
    
    def _init_database(self):
        """Initialize database for geopolitical intelligence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geopolitical_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                title TEXT,
                description TEXT,
                country TEXT,
                region TEXT,
                event_type TEXT,
                severity TEXT,
                start_date TIMESTAMP,
                affected_industries TEXT,
                supply_chain_impact REAL,
                confidence_level REAL,
                source TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS supplier_risk_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT,
                primary_country TEXT,
                secondary_countries TEXT,
                current_risk_score REAL,
                risk_factors TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_country_data(self):
        """Initialize country and region mapping"""
        self.country_regions = {
            'United States': 'North America',
            'Canada': 'North America',
            'Mexico': 'North America',
            'United Kingdom': 'Europe',
            'Germany': 'Europe',
            'France': 'Europe',
            'China': 'Asia Pacific',
            'Japan': 'Asia Pacific',
            'India': 'Asia Pacific',
            'Brazil': 'South America',
            'Russia': 'Europe/Asia',
            'South Africa': 'Africa'
        }
    
    def analyze_geopolitical_events(self, context: Dict[str, Any], progress_callback=None) -> List[GeopoliticalEvent]:
        """Analyze current geopolitical events affecting supply chain"""
        events = []
        
        if progress_callback:
            progress_callback("Analyzing global geopolitical events affecting supply chains...")
        
        # Key geopolitical search queries
        geopolitical_queries = [
            "international trade sanctions supply chain impact 2024",
            "geopolitical tensions affecting global procurement",
            "regional conflicts supply chain disruption",
            "trade war impact procurement costs",
            "regulatory changes international suppliers"
        ]
        
        for query in geopolitical_queries:
            if progress_callback:
                progress_callback(f"Searching: {query}")
            
            results = self.search_engine.search_market_data(query, 3)
            
            for result in results:
                content = self.web_crawler.crawl_web_content(result['link'])
                if content:
                    analysis = self.ai_analyzer.analyze_with_ai(content, {
                        **context,
                        'analysis_type': 'geopolitical_analysis'
                    })
                    
                    # Extract geopolitical event details
                    country = analysis.get('affected_country', 'Global')
                    region = self.country_regions.get(country, 'Global')
                    event_type = analysis.get('event_type', 'regulatory')
                    severity = analysis.get('severity', 'medium')
                    impact_score = analysis.get('supply_chain_impact', 50.0)
                    
                    event = GeopoliticalEvent(
                        event_id=f"geo_{len(events) + 1}",
                        title=result['title'][:100],
                        description=analysis.get('event_description', '')[:300],
                        country=country,
                        region=region,
                        event_type=event_type,
                        severity=severity,
                        start_date=datetime.now() - timedelta(days=len(events)),
                        affected_industries=context.get('categories', []),
                        supply_chain_impact=impact_score,
                        confidence_level=analysis.get('confidence', 0.75),
                        source=result['source']
                    )
                    events.append(event)
                    
                    if progress_callback:
                        progress_callback(f"Found event: {country} - {severity} severity, {impact_score:.1f}% impact")
        
        # Save events to database
        self._save_geopolitical_events(events)
        return events[:10]
    
    def analyze_supplier_geopolitical_risk(self, context: Dict[str, Any], progress_callback=None) -> List[SupplierRiskProfile]:
        """Analyze geopolitical risk for each supplier"""
        suppliers = context.get('suppliers', [])
        risk_profiles = []
        
        if progress_callback:
            progress_callback(f"Analyzing geopolitical risk for {len(suppliers)} suppliers...")
        
        for supplier in suppliers[:5]:
            if progress_callback:
                progress_callback(f"Assessing geopolitical risk for {supplier}...")
            
            # Search for supplier location and geopolitical exposure
            queries = [
                f"{supplier} headquarters location country operations",
                f"{supplier} international operations global presence",
                f"{supplier} geopolitical risk exposure analysis"
            ]
            
            risk_factors = []
            countries = []
            risk_scores = []
            
            for query in queries:
                results = self.search_engine.search_market_data(query, 2)
                
                for result in results:
                    content = self.web_crawler.crawl_web_content(result['link'])
                    if content:
                        analysis = self.ai_analyzer.analyze_with_ai(content, {
                            **context,
                            'supplier_focus': supplier,
                            'analysis_type': 'supplier_geopolitical_risk'
                        })
                        
                        # Extract location data
                        primary_country = analysis.get('primary_country', 'Unknown')
                        secondary_countries = analysis.get('secondary_countries', [])
                        
                        if primary_country != 'Unknown':
                            countries.append(primary_country)
                        countries.extend(secondary_countries)
                        
                        # Extract risk factors
                        supplier_risk_factors = analysis.get('risk_factors', [])
                        risk_factors.extend(supplier_risk_factors)
                        
                        # Calculate risk score
                        risk_score = analysis.get('geopolitical_risk_score', 40.0)
                        risk_scores.append(risk_score)
            
            # Calculate overall risk profile
            avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 40.0
            unique_countries = list(set(countries))
            primary_country = unique_countries[0] if unique_countries else 'Unknown'
            secondary_countries = unique_countries[1:5] if len(unique_countries) > 1 else []
            
            # Generate mitigation recommendations
            recommendations = self._generate_geopolitical_recommendations(
                supplier, primary_country, avg_risk, risk_factors
            )
            
            profile = SupplierRiskProfile(
                supplier_name=supplier,
                primary_country=primary_country,
                secondary_countries=secondary_countries,
                current_risk_score=round(avg_risk, 1),
                risk_factors=list(set(risk_factors))[:5],
                affected_events=[],  # Would be populated by matching events
                mitigation_recommendations=recommendations
            )
            risk_profiles.append(profile)
            
            if progress_callback:
                progress_callback(f"Risk assessment complete: {supplier} - {avg_risk:.1f}% risk in {primary_country}")
        
        return risk_profiles
    
    def _generate_geopolitical_recommendations(self, supplier: str, country: str, risk_score: float, risk_factors: List[str]) -> List[str]:
        """Generate geopolitical risk mitigation recommendations"""
        recommendations = []
        
        if risk_score > 70:
            recommendations.extend([
                f"Consider diversifying suppliers away from {country} due to high geopolitical risk",
                "Implement dual sourcing strategy for critical components",
                "Establish buffer inventory for supply chain resilience"
            ])
        elif risk_score > 50:
            recommendations.extend([
                f"Monitor geopolitical developments in {country} closely",
                "Develop contingency plans for supply disruption",
                "Assess alternative suppliers in stable regions"
            ])
        else:
            recommendations.extend([
                f"Current geopolitical risk in {country} is manageable",
                "Maintain regular monitoring of regional stability",
                "Consider expanding partnerships given stable environment"
            ])
        
        # Risk factor specific recommendations
        if 'trade_tensions' in str(risk_factors).lower():
            recommendations.append("Monitor trade policy changes and tariff implications")
        if 'sanctions' in str(risk_factors).lower():
            recommendations.append("Ensure compliance with international sanctions regulations")
        if 'conflict' in str(risk_factors).lower():
            recommendations.append("Develop crisis management protocols for conflict scenarios")
        
        return recommendations[:4]
    
    def _save_geopolitical_events(self, events: List[GeopoliticalEvent]):
        """Save geopolitical events to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for event in events:
            cursor.execute('''
                INSERT OR REPLACE INTO geopolitical_events 
                (event_id, title, description, country, region, event_type, 
                 severity, start_date, affected_industries, supply_chain_impact, 
                 confidence_level, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.event_id,
                event.title,
                event.description,
                event.country,
                event.region,
                event.event_type,
                event.severity,
                event.start_date,
                json.dumps(event.affected_industries),
                event.supply_chain_impact,
                event.confidence_level,
                event.source
            ))
        
        conn.commit()
        conn.close()

def create_geopolitical_risk_map(risk_profiles: List[SupplierRiskProfile]) -> go.Figure:
    """Create interactive world map showing supplier geopolitical risks"""
    
    # Prepare data for visualization
    countries = []
    risk_scores = []
    supplier_counts = []
    
    country_data = {}
    for profile in risk_profiles:
        country = profile.primary_country
        if country != 'Unknown':
            if country not in country_data:
                country_data[country] = {
                    'risk_scores': [],
                    'suppliers': []
                }
            country_data[country]['risk_scores'].append(profile.current_risk_score)
            country_data[country]['suppliers'].append(profile.supplier_name)
    
    # Calculate averages per country
    for country, data in country_data.items():
        countries.append(country)
        risk_scores.append(np.mean(data['risk_scores']))
        supplier_counts.append(len(data['suppliers']))
    
    if not countries:
        # Create empty map if no data
        fig = go.Figure(go.Scattergeo())
        fig.update_layout(
            title="Supplier Geopolitical Risk Map",
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular')
        )
        return fig
    
    # Create choropleth map
    fig = go.Figure(data=go.Choropleth(
        locations=countries,
        z=risk_scores,
        locationmode='country names',
        colorscale='RdYlGn_r',
        text=[f"{country}<br>Risk Score: {score:.1f}<br>Suppliers: {count}" 
              for country, score, count in zip(countries, risk_scores, supplier_counts)],
        hovertemplate='<b>%{text}</b><extra></extra>',
        colorbar_title="Risk Score"
    ))
    
    fig.update_layout(
        title="Supplier Geopolitical Risk Map",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        height=500
    )
    
    return fig

def create_risk_timeline(events: List[GeopoliticalEvent]) -> go.Figure:
    """Create timeline of geopolitical events"""
    
    if not events:
        fig = go.Figure()
        fig.add_annotation(text="No geopolitical events data available", 
                          x=0.5, y=0.5, xref="paper", yref="paper")
        return fig
    
    # Prepare timeline data
    dates = [event.start_date for event in events]
    impacts = [event.supply_chain_impact for event in events]
    severities = [event.severity for event in events]
    titles = [event.title[:50] + '...' if len(event.title) > 50 else event.title for event in events]
    countries = [event.country for event in events]
    
    # Color mapping for severity
    severity_colors = {
        'low': 'green',
        'medium': 'orange', 
        'high': 'red',
        'critical': 'darkred'
    }
    colors = [severity_colors.get(sev, 'blue') for sev in severities]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=impacts,
        mode='markers+text',
        marker=dict(
            size=[impact/3 for impact in impacts],
            color=colors,
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        text=countries,
        textposition="top center",
        hovertemplate='<b>%{text}</b><br>' +
                     'Date: %{x}<br>' +
                     'Impact: %{y:.1f}%<br>' +
                     '<extra></extra>',
        customdata=titles,
        name='Geopolitical Events'
    ))
    
    fig.update_layout(
        title="Geopolitical Events Timeline - Supply Chain Impact",
        xaxis_title="Date",
        yaxis_title="Supply Chain Impact (%)",
        height=400,
        showlegend=False
    )
    
    return fig

def render_geopolitical_impact_visualizer(context: Dict[str, Any], engine):
    """Render the interactive geopolitical impact visualizer"""
    st.subheader("🌍 Interactive Geopolitical Impact Visualizer")
    st.caption("Real-time analysis of geopolitical events affecting your supply chain")
    
    # Initialize geopolitical analyzer
    geo_analyzer = GeopoliticalImpactAnalyzer(engine, engine, engine)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌐 Analyze Global Events", help="Analyze current geopolitical events"):
            with st.spinner("Analyzing global geopolitical events..."):
                progress_placeholder = st.empty()
                
                def progress_callback(message):
                    progress_placeholder.info(message)
                
                events = geo_analyzer.analyze_geopolitical_events(context, progress_callback)
                progress_placeholder.empty()
                
                st.session_state.geo_events = events
                st.success(f"Analyzed {len(events)} geopolitical events")
    
    with col2:
        if st.button("📍 Assess Supplier Risks", help="Analyze supplier geopolitical risk"):
            with st.spinner("Assessing supplier geopolitical risks..."):
                progress_placeholder = st.empty()
                
                def progress_callback(message):
                    progress_placeholder.info(message)
                
                risk_profiles = geo_analyzer.analyze_supplier_geopolitical_risk(context, progress_callback)
                progress_placeholder.empty()
                
                st.session_state.supplier_risks = risk_profiles
                st.success(f"Assessed {len(risk_profiles)} supplier risk profiles")
    
    # Display visualizations if data exists
    if 'supplier_risks' in st.session_state:
        st.subheader("🗺️ Global Risk Map")
        risk_map = create_geopolitical_risk_map(st.session_state.supplier_risks)
        st.plotly_chart(risk_map, use_container_width=True)
        
        # Supplier risk details
        st.subheader("📊 Supplier Risk Profiles")
        for profile in st.session_state.supplier_risks:
            with st.expander(f"🏢 {profile.supplier_name} - Risk: {profile.current_risk_score}%"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Primary Country:** {profile.primary_country}")
                    if profile.secondary_countries:
                        st.write(f"**Secondary Countries:** {', '.join(profile.secondary_countries)}")
                    st.write(f"**Risk Score:** {profile.current_risk_score}%")
                
                with col2:
                    if profile.risk_factors:
                        st.write("**Risk Factors:**")
                        for factor in profile.risk_factors:
                            st.write(f"• {factor}")
                
                if profile.mitigation_recommendations:
                    st.write("**Recommendations:**")
                    for rec in profile.mitigation_recommendations:
                        st.write(f"• {rec}")
    
    if 'geo_events' in st.session_state:
        st.subheader("📅 Events Timeline")
        timeline = create_risk_timeline(st.session_state.geo_events)
        st.plotly_chart(timeline, use_container_width=True)
        
        # Event details
        st.subheader("🚨 Recent Geopolitical Events")
        for event in st.session_state.geo_events:
            severity_color = {
                'low': '🟢',
                'medium': '🟡', 
                'high': '🟠',
                'critical': '🔴'
            }.get(event.severity, '⚪')
            
            with st.expander(f"{severity_color} {event.title}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Country/Region:** {event.country} ({event.region})")
                    st.write(f"**Event Type:** {event.event_type.replace('_', ' ').title()}")
                    st.write(f"**Severity:** {event.severity.title()}")
                
                with col2:
                    st.write(f"**Supply Chain Impact:** {event.supply_chain_impact:.1f}%")
                    st.write(f"**Confidence Level:** {event.confidence_level:.1%}")
                    st.write(f"**Source:** {event.source}")
                
                if event.description:
                    st.write(f"**Description:** {event.description}")