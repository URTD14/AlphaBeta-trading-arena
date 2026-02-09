import React, { createContext, useContext, useEffect, useState, useRef } from 'react';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const [lastMessage, setLastMessage] = useState(null);
    const [readyState, setReadyState] = useState(0); // 0: CLOSED, 1: OPEN, 2: CLOSING, 3: CLOSED

    const ws = useRef(null);

    useEffect(() => {
        // Connect to local backend
        const connect = () => {
            ws.current = new WebSocket('ws://localhost:8000/ws');

            ws.current.onopen = () => {
                console.log("WebSocket Connected");
                setReadyState(1);
            };

            ws.current.onmessage = (event) => {
                const message = JSON.parse(event.data);
                setLastMessage(message);
            };

            ws.current.onclose = () => {
                console.log("WebSocket Disconnected");
                setReadyState(0);
                setTimeout(connect, 3000); // Reconnect after 3s
            };
            
            setSocket(ws.current);
        };

        connect();

        return () => {
            if (ws.current) ws.current.close();
        };
    }, []);

    return (
        <WebSocketContext.Provider value={{ socket, lastMessage, readyState }}>
            {children}
        </WebSocketContext.Provider>
    );
};

export const useWebSocket = () => useContext(WebSocketContext);
