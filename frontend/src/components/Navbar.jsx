import React from 'react';
import { LayoutDashboard, TrendingUp, Ship, Search, KeyRound, Globe, Zap, Lock, Unlock } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, selectedRegion, setSelectedRegion, privacyMode, setPrivacyMode }) {
  const navItems = [
    { id: 'control-tower', label: 'GCC Control Tower', icon: LayoutDashboard },
    { id: 'predictor', label: 'AI Profit Predictor', icon: TrendingUp },
    { id: 'logistics', label: 'Cross-Border Logistics', icon: Ship },
    { id: 'blackbox', label: 'Black Box Research', icon: Search },
    { id: 'magnet', label: 'Magnet Keywords', icon: KeyRound },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-800/80 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Brand Logo - NexaPulse AI */}
          <div 
            className="flex items-center space-x-3 cursor-pointer shrink-0 mr-4 sm:mr-8" 
            onClick={() => setActiveTab('control-tower')}
          >
            <div className="bg-gradient-to-r from-blue-600 to-sky-500 p-2.5 rounded-xl text-white shadow-lg shadow-sky-500/20">
              <Zap className="w-5 h-5 fill-current" />
            </div>
            <div className="whitespace-nowrap">
              <div className="flex items-center space-x-2">
                <span className="font-display font-extrabold text-xl tracking-tight text-white">NexaPulse</span>
                <span className="bg-sky-500/20 text-sky-400 border border-sky-500/30 text-[10px] font-bold px-1.5 py-0.5 rounded">AI</span>
              </div>
              <p className="text-[11px] font-medium text-slate-400">Global Commerce Suite</p>
            </div>
          </div>

          {/* Centered Navigation Tabs */}
          <nav className="hidden xl:flex items-center justify-center flex-1 space-x-2 px-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25 ring-1 ring-blue-400/50'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
                  }`}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Controls: Financial Privacy Toggle & Region Selector */}
          <div className="flex items-center space-x-3 shrink-0 ml-2">
            
            {/* Financial Privacy Best Practice Toggle */}
            <button
              onClick={() => setPrivacyMode(!privacyMode)}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-xl text-xs font-semibold border transition-all ${
                privacyMode
                  ? 'bg-amber-500/10 border-amber-500/40 text-amber-300 hover:bg-amber-500/20'
                  : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200'
              }`}
              title={privacyMode ? "Privacy Mode Active: Raw revenue numbers are masked for portfolio safety" : "Demo Mode: Displaying raw estimates"}
            >
              {privacyMode ? <Lock className="w-3.5 h-3.5 text-amber-400" /> : <Unlock className="w-3.5 h-3.5 text-slate-400" />}
              <span className="hidden md:inline">{privacyMode ? "Privacy Mode (ON)" : "Privacy Mode (OFF)"}</span>
            </button>

            {/* Marketplace Region Selector */}
            <div className="flex items-center bg-slate-800/90 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-slate-200 shadow-sm">
              <Globe className="w-4 h-4 text-sky-400 mr-2 shrink-0" />
              <select
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
                className="bg-transparent font-semibold text-white focus:outline-none cursor-pointer pr-1"
              >
                <option value="US" className="bg-slate-900 text-white">🇺🇸 USA (USD $)</option>
                <option value="EU" className="bg-slate-900 text-white">🇪🇺 Europe (EUR €)</option>
                <option value="UK" className="bg-slate-900 text-white">🇬🇧 UK (GBP £)</option>
                <option value="UAE" className="bg-slate-900 text-white">🇦🇪 UAE (AED)</option>
                <option value="IN" className="bg-slate-900 text-white">🇮🇳 India (INR ₹)</option>
              </select>
            </div>

          </div>

        </div>

        {/* Mobile / Tablet Sub-Navigation Bar */}
        <div className="flex xl:hidden overflow-x-auto py-2.5 border-t border-slate-800/60 no-scrollbar space-x-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap shrink-0 ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

      </div>
    </header>
  );
}
