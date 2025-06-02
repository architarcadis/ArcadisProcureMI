"""
Credible Source Direct Access Module
Direct crawling of authoritative UK sources for procurement intelligence
"""

import requests
import trafilatura
from typing import List, Dict, Any
import json
import time

class CredibleSourceCrawler:
    """Direct access to authoritative global sources"""
    
    def __init__(self):
        # Regional credible sources mapping
        self.credible_sources = {
            'UK': {
                'government': ['companieshouse.gov.uk', 'gov.uk', 'ons.gov.uk', 'bankofengland.co.uk'],
                'financial': ['ft.com', 'reuters.com', 'bbc.co.uk/news/business'],
                'regulatory': ['fca.org.uk', 'legislation.gov.uk']
            },
            'US': {
                'government': ['sec.gov', 'treasury.gov', 'commerce.gov'],
                'financial': ['wsj.com', 'bloomberg.com', 'cnbc.com'],
                'regulatory': ['federalregister.gov', 'ftc.gov']
            },
            'EU': {
                'government': ['europa.eu', 'ecb.europa.eu'],
                'financial': ['ft.com', 'reuters.com'],
                'regulatory': ['eur-lex.europa.eu', 'esma.europa.eu']
            },
            'Global': {
                'government': ['worldbank.org', 'imf.org'],
                'financial': ['reuters.com', 'bloomberg.com', 'ft.com'],
                'regulatory': ['bis.org', 'oecd.org']
            }
        }
        
        # Alert deduplication tracking
        self.processed_alerts = set()
        self.alert_signatures = {}
    
    def crawl_companies_house_data(self, company_name: str) -> Dict[str, Any]:
        """
        Direct access to Companies House public data
        Using their search interface for company information
        """
        search_url = f"https://find-and-update.company-information.service.gov.uk/search/companies?q={company_name}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Extract text content using trafilatura
                content = trafilatura.extract(response.text)
                
                return {
                    'source': 'Companies House (Official UK Government)',
                    'authority_level': 'High Authority',
                    'url': search_url,
                    'content': content,
                    'data_type': 'Official Company Registry',
                    'credibility': 'Government Source'
                }
        except Exception as e:
            return {'error': f"Failed to access Companies House: {str(e)}"}
        
        return {'error': 'No data found'}
    
    def crawl_gov_uk_news(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Crawl gov.uk news and announcements
        """
        search_url = f"https://www.gov.uk/search/news-and-communications?keywords={search_term}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = trafilatura.extract(response.text)
                
                return [{
                    'source': 'GOV.UK Official News',
                    'authority_level': 'High Authority',
                    'url': search_url,
                    'content': content,
                    'data_type': 'Government News & Policy',
                    'credibility': 'Official Government Source'
                }]
        except Exception as e:
            return [{'error': f"Failed to access GOV.UK: {str(e)}"}]
        
        return []
    
    def crawl_financial_times(self, company_name: str) -> Dict[str, Any]:
        """
        Crawl Financial Times for company news
        """
        search_url = f"https://www.ft.com/search?q={company_name}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = trafilatura.extract(response.text)
                
                return {
                    'source': 'Financial Times',
                    'authority_level': 'High Authority',
                    'url': search_url,
                    'content': content,
                    'data_type': 'Financial News',
                    'credibility': 'Authoritative Financial Media'
                }
        except Exception as e:
            return {'error': f"Failed to access Financial Times: {str(e)}"}
        
        return {'error': 'No data found'}
    
    def generate_alert_signature(self, title: str, supplier: str, description: str) -> str:
        """Generate unique signature for alert deduplication"""
        import hashlib
        content = f"{title.lower()}{supplier.lower()}{description[:100].lower()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def is_duplicate_alert(self, alert: Dict[str, Any]) -> bool:
        """Check if alert is duplicate based on content similarity"""
        signature = self.generate_alert_signature(
            alert.get('title', ''), 
            alert.get('supplier', ''), 
            alert.get('description', '')
        )
        
        if signature in self.processed_alerts:
            return True
        
        # Check for similar alerts (different categories, same content)
        for existing_sig, existing_alert in self.alert_signatures.items():
            if (alert.get('supplier') == existing_alert.get('supplier') and
                alert.get('title', '').lower() in existing_alert.get('title', '').lower() or
                existing_alert.get('title', '').lower() in alert.get('title', '').lower()):
                return True
        
        self.processed_alerts.add(signature)
        self.alert_signatures[signature] = alert
        return False
    
    def crawl_regional_sources(self, supplier_name: str, regions: List[str]) -> List[Dict[str, Any]]:
        """Crawl credible sources based on regions"""
        results = []
        
        for region in regions:
            if region not in self.credible_sources:
                continue
                
            regional_sources = self.credible_sources[region]
            
            # Government sources
            for gov_source in regional_sources['government'][:2]:  # Limit to prevent overload
                try:
                    search_url = f"https://{gov_source}/search?q={supplier_name}"
                    data = self.crawl_generic_source(search_url, f"{region} Government - {gov_source}", "High Authority")
                    if data and 'error' not in data:
                        results.append(data)
                except Exception:
                    continue
            
            # Financial sources
            for fin_source in regional_sources['financial'][:2]:
                try:
                    search_url = f"https://{fin_source}/search?q={supplier_name}"
                    data = self.crawl_generic_source(search_url, f"{region} Financial - {fin_source}", "High Authority")
                    if data and 'error' not in data:
                        results.append(data)
                except Exception:
                    continue
            
            # Add delay between regions
            time.sleep(0.5)
        
        return results
    
    def crawl_generic_source(self, url: str, source_name: str, authority_level: str) -> Dict[str, Any]:
        """Generic crawler for any credible source"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = trafilatura.extract(response.text)
                
                if content and len(content) > 100:  # Ensure meaningful content
                    return {
                        'source': source_name,
                        'authority_level': authority_level,
                        'url': url,
                        'content': content,
                        'data_type': 'Authoritative Source',
                        'credibility': f'{authority_level} Source'
                    }
        except Exception as e:
            return {'error': f"Failed to access {source_name}: {str(e)}"}
        
        return {'error': 'No meaningful content found'}
    
    def get_comprehensive_supplier_intelligence(self, supplier_name: str, regions: List[str] = ['UK']) -> List[Dict[str, Any]]:
        """
        Get comprehensive intelligence from multiple credible sources across regions
        """
        results = []
        
        # Reset deduplication for new supplier
        self.processed_alerts.clear()
        self.alert_signatures.clear()
        
        # Get regional intelligence
        regional_data = self.crawl_regional_sources(supplier_name, regions)
        results.extend(regional_data)
        
        # Add specific high-value sources
        if 'UK' in regions:
            # Companies House data
            ch_data = self.crawl_companies_house_data(supplier_name)
            if 'error' not in ch_data:
                results.append(ch_data)
            
            # Government news
            gov_news = self.crawl_gov_uk_news(supplier_name)
            results.extend(gov_news)
        
        # Global financial sources
        ft_data = self.crawl_financial_times(supplier_name)
        if 'error' not in ft_data:
            results.append(ft_data)
        
        # Add delays to be respectful to servers
        time.sleep(1)
        
        return results