from typing import Dict, List
import datetime

class PaperEngine:
    def __init__(self, initial_cash=100000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Dict] = {}  # Ticker -> {qty, avg_price}
        self.portfolio_value = initial_cash
        self.trade_log: List[Dict] = []
        self.start_time = datetime.datetime.now()
        self.pnl = 0.0

    def execute_trade(self, decision: Dict, current_price: float):
        """
        Executes a trade based on the agent's decision using REAL prices.
        """
        ticker = decision.get("ticker", "SPY")
        action = decision.get("action")
        confidence = decision.get("confidence", 0)
        allocation_pct = decision.get("allocation_percent", 0.05)

        if confidence < 0.35 or action == "HOLD":
            return  # Skip low confidence or hold

        trade_amount = self.portfolio_value * allocation_pct
        quantity = int(trade_amount / current_price) if current_price > 0 else 0

        if quantity == 0:
            return

        timestamp = datetime.datetime.now().isoformat()
        
        if action == "BUY":
            cost = quantity * current_price
            if self.cash >= cost:
                self.cash -= cost
                
                if ticker in self.positions:
                    # Average down/up
                    old_qty = self.positions[ticker]['qty']
                    old_avg = self.positions[ticker]['avg_price']
                    new_qty = old_qty + quantity
                    new_avg = ((old_qty * old_avg) + (quantity * current_price)) / new_qty
                    self.positions[ticker] = {'qty': new_qty, 'avg_price': new_avg}
                else:
                    self.positions[ticker] = {'qty': quantity, 'avg_price': current_price}
                
                self.trade_log.insert(0, {
                    "time": timestamp,
                    "action": "BUY",
                    "ticker": ticker,
                    "qty": quantity,
                    "price": round(current_price, 2),
                    "reason": decision.get("reasoning", "")[:50]
                })

        elif action == "SELL":
            if ticker in self.positions:
                current_qty = self.positions[ticker]['qty']
                avg_price = self.positions[ticker]['avg_price']
                qty_to_sell = min(current_qty, quantity)
                
                if qty_to_sell > 0:
                    revenue = qty_to_sell * current_price
                    realized_pnl = (current_price - avg_price) * qty_to_sell
                    self.pnl += realized_pnl
                    self.cash += revenue
                    
                    self.positions[ticker]['qty'] -= qty_to_sell
                    if self.positions[ticker]['qty'] <= 0:
                        del self.positions[ticker]
                    
                    self.trade_log.insert(0, {
                        "time": timestamp,
                        "action": "SELL",
                        "ticker": ticker,
                        "qty": qty_to_sell,
                        "price": round(current_price, 2),
                        "pnl": round(realized_pnl, 2),
                        "reason": decision.get("reasoning", "")[:50]
                    })

        # Keep only last 50 trades
        self.trade_log = self.trade_log[:50]
        self._update_valuation({ticker: current_price})

    def _update_valuation(self, current_prices: Dict[str, float]):
        """Updates total portfolio value based on LIVE prices."""
        pos_value = 0
        for ticker, data in self.positions.items():
            qty = data['qty']
            price = current_prices.get(ticker, data['avg_price'])
            pos_value += qty * price
        self.portfolio_value = self.cash + pos_value

    def get_state(self):
        # Format positions for frontend
        positions_display = {}
        for ticker, data in self.positions.items():
            positions_display[ticker] = data['qty']
        
        roi = ((self.portfolio_value - self.initial_cash) / self.initial_cash) * 100
        
        return {
            "cash": round(self.cash, 2),
            "portfolio_value": round(self.portfolio_value, 2),
            "positions": positions_display,
            "trade_log": self.trade_log[:20],
            "roi": round(roi, 2),
            "realized_pnl": round(self.pnl, 2),
            "total_trades": len(self.trade_log)
        }

paper_engine = PaperEngine()
