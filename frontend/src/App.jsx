import React, { useEffect, useState } from 'react';
import { WebSocketProvider, useWebSocket } from './context/WebSocketContext';
import './App.css';

const Dashboard = () => {
    const { lastMessage, readyState } = useWebSocket();
    const [portfolio, setPortfolio] = useState({
        cash: 100000,
        portfolio_value: 100000,
        positions: {},
        trade_log: [],
        roi: 0,
        realized_pnl: 0,
        total_trades: 0
    });
    const [news, setNews] = useState([]);
    const [agentThought, setAgentThought] = useState(null);

    useEffect(() => {
        if (lastMessage) {
            if (lastMessage.type === "PORTFOLIO_UPDATE") {
                setPortfolio(lastMessage.data);
            } else if (lastMessage.type === "NEWS_ALERT") {
                setNews(prev => [lastMessage.data, ...prev].slice(0, 50));
            } else if (lastMessage.type === "AGENT_THOUGHT") {
                setAgentThought(lastMessage.data);
            }
        }
    }, [lastMessage]);

    const roi = portfolio.roi || 0;
    const pnl = portfolio.realized_pnl || 0;
    const unrealizedPnl = portfolio.portfolio_value - 100000 - pnl;

    return (
        <div className="dashboard-grid">
            {/* Header */}
            <header className="header glass-card">
                <div>
                    <h1>ALGO<span style={{ color: 'var(--neon-blue)' }}>MATES</span> AI TRADER</h1>
                    <div style={{ fontSize: '11px', color: '#666', marginTop: '5px' }}>
                        Trades: {portfolio.total_trades || 0} | Cash: ${(portfolio.cash || 0).toFixed(2)}
                    </div>
                </div>
                <div style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
                    {/* P&L Cards */}
                    <div className="pnl-card">
                        <div style={{ fontSize: '10px', color: '#888', textTransform: 'uppercase' }}>Realized P&L</div>
                        <div style={{
                            fontSize: '18px',
                            fontWeight: 'bold',
                            color: pnl >= 0 ? '#00ff9d' : '#ff0055'
                        }}>
                            {pnl >= 0 ? '+' : ''}{pnl.toFixed(2)}
                        </div>
                    </div>
                    <div className="pnl-card">
                        <div style={{ fontSize: '10px', color: '#888', textTransform: 'uppercase' }}>Unrealized P&L</div>
                        <div style={{
                            fontSize: '18px',
                            fontWeight: 'bold',
                            color: unrealizedPnl >= 0 ? '#00ff9d' : '#ff0055'
                        }}>
                            {unrealizedPnl >= 0 ? '+' : ''}{unrealizedPnl.toFixed(2)}
                        </div>
                    </div>
                    <div className="pnl-card">
                        <div style={{ fontSize: '10px', color: '#888', textTransform: 'uppercase' }}>ROI</div>
                        <div style={{
                            fontSize: '18px',
                            fontWeight: 'bold',
                            color: roi >= 0 ? '#00ff9d' : '#ff0055'
                        }}>
                            {roi >= 0 ? '+' : ''}{roi.toFixed(2)}%
                        </div>
                    </div>
                    {/* Portfolio Value */}
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '12px', color: '#888' }}>TOTAL EQUITY</div>
                        <div className="portfolio-value">
                            ${(portfolio.portfolio_value || 0).toFixed(2)}
                        </div>
                        <div style={{ color: readyState === 1 ? '#00ff00' : '#ff0000', fontSize: '10px' }}>
                            {readyState === 1 ? '● LIVE SYSTEM' : '● DISCONNECTED'}
                        </div>
                    </div>
                </div>
            </header>

            {/* Left Col: News */}
            <div className="news-panel glass-card scrollbar-hide">
                <h2>Live Market Intelligence</h2>
                {news.map((item, i) => (
                    <div key={i} className="news-item">
                        <h3 style={{ color: '#fff' }}>{item.title}</h3>
                        <div className="news-meta">{item.source} • {item.published}</div>
                    </div>
                ))}
                {news.length === 0 && <p>Waiting for market news...</p>}
            </div>

            {/* Center Col: Agent Activity */}
            <div className="main-panel">
                <div className="agent-thought glass-card">
                    <h2>Gemini Agent Brain</h2>
                    {agentThought ? (
                        <div>
                            <div style={{ marginBottom: '10px', color: '#aaa', fontSize: '13px' }}>
                                Analyzed: "{agentThought.article?.substring(0, 80)}..."
                            </div>
                            <div style={{ fontSize: '20px', color: '#fff', marginBottom: '10px' }}>
                                Decision: <span style={{
                                    color: agentThought.action === 'BUY' ? '#00ff9d' :
                                        agentThought.action === 'SELL' ? '#ff0055' : '#ffff00',
                                    fontWeight: 'bold'
                                }}>{agentThought.action}</span>
                                {agentThought.ticker && (
                                    <span style={{ marginLeft: '10px', color: 'var(--neon-blue)' }}>
                                        {agentThought.ticker}
                                    </span>
                                )}
                                {agentThought.live_price && (
                                    <span style={{ marginLeft: '10px', color: '#888', fontSize: '14px' }}>
                                        @ ${agentThought.live_price.toFixed(2)}
                                    </span>
                                )}
                            </div>
                            <div style={{ fontStyle: 'italic', borderLeft: '2px solid var(--neon-purple)', paddingLeft: '10px', color: '#ccc' }}>
                                "{agentThought.thought}"
                            </div>
                            <div style={{ marginTop: '10px', fontSize: '12px', color: '#888' }}>
                                Confidence: {((agentThought.confidence || 0) * 100).toFixed(0)}%
                            </div>
                        </div>
                    ) : (
                        <div style={{ textAlign: 'center', padding: '20px', color: '#666' }}>
                            Agent is scanning global feeds...
                        </div>
                    )}
                </div>

                <div className="glass-card" style={{ flex: 1 }}>
                    <h2>Asset Allocation</h2>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                        {Object.entries(portfolio.positions || {}).map(([ticker, qty]) => (
                            <div key={ticker} style={{
                                background: 'rgba(255,255,255,0.05)',
                                padding: '12px',
                                borderRadius: '8px',
                                minWidth: '100px',
                                textAlign: 'center'
                            }}>
                                <div style={{ fontWeight: 'bold', color: 'var(--neon-blue)', fontSize: '16px' }}>{ticker}</div>
                                <div style={{ fontSize: '14px', color: '#fff' }}>{qty} shares</div>
                            </div>
                        ))}
                        {Object.keys(portfolio.positions || {}).length === 0 && <p>No active positions.</p>}
                    </div>
                </div>
            </div>

            {/* Right Col: Trade Log */}
            <div className="trade-panel glass-card scrollbar-hide">
                <h2>Execution Log</h2>
                {(portfolio.trade_log || []).map((trade, i) => (
                    <div key={i} className="trade-item">
                        <div>
                            <div style={{ fontWeight: 'bold', color: '#fff' }}>{trade.ticker}</div>
                            <div style={{ fontSize: '10px', color: '#666' }}>
                                {trade.time?.split('T')[1]?.split('.')[0] || ''}
                            </div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                            <div className={trade.action === 'BUY' ? 'trade-buy' : 'trade-sell'}>
                                {trade.action} {trade.qty}
                            </div>
                            <div style={{ fontSize: '12px', color: '#aaa' }}>@ ${trade.price}</div>
                            {trade.pnl !== undefined && (
                                <div style={{
                                    fontSize: '11px',
                                    fontWeight: 'bold',
                                    color: trade.pnl >= 0 ? '#00ff9d' : '#ff0055'
                                }}>
                                    {trade.pnl >= 0 ? '+' : ''}{trade.pnl}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {(portfolio.trade_log || []).length === 0 && <p>No trades executed yet.</p>}
            </div>
        </div>
    );
};

const App = () => {
    return (
        <WebSocketProvider>
            <Dashboard />
        </WebSocketProvider>
    );
};

export default App;
