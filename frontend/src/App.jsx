import React, { useState } from 'react';
import Navbar from './components/Navbar.jsx';
import HeroBanner from './components/HeroBanner.jsx';
import ControlTower from './components/ControlTower.jsx';
import ProfitPredictor from './components/ProfitPredictor.jsx';
import CrossBorderLogistics from './components/CrossBorderLogistics.jsx';
import BlackBoxResearch from './components/BlackBoxResearch.jsx';
import MagnetKeywords from './components/MagnetKeywords.jsx';
import { Zap, Lock } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('control-tower');
  const [selectedRegion, setSelectedRegion] = useState('US');
  const [privacyMode, setPrivacyMode] = useState(true); // Default ON for Safe Financial Portfolio Showcase

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* Header Navigation with Privacy Mode Toggle */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedRegion={selectedRegion}
        setSelectedRegion={setSelectedRegion}
        privacyMode={privacyMode}
        setPrivacyMode={setPrivacyMode}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        
        {/* Render Hero Banner ONLY on the 1st page (GCC Control Tower) */}
        {activeTab === 'control-tower' && <HeroBanner />}

        {/* Dynamic Tool Suite Views with Financial Privacy Mode */}
        {activeTab === 'control-tower' && (
          <ControlTower selectedRegion={selectedRegion} privacyMode={privacyMode} />
        )}
        {activeTab === 'predictor' && (
          <ProfitPredictor selectedRegion={selectedRegion} privacyMode={privacyMode} />
        )}
        {activeTab === 'logistics' && (
          <CrossBorderLogistics selectedRegion={selectedRegion} privacyMode={privacyMode} />
        )}
        {activeTab === 'blackbox' && (
          <BlackBoxResearch selectedRegion={selectedRegion} privacyMode={privacyMode} />
        )}
        {activeTab === 'magnet' && (
          <MagnetKeywords privacyMode={privacyMode} />
        )}

      </main>

      {/* Modern SaaS Footer */}
      <footer className="bg-slate-900/90 border-t border-slate-800 text-slate-400 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <div className="bg-gradient-to-r from-blue-600 to-sky-500 p-1.5 rounded-lg text-white">
              <Zap className="w-4 h-4 fill-current" />
            </div>
            <span className="font-display font-extrabold text-lg text-white">NexaPulse AI</span>
          </div>

          <div className="flex items-center justify-center space-x-2 text-xs text-amber-400/90 bg-amber-500/10 border border-amber-500/20 py-1.5 px-4 rounded-full max-w-md mx-auto">
            <Lock className="w-3.5 h-3.5" />
            <span>Financial Data Best Practices: Absolute Revenue Figures Masked</span>
          </div>

          <p className="text-xs text-slate-500 max-w-xl mx-auto">
            © 2026 NexaPulse AI Enterprise Suite. Engineered for Global E-Commerce Sellers, Dropshippers, and Multi-Market Intelligence (US, EU, UK, UAE, IN).
          </p>
        </div>
      </footer>

    </div>
  );
}
