import React, { useState } from 'react';
import { BarChart3, Sliders, Share2, Check, ArrowUpRight } from 'lucide-react';

export default function PricingPlans() {
  const [selectedPlan, setSelectedPlan] = useState('platinum');

  return (
    <div className="py-10 space-y-16">
      
      {/* 3 Top Feature Cards matching user screenshot */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-8 hover:border-sky-500/50 hover:shadow-xl hover:shadow-sky-500/10 transition-all group">
          <div className="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400 mb-6 group-hover:scale-110 transition-transform">
            <BarChart3 className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold font-display text-white mb-3">Product & Keyword Research</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Instantly find profitable products and high-volume keywords to excel on Amazon.
          </p>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-8 hover:border-sky-500/50 hover:shadow-xl hover:shadow-sky-500/10 transition-all group">
          <div className="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400 mb-6 group-hover:scale-110 transition-transform">
            <Sliders className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold font-display text-white mb-3">Amazon to TikTok Shop Listing Converter</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Automatically reformat and cross post your Amazon listings to TikTok Shop to save you hours of manual work.
          </p>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-8 hover:border-sky-500/50 hover:shadow-xl hover:shadow-sky-500/10 transition-all group">
          <div className="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400 mb-6 group-hover:scale-110 transition-transform">
            <Share2 className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold font-display text-white mb-3">AI Powered Listing Optimization</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Optimize product listings for maximum sales velocity with listing optimization tools.
          </p>
        </div>

      </div>

      {/* Pricing Plan Section matching user screenshot */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-3xl p-8 lg:p-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Title & Toggle */}
          <div className="lg:col-span-5 space-y-6">
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold text-white leading-tight">
              Find the Right Plan For You
            </h2>
            <p className="text-sm text-slate-400 leading-relaxed">
              A pricing plan for every budget, business goal, and seller across global marketplaces.
            </p>

            {/* Platinum vs Diamond Toggle matching user screenshot */}
            <div className="inline-flex p-1.5 bg-slate-800/90 border border-slate-700 rounded-full">
              <button
                onClick={() => setSelectedPlan('platinum')}
                className={`px-6 py-2 rounded-full text-xs font-bold transition-all ${
                  selectedPlan === 'platinum'
                    ? 'bg-white text-slate-900 shadow-md'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Platinum
              </button>
              <button
                onClick={() => setSelectedPlan('diamond')}
                className={`px-6 py-2 rounded-full text-xs font-bold transition-all ${
                  selectedPlan === 'diamond'
                    ? 'bg-white text-slate-900 shadow-md'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Diamond
              </button>
            </div>
          </div>

          {/* Right Pricing Card matching user screenshot */}
          <div className="lg:col-span-7 bg-gradient-to-br from-slate-800/80 to-slate-900 border border-slate-700/80 rounded-2xl p-8 shadow-2xl">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
              
              <div className="md:col-span-7 space-y-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-sky-400">
                  Scale with {selectedPlan === 'platinum' ? 'Platinum' : 'Diamond'}
                </span>
                <h3 className="text-xl font-bold text-white">
                  The must-have solution for your growing business
                </h3>

                <ul className="space-y-2.5 pt-2">
                  <li className="flex items-center space-x-2 text-xs text-slate-300">
                    <ArrowUpRight className="w-4 h-4 text-sky-400 shrink-0" />
                    <span>Find new profitable products globally</span>
                  </li>
                  <li className="flex items-center space-x-2 text-xs text-slate-300">
                    <ArrowUpRight className="w-4 h-4 text-sky-400 shrink-0" />
                    <span>Reduce your manual workload by 80%</span>
                  </li>
                  <li className="flex items-center space-x-2 text-xs text-slate-300">
                    <ArrowUpRight className="w-4 h-4 text-sky-400 shrink-0" />
                    <span>Maximize sales with AI-powered ads</span>
                  </li>
                </ul>
              </div>

              <div className="md:col-span-5 text-center border-t md:border-t-0 md:border-l border-slate-700/80 pt-6 md:pt-0 md:pl-6 space-y-4">
                <span className="inline-block bg-sky-500/20 text-sky-300 border border-sky-500/30 text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">
                  Most Popular
                </span>
                <div>
                  <div className="text-3xl font-extrabold text-white font-display">
                    {selectedPlan === 'platinum' ? '$103' : '$229'}
                    <span className="text-xs text-slate-400 font-normal">/mo.</span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1">20% off for 6 months</p>
                </div>

                <button className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-sky-500 hover:from-blue-500 hover:to-sky-400 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/20 hover:shadow-sky-500/35 transition-all">
                  Claim Offer
                </button>
              </div>

            </div>
          </div>

        </div>
      </div>

    </div>
  );
}
