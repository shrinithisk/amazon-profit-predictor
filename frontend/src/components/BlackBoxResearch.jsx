import React, { useState, useEffect } from 'react';
import { Search, Globe, ShieldCheck, Zap, Lock } from 'lucide-react';

export default function BlackBoxResearch({ selectedRegion, privacyMode = true }) {
  const [products, setProducts] = useState([]);
  const [regionFilter, setRegionFilter] = useState(selectedRegion || 'US');
  const [searchTerm, setSearchTerm] = useState('');
  const [dataSource, setDataSource] = useState('CATALOG_DATABASE');

  useEffect(() => {
    setRegionFilter(selectedRegion);
  }, [selectedRegion]);

  useEffect(() => {
    fetchProducts();
  }, [regionFilter, searchTerm]);

  const fetchProducts = async () => {
    try {
      const queryParam = searchTerm ? `&query=${encodeURIComponent(searchTerm)}` : '';
      const res = await fetch(`/api/products?region=${regionFilter}${queryParam}`);
      const data = await res.json();
      setProducts(data.products || []);
      setDataSource(data.source || 'CATALOG_DATABASE');
    } catch (e) {
      console.error("Products fetch error:", e);
    }
  };

  return (
    <div className="space-y-6 py-6">
      
      {/* Header & Live Data Indicator */}
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-display text-white flex items-center space-x-3">
            <Search className="w-8 h-8 text-sky-400" />
            <span>Black Box Real-Time Product Research</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Search live Amazon product ASINs and filter catalog metrics across US, EU, UK, UAE, and India hubs.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          {privacyMode && (
            <span className="inline-flex items-center space-x-1.5 bg-amber-500/10 text-amber-300 border border-amber-500/30 text-xs font-semibold px-3 py-1.5 rounded-xl">
              <Lock className="w-3.5 h-3.5 text-amber-400" />
              <span>Privacy Mode Active</span>
            </span>
          )}

          {dataSource === 'LIVE_AMAZON_REALTIME' && (
            <span className="inline-flex items-center space-x-1.5 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold px-3 py-1.5 rounded-xl animate-pulse">
              <Zap className="w-3.5 h-3.5 fill-current" />
              <span>Live Real Amazon Data Connected</span>
            </span>
          )}
        </div>
      </div>

      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
        
        {/* Search Input */}
        <div className="relative">
          <Search className="w-4.5 h-4.5 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Search live products or ASIN (e.g. iPhone 15 Pro Max, AirPods, Nike, Samsung, LEGO)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-11 pr-4 py-3 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-sky-500 font-medium shadow-inner"
          />
        </div>

        {/* Products Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400">
                <th className="pb-3 font-semibold">Product Title & ASIN</th>
                <th className="pb-3 font-semibold">Category</th>
                <th className="pb-3 font-semibold">Region</th>
                <th className="pb-3 font-semibold text-right">Price</th>
                <th className="pb-3 font-semibold text-right">Rating ⭐</th>
                <th className="pb-3 font-semibold text-right">Est. Monthly Sales</th>
                <th className="pb-3 font-semibold text-right">
                  {privacyMode ? "Margin %" : "Est. Monthly Profit"}
                </th>
                <th className="pb-3 font-semibold text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-200">
              {products.length === 0 ? (
                <tr>
                  <td colSpan="8" className="py-8 text-center text-slate-400 font-medium">
                    No products found. Type a search query above to fetch live Amazon items.
                  </td>
                </tr>
              ) : (
                products.map((p, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 font-medium text-white max-w-xs truncate">
                      <div className="font-semibold text-slate-100">{p.product_name}</div>
                      {p.asin && (
                        <div className="text-[10px] text-sky-400 font-mono">ASIN: {p.asin}</div>
                      )}
                    </td>
                    <td className="py-3 text-slate-400">{p.category}</td>
                    <td className="py-3 font-semibold text-sky-400">{p.marketplace_region}</td>
                    <td className="py-3 text-right font-semibold">{p.price ? `${p.currency || '$'} ${p.price.toLocaleString()}` : '--'}</td>
                    <td className="py-3 text-right text-amber-400 font-bold">{p.rating || 4.1}</td>
                    <td className="py-3 text-right font-semibold text-sky-400">{p.monthly_sales ? p.monthly_sales.toLocaleString() : '--'}</td>
                    <td className="py-3 text-right font-semibold text-emerald-400">
                      {privacyMode ? (
                        <span>{p.margin_pct ? `${p.margin_pct}%` : '24.5%'}</span>
                      ) : (
                        <span>{p.currency || '$'} {p.monthly_profit ? p.monthly_profit.toLocaleString() : '--'}</span>
                      )}
                    </td>
                    <td className="py-3 text-center">
                      {p.is_profitable ? (
                        <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                          WINNER 🏆
                        </span>
                      ) : (
                        <span className="bg-slate-800 text-slate-400 text-[10px] font-medium px-2 py-0.5 rounded-full">
                          STANDARD
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
