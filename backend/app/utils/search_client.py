import os
from dotenv import load_dotenv
import requests
from ..config import SEARCH_API_KEY

load_dotenv()  
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY") or os.getenv("SEARCH_API_KEY")

def search_web(query, top_k=3):
    if not SEARCH_API_KEY:
        return []

    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SEARCH_API_KEY,
            "num": top_k
        }
        r = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        results = []
        for item in data.get("organic_results", [])[:top_k]:
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet", ""),
                "url": item.get("link", "")
            })
        return results

    except:
        return []
