import React from 'react';
import { Sparkles } from 'lucide-react';

export default function HeroBanner() {
  return (
    <div className="relative overflow-hidden helium-hero-gradient rounded-3xl p-8 sm:p-12 lg:p-14 my-6 shadow-2xl text-white">
      
      {/* Background Decorative Lighting */}
      <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-sky-400/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-1/3 -mb-20 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-4xl mx-auto text-center">
        
        {/* Sub-badge */}
        <div className="inline-flex items-center space-x-2 bg-white/10 border border-white/20 px-3.5 py-1.5 rounded-full text-xs font-semibold text-sky-200 backdrop-blur-md mb-6">
          <Sparkles className="w-3.5 h-3.5 text-sky-300" />
          <span>Amazon Marketplace Intelligence Platform</span>
        </div>

        {/* Main Headline */}
        <h1 className="font-display text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight mb-6">
          Scale profit & seller intelligence <span className="text-sky-200">with NexaPulse AI.</span>
        </h1>

        <p className="text-sm sm:text-base font-medium text-blue-100 opacity-90 max-w-2xl mx-auto leading-relaxed">
          Predict sales volume, calculate cross-border landed costs, optimize listings, and manage multi-region portfolio EBITDA across global Amazon marketplaces.
        </p>

      </div>
    </div>
  );
}
