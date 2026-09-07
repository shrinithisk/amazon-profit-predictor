import React, { useState, useEffect } from 'react';
import { TrendingUp, Award, DollarSign, Calculator, Percent, Sparkles, CheckCircle, AlertTriangle, ShieldCheck, Clock, Lock } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const COST_COLORS = ['#64748b', '#3b82f6', '#ef4444', '#f59e0b', '#10b981'];

export default function ProfitPredictor({ selectedRegion, privacyMode = true }) {
  const [formData, setFormData] = useState({
    category: 'Consumer Electronics',
    region: selectedRegion || 'US',
    price: selectedRegion === 'IN' ? 2500 : 35,
    cost: selectedRegion === 'IN' ? 800 : 11,
    rating: 4.3,
    num_reviews: 350,
    competition: 3,
    listing_score: 7,
    ads_spend_pct: 0.12,
    fulfillment_type: 'Amazon FBA',
    supplier_lead_days: 2,
    restocking_fee_pct: 10
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setFormData(prev => ({ ...prev, region: selectedRegion }));
  }, [selectedRegion]);

  useEffect(() => {
    runPrediction();
  }, [formData.category, formData.region, formData.price, formData.cost, formData.rating, formData.num_reviews, formData.competition, formData.listing_score, formData.ads_spend_pct, formData.fulfillment_type]);

  const runPrediction = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error("Prediction error:", e);
    } finally {
      setLoading(false);
    }
  };

  const sym = result?.symbol || '$';

  const chartData = result?.cost_breakdown ? [
    { name: 'Sourcing Cost', value: result.cost_breakdown.sourcing_cost },
    { name: 'Amazon Fees', value: result.cost_breakdown.amazon_fees },
    { name: 'Taxes', value: result.cost_breakdown.tax_liability },
    { name: 'Ads Spend', value: result.cost_breakdown.ads_cost },
    { name: 'Net Profit', value: result.cost_breakdown.net_profit }
  ] : [];

  const roiPct = (result?.net_unit_profit && formData.cost > 0)
    ? Math.round((result.net_unit_profit / formData.cost) * 100)
    : 0;

  return (
    <div className="space-y-8 py-6">
      
      {/* Tool Header & Dropshipping Policy Banner */}
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-display text-white flex items-center space-x-3">
            <TrendingUp className="w-8 h-8 text-sky-400" />
            <span>Multi-Region AI Profit Predictor</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Predict monthly sales volume and winner probability across global Amazon marketplaces using Random Forest ML models.
          </p>
        </div>

        {/* Badges */}
        <div className="flex flex-wrap items-center gap-2">
          {privacyMode && (
            <span className="flex items-center space-x-1.5 bg-amber-500/10 border border-amber-500/30 px-3 py-2 rounded-xl text-amber-300 text-xs font-semibold shrink-0">
              <Lock className="w-3.5 h-3.5 text-amber-400" />
              <span>Privacy Mode Active</span>
            </span>
          )}

          <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 px-3.5 py-2 rounded-xl text-emerald-400 text-xs font-semibold shrink-0">
            <ShieldCheck className="w-4 h-4 shrink-0" />
            <span>Amazon Policy Compliant (Seller of Record)</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Inputs Column */}
        <div className="lg:col-span-6 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h3 className="text-base font-bold font-display text-white flex items-center space-x-2">
            <Calculator className="w-4.5 h-4.5 text-sky-400" />
            <span>Product Unit Economics Inputs</span>
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Category</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-medium text-white focus:outline-none focus:border-sky-500"
              >
                <option value="Consumer Electronics">Consumer Electronics</option>
                <option value="Home & Kitchen">Home & Kitchen</option>
                <option value="Apparel & Fashion">Apparel & Fashion</option>
                <option value="Beauty & Personal Care">Beauty & Personal Care</option>
                <option value="Sports & Fitness">Sports & Fitness</option>
                <option value="Toys & Games">Toys & Games</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Fulfillment Mode</label>
              <select
                value={formData.fulfillment_type}
                onChange={(e) => setFormData({ ...formData, fulfillment_type: e.target.value })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-medium text-white focus:outline-none focus:border-sky-500"
              >
                <option value="Amazon FBA">Amazon FBA</option>
                <option value="Merchant FBM / Dropship">Merchant FBM / Dropship</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Retail Selling Price ({sym})</label>
              <input
                type="number"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Supplier Cost Price ({sym})</label>
              <input
                type="number"
                value={formData.cost}
                onChange={(e) => setFormData({ ...formData, cost: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          {/* Dropshipping Lead Time & SLA Parameters */}
          {formData.fulfillment_type.includes('Dropship') && (
            <div className="p-4 bg-slate-800/60 border border-slate-700/80 rounded-xl space-y-3">
              <div className="flex items-center justify-between text-xs font-bold text-sky-400">
                <span className="flex items-center space-x-1.5"><Clock className="w-3.5 h-3.5" /> Supplier Handling SLA</span>
                <span>{formData.supplier_lead_days} Days</span>
              </div>
              <input
                type="range" min="1" max="7" step="1"
                value={formData.supplier_lead_days}
                onChange={(e) => setFormData({ ...formData, supplier_lead_days: parseInt(e.target.value) })}
                className="w-full accent-sky-500 cursor-pointer"
              />
              <div className="flex items-center justify-between text-[11px]">
                <span className="text-slate-400">Amazon Late Shipment Rate (LSR):</span>
                {formData.supplier_lead_days <= 2 ? (
                  <span className="text-emerald-400 font-bold">2-Day Handling SLA OK ✅</span>
                ) : (
                  <span className="text-amber-400 font-bold">Handling SLA Warning (&gt;2 Days) ⚠️</span>
                )}
              </div>
            </div>
          )}

          <div className="space-y-4 pt-2 border-t border-slate-800">
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
                <span>Customer Rating ⭐</span>
                <span className="text-sky-400">{formData.rating} / 5.0</span>
              </div>
              <input
                type="range" min="1.0" max="5.0" step="0.1"
                value={formData.rating}
                onChange={(e) => setFormData({ ...formData, rating: parseFloat(e.target.value) })}
                className="w-full accent-sky-500 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
                <span>Competition Level</span>
                <span className="text-sky-400">{formData.competition} / 5</span>
              </div>
              <input
                type="range" min="1" max="5" step="1"
                value={formData.competition}
                onChange={(e) => setFormData({ ...formData, competition: parseInt(e.target.value) })}
                className="w-full accent-sky-500 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
                <span>Target ACOS / Ads Spend %</span>
                <span className="text-sky-400">{intPercent(formData.ads_spend_pct)}%</span>
              </div>
              <input
                type="range" min="0.0" max="0.5" step="0.01"
                value={formData.ads_spend_pct}
                onChange={(e) => setFormData({ ...formData, ads_spend_pct: parseFloat(e.target.value) })}
                className="w-full accent-sky-500 cursor-pointer"
              />
            </div>
          </div>

        </div>

        {/* Prediction Results Column */}
        <div className="lg:col-span-6 space-y-6">
          
          <div className="grid grid-cols-2 gap-4">
            
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 glow-green">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Profit / Unit</span>
              <div className="text-2xl font-extrabold font-display text-white mt-1">
                {sym}{result?.net_unit_profit ?? '--'}
              </div>
              <div className="text-xs font-semibold text-emerald-400 mt-1">
                {result?.margin_pct ?? '--'}% margin
              </div>
            </div>

            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 glow-blue">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">AI Est. Monthly Sales</span>
              <div className="text-2xl font-extrabold font-display text-sky-400 mt-1">
                {result?.predicted_monthly_sales ?? '--'} units
              </div>
              <div className="text-xs font-semibold text-slate-400 mt-1">
                Est. Monthly Volume
              </div>
            </div>

            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {privacyMode ? "Estimated Sourcing ROI" : "Est. Monthly Profit"}
              </span>
              <div className="text-2xl font-extrabold font-display text-emerald-400 mt-1">
                {privacyMode ? `${roiPct}% ROI` : `${sym}${result?.estimated_monthly_profit ?? '--'}`}
              </div>
              <div className="text-xs font-semibold text-emerald-400 mt-1">
                {privacyMode ? "Return on Capital" : "EBITDA Contribution"}
              </div>
            </div>

            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Winner Probability</span>
              <div className={`text-2xl font-extrabold font-display mt-1 ${result?.is_winner ? 'text-emerald-400' : 'text-rose-400'}`}>
                {result?.winner_probability ?? '--'}%
              </div>
              <div className="text-xs font-bold mt-1 flex items-center space-x-1">
                {result?.is_winner ? (
                  <span className="text-emerald-400 flex items-center"><CheckCircle className="w-3.5 h-3.5 mr-1" /> WINNER 🏆</span>
                ) : (
                  <span className="text-rose-400 flex items-center"><AlertTriangle className="w-3.5 h-3.5 mr-1" /> RISKY ⚠️</span>
                )}
              </div>
            </div>

          </div>

          {/* Cost Breakdown Chart */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
            <h4 className="text-sm font-bold font-display text-white mb-4">Per-Unit Financial Breakdown</h4>
            <div className="h-52 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData} cx="50%" cy="50%" innerRadius={45} outerRadius={70} paddingAngle={4} dataKey="value">
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COST_COLORS[index % COST_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}

function intPercent(val) {
  return Math.round((val || 0) * 100);
}
