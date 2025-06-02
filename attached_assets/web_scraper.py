import logging
import requests
from bs4 import BeautifulSoup
import trafilatura
from typing import Optional, Dict, Any
import time
from urllib.parse import urljoin, urlparse
import re

logger = logging.getLogger(__name__)

class WebScraper:
    """Service for web content scraping and extraction"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 30
        self.max_content_length = 50000  # Maximum content length to process
    
    def scrape_url_content(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape content from a single URL using trafilatura for better text extraction
        """
        try:
            logger.info(f"Scraping content from: {url}")
            
            # Use trafilatura for content extraction
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                logger.warning(f"Failed to download content from: {url}")
                return None
            
            # Extract main text content
            text_content = trafilatura.extract(downloaded)
            if not text_content:
                logger.warning(f"No text content extracted from: {url}")
                return None
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(downloaded)
            
            # Get additional page information
            soup = BeautifulSoup(downloaded, 'html.parser')
            page_title = self._extract_page_title(soup)
            
            result = {
                'url': url,
                'title': page_title,
                'content': text_content[:self.max_content_length],  # Limit content length
                'content_length': len(text_content),
                'metadata': {
                    'author': metadata.author if metadata else None,
                    'date': metadata.date if metadata else None,
                    'description': metadata.description if metadata else None,
                    'tags': metadata.tags if metadata else None,
                    'categories': metadata.categories if metadata else None
                },
                'domain': urlparse(url).netloc,
                'scrape_timestamp': time.time()
            }
            
            logger.info(f"Successfully scraped {len(text_content)} characters from: {url}")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {e}")
            return None
    
    def scrape_company_subpages(self, base_url: str, max_pages: int = 3) -> Dict[str, Any]:
        """
        Attempt to scrape relevant subpages from a company website
        Focus on About, Products, Technology, News pages
        """
        scraped_data = {
            'base_url': base_url,
            'pages': {},
            'total_content_length': 0
        }
        
        try:
            # First scrape the main page
            main_content = self.scrape_url_content(base_url)
            if main_content:
                scraped_data['pages']['main'] = main_content
                scraped_data['total_content_length'] += main_content['content_length']
            
            # Find and scrape relevant subpages
            subpage_urls = self._find_relevant_subpages(base_url)
            
            pages_scraped = 1  # Already scraped main page
            for page_type, url in subpage_urls.items():
                if pages_scraped >= max_pages:
                    break
                
                content = self.scrape_url_content(url)
                if content:
                    scraped_data['pages'][page_type] = content
                    scraped_data['total_content_length'] += content['content_length']
                    pages_scraped += 1
                
                # Small delay between requests
                time.sleep(1)
            
            logger.info(f"Scraped {pages_scraped} pages from {base_url}")
            return scraped_data
            
        except Exception as e:
            logger.error(f"Error scraping company subpages from {base_url}: {e}")
            return scraped_data
    
    def _find_relevant_subpages(self, base_url: str) -> Dict[str, str]:
        """
        Find relevant subpages on a company website
        """
        subpages = {}
        
        try:
            response = self.session.get(base_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Common patterns for relevant pages
            page_patterns = {
                'about': ['about', 'about-us', 'company', 'who-we-are'],
                'products': ['products', 'services', 'solutions', 'offerings'],
                'technology': ['technology', 'innovation', 'research', 'tech'],
                'news': ['news', 'press', 'media', 'blog', 'updates'],
                'sustainability': ['sustainability', 'esg', 'environment', 'csr']
            }
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                link_text = link.get_text(strip=True).lower()
                
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, href)
                
                # Check if link matches our patterns
                for page_type, patterns in page_patterns.items():
                    if page_type not in subpages:  # Only take first match
                        for pattern in patterns:
                            if (pattern in href.lower() or pattern in link_text) and \
                               self._is_same_domain(base_url, full_url):
                                subpages[page_type] = full_url
                                break
            
            logger.info(f"Found {len(subpages)} relevant subpages for {base_url}")
            return subpages
            
        except Exception as e:
            logger.error(f"Error finding subpages for {base_url}: {e}")
            return {}
    
    def _extract_page_title(self, soup: BeautifulSoup) -> str:
        """Extract page title from BeautifulSoup object"""
        try:
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text(strip=True)
            
            # Fallback to h1
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.get_text(strip=True)
            
            return "No title found"
        except:
            return "No title found"
    
    def _is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain"""
        try:
            domain1 = urlparse(url1).netloc.lower()
            domain2 = urlparse(url2).netloc.lower()
            
            # Remove www. prefix for comparison
            domain1 = re.sub(r'^www\.', '', domain1)
            domain2 = re.sub(r'^www\.', '', domain2)
            
            return domain1 == domain2
        except:
            return False
    
    def batch_scrape_urls(self, urls: list, max_concurrent: int = 5) -> Dict[str, Any]:
        """
        Scrape multiple URLs with rate limiting
        """
        results = {}
        
        for i, url in enumerate(urls[:max_concurrent]):  # Limit concurrent requests
            try:
                result = self.scrape_url_content(url)
                if result:
                    results[url] = result
                
                # Rate limiting
                if i < len(urls) - 1:
                    time.sleep(2)  # 2 second delay between requests
                    
            except Exception as e:
                logger.error(f"Error in batch scraping URL {url}: {e}")
                continue
        
        logger.info(f"Batch scraped {len(results)} URLs successfully")
        return results
    
    def clean_text_content(self, content: str) -> str:
        """
        Clean and normalize text content for better analysis
        """
        try:
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            
            # Remove common web artifacts
            content = re.sub(r'(cookie|privacy policy|terms of service|newsletter)', '', content, flags=re.IGNORECASE)
            
            # Remove navigation elements
            content = re.sub(r'(home|contact|about|products|services)\s*\|', '', content, flags=re.IGNORECASE)
            
            # Trim and return
            return content.strip()
        except:
            return content
