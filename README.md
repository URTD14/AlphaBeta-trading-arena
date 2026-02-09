# 🚀 AlphaBeta Trading Arena

**AI-Powered Real-Time Paper Trading Platform** — Watch Gemini AI agents analyze live market news and execute trades in real-time!

![Demo](https://img.shields.io/badge/Status-Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- **🤖 Gemini AI Agent** — Analyzes news headlines and makes BUY/SELL/HOLD decisions
- **📰 Live Market News** — Real-time news from NewsAPI + synthetic market signals
- **💹 Live Stock Prices** — Real prices from Yahoo Finance
- **📊 Paper Trading Engine** — Simulated $100,000 portfolio with P&L tracking
- **⚡ WebSocket Updates** — Real-time UI updates without page refresh
- **🎨 Glassmorphism UI** — Modern, premium dark theme dashboard

## 🖼️ Preview

The dashboard shows:
- Live news feed (left)
- AI agent thinking process (center)
- Asset allocation & trade execution log (right)
- Real-time P&L, ROI, and portfolio value (header)

## 🛠️ Tech Stack

| Backend | Frontend |
|---------|----------|
| Python 3.8+ | React 18 |
| FastAPI | Vite |
| WebSockets | Vanilla CSS |
| Google Gemini AI | WebSocket Context |
| Yahoo Finance | Glassmorphism Design |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 18+ and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AlphaBeta-trading-arena.git
cd AlphaBeta-trading-arena
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Get API Keys

You'll need two API keys:

| Service | Get Key | Purpose |
|---------|---------|---------|
| **Google Gemini** | [Google AI Studio](https://aistudio.google.com/apikey) | AI trading decisions |
| **NewsAPI** | [NewsAPI.org](https://newsapi.org/register) | Real-time news |

Add them to `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_key_here
NEWS_API_KEY=your_newsapi_key_here
```

## 🚀 Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

### Open in Browser
Navigate to: **http://localhost:5173**

## 📁 Project Structure

```
AlphaBeta-trading-arena/
├── backend/
│   ├── main.py           # FastAPI app + WebSocket
│   ├── news_fetcher.py   # NewsAPI + synthetic signals
│   ├── trader_agent.py   # Gemini AI agent
│   ├── paper_engine.py   # Trading engine + P&L
│   ├── price_fetcher.py  # Yahoo Finance prices
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main dashboard
│   │   ├── App.css       # Glassmorphism styles
│   │   └── context/      # WebSocket provider
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## ⚙️ Configuration

| Environment Variable | Description | Required |
|---------------------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `NEWS_API_KEY` | NewsAPI key for live news | Optional* |

*If NewsAPI key is not provided, the system uses synthetic market signals.

## 🎮 How It Works

1. **News Fetcher** polls for latest financial news every 60 seconds
2. **Gemini Agent** analyzes each headline and decides: BUY, SELL, or HOLD
3. **Price Fetcher** gets live stock prices from Yahoo Finance
4. **Paper Engine** executes trades and tracks portfolio P&L
5. **WebSocket** broadcasts all updates to the React dashboard in real-time

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This is a **paper trading simulation** for educational purposes only. It does not involve real money or real trades. Always do your own research before making actual investment decisions.

---

**Built with ❤️ using Gemini AI, FastAPI, and React**
