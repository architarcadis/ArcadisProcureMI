import os
import requests
import logging
from typing import List, Dict, Any, Optional
import time

logger = logging.getLogger(__name__)

class SerpAPIService:
    """Service for SerpAPI Google search interactions"""
    
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY", "")
        if not self.api_key:
            logger.error("SerpAPI key not found in environment variables")
            raise ValueError("SerpAPI key is required")
        
        self.base_url = "https://serpapi.com/search"
        self.results_per_query = 20  # Number of results to fetch per search
    
    def search_market_intelligence(self, keywords: List[str], num_results: int = None) -> List[Dict[str, Any]]:
        """
        Search for market intelligence using provided keywords
        Returns aggregated search results from all keywords
        """
        if num_results is None:
            num_results = self.results_per_query
            
        all_results = []
        
        for keyword in keywords:
            try:
                logger.info(f"Searching for keyword: {keyword}")
                results = self._perform_search(keyword, num_results)
                
                # Add keyword context to results
                for result in results:
                    result['search_keyword'] = keyword
                
                all_results.extend(results)
                
                # Rate limiting - small delay between requests
                time.sleep(0.5)
                
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
        
        logger.info(f"Total unique search results collected: {len(unique_results)}")
        return unique_results
    
    def _perform_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Perform individual search query via SerpAPI
        """
        params = {
            'q': query,
            'api_key': self.api_key,
            'engine': 'google',
            'num': min(num_results, 100),  # SerpAPI limit
            'hl': 'en',
            'gl': 'us'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract organic results
            organic_results = data.get('organic_results', [])
            
            # Filter and structure results
            processed_results = []
            for result in organic_results:
                processed_result = self._process_search_result(result)
                if processed_result:
                    processed_results.append(processed_result)
            
            logger.info(f"Processed {len(processed_results)} results for query: {query}")
            return processed_results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error during search: {e}")
            return []
        except KeyError as e:
            logger.error(f"Unexpected API response format: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []
    
    def _process_search_result(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process and validate individual search result
        """
        try:
            # Extract key information
            processed = {
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', ''),
                'position': result.get('position', 0),
                'source': self._extract_domain(result.get('link', '')),
                'displayed_link': result.get('displayed_link', ''),
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
            logger.error(f"Error processing search result: {e}")
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
        if any(indicator in domain for indicator in ['.com', '.co.uk', '.org']) and \
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
