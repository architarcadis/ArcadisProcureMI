"""
Macro Intelligence Service
Enhanced granular intelligence gathering for comprehensive market analysis
"""
import os
import json
import requests
import streamlit as st
from typing import Dict, List, Any, Optional
from openai import OpenAI
import pandas as pd

class MacroIntelligenceEngine:
    """Advanced intelligence engine for macroeconomic and government intelligence"""
    
    def __init__(self):
        self.google_api_key = os.environ.get('GOOGLE_API_KEY')
        self.google_cse_id = os.environ.get('GOOGLE_CSE_ID')
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def gather_comprehensive_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather comprehensive intelligence across multiple dimensions"""
        
        intelligence_data = {
            'macroeconomic_factors': self._gather_macro_intelligence(company_name, sector),
            'government_policy': self._gather_government_intelligence(company_name, sector),
            'regulatory_landscape': self._gather_regulatory_intelligence(company_name, sector),
            'market_dynamics': self._gather_market_dynamics(company_name, sector),
            'supply_chain_intelligence': self._gather_supply_chain_intel(company_name, sector),
            'financial_intelligence': self._gather_financial_intelligence(company_name, sector),
            'competitive_landscape': self._gather_competitive_intelligence(company_name, sector),
            'risk_assessment': self._gather_risk_intelligence(company_name, sector)
        }
        
        return intelligence_data
    
    def _gather_macro_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather macroeconomic intelligence"""
        macro_queries = [
            f"{sector} UK GDP impact inflation economic outlook 2024 2025",
            f"{sector} Bank of England interest rates monetary policy",
            f"{sector} UK government spending budget allocation infrastructure",
            f"{company_name} economic indicators market conditions",
            f"{sector} inflation supply chain costs commodity prices"
        ]
        
        macro_data = []
        for query in macro_queries:
            results = self._enhanced_search(query, ["site:gov.uk", "site:bankofengland.co.uk", "site:ons.gov.uk"])
            macro_data.extend(results)
        
        return {
            'data_points': len(macro_data),
            'sources': macro_data[:10],
            'analysis': self._analyze_macro_trends(macro_data, company_name, sector) if macro_data else {}
        }
    
    def _gather_government_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather government policy and planning intelligence"""
        gov_queries = [
            f"{sector} UK government policy strategy white paper",
            f"{company_name} government contracts tender opportunities",
            f"{sector} Net Zero carbon reduction government plans",
            f"{sector} infrastructure spending government investment",
            f"{sector} regulatory changes legislation upcoming"
        ]
        
        gov_data = []
        for query in gov_queries:
            results = self._enhanced_search(query, [
                "site:gov.uk", 
                "site:parliament.uk", 
                "filetype:pdf government",
                "site:hm-treasury.gov.uk"
            ])
            gov_data.extend(results)
        
        return {
            'policy_documents': len(gov_data),
            'sources': gov_data[:10],
            'policy_analysis': self._analyze_government_policy(gov_data, company_name, sector) if gov_data else {}
        }
    
    def _gather_regulatory_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather regulatory landscape intelligence"""
        reg_queries = [
            f"{sector} regulatory framework compliance requirements UK",
            f"{company_name} regulatory approvals licenses permits",
            f"{sector} health safety environmental regulations",
            f"{sector} competition authority investigations",
            f"{sector} data protection GDPR compliance requirements"
        ]
        
        reg_data = []
        for query in reg_queries:
            results = self._enhanced_search(query, [
                "site:gov.uk regulatory",
                "site:hse.gov.uk",
                "site:cma.gov.uk",
                "site:ico.org.uk"
            ])
            reg_data.extend(results)
        
        return {
            'regulatory_sources': len(reg_data),
            'sources': reg_data[:10],
            'compliance_analysis': self._analyze_regulatory_landscape(reg_data, company_name, sector) if reg_data else {}
        }
    
    def _gather_market_dynamics(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather market dynamics and trends"""
        market_queries = [
            f"{sector} market size growth rate UK trends analysis",
            f"{company_name} market share competitive position",
            f"{sector} customer demand patterns consumer behaviour",
            f"{sector} technology disruption innovation trends",
            f"{sector} merger acquisition consolidation activity"
        ]
        
        market_data = []
        for query in market_queries:
            results = self._enhanced_search(query, [
                "market research",
                "industry analysis",
                "site:ft.com",
                "site:reuters.com"
            ])
            market_data.extend(results)
        
        return {
            'market_indicators': len(market_data),
            'sources': market_data[:10],
            'market_analysis': self._analyze_market_dynamics(market_data, company_name, sector) if market_data else {}
        }
    
    def _gather_supply_chain_intel(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather supply chain intelligence"""
        supply_queries = [
            f"{company_name} suppliers vendor list procurement partners",
            f"{sector} supply chain disruption risk resilience",
            f"{sector} critical materials dependencies import export",
            f"{sector} logistics distribution network UK",
            f"{company_name} contract awards supplier announcements"
        ]
        
        supply_data = []
        for query in supply_queries:
            results = self._enhanced_search(query, [
                "supplier directory",
                "procurement tender",
                "supply chain",
                "site:linkedin.com"
            ])
            supply_data.extend(results)
        
        return {
            'supplier_intelligence': len(supply_data),
            'sources': supply_data[:10],
            'supply_analysis': self._analyze_supply_chain(supply_data, company_name, sector) if supply_data else {}
        }
    
    def _gather_financial_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather financial and investment intelligence"""
        financial_queries = [
            f"{company_name} financial results revenue profit margins",
            f"{sector} investment funding venture capital private equity",
            f"{company_name} bond ratings credit analysis debt financing",
            f"{sector} capital expenditure investment plans",
            f"{company_name} dividend payments shareholder returns"
        ]
        
        financial_data = []
        for query in financial_queries:
            results = self._enhanced_search(query, [
                "financial statements",
                "investor relations",
                "annual report",
                "site:companieshouse.gov.uk"
            ])
            financial_data.extend(results)
        
        return {
            'financial_indicators': len(financial_data),
            'sources': financial_data[:10],
            'financial_analysis': self._analyze_financial_position(financial_data, company_name, sector) if financial_data else {}
        }
    
    def _gather_competitive_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather competitive landscape intelligence"""
        competitive_queries = [
            f"{sector} competitors market leaders UK ranking",
            f"{company_name} vs competitors comparison analysis",
            f"{sector} new entrants startup companies emerging players",
            f"{sector} pricing strategy competitive positioning",
            f"{sector} innovation patent filings R&D investment"
        ]
        
        competitive_data = []
        for query in competitive_queries:
            results = self._enhanced_search(query, [
                "competitive analysis",
                "market share",
                "industry report",
                "benchmarking"
            ])
            competitive_data.extend(results)
        
        return {
            'competitive_intelligence': len(competitive_data),
            'sources': competitive_data[:10],
            'competitive_analysis': self._analyze_competitive_landscape(competitive_data, company_name, sector) if competitive_data else {}
        }
    
    def _gather_risk_intelligence(self, company_name: str, sector: str) -> Dict[str, Any]:
        """Gather comprehensive risk intelligence"""
        risk_queries = [
            f"{company_name} risk factors operational financial regulatory",
            f"{sector} cyber security data breach incidents",
            f"{sector} climate change environmental risks ESG",
            f"{company_name} legal disputes litigation regulatory issues",
            f"{sector} geopolitical risks international trade"
        ]
        
        risk_data = []
        for query in risk_queries:
            results = self._enhanced_search(query, [
                "risk assessment",
                "due diligence",
                "compliance issues",
                "incidents"
            ])
            risk_data.extend(results)
        
        return {
            'risk_indicators': len(risk_data),
            'sources': risk_data[:10],
            'risk_analysis': self._analyze_risk_profile(risk_data, company_name, sector) if risk_data else {}
        }
    
    def _enhanced_search(self, query: str, site_modifiers: List[str]) -> List[Dict[str, Any]]:
        """Enhanced search with site-specific modifiers"""
        
        if not self.google_api_key or not self.google_cse_id:
            return []
        
        all_results = []
        
        # Search with each site modifier
        for modifier in site_modifiers[:2]:  # Limit to prevent API overuse
            search_query = f"{query} {modifier}"
            
            try:
                url = 'https://www.googleapis.com/customsearch/v1'
                params = {
                    'key': self.google_api_key,
                    'cx': self.google_cse_id,
                    'q': search_query,
                    'num': 5
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get('items', []):
                        result_data = {
                            'title': item.get('title', ''),
                            'url': item.get('link', ''),
                            'snippet': item.get('snippet', ''),
                            'source': item.get('displayLink', ''),
                            'search_modifier': modifier,
                            'relevance_score': len(item.get('snippet', '')) / 200
                        }
                        
                        # Enhanced analysis with LLM
                        if self.openai_api_key:
                            result_data.update(self._deep_intelligence_analysis(result_data, query))
                        
                        all_results.append(result_data)
                        
            except Exception as e:
                st.warning(f"Search error for {modifier}: {e}")
                continue
        
        return all_results[:10]  # Return top 10 results
    
    def _deep_intelligence_analysis(self, result: Dict[str, Any], context: str) -> Dict[str, Any]:
        """Deep LLM analysis for intelligence extraction"""
        
        try:
            content = f"Context: {context}\nTitle: {result['title']}\nContent: {result['snippet']}\nSource: {result['source']}"
            
            prompt = f"""
            Analyze this search result for comprehensive business intelligence:
            {content}
            
            Extract and return JSON with:
            1. intelligence_value: 0-1 (how valuable for strategic decision making)
            2. data_type: "macroeconomic", "policy", "regulatory", "competitive", "financial", "operational", "risk"
            3. key_metrics: [list of specific numbers, percentages, dates mentioned]
            4. strategic_insights: [2-3 actionable strategic insights]
            5. credibility_score: 0-1 (source credibility and data reliability)
            6. time_relevance: "current", "recent", "historical" (data recency)
            7. decision_impact: "high", "medium", "low" (potential impact on business decisions)
            8. extracted_entities: [specific company names, government bodies, technologies, locations]
            
            Focus on extracting concrete, actionable intelligence for procurement and business strategy.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=500
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            return {
                'intelligence_value': 0.5,
                'data_type': 'general',
                'credibility_score': 0.5,
                'decision_impact': 'medium'
            }
    
    def _analyze_macro_trends(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze macroeconomic trends using LLM"""
        if not self.openai_api_key or not data:
            return {}
        
        try:
            data_summary = "\n".join([f"- {item['title']}: {item['snippet'][:100]}" for item in data[:5]])
            
            prompt = f"""
            Analyze macroeconomic intelligence for {company_name} in {sector} sector:
            {data_summary}
            
            Provide JSON analysis with:
            1. economic_outlook: summary of economic conditions affecting this sector
            2. inflation_impact: how inflation affects costs and pricing
            3. interest_rate_impact: effect of monetary policy
            4. government_spending: relevant public sector investment
            5. key_risks: top 3 macroeconomic risks
            6. opportunities: economic opportunities to leverage
            7. recommendations: 3 strategic recommendations
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=600
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {'error': f'Analysis failed: {e}'}
    
    def _analyze_government_policy(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze government policy implications"""
        if not self.openai_api_key or not data:
            return {}
        
        try:
            policy_summary = "\n".join([f"- {item['title']}: {item['snippet'][:100]}" for item in data[:5]])
            
            prompt = f"""
            Analyze government policy intelligence for {company_name} in {sector}:
            {policy_summary}
            
            Provide JSON with:
            1. policy_direction: government strategy and priorities
            2. funding_opportunities: available grants, contracts, investments
            3. regulatory_changes: upcoming policy changes
            4. compliance_requirements: new obligations or standards
            5. strategic_alignment: how company can align with government priorities
            6. policy_risks: potential negative policy impacts
            7. action_items: specific steps to take advantage of policies
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=600
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {'error': f'Policy analysis failed: {e}'}
    
    def _analyze_regulatory_landscape(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze regulatory landscape"""
        if not self.openai_api_key or not data:
            return {}
        
        # Similar pattern for other analysis methods...
        return {'regulatory_summary': 'Analysis pending implementation'}
    
    def _analyze_market_dynamics(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze market dynamics"""
        return {'market_summary': 'Analysis pending implementation'}
    
    def _analyze_supply_chain(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze supply chain intelligence"""
        return {'supply_chain_summary': 'Analysis pending implementation'}
    
    def _analyze_financial_position(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze financial intelligence"""
        return {'financial_summary': 'Analysis pending implementation'}
    
    def _analyze_competitive_landscape(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze competitive intelligence"""
        return {'competitive_summary': 'Analysis pending implementation'}
    
    def _analyze_risk_profile(self, data: List[Dict], company_name: str, sector: str) -> Dict[str, Any]:
        """Analyze risk profile"""
        return {'risk_summary': 'Analysis pending implementation'}