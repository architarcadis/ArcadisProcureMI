import os
import logging
from outscraper import ApiClient
from typing import List, Dict, Any, Optional
import time

logger = logging.getLogger(__name__)

class OutscraperService:
    """Service for Outscraper Google search and data extraction"""
    
    def __init__(self):
        self.api_key = os.getenv("OUTSCRAPER_API_KEY", "")
        if not self.api_key:
            logger.error("Outscraper API key not found in environment variables")
            raise ValueError("Outscraper API key is required")
        
        self.client = ApiClient(api_key=self.api_key)
        self.results_per_query = 20  # Number of results to fetch per search
    
    def search_market_intelligence(self, keywords: List[str], num_results: int = None) -> List[Dict[str, Any]]:
        """
        Search for market intelligence using Outscraper Google Search
        Returns aggregated search results from all keywords
        """
        if num_results is None:
            num_results = self.results_per_query
            
        all_results = []
        
        for keyword in keywords:
            try:
                logger.info(f"Searching for keyword with Outscraper: {keyword}")
                results = self._perform_search(keyword, num_results)
                
                # Add keyword context to results
                for result in results:
                    result['search_keyword'] = keyword
                
                all_results.extend(results)
                
                # Rate limiting - small delay between requests
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            url = result.get('link', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        logger.info(f"Total unique search results collected with Outscraper: {len(unique_results)}")
        return unique_results
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies using the query"""
        try:
            results = self.client.google_search(
                query=f"{query} company",
                pages_per_query=1,
                language='en',
                region='US'
            )
            
            companies = []
            if results and len(results) > 0:
                search_results = results[0].get('results_organic', [])
                
                for result in search_results:
                    company = {
                        'name': result.get('title', ''),
                        'domain': result.get('link', ''),
                        'description': result.get('snippet', ''),
                        'source_url': result.get('link', ''),
                        'search_query': query
                    }
                    companies.append(company)
            
            return companies
            
        except Exception as e:
            logger.error(f"Error searching companies: {e}")
            return []
    
    def search_market_insights(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for market insights and analysis"""
        try:
            insights_query = f"{query} market analysis report insights"
            results = self.client.google_search(
                query=insights_query,
                pages_per_query=1,
                language='en',
                region='US'
            )
            
            insights = []
            if results and len(results) > 0:
                search_results = results[0].get('results_organic', [])
                
                for result in search_results:
                    insight = {
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'summary': result.get('snippet', ''),
                        'type': 'market_insight',
                        'search_query': query
                    }
                    insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error searching market insights: {e}")
            return []
    
    def _perform_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Perform individual search query via Outscraper
        """
        try:
            # Use Outscraper's Google Search API with correct parameters
            results = self.client.google_search(
                query=query,
                pages_per_query=1,
                language='en',
                region='US'
            )
            
            # Process results from Outscraper format
            processed_results = []
            
            if results and len(results) > 0:
                search_results = results[0].get('results_organic', [])
                
                for i, result in enumerate(search_results):
                    processed_result = self._process_search_result(result, i + 1)
                    if processed_result:
                        processed_results.append(processed_result)
            
            logger.info(f"Processed {len(processed_results)} results for query: {query}")
            return processed_results
            
        except Exception as e:
            logger.error(f"Error during Outscraper search: {e}")
            return []
    
    def _process_search_result(self, result: Dict[str, Any], position: int) -> Optional[Dict[str, Any]]:
        """
        Process and validate individual search result from Outscraper
        """
        try:
            # Extract key information from Outscraper result format
            processed = {
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', ''),
                'position': position,
                'source': self._extract_domain(result.get('link', '')),
                'displayed_link': result.get('displayed_link', result.get('link', '')),
            }
            
            # Basic validation
            if not processed['title'] or not processed['link']:
                return None
            
            # Classify result type based on domain and content
            processed['result_type'] = self._classify_result(processed)
            
            # Calculate relevance score based on title and snippet
            processed['relevance_score'] = self._calculate_relevance_score(processed)
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing Outscraper search result: {e}")
            return None
    
    def search_companies_in_industry(self, industry: str, location: str = "United States") -> List[Dict[str, Any]]:
        """
        Search for companies in a specific industry using Outscraper
        """
        try:
            query = f"{industry} companies {location}"
            logger.info(f"Searching for companies: {query}")
            
            results = self.client.google_search(
                query=query,
                pages_per_query=1,
                language='en',
                region='US'
            )
            
            companies = []
            if results and len(results) > 0:
                search_results = results[0].get('results_organic', [])
                
                for result in search_results:
                    if self._is_company_result(result):
                        company_info = {
                            'name': result.get('title', ''),
                            'website': result.get('link', ''),
                            'description': result.get('snippet', ''),
                            'domain': self._extract_domain(result.get('link', '')),
                            'industry': industry,
                            'source': 'outscraper_search'
                        }
                        companies.append(company_info)
            
            logger.info(f"Found {len(companies)} companies in {industry}")
            return companies
            
        except Exception as e:
            logger.error(f"Error searching companies in industry: {e}")
            return []
    
    def get_company_business_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed business data for a specific company using Outscraper
        """
        try:
            # Search for the company
            query = f"{company_name} company website"
            results = self.client.google_search(
                query=query,
                pages_per_query=1,
                language='en'
            )
            
            if results and len(results) > 0:
                search_results = results[0].get('results_organic', [])
                
                for result in search_results:
                    if self._is_company_official_site(result, company_name):
                        return {
                            'company_name': company_name,
                            'website': result.get('link', ''),
                            'description': result.get('snippet', ''),
                            'title': result.get('title', ''),
                            'domain': self._extract_domain(result.get('link', '')),
                            'source': 'outscraper_business_search'
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting business data for {company_name}: {e}")
            return None
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            return parsed_url.netloc.lower()
        except:
            return ""
    
    def _classify_result(self, result: Dict[str, Any]) -> str:
        """
        Classify search result type based on domain and content patterns
        """
        domain = result.get('source', '').lower()
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        
        # Company website indicators
        if any(indicator in domain for indicator in ['.com', '.co.uk', '.org', '.net']) and \
           any(keyword in title + snippet for keyword in ['company', 'solutions', 'products', 'services', 'about']):
            return 'company_website'
        
        # News and articles
        if any(indicator in domain for indicator in ['news', 'reuters', 'bloomberg', 'techcrunch', 'forbes']) or \
           any(keyword in title for keyword in ['news', 'announces', 'launches', 'acquires']):
            return 'news_article'
        
        # Research reports
        if any(indicator in title + snippet for indicator in ['report', 'market research', 'analysis', 'study', 'forecast']):
            return 'research_report'
        
        # Government/regulatory
        if any(indicator in domain for indicator in ['.gov', '.mil', 'regulation']) or \
           any(keyword in title for keyword in ['regulation', 'policy', 'government', 'regulatory']):
            return 'regulatory'
        
        return 'other'
    
    def _calculate_relevance_score(self, result: Dict[str, Any]) -> float:
        """
        Calculate relevance score based on various factors
        """
        score = 0.0
        
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        position = result.get('position', 10)
        
        # Position-based scoring (higher positions get higher scores)
        position_score = max(0, (10 - position) / 10)
        score += position_score * 0.3
        
        # Content relevance keywords
        relevance_keywords = [
            'innovative', 'leading', 'technology', 'solutions', 'market leader',
            'enterprise', 'industry', 'advanced', 'next-generation', 'ai',
            'digital', 'platform', 'software', 'services', 'partnership'
        ]
        
        keyword_matches = sum(1 for keyword in relevance_keywords 
                             if keyword in title + snippet)
        score += (keyword_matches / len(relevance_keywords)) * 0.4
        
        # Result type bonus
        type_bonuses = {
            'company_website': 0.3,
            'research_report': 0.2,
            'news_article': 0.1,
            'regulatory': 0.1,
            'other': 0.0
        }
        score += type_bonuses.get(result.get('result_type', 'other'), 0.0)
        
        return min(1.0, score)  # Cap at 1.0
    
    def _is_company_result(self, result: Dict[str, Any]) -> bool:
        """Check if search result appears to be a company"""
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        
        company_indicators = ['company', 'corporation', 'inc', 'ltd', 'llc', 'solutions', 'services', 'technologies']
        return any(indicator in title + snippet for indicator in company_indicators)
    
    def _is_company_official_site(self, result: Dict[str, Any], company_name: str) -> bool:
        """Check if result is likely the official company website"""
        title = result.get('title', '').lower()
        domain = self._extract_domain(result.get('link', ''))
        company_lower = company_name.lower()
        
        # Check if company name appears in title or domain
        return company_lower in title or any(word in domain for word in company_lower.split())
    
    def filter_high_quality_results(self, results: List[Dict[str, Any]], 
                                  min_relevance: float = 0.3) -> List[Dict[str, Any]]:
        """
        Filter results to keep only high-quality, relevant ones
        """
        filtered = []
        
        for result in results:
            # Check relevance score
            if result.get('relevance_score', 0) < min_relevance:
                continue
            
            # Filter out low-quality domains
            domain = result.get('source', '').lower()
            if any(exclude in domain for exclude in ['pinterest', 'facebook', 'twitter', 'instagram']):
                continue
            
            # Prioritize authoritative sources
            if any(authoritative in domain for authoritative in [
                'reuters.com', 'bloomberg.com', 'techcrunch.com', 'forbes.com',
                'mckinsey.com', 'bcg.com', 'deloitte.com', 'accenture.com',
                'gartner.com', 'forrester.com', 'idc.com'
            ]):
                result['authority_bonus'] = True
            
            filtered.append(result)
        
        # Sort by relevance score and authority
        filtered.sort(key=lambda x: (
            x.get('authority_bonus', False),
            x.get('relevance_score', 0)
        ), reverse=True)
        
        logger.info(f"Filtered to {len(filtered)} high-quality results from {len(results)} total")
        return filtered