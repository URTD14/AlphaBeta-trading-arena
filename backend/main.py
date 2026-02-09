import asyncio
import json
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from news_fetcher import NewsFetcher
from trader_agent import TraderAgent
from paper_engine import PaperEngine
from price_fetcher import get_live_price

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
news_service = NewsFetcher()
agent = TraderAgent()
engine = PaperEngine()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json({
            "type": "PORTFOLIO_UPDATE",
            "data": engine.get_state()
        })
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def process_article(article: dict):
    """Process a single article with LIVE prices."""
    # Broadcast News
    await manager.broadcast({
        "type": "NEWS_ALERT",
        "data": article
    })

    # Agent Analyzes
    decision = agent.analyze_news(article)
    
    if decision:
        ticker = decision.get('ticker', 'SPY')
        
        # Get LIVE price from Yahoo Finance
        live_price = get_live_price(ticker)
        
        # Broadcast Decision with live price
        await manager.broadcast({
            "type": "AGENT_THOUGHT",
            "data": {
                "article": article['title'],
                "thought": decision.get('reasoning', 'Analyzing...'),
                "action": decision.get('action', 'HOLD'),
                "confidence": decision.get('confidence', 0.5),
                "ticker": ticker,
                "live_price": live_price
            }
        })

        # Execute Trade with REAL live price
        engine.execute_trade(decision, current_price=live_price)

        # Broadcast Portfolio Update
        await manager.broadcast({
            "type": "PORTFOLIO_UPDATE",
            "data": engine.get_state()
        })

async def market_loop():
    """
    CONTINUOUS trading loop - never stops!
    """
    cycle = 0
    while True:
        try:
            cycle += 1
            print(f"[Market Loop] Cycle {cycle} - Fetching news...")
            
            # Fetch News
            news = news_service.fetch_latest_news()
            
            if news:
                print(f"[Market Loop] Got {len(news)} new articles")
                for article in news:
                    await process_article(article)
                    await asyncio.sleep(0.3)  # Fast processing
            else:
                # No new news - do a quick portfolio valuation update with live prices
                print("[Market Loop] No new news - updating portfolio valuations...")
                all_tickers = list(engine.positions.keys())
                if all_tickers:
                    prices = {t: get_live_price(t) for t in all_tickers}
                    engine._update_valuation(prices)
                    await manager.broadcast({
                        "type": "PORTFOLIO_UPDATE",
                        "data": engine.get_state()
                    })
            
            # Very short delay - continuous operation
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"[Market Loop] Error: {e}")
            await asyncio.sleep(2)  # Brief pause on error, then continue

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(market_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
