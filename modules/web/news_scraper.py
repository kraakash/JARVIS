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
    
    def get_election_results(self, query):
        """Get election results from NewsAPI"""
        try:
            # Use NewsAPI for election results
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
                return "Sir, news service mein thoda issue hai. Baad mein try kariye."
            
        except Exception as e:
            print(f"[NEWS] Error: {e}")
            return "Sir, internet connection check kariye. News fetch nahi ho pa raha."
    
    def get_current_news(self, topic):
        """Get current news about any topic using NewsAPI"""
        try:
            # Use NewsAPI for current news
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
                return "Sir, news service temporarily unavailable hai."
            
        except Exception as e:
            print(f"[NEWS] Error: {e}")
            return "Sir, news fetch karne mein technical issue aa gaya."

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