import os
import requests
import time
import random
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Synthetic news for continuous trading when real news runs out
SYNTHETIC_NEWS_TEMPLATES = [
    {"title": "Apple announces breakthrough in AI chip development", "ticker": "AAPL", "sentiment": "bullish"},
    {"title": "Tesla Cybertruck deliveries exceed expectations", "ticker": "TSLA", "sentiment": "bullish"},
    {"title": "NVIDIA reports record data center revenue", "ticker": "NVDA", "sentiment": "bullish"},
    {"title": "Microsoft Azure growth accelerates to new highs", "ticker": "MSFT", "sentiment": "bullish"},
    {"title": "Amazon Web Services expands into new markets", "ticker": "AMZN", "sentiment": "bullish"},
    {"title": "Meta's Reality Labs shows improved financials", "ticker": "META", "sentiment": "bullish"},
    {"title": "Google Cloud wins major enterprise contracts", "ticker": "GOOGL", "sentiment": "bullish"},
    {"title": "AMD gains market share in server processors", "ticker": "AMD", "sentiment": "bullish"},
    {"title": "Bitcoin surges on institutional adoption news", "ticker": "BTC-USD", "sentiment": "bullish"},
    {"title": "S&P 500 futures point to higher open", "ticker": "SPY", "sentiment": "bullish"},
    {"title": "Tech sector faces regulatory headwinds", "ticker": "QQQ", "sentiment": "bearish"},
    {"title": "Tesla factory production delays reported", "ticker": "TSLA", "sentiment": "bearish"},
    {"title": "Apple iPhone sales slow in China market", "ticker": "AAPL", "sentiment": "bearish"},
    {"title": "NVIDIA faces supply chain constraints", "ticker": "NVDA", "sentiment": "bearish"},
    {"title": "Market volatility spikes on economic data", "ticker": "VIX", "sentiment": "bearish"},
    {"title": "Intel announces restructuring plan", "ticker": "INTC", "sentiment": "bearish"},
    {"title": "Crypto market sees profit-taking pressure", "ticker": "BTC-USD", "sentiment": "bearish"},
    {"title": "Oil prices surge on supply concerns", "ticker": "USO", "sentiment": "bullish"},
    {"title": "Gold rallies as safe-haven demand increases", "ticker": "GLD", "sentiment": "bullish"},
    {"title": "Netflix subscriber growth beats estimates", "ticker": "NFLX", "sentiment": "bullish"},
]

class NewsFetcher:
    def __init__(self):
        self.seen_ids = set()
        self.last_real_fetch = 0
        self.synthetic_index = 0
        self.real_news_cooldown = 60  # Try real news every 60 seconds

    def _get_synthetic_news(self) -> Dict:
        """Generate synthetic news for continuous trading."""
        template = SYNTHETIC_NEWS_TEMPLATES[self.synthetic_index % len(SYNTHETIC_NEWS_TEMPLATES)]
        self.synthetic_index += 1
        
        return {
            "title": f"{template['title']} - {time.strftime('%H:%M:%S')}",
            "link": "#",
            "published": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "Market Signals",
            "ticker_hint": template["ticker"],
            "sentiment_hint": template["sentiment"]
        }

    def fetch_latest_news(self) -> List[Dict]:
        """Fetch real news or generate synthetic for continuous trading."""
        new_articles = []
        current_time = time.time()
        
        # Try real news periodically
        if NEWS_API_KEY and (current_time - self.last_real_fetch) > self.real_news_cooldown:
            self.last_real_fetch = current_time
            try:
                params = {
                    "apiKey": NEWS_API_KEY,
                    "q": "stock market trading finance earnings crypto",
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 10
                }
                
                response = requests.get(NEWS_API_URL, params=params, timeout=5)
                data = response.json()
                
                if data.get("status") == "ok":
                    for article in data.get("articles", []):
                        article_id = article.get("url", article.get("title"))
                        if article_id not in self.seen_ids:
                            self.seen_ids.add(article_id)
                            new_articles.append({
                                "title": article.get("title", "Market Update"),
                                "link": article.get("url", ""),
                                "published": article.get("publishedAt", time.ctime()),
                                "source": article.get("source", {}).get("name", "NewsAPI")
                            })
                            
            except Exception as e:
                print(f"Real news fetch error: {e}")
        
        # If no real news, generate synthetic for continuous trading
        if not new_articles:
            # Generate 1-3 synthetic news items
            for _ in range(random.randint(1, 3)):
                new_articles.append(self._get_synthetic_news())
        
        # Reset seen cache if it gets too large
        if len(self.seen_ids) > 500:
            self.seen_ids = set(list(self.seen_ids)[-100:])
        
        return new_articles

news_fetcher = NewsFetcher()
