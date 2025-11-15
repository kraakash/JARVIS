"""
Real-time News and Information Scraper
Gets current information without opening browser
"""

import requests
from bs4 import BeautifulSoup
import json

class NewsInfoScraper:
    def __init__(self):
        self.api_key = "rioxjE0JG42piQclawm1GjH5ISRgHykqs3ig2DCQ"
        self.base_url = "https://newsapi.org/v2/everything"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.use_fallback = False
    
    def scrape_google_news(self, query):
        """Fallback method using simple news scraping"""
        try:
            # Use a simpler approach with RSS feeds or basic news sites
            search_query = query.replace(' ', '+')
            
            # Try BBC News RSS for reliable content
            rss_url = "http://feeds.bbci.co.uk/news/rss.xml"
            response = requests.get(rss_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item', limit=5)
                
                if items:
                    result = f"Latest news, Sir:\n"
                    count = 0
                    for item in items:
                        title = item.find('title')
                        if title and query.lower() in title.get_text().lower():
                            count += 1
                            result += f"{count}. {title.get_text().strip()}\n"
                            if count >= 3:
                                break
                    
                    if count > 0:
                        return result
                    else:
                        # If no matching news, return general headlines
                        result = "Top Headlines, Sir:\n"
                        for i, item in enumerate(items[:3], 1):
                            title = item.find('title')
                            if title:
                                result += f"{i}. {title.get_text().strip()}\n"
                        return result
                else:
                    return f"Sir, {query} ke baare mein abhi koi news nahi mili."
            else:
                return "Sir, news service temporarily unavailable hai."
                
        except Exception as e:
            print(f"[NEWS] Scraping Error: {e}")
            return "Sir, abhi news fetch nahi kar pa raha. Thoda baad try kariye."
    
    def get_election_results(self, query):
        """Get election results from NewsAPI or fallback"""
        try:
            # Try NewsAPI first
            params = {
                'q': f"election results {query}",
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 3,
                'apiKey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    result = "Latest Election News, Sir:\n"
                    for i, article in enumerate(articles[:3], 1):
                        title = article.get('title', 'No title')
                        description = article.get('description', '')
                        result += f"{i}. {title}\n"
                        if description:
                            result += f"   {description[:100]}...\n"
                    return result
                else:
                    return "Sir, election results abhi available nahi hain. Thoda baad check karte hain."
            else:
                # API failed, use fallback
                print(f"[NEWS] API failed, using fallback scraping")
                return self.scrape_google_news(f"election results {query}")
            
        except Exception as e:
            print(f"[NEWS] Error: {e}")
            # Try fallback on any error
            return self.scrape_google_news(f"election results {query}")
    
    def get_current_news(self, topic):
        """Get current news about any topic using NewsAPI or fallback"""
        try:
            # Try NewsAPI first
            params = {
                'q': topic,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 3,
                'apiKey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    result = f"Latest news about {topic}, Sir:\n"
                    for i, article in enumerate(articles[:3], 1):
                        title = article.get('title', 'No title')
                        description = article.get('description', '')
                        result += f"{i}. {title}\n"
                        if description:
                            result += f"   {description[:100]}...\n"
                    return result
                else:
                    return f"Sir, {topic} ke baare mein abhi koi fresh news nahi mili."
            else:
                # API failed, use fallback
                print(f"[NEWS] API failed, using fallback scraping")
                return self.scrape_google_news(topic)
            
        except Exception as e:
            print(f"[NEWS] Error: {e}")
            # Try fallback on any error
            return self.scrape_google_news(topic)

    def get_top_headlines(self, country='in'):
        """Get top headlines for India"""
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'country': country,
                'pageSize': 5,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    result = "Top Headlines, Sir:\n"
                    for i, article in enumerate(articles[:5], 1):
                        title = article.get('title', 'No title')
                        result += f"{i}. {title}\n"
                    return result
                else:
                    return "Sir, abhi koi major headlines nahi hain."
            else:
                return "Sir, headlines fetch karne mein issue aa gaya."
                
        except Exception as e:
            print(f"[NEWS] Error: {e}")
            return "Sir, headlines service mein problem hai."

# Singleton instance
news_scraper = NewsInfoScraper()