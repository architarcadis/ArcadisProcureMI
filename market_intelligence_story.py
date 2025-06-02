"""
Story-Driven Market Intelligence
A simple, narrative approach to market intelligence that tells the story of your procurement landscape
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any

def render_market_intelligence_story():
    """Render the story-driven market intelligence experience"""
    st.header("📖 Your Market Intelligence Story")
    st.caption("Understanding your procurement landscape through real market data")
    
    # Check if data is available
    if 'uploaded_data' not in st.session_state or st.session_state.uploaded_data is None:
        st.info("📋 Upload your procurement data first to begin your market intelligence story")
        return
    
    df = st.session_state.uploaded_data
    
    # Extract context from data
    context = extract_story_context(df)
    
    if not context['suppliers'] and not context['categories']:
        st.warning("Could not identify suppliers or categories in your data. Please ensure your data contains supplier/vendor and category/type columns.")
        return
    
    # Story Navigation
    story_phase = st.radio(
        "Navigate Your Story:",
        ["📊 Chapter 1: Your Current Landscape", 
         "🌍 Chapter 2: What's Happening", 
         "🎯 Chapter 3: Your Action Plan"],
        horizontal=True
    )
    
    if story_phase == "📊 Chapter 1: Your Current Landscape":
        render_chapter_1_landscape(context, df)
    elif story_phase == "🌍 Chapter 2: What's Happening":
        render_chapter_2_happening(context)
    else:
        render_chapter_3_action_plan(context)

def extract_story_context(df: pd.DataFrame) -> Dict[str, Any]:
    """Extract key context from uploaded data for the story"""
    context = {
        'suppliers': [],
        'categories': [],
        'total_records': len(df),
        'key_metrics': {}
    }
    
    # Extract suppliers
    supplier_columns = ['supplier', 'vendor', 'supplier_name', 'vendor_name', 'company']
    for col in df.columns:
        if any(term in col.lower() for term in supplier_columns):
            unique_suppliers = df[col].dropna().astype(str).str.strip()
            unique_suppliers = unique_suppliers[unique_suppliers != ''].unique()
            context['suppliers'] = list(unique_suppliers)[:8]  # Top 8 suppliers
            break
    
    # Extract categories
    category_columns = ['category', 'product_category', 'service_category', 'type', 'classification']
    for col in df.columns:
        if any(term in col.lower() for term in category_columns):
            unique_categories = df[col].dropna().astype(str).str.strip()
            unique_categories = unique_categories[unique_categories != ''].unique()
            context['categories'] = list(unique_categories)[:6]  # Top 6 categories
            break
    
    # Extract key metrics
    value_columns = ['value', 'amount', 'cost', 'price', 'total']
    for col in df.columns:
        if any(term in col.lower() for term in value_columns):
            try:
                total_value = pd.to_numeric(df[col], errors='coerce').sum()
                context['key_metrics']['total_value'] = total_value
                break
            except:
                pass
    
    return context

def render_chapter_1_landscape(context: Dict[str, Any], df: pd.DataFrame):
    """Chapter 1: Understanding your current procurement landscape"""
    st.subheader("📊 Chapter 1: Your Current Procurement Landscape")
    st.write("Let's start by understanding what you're working with...")
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{context['total_records']:,}")
    with col2:
        st.metric("Active Suppliers", len(context['suppliers']))
    with col3:
        st.metric("Categories", len(context['categories']))
    
    # Your Suppliers Story
    if context['suppliers']:
        st.subheader("🏢 Your Key Suppliers")
        st.write("These are the suppliers we'll be monitoring for market intelligence:")
        
        # Display suppliers in a clean format
        supplier_cols = st.columns(min(3, len(context['suppliers'])))
        for i, supplier in enumerate(context['suppliers'][:6]):
            with supplier_cols[i % 3]:
                st.info(f"**{supplier}**")
    
    # Your Categories Story
    if context['categories']:
        st.subheader("📦 Your Procurement Categories")
        st.write("We'll track market trends for these categories:")
        
        # Display categories
        for i, category in enumerate(context['categories']):
            st.write(f"• {category}")
    
    # Total value if available
    if 'total_value' in context['key_metrics']:
        st.subheader("💰 Your Procurement Value")
        total_value = context['key_metrics']['total_value']
        if total_value > 0:
            st.metric("Total Procurement Value", f"${total_value:,.2f}")
    
    # Next steps
    st.info("👉 **Ready for Chapter 2?** We'll scan the market for news and trends affecting your specific suppliers and categories.")

def render_chapter_2_happening(context: Dict[str, Any]):
    """Chapter 2: What's happening in your market"""
    st.subheader("🌍 Chapter 2: What's Happening in Your World")
    st.write("Let's see what's happening in the market that could affect your suppliers and categories...")
    
    # Market Scanning Button
    if st.button("🔍 Scan Market for Your Suppliers & Categories", type="primary"):
        scan_market_for_story(context)
    
    # Display results if available
    if 'story_market_scan' in st.session_state:
        display_market_story_results(st.session_state.story_market_scan)
    else:
        st.info("Click the button above to scan the market for news and trends affecting your specific suppliers and categories.")

def scan_market_for_story(context: Dict[str, Any]):
    """Scan market for story-relevant information"""
    from enhanced_market_intelligence import EnhancedMarketIntelligence
    
    # Initialize engine
    if 'enhanced_intel_engine' not in st.session_state:
        st.session_state.enhanced_intel_engine = EnhancedMarketIntelligence()
    
    engine = st.session_state.enhanced_intel_engine
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    live_updates = st.empty()
    
    story_results = {
        'supplier_news': [],
        'category_trends': [],
        'risk_alerts': [],
        'opportunities': []
    }
    
    updates = []
    
    def update_progress(message):
        updates.append(f"• {message}")
        live_updates.text("\n".join(updates[-5:]))  # Show last 5 updates
    
    try:
        # Scan for supplier news
        status_text.info("Searching for news about your suppliers...")
        progress_bar.progress(25)
        
        for supplier in context['suppliers'][:3]:  # Focus on top 3
            update_progress(f"Searching news for {supplier}")
            
            query = f"{supplier} company news 2024"
            results = engine.search_market_data(query, 2)
            
            for result in results:
                content = engine.crawl_web_content(result['link'])
                if content:
                    analysis = engine.analyze_with_ai(content, {
                        'supplier_focus': supplier,
                        'analysis_type': 'supplier_news'
                    })
                    
                    story_results['supplier_news'].append({
                        'supplier': supplier,
                        'title': result['title'],
                        'summary': analysis.get('insights', 'Recent news about this supplier'),
                        'impact': analysis.get('impact', 'medium'),
                        'source': result['source']
                    })
                    
                    update_progress(f"Found news: {result['title'][:30]}...")
        
        # Scan for category trends
        status_text.info("Analyzing trends in your categories...")
        progress_bar.progress(50)
        
        for category in context['categories'][:2]:  # Focus on top 2
            update_progress(f"Analyzing trends for {category}")
            
            query = f"{category} market trends pricing 2024"
            results = engine.search_market_data(query, 2)
            
            for result in results:
                content = engine.crawl_web_content(result['link'])
                if content:
                    analysis = engine.analyze_with_ai(content, {
                        'category_focus': category,
                        'analysis_type': 'category_trends'
                    })
                    
                    story_results['category_trends'].append({
                        'category': category,
                        'trend': analysis.get('trend', 'stable'),
                        'summary': analysis.get('insights', 'Market trend analysis'),
                        'impact': analysis.get('impact', 'medium'),
                        'source': result['source']
                    })
                    
                    update_progress(f"Analyzed {category} trends")
        
        # Look for risks and opportunities
        status_text.info("Identifying risks and opportunities...")
        progress_bar.progress(75)
        
        risk_query = f"supply chain risks {' '.join(context['categories'][:2])}"
        update_progress(f"Searching for risks: {risk_query}")
        
        results = engine.search_market_data(risk_query, 2)
        for result in results:
            content = engine.crawl_web_content(result['link'])
            if content:
                analysis = engine.analyze_with_ai(content, {
                    'analysis_type': 'risk_opportunity'
                })
                
                if analysis.get('risk_level', 0) > 50:
                    story_results['risk_alerts'].append({
                        'title': result['title'],
                        'summary': analysis.get('insights', 'Potential risk identified'),
                        'severity': analysis.get('severity', 'medium'),
                        'source': result['source']
                    })
                else:
                    story_results['opportunities'].append({
                        'title': result['title'],
                        'summary': analysis.get('insights', 'Potential opportunity identified'),
                        'potential': analysis.get('opportunity_score', 50),
                        'source': result['source']
                    })
        
        # Complete
        progress_bar.progress(100)
        status_text.success("Market scan complete!")
        live_updates.empty()
        
        # Store results
        st.session_state.story_market_scan = story_results
        
    except Exception as e:
        st.error(f"Market scan encountered an issue: {str(e)}")
        st.info("This may be due to missing API keys. Please ensure you have provided the necessary API keys for market data access.")

def display_market_story_results(results: Dict[str, Any]):
    """Display market scan results in story format"""
    
    # Supplier News
    if results['supplier_news']:
        st.subheader("📰 News About Your Suppliers")
        for news in results['supplier_news']:
            with st.expander(f"📢 {news['supplier']}: {news['title'][:50]}..."):
                st.write(f"**Impact Level:** {news['impact'].title()}")
                st.write(f"**Summary:** {news['summary']}")
                st.write(f"**Source:** {news['source']}")
    
    # Category Trends
    if results['category_trends']:
        st.subheader("📈 Trends in Your Categories")
        for trend in results['category_trends']:
            trend_emoji = {"up": "📈", "down": "📉", "stable": "➡️"}.get(trend['trend'], "📊")
            with st.expander(f"{trend_emoji} {trend['category']} - {trend['trend'].title()} Trend"):
                st.write(f"**Trend Direction:** {trend['trend'].title()}")
                st.write(f"**Summary:** {trend['summary']}")
                st.write(f"**Source:** {trend['source']}")
    
    # Risk Alerts
    if results['risk_alerts']:
        st.subheader("⚠️ Risks to Watch")
        for risk in results['risk_alerts']:
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk['severity'], "⚪")
            with st.expander(f"{severity_emoji} {risk['title'][:50]}..."):
                st.write(f"**Severity:** {risk['severity'].title()}")
                st.write(f"**Summary:** {risk['summary']}")
                st.write(f"**Source:** {risk['source']}")
    
    # Opportunities
    if results['opportunities']:
        st.subheader("🌟 Opportunities to Consider")
        for opp in results['opportunities']:
            with st.expander(f"💡 {opp['title'][:50]}..."):
                st.write(f"**Potential Value:** {opp['potential']}%")
                st.write(f"**Summary:** {opp['summary']}")
                st.write(f"**Source:** {opp['source']}")
    
    st.info("👉 **Ready for Chapter 3?** We'll create your personalized action plan based on these findings.")

def render_chapter_3_action_plan(context: Dict[str, Any]):
    """Chapter 3: Your personalized action plan"""
    st.subheader("🎯 Chapter 3: Your Action Plan")
    st.write("Based on your data and market analysis, here's what you should focus on...")
    
    if 'story_market_scan' not in st.session_state:
        st.info("Complete Chapter 2 first to generate your personalized action plan.")
        return
    
    results = st.session_state.story_market_scan
    
    # Generate action plan
    action_plan = generate_action_plan(context, results)
    
    # Display action plan
    st.subheader("📋 Your Prioritized Actions")
    
    for i, action in enumerate(action_plan, 1):
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[action['priority']]
        
        with st.expander(f"{priority_emoji} Action {i}: {action['title']}"):
            st.write(f"**Priority:** {action['priority'].title()}")
            st.write(f"**Timeline:** {action['timeline']}")
            st.write(f"**Description:** {action['description']}")
            st.write(f"**Expected Impact:** {action['impact']}")
            
            if action['steps']:
                st.write("**Next Steps:**")
                for step in action['steps']:
                    st.write(f"• {step}")
    
    # Summary
    st.subheader("📊 Summary")
    high_priority = len([a for a in action_plan if a['priority'] == 'high'])
    st.write(f"You have **{high_priority} high-priority actions** and **{len(action_plan)} total recommendations** based on real market intelligence.")

def generate_action_plan(context: Dict[str, Any], results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate personalized action plan based on context and results"""
    actions = []
    
    # High-risk supplier actions
    for news in results.get('supplier_news', []):
        if news['impact'] == 'high':
            actions.append({
                'title': f"Review relationship with {news['supplier']}",
                'priority': 'high',
                'timeline': 'Next 30 days',
                'description': f"Recent news indicates potential impact to {news['supplier']}. Assess contract terms and backup options.",
                'impact': 'Mitigate supply chain risk',
                'steps': [
                    f"Contact {news['supplier']} for status update",
                    "Review contract terms and SLAs",
                    "Identify alternative suppliers if needed"
                ]
            })
    
    # Category trend actions
    for trend in results.get('category_trends', []):
        if trend['trend'] == 'up':
            actions.append({
                'title': f"Capitalize on positive trends in {trend['category']}",
                'priority': 'medium',
                'timeline': 'Next 60 days',
                'description': f"Market trends show improving conditions in {trend['category']}. Consider strategic expansions.",
                'impact': 'Cost optimization opportunity',
                'steps': [
                    f"Negotiate better terms for {trend['category']}",
                    "Consider volume increases",
                    "Explore long-term contracts"
                ]
            })
        elif trend['trend'] == 'down':
            actions.append({
                'title': f"Prepare for challenges in {trend['category']}",
                'priority': 'high',
                'timeline': 'Next 30 days',
                'description': f"Declining trends in {trend['category']} may affect costs and availability.",
                'impact': 'Risk mitigation',
                'steps': [
                    f"Review {trend['category']} supplier contracts",
                    "Consider forward buying if appropriate",
                    "Identify alternative categories or suppliers"
                ]
            })
    
    # Risk mitigation actions
    for risk in results.get('risk_alerts', []):
        if risk['severity'] in ['high', 'medium']:
            actions.append({
                'title': f"Address identified risk: {risk['title'][:30]}...",
                'priority': 'high' if risk['severity'] == 'high' else 'medium',
                'timeline': 'Next 45 days',
                'description': 'Market intelligence identified a potential risk that could affect your supply chain.',
                'impact': 'Prevent supply disruption',
                'steps': [
                    "Assess impact on current suppliers",
                    "Develop contingency plans",
                    "Consider risk mitigation strategies"
                ]
            })
    
    # Opportunity actions
    for opp in results.get('opportunities', []):
        if opp['potential'] > 60:
            actions.append({
                'title': f"Explore opportunity: {opp['title'][:30]}...",
                'priority': 'medium',
                'timeline': 'Next 90 days',
                'description': 'Market intelligence identified a potential opportunity for cost savings or process improvements.',
                'impact': 'Cost savings potential',
                'steps': [
                    "Research opportunity details",
                    "Assess feasibility for your organization",
                    "Develop implementation plan if viable"
                ]
            })
    
    # Default actions if no specific actions generated
    if not actions:
        actions.append({
            'title': 'Continue market monitoring',
            'priority': 'medium',
            'timeline': 'Ongoing',
            'description': 'Continue monitoring your suppliers and categories for market changes.',
            'impact': 'Stay informed of market developments',
            'steps': [
                'Set up regular market intelligence reviews',
                'Monitor key supplier news',
                'Track category pricing trends'
            ]
        })
    
    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    actions.sort(key=lambda x: priority_order[x['priority']])
    
    return actions[:5]  # Return top 5 actions