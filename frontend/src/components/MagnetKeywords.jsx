import React, { useState, useEffect } from 'react';
import { KeyRound, Search, TrendingUp, Zap } from 'lucide-react';

export default function MagnetKeywords() {
  const [query, setQuery] = useState('earbuds');
  const [keywords, setKeywords] = useState([]);

  useEffect(() => {
    fetchKeywords(query);
  }, [query]);

  const fetchKeywords = async (q) => {
    try {
      const res = await fetch(`/api/keywords?query=${q}`);
      const data = await res.json();
      setKeywords(data.keywords || []);
    } catch (e) {
      console.error("Keywords error:", e);
    }
  };

  return (
    <div className="space-y-6 py-6">
      
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <h1 className="text-2xl sm:text-3xl font-extrabold font-display text-white flex items-center space-x-3">
          <KeyRound className="w-8 h-8 text-sky-400" />
          <span>Magnet Keyword Research</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Uncover customer search volume metrics, CPC bids ($), and competitive Magnet Opportunity Scores.
        </p>
      </div>

      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter seed keyword (e.g. earbuds, yoga mat, kettle)..."
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 font-medium"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400">
                <th className="pb-3 font-semibold">Search Term</th>
                <th className="pb-3 font-semibold text-right">Search Volume</th>
                <th className="pb-3 font-semibold text-right">Avg CPC Bid ($)</th>
                <th className="pb-3 font-semibold text-right">Competing Sellers</th>
                <th className="pb-3 font-semibold text-center">Opportunity Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-200">
              {keywords.map((k, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 font-semibold text-white">{k.keyword}</td>
                  <td className="py-3 text-right font-semibold text-sky-400">{k.search_volume.toLocaleString()}</td>
                  <td className="py-3 text-right text-emerald-400 font-medium">${k.cpc_bid_usd}</td>
                  <td className="py-3 text-right text-slate-400">{k.competing_products}</td>
                  <td className="py-3 text-center">
                    <span className="bg-sky-500/20 text-sky-300 border border-sky-500/30 text-[10px] font-bold px-2.5 py-0.5 rounded-full">
                      {k.magnet_score} / 100
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
