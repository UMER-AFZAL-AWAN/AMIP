import { Activity, BarChart2, Brain, Compass, Cpu, Layers, ShieldAlert } from 'lucide-react';
import React, { useState, useEffect } from 'react';
import { Routes, Route, NavLink, useLocation } from 'react-router-dom';
import Overview from './pages/Overview';
import MarketAnalysis from './pages/MarketAnalysis';
import Predictions from './pages/Predictions';
import Models from './pages/Models';
import Patterns from './pages/Patterns';
import Risk from './pages/Risk';

function App() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <Brain color="var(--accent-blue)" size={28} />
          <span>AMIP</span>
        </div>
        <nav className="sidebar-nav">
          <NavLink to="/" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
            <Activity size={20} /> Overview
          </NavLink>
          <NavLink to="/analysis" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
            <BarChart2 size={20} /> Market Analysis
          </NavLink>
          <NavLink to="/predictions" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
            <Compass size={20} /> Predictions
          </NavLink>
          <NavLink to="/models" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
            <Cpu size={20} /> Models
          </NavLink>
          <NavLink to="/patterns" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
            <Layers size={20} /> Patterns
          </NavLink>
          <NavLink to="/risk" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
            <ShieldAlert size={20} /> Risk Dashboard
          </NavLink>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="topbar">
          <div className="topbar-time">{new Date().toLocaleDateString()} {time} (UTC)</div>
          <div className="topbar-status">
            <div className="status-dot"></div>
            <span>System Online • Latency 24ms</span>
          </div>
        </header>

        <div className="page-content">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/analysis" element={<MarketAnalysis />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/models" element={<Models />} />
            <Route path="/patterns" element={<Patterns />} />
            <Route path="/risk" element={<Risk />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}

export default App;
