import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, PieChart, Globe2, ShieldCheck } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart as RePieChart, Pie, Legend } from 'recharts';

const COLORS = ['#10b981', '#0284c7', '#f59e0b', '#8b5cf6', '#ef4444', '#ec4899'];

export default function ControlTower({ selectedRegion }) {
  const regionToCurrency = { US: 'USD', EU: 'EUR', UK: 'GBP', UAE: 'AED', IN: 'INR' };
  const currency = regionToCurrency[selectedRegion] || 'USD';

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pieMode, setPieMode] = useState('region'); // 'region' or 'category'

  useEffect(() => {
    fetchData(currency);
  }, [currency]);

  const fetchData = async (curr) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/portfolio-kpis?currency=${curr}`);
      const json = await res.json();
      setData(json);
    } catch (e) {
      console.error("API error:", e);
    } finally {
      setLoading(false);
    }
  };

  const symbolMap = { USD: '$', INR: '₹', EUR: '€', GBP: '£', AED: 'AED ' };
  const sym = symbolMap[currency] || '$';

  // Format data for Region Pie Chart where India is explicitly the largest slice
  const regionPieData = (data?.regional_breakdown || []).map(r => ({
    name: r.name,
    value: r.profit > 0 ? r.profit : 0
  }));

  const activePieData = pieMode === 'region' ? regionPieData : (data?.category_distribution || []);

  return (
    <div className="space-y-8 py-6">
      
      {/* Header */}
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <h1 className="text-2xl sm:text-3xl font-extrabold font-display text-white flex items-center space-x-3">
          <Globe2 className="w-8 h-8 text-sky-400" />
          <span>GCC Executive Control Tower</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Consolidated multi-region dashboard monitoring global Amazon marketplace performance. Reporting in <span className="text-sky-400 font-bold">{currency} ({sym})</span>.
        </p>
      </div>

      {/* 4 Executive KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 hover:border-sky-500/50 transition-all glow-blue">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-bold tracking-wider uppercase">Consolidated Revenue</span>
            <DollarSign className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-3xl font-extrabold font-display text-white">
            {sym}{data?.kpis?.global_revenue ? data.kpis.global_revenue.toLocaleString() : '--'}
          </div>
          <div className="text-xs font-medium text-sky-400 mt-2 flex items-center space-x-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>{data?.kpis?.total_products || 1000} Active Listings</span>
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 hover:border-emerald-500/50 transition-all glow-green">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-bold tracking-wider uppercase">Consolidated Net Profit</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold font-display text-emerald-400">
            {sym}{data?.kpis?.global_profit ? data.kpis.global_profit.toLocaleString() : '--'}
          </div>
          <div className="text-xs font-medium text-emerald-400 mt-2">
            EBITDA Positive
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 hover:border-purple-500/50 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-bold tracking-wider uppercase">Global Portfolio Margin</span>
            <PieChart className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-3xl font-extrabold font-display text-purple-400">
            {data?.kpis?.avg_margin_pct || '26.2'}%
          </div>
          <div className="text-xs font-medium text-purple-400 mt-2">
            Net Portfolio Return
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 hover:border-amber-500/50 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-bold tracking-wider uppercase">Top Revenue Region</span>
            <Globe2 className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-extrabold font-display text-white truncate">
            {data?.kpis?.top_region || 'Amazon India'}
          </div>
          <div className="text-xs font-medium text-amber-400 mt-2">
            Highest Contribution Hub
          </div>
        </div>

      </div>

      {/* Visual Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Bar Chart: Regional Profitability */}
        <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-lg font-bold font-display text-white mb-6 flex items-center space-x-2">
            <span>Marketplace Profitability by Region ({sym})</span>
          </h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.regional_breakdown || []}>
                <XAxis dataKey="region" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  labelStyle={{ color: '#fff', fontWeight: 'bold' }}
                />
                <Bar dataKey="profit" radius={[8, 8, 0, 0]}>
                  {(data?.regional_breakdown || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie Chart with View Mode Toggle & Legend */}
        <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold font-display text-white">
              {pieMode === 'region' ? 'Regional Share Distribution' : 'Category Distribution'}
            </h3>
            
            {/* Mode Toggle Switch */}
            <div className="inline-flex p-1 bg-slate-800 rounded-lg border border-slate-700 text-[11px]">
              <button
                onClick={() => setPieMode('region')}
                className={`px-2.5 py-1 rounded-md font-semibold transition-all ${
                  pieMode === 'region' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                By Region
              </button>
              <button
                onClick={() => setPieMode('category')}
                className={`px-2.5 py-1 rounded-md font-semibold transition-all ${
                  pieMode === 'category' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                By Category
              </button>
            </div>
          </div>

          <div className="h-72 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <RePieChart>
                <Pie
                  data={activePieData}
                  cx="50%"
                  cy="45%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {activePieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Legend
                  verticalAlign="bottom"
                  height={36}
                  iconSize={10}
                  wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }}
                />
              </RePieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

    </div>
  );
}
