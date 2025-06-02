"""
Comprehensive Source Discovery Engine
Identifies all possible intelligence sources and implements granular crawling
"""
import os
import json
import requests
import streamlit as st
from typing import Dict, List, Any, Optional
from openai import OpenAI
import pandas as pd
from urllib.parse import urlparse
import time

class ComprehensiveSourceDiscovery:
    """Advanced source discovery and granular crawling engine"""
    
    def __init__(self):
        self.google_api_key = os.environ.get('GOOGLE_API_KEY')
        self.google_cse_id = os.environ.get('GOOGLE_CSE_ID')
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Comprehensive source categories
        self.source_categories = {
            'government_uk': {
                'domains': ['gov.uk', 'parliament.uk', 'hm-treasury.gov.uk', 'bankofengland.co.uk', 'ons.gov.uk'],
                'types': ['policy', 'legislation', 'statistics', 'reports', 'consultations']
            },
            'regulatory_bodies': {
                'domains': ['hse.gov.uk', 'cma.gov.uk', 'ico.org.uk', 'fca.org.uk', 'ofwat.gov.uk'],
                'types': ['compliance', 'investigations', 'guidance', 'enforcement']
            },
            'industry_authorities': {
                'domains': ['water.org.uk', 'ukwir.org', 'ciwem.org'],
                'types': ['standards', 'best_practice', 'research', 'industry_data']
            },
            'financial_data': {
                'domains': ['companieshouse.gov.uk', 'londonstockexchange.com'],
                'types': ['financial_statements', 'annual_reports', 'investor_relations']
            },
            'news_intelligence': {
                'domains': ['ft.com', 'reuters.com', 'bbc.co.uk', 'theguardian.com'],
                'types': ['market_news', 'analysis', 'sector_updates', 'company_announcements']
            },
            'professional_networks': {
                'domains': ['linkedin.com'],
                'types': ['company_profiles', 'executive_profiles', 'network_analysis']
            },
            'academic_research': {
                'domains': ['ac.uk', 'researchgate.net'],
                'types': ['research_papers', 'case_studies', 'technical_analysis']
            },
            'procurement_sources': {
                'domains': ['ted.europa.eu', 'contracts.gov.uk', 'sell2wales.gov.wales'],
                'types': ['tender_opportunities', 'contract_awards', 'supplier_registers']
            }
        }
    
    def discover_comprehensive_sources(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Discover all possible intelligence sources for a company/sector"""
        
        st.markdown("## 🔍 Comprehensive Source Discovery")
        st.markdown("*Mapping all possible intelligence sources across multiple dimensions*")
        
        source_map = {}
        total_sources_found = 0
        
        # Progress tracking
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            categories = list(self.source_categories.keys())
            
            for i, category in enumerate(categories):
                status_text.text(f"Discovering {category.replace('_', ' ').title()} sources...")
                
                category_sources = self._discover_category_sources(
                    company_name, sector, category, self.source_categories[category]
                )
                
                source_map[category] = category_sources
                total_sources_found += len(category_sources.get('discovered_sources', []))
                
                progress_bar.progress((i + 1) / len(categories))
                time.sleep(0.5)  # Brief pause for visual feedback
        
        # Display source discovery results
        self._display_source_map(source_map, total_sources_found)
        
        return source_map
    
    def _discover_category_sources(self, company_name: str, sector: str, category: str, category_config: Dict) -> Dict[str, Any]:
        """Discover sources within a specific category"""
        
        discovered_sources = []
        
        # Generate category-specific search queries
        search_queries = self._generate_category_queries(company_name, sector, category, category_config)
        
        for query in search_queries[:3]:  # Limit queries per category
            # Search with domain restrictions
            for domain in category_config['domains'][:2]:  # Limit domains per category
                enhanced_query = f"{query} site:{domain}"
                
                try:
                    results = self._search_with_pagination(enhanced_query, max_results=10)
                    
                    for result in results:
                        source_info = {
                            'url': result.get('link', ''),
                            'title': result.get('title', ''),
                            'snippet': result.get('snippet', ''),
                            'domain': result.get('displayLink', ''),
                            'category': category,
                            'source_type': self._classify_source_type(result, category_config['types']),
                            'discovery_query': query,
                            'authority_indicators': self._analyze_authority_indicators(result),
                            'content_depth_estimate': len(result.get('snippet', '')) / 20,
                            'last_discovered': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # Enhanced source analysis with LLM
                        if self.openai_api_key:
                            source_info.update(self._analyze_source_potential(source_info, company_name, sector))
                        
                        discovered_sources.append(source_info)
                        
                except Exception as e:
                    st.warning(f"Discovery error for {domain}: {e}")
                    continue
        
        return {
            'category': category,
            'total_sources': len(discovered_sources),
            'discovered_sources': discovered_sources,
            'coverage_assessment': self._assess_category_coverage(discovered_sources, category_config)
        }
    
    def _generate_category_queries(self, company_name: str, sector: str, category: str, config: Dict) -> List[str]:
        """Generate intelligent search queries for each category"""
        
        base_queries = {
            'government_uk': [
                f"{company_name} government policy strategy consultation",
                f"{sector} UK policy framework legislation regulation",
                f"{company_name} public sector contracts government tender"
            ],
            'regulatory_bodies': [
                f"{company_name} regulatory compliance requirements",
                f"{sector} regulatory framework standards guidance",
                f"{company_name} regulatory approval license investigation"
            ],
            'industry_authorities': [
                f"{company_name} industry standards best practice",
                f"{sector} industry association research reports",
                f"{company_name} sector authority guidance"
            ],
            'financial_data': [
                f"{company_name} financial statements annual report",
                f"{company_name} investor relations financial performance",
                f"{company_name} company information director details"
            ],
            'news_intelligence': [
                f"{company_name} news analysis market commentary",
                f"{sector} market news industry developments",
                f"{company_name} business news financial updates"
            ],
            'professional_networks': [
                f"{company_name} company profile executive team",
                f"{company_name} leadership team professional network",
                f"{sector} industry professionals {company_name}"
            ],
            'academic_research': [
                f"{company_name} research case study academic",
                f"{sector} research papers technical analysis",
                f"{company_name} university research collaboration"
            ],
            'procurement_sources': [
                f"{company_name} tender opportunities contract awards",
                f"{sector} procurement contracts supplier opportunities",
                f"{company_name} public procurement contract notices"
            ]
        }
        
        return base_queries.get(category, [f"{company_name} {category}"])
    
    def _search_with_pagination(self, query: str, max_results: int = 10) -> List[Dict]:
        """Enhanced search with pagination support"""
        
        if not self.google_api_key or not self.google_cse_id:
            return []
        
        all_results = []
        
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': query,
                'num': min(max_results, 10)
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                all_results.extend(data.get('items', []))
            
        except Exception as e:
            st.warning(f"Search error: {e}")
        
        return all_results
    
    def _classify_source_type(self, result: Dict, possible_types: List[str]) -> str:
        """Classify the type of source based on content analysis"""
        
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        url = result.get('link', '').lower()
        
        content = f"{title} {snippet} {url}"
        
        # Simple keyword-based classification
        type_keywords = {
            'policy': ['policy', 'strategy', 'framework', 'white paper'],
            'legislation': ['act', 'law', 'regulation', 'statute'],
            'statistics': ['data', 'statistics', 'figures', 'numbers'],
            'reports': ['report', 'analysis', 'study', 'research'],
            'compliance': ['compliance', 'requirements', 'standards'],
            'guidance': ['guidance', 'best practice', 'guidelines'],
            'financial_statements': ['financial', 'accounts', 'balance sheet'],
            'news': ['news', 'article', 'update', 'announcement']
        }
        
        for source_type, keywords in type_keywords.items():
            if source_type in possible_types and any(keyword in content for keyword in keywords):
                return source_type
        
        return 'general'
    
    def _analyze_authority_indicators(self, result: Dict) -> Dict[str, Any]:
        """Analyze authority indicators for a source"""
        
        url = result.get('link', '').lower()
        title = result.get('title', '').lower()
        domain = result.get('displayLink', '').lower()
        
        authority_score = 0.5  # Base score
        indicators = []
        
        # Government authority
        if any(gov_domain in domain for gov_domain in ['.gov.uk', '.gov.com', 'parliament']):
            authority_score += 0.3
            indicators.append('Government Source')
        
        # Academic authority
        if '.ac.uk' in domain or '.edu' in domain:
            authority_score += 0.2
            indicators.append('Academic Institution')
        
        # Official organization
        if any(word in title for word in ['official', 'authority', 'commission', 'office']):
            authority_score += 0.15
            indicators.append('Official Organization')
        
        # Professional network
        if 'linkedin.com' in domain:
            authority_score += 0.1
            indicators.append('Professional Network')
        
        # News authority
        if any(news in domain for news in ['bbc.', 'ft.com', 'reuters', 'guardian']):
            authority_score += 0.15
            indicators.append('Established Media')
        
        return {
            'authority_score': min(authority_score, 1.0),
            'authority_indicators': indicators,
            'domain_type': self._classify_domain_type(domain)
        }
    
    def _classify_domain_type(self, domain: str) -> str:
        """Classify the type of domain"""
        
        if '.gov.' in domain:
            return 'Government'
        elif '.ac.uk' in domain or '.edu' in domain:
            return 'Academic'
        elif '.org' in domain:
            return 'Organization'
        elif '.com' in domain:
            return 'Commercial'
        else:
            return 'Other'
    
    def _analyze_source_potential(self, source_info: Dict, company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze source potential using LLM"""
        
        try:
            content = f"Title: {source_info['title']}\nSnippet: {source_info['snippet']}\nDomain: {source_info['domain']}"
            
            prompt = f"""
            Analyze this source for intelligence potential regarding {company_name} in {sector} sector:
            {content}
            
            Return JSON with:
            {{
                "intelligence_potential": 0-1 (how valuable for strategic intelligence),
                "data_richness": 0-1 (estimated amount of useful data),
                "strategic_relevance": 0-1 (relevance to business strategy),
                "information_type": "quantitative", "qualitative", "mixed",
                "expected_insights": ["insight1", "insight2", "insight3"],
                "crawling_priority": "high", "medium", "low",
                "content_indicators": ["indicator1", "indicator2"],
                "potential_connections": ["connection1", "connection2"]
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=400
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                'intelligence_potential': 0.5,
                'data_richness': 0.5,
                'strategic_relevance': 0.5,
                'crawling_priority': 'medium'
            }
    
    def _assess_category_coverage(self, sources: List[Dict], config: Dict) -> Dict[str, Any]:
        """Assess how well we've covered a category"""
        
        total_sources = len(sources)
        domains_covered = len(set(source['domain'] for source in sources))
        types_covered = len(set(source['source_type'] for source in sources))
        
        high_potential_sources = len([s for s in sources if s.get('intelligence_potential', 0.5) > 0.7])
        
        coverage_score = min(1.0, (domains_covered / len(config['domains']) + 
                                 types_covered / len(config['types']) + 
                                 total_sources / 20) / 3)
        
        return {
            'coverage_score': coverage_score,
            'total_sources': total_sources,
            'domains_covered': domains_covered,
            'types_covered': types_covered,
            'high_potential_sources': high_potential_sources,
            'coverage_gaps': self._identify_coverage_gaps(sources, config)
        }
    
    def _identify_coverage_gaps(self, sources: List[Dict], config: Dict) -> List[str]:
        """Identify gaps in source coverage"""
        
        covered_domains = set(source['domain'] for source in sources)
        covered_types = set(source['source_type'] for source in sources)
        
        domain_gaps = set(config['domains']) - covered_domains
        type_gaps = set(config['types']) - covered_types
        
        gaps = []
        if domain_gaps:
            gaps.extend([f"Missing domain: {domain}" for domain in domain_gaps])
        if type_gaps:
            gaps.extend([f"Missing type: {source_type}" for source_type in type_gaps])
        
        return gaps
    
    def _display_source_map(self, source_map: Dict, total_sources: int):
        """Display comprehensive source discovery results"""
        
        st.markdown(f"## 📊 Source Discovery Results")
        st.success(f"🎉 Discovered {total_sources} potential intelligence sources across {len(source_map)} categories")
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sources", total_sources)
        
        with col2:
            high_potential = sum(len([s for s in cat['discovered_sources'] 
                                    if s.get('intelligence_potential', 0.5) > 0.7])
                               for cat in source_map.values())
            st.metric("High Potential", high_potential)
        
        with col3:
            unique_domains = len(set(source['domain'] 
                                   for cat in source_map.values() 
                                   for source in cat['discovered_sources']))
            st.metric("Unique Domains", unique_domains)
        
        with col4:
            avg_coverage = sum(cat['coverage_assessment']['coverage_score'] 
                             for cat in source_map.values()) / len(source_map)
            st.metric("Avg Coverage", f"{avg_coverage:.1%}")
        
        # Detailed category breakdown
        st.markdown("### 📋 Category-by-Category Analysis")
        
        for category, data in source_map.items():
            with st.expander(f"🔍 {category.replace('_', ' ').title()} ({data['total_sources']} sources)"):
                
                coverage = data['coverage_assessment']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Coverage Metrics:**")
                    st.write(f"• Coverage Score: {coverage['coverage_score']:.1%}")
                    st.write(f"• Domains Covered: {coverage['domains_covered']}")
                    st.write(f"• Types Covered: {coverage['types_covered']}")
                    st.write(f"• High Potential: {coverage['high_potential_sources']}")
                
                with col2:
                    st.markdown("**Coverage Gaps:**")
                    for gap in coverage['coverage_gaps'][:3]:
                        st.write(f"• {gap}")
                
                # Top sources in category
                if data['discovered_sources']:
                    st.markdown("**Top Sources Found:**")
                    top_sources = sorted(data['discovered_sources'], 
                                       key=lambda x: x.get('intelligence_potential', 0.5), 
                                       reverse=True)[:5]
                    
                    for source in top_sources:
                        authority_score = source['authority_indicators']['authority_score']
                        intel_potential = source.get('intelligence_potential', 0.5)
                        
                        st.write(f"🔗 **{source['title'][:60]}**")
                        st.write(f"   Authority: {authority_score:.1%} | Intelligence: {intel_potential:.1%} | Domain: {source['domain']}")
    
    def initiate_granular_crawling(self, source_map: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """Initiate systematic granular crawling of discovered sources"""
        
        st.markdown("## 🚀 Granular Intelligence Crawling")
        st.markdown("*Systematic deep crawling of high-priority sources*")
        
        # Prioritize sources for crawling
        prioritized_sources = self._prioritize_sources_for_crawling(source_map)
        
        # Display crawling plan
        st.markdown("### 📋 Crawling Execution Plan")
        
        total_high_priority = len([s for s in prioritized_sources if s['crawling_priority'] == 'high'])
        total_medium_priority = len([s for s in prioritized_sources if s['crawling_priority'] == 'medium'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("High Priority", total_high_priority)
        with col2:
            st.metric("Medium Priority", total_medium_priority)
        with col3:
            st.metric("Total Planned", len(prioritized_sources))
        
        # Execute crawling for high-priority sources
        if st.button("🎯 Execute High-Priority Crawling", key="execute_crawling"):
            crawling_results = self._execute_priority_crawling(prioritized_sources, company_name)
            self._display_crawling_results(crawling_results)
            return crawling_results
        
        return {}
    
    def _prioritize_sources_for_crawling(self, source_map: Dict[str, Any]) -> List[Dict]:
        """Prioritize sources for systematic crawling"""
        
        all_sources = []
        for category_data in source_map.values():
            all_sources.extend(category_data['discovered_sources'])
        
        # Calculate priority score
        for source in all_sources:
            intelligence_potential = source.get('intelligence_potential', 0.5)
            authority_score = source['authority_indicators']['authority_score']
            content_depth = source['content_depth_estimate']
            
            priority_score = (intelligence_potential * 0.4 + 
                            authority_score * 0.4 + 
                            min(content_depth, 1.0) * 0.2)
            
            source['priority_score'] = priority_score
            
            if priority_score > 0.75:
                source['crawling_priority'] = 'high'
            elif priority_score > 0.5:
                source['crawling_priority'] = 'medium'
            else:
                source['crawling_priority'] = 'low'
        
        # Sort by priority score
        return sorted(all_sources, key=lambda x: x['priority_score'], reverse=True)
    
    def _execute_priority_crawling(self, prioritized_sources: List[Dict], company_name: str) -> Dict[str, Any]:
        """Execute systematic crawling of priority sources"""
        
        high_priority_sources = [s for s in prioritized_sources if s['crawling_priority'] == 'high'][:10]
        
        crawling_results = {
            'sources_crawled': 0,
            'intelligence_extracted': [],
            'crawling_summary': {},
            'failed_crawls': []
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, source in enumerate(high_priority_sources):
            status_text.text(f"Crawling: {source['title'][:50]}...")
            
            try:
                # Simulate granular crawling (in real implementation, would use web scraping)
                crawl_result = self._simulate_granular_crawl(source, company_name)
                crawling_results['intelligence_extracted'].append(crawl_result)
                crawling_results['sources_crawled'] += 1
                
            except Exception as e:
                crawling_results['failed_crawls'].append({
                    'source': source['title'],
                    'error': str(e)
                })
            
            progress_bar.progress((i + 1) / len(high_priority_sources))
            time.sleep(0.3)  # Brief pause for visual feedback
        
        return crawling_results
    
    def _simulate_granular_crawl(self, source: Dict, company_name: str) -> Dict[str, Any]:
        """Simulate granular crawling of a source (placeholder for actual implementation)"""
        
        # In a real implementation, this would:
        # 1. Fetch the full webpage content
        # 2. Extract structured data using parsing libraries
        # 3. Apply NLP to extract entities, metrics, relationships
        # 4. Store structured intelligence data
        
        return {
            'source_url': source['url'],
            'source_title': source['title'],
            'category': source['category'],
            'crawl_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'extracted_data': {
                'key_metrics': ['Metric 1', 'Metric 2', 'Metric 3'],
                'entities_found': [company_name, 'Entity 1', 'Entity 2'],
                'relationships': ['Relationship 1', 'Relationship 2'],
                'structured_data': {
                    'financial_figures': [],
                    'dates': [],
                    'locations': [],
                    'contacts': []
                }
            },
            'intelligence_quality': source.get('intelligence_potential', 0.5),
            'data_richness': len(source['snippet']) / 100
        }
    
    def _display_crawling_results(self, results: Dict[str, Any]):
        """Display results of granular crawling"""
        
        st.markdown("### ✅ Crawling Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sources Crawled", results['sources_crawled'])
        with col2:
            st.metric("Intelligence Items", len(results['intelligence_extracted']))
        with col3:
            st.metric("Failed Crawls", len(results['failed_crawls']))
        
        # Display extracted intelligence
        if results['intelligence_extracted']:
            st.markdown("**🧠 Extracted Intelligence:**")
            
            for item in results['intelligence_extracted'][:5]:
                with st.expander(f"📄 {item['source_title'][:60]}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Category:** {item['category']}")
                        st.write(f"**Quality:** {item['intelligence_quality']:.1%}")
                        st.write(f"**Data Richness:** {item['data_richness']:.1f}")
                    
                    with col2:
                        st.write("**Entities Found:**")
                        for entity in item['extracted_data']['entities_found'][:3]:
                            st.write(f"• {entity}")
                        
                        st.write("**Key Metrics:**")
                        for metric in item['extracted_data']['key_metrics'][:3]:
                            st.write(f"• {metric}")