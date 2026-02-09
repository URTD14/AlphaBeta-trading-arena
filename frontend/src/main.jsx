import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css' // We can keep the default vite index.css or remove it if App.css covers everything. 
// Actually App.jsx imports App.css. index.css usually has base tailwind or resets. 
// I'll make sure index.css is empty or basic reset to avoid conflicts.

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
