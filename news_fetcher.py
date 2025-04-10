import requests
from config import Config
from urllib.parse import urlencode

class NewsFetcher:
    BASE_URL = "https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey=b59c87e76a8181edb273623223c844c7"
    
    @staticmethod
    def fetch_news(query="technology", lang="en", country="us", max_results=5):
        # Clean the query string
        query = query.strip()
        if not query:
            return []
            
        params = {
            "q": query,
            "lang": lang,
            "country": country,
            "max": max_results,
            "apikey": Config.GNEWS_API_KEY
        }
        
        try:
            response = requests.get(
                NewsFetcher.BASE_URL,
                params=params,
                timeout=15  # Increased timeout
            )
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Filter out empty articles
            return [
                {
                    'title': article.get('title', 'No title available'),
                    'description': article.get('description', ''),
                    'content': article.get('content', 'Description not available'),
                    'url': article.get('url', '#'),
                    'publishedAt': article.get('publishedAt', 'Date not available'),
                    'image': article.get('image')
                }
                for article in articles
                if article.get('title')  # Only include articles with titles
            ]
            
        except requests.exceptions.RequestException as e:
            print(f"News API error: {str(e)}")
            return []