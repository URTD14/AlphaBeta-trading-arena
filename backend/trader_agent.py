import os
import json
import time
import random
import google.generativeai as genai
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

# Keywords for simple sentiment analysis fallback
BULLISH_KEYWORDS = ['surge', 'soar', 'rally', 'gain', 'profit', 'beat', 'growth', 'record', 'bullish', 'buy', 'upgrade', 'positive', 'strong', 'rise', 'jump', 'boom', 'breakthrough', 'success']
BEARISH_KEYWORDS = ['crash', 'plunge', 'fall', 'drop', 'loss', 'miss', 'decline', 'bearish', 'sell', 'downgrade', 'negative', 'weak', 'slump', 'tumble', 'warning', 'crisis', 'fail', 'cut']

# Ticker extraction
TICKER_KEYWORDS = {
    'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'alphabet': 'GOOGL',
    'amazon': 'AMZN', 'tesla': 'TSLA', 'nvidia': 'NVDA', 'meta': 'META', 
    'facebook': 'META', 'netflix': 'NFLX', 'amd': 'AMD', 'intel': 'INTC',
    'bitcoin': 'BTC-USD', 'crypto': 'BTC-USD', 'ethereum': 'ETH-USD',
    'oil': 'USO', 'gold': 'GLD', 'sp500': 'SPY', 's&p': 'SPY'
}

class TraderAgent:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.last_api_call = 0
        self.rate_limit_delay = 3  # 3 seconds between API calls

    def _fallback_analysis(self, news_item: Dict) -> Dict:
        """Fast fallback when API is rate limited - uses simple sentiment analysis."""
        title = news_item.get('title', '').lower()
        
        # Count sentiment keywords
        bullish_score = sum(1 for word in BULLISH_KEYWORDS if word in title)
        bearish_score = sum(1 for word in BEARISH_KEYWORDS if word in title)
        
        # Extract ticker
        ticker = 'SPY'
        for keyword, symbol in TICKER_KEYWORDS.items():
            if keyword in title:
                ticker = symbol
                break
        
        # Determine action
        if bullish_score > bearish_score:
            action = 'BUY'
            confidence = min(0.5 + (bullish_score * 0.1), 0.9)
            reasoning = f"Bullish signals detected ({bullish_score} positive keywords)"
        elif bearish_score > bullish_score:
            action = 'SELL'
            confidence = min(0.5 + (bearish_score * 0.1), 0.9)
            reasoning = f"Bearish signals detected ({bearish_score} negative keywords)"
        else:
            action = random.choice(['BUY', 'SELL'])  # Random for excitement!
            confidence = 0.45
            reasoning = "Neutral sentiment - taking speculative position"
        
        return {
            "action": action,
            "ticker": ticker,
            "confidence": confidence,
            "reasoning": reasoning,
            "allocation_percent": random.uniform(0.02, 0.08)
        }

    def analyze_news(self, news_item: Dict) -> Optional[Dict]:
        """Analyzes news - uses Gemini when possible, falls back to simple analysis."""
        
        # Rate limiting
        time_since_last = time.time() - self.last_api_call
        if time_since_last < self.rate_limit_delay:
            # Use fallback instead of waiting
            print("Rate limit: Using fast fallback analysis")
            return self._fallback_analysis(news_item)
        
        prompt = f"""You are an AI trader. Analyze this headline and decide BUY, SELL, or HOLD.

News: "{news_item['title']}"

Output JSON only:
{{"action": "BUY/SELL/HOLD", "ticker": "SYMBOL", "confidence": 0.0-1.0, "reasoning": "one sentence", "allocation_percent": 0.01-0.10}}"""
        
        try:
            self.last_api_call = time.time()
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean markdown
            if '```' in text:
                text = text.split('```')[1] if '```' in text else text
                if text.startswith('json'):
                    text = text[4:]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"Gemini Error (using fallback): {e}")
            return self._fallback_analysis(news_item)

trader_agent = TraderAgent()
