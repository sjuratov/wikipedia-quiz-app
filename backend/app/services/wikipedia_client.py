"""Wikipedia API client."""
import httpx
from typing import List, Optional, Dict, Any
from app.utils.cache import cache_manager


class WikipediaClient:
    """Client for interacting with Wikipedia API."""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    CACHE_TTL = 7 * 24 * 60 * 60  # 7 days
    
    def __init__(self):
        # Wikipedia requires a User-Agent header
        headers = {
            "User-Agent": "WikipediaQuizApp/1.0 (Educational; Python/httpx)"
        }
        self.session = httpx.AsyncClient(timeout=10.0, headers=headers)
        
    async def search_topic(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search Wikipedia for topics."""
        cache_key = f"wiki_search:{query}:{limit}"
        cached = cache_manager.get(cache_key)
        if cached:
            return cached
            
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
            "utf8": 1
        }
        
        try:
            response = await self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "query" in data and "search" in data["query"]:
                for item in data["query"]["search"]:
                    results.append({
                        "title": item["title"],
                        "snippet": item.get("snippet", ""),
                        "pageid": item["pageid"]
                    })
            
            cache_manager.set(cache_key, results, self.CACHE_TTL)
            return results
            
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
            
    async def get_article_content(self, title: str) -> Optional[str]:
        """Get full article content by title."""
        cache_key = f"wiki_content:{title}"
        cached = cache_manager.get(cache_key)
        if cached:
            return cached
            
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
            "exsectionformat": "plain",
            "format": "json",
            "utf8": 1
        }
        
        try:
            response = await self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "query" in data and "pages" in data["query"]:
                pages = data["query"]["pages"]
                page = next(iter(pages.values()))
                
                if "extract" in page:
                    content = page["extract"]
                    cache_manager.set(cache_key, content, self.CACHE_TTL)
                    return content
                    
            return None
            
        except Exception as e:
            print(f"Wikipedia content fetch error: {e}")
            return None
            
    async def is_disambiguation_page(self, title: str) -> bool:
        """Check if a page is a disambiguation page."""
        params = {
            "action": "query",
            "titles": title,
            "prop": "categories",
            "format": "json",
            "utf8": 1
        }
        
        try:
            response = await self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "query" in data and "pages" in data["query"]:
                pages = data["query"]["pages"]
                page = next(iter(pages.values()))
                
                if "categories" in page:
                    for cat in page["categories"]:
                        if "disambiguation" in cat.get("title", "").lower():
                            return True
                            
            return False
            
        except Exception as e:
            print(f"Disambiguation check error: {e}")
            return False
            
    async def close(self):
        """Close the HTTP client."""
        await self.session.aclose()


# Global instance
wikipedia_client = WikipediaClient()
