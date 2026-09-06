import React, { useState, useEffect } from 'react';
import { Ship, Plane, DollarSign, Shield, FileText, ArrowRight } from 'lucide-react';

export default function CrossBorderLogistics({ selectedRegion }) {
  const [formData, setFormData] = useState({
    sourcing_cost_usd: 8.50,
    weight_kg: 0.75,
    length_cm: 25.0,
    width_cm: 15.0,
    height_cm: 10.0,
    shipping_mode: 'sea',
    dest_region: selectedRegion || 'US'
  });

  const [result, setResult] = useState(null);

  useEffect(() => {
    setFormData(prev => ({ ...prev, dest_region: selectedRegion }));
  }, [selectedRegion]);

  useEffect(() => {
    calculateLandedCost();
  }, [formData]);

  const calculateLandedCost = async () => {
    try {
      const res = await fetch('/api/landed-cost', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error("Landed cost calculation error:", e);
    }
  };

  return (
    <div className="space-y-8 py-6">
      
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <h1 className="text-2xl sm:text-3xl font-extrabold font-display text-white flex items-center space-x-3">
          <Ship className="w-8 h-8 text-sky-400" />
          <span>Cross-Border Logistics & Tariffs</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Calculate sea/air freight fees, cargo insurance (0.5%), and import tariffs for international sourcing.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Input Parameters */}
        <div className="lg:col-span-6 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
          <h3 className="text-lg font-bold font-display text-white border-b border-slate-800 pb-3">
            📦 Shipment & Package Parameters
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Sourcing Price ($ USD)</label>
              <input
                type="number" step="0.5"
                value={formData.sourcing_cost_usd}
                onChange={(e) => setFormData({ ...formData, sourcing_cost_usd: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Package Weight (kg)</label>
              <input
                type="number" step="0.1"
                value={formData.weight_kg}
                onChange={(e) => setFormData({ ...formData, weight_kg: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Length (cm)</label>
              <input
                type="number"
                value={formData.length_cm}
                onChange={(e) => setFormData({ ...formData, length_cm: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Width (cm)</label>
              <input
                type="number"
                value={formData.width_cm}
                onChange={(e) => setFormData({ ...formData, width_cm: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Height (cm)</label>
              <input
                type="number"
                value={formData.height_cm}
                onChange={(e) => setFormData({ ...formData, height_cm: parseFloat(e.target.value) || 0 })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2">Freight Mode</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setFormData({ ...formData, shipping_mode: 'sea' })}
                className={`flex items-center justify-center space-x-2 py-2.5 rounded-xl border text-xs font-bold transition-all ${
                  formData.shipping_mode === 'sea'
                    ? 'bg-sky-600 border-sky-500 text-white shadow-lg shadow-sky-500/20'
                    : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white'
                }`}
              >
                <Ship className="w-4 h-4" />
                <span>Sea Freight (LCL)</span>
              </button>

              <button
                type="button"
                onClick={() => setFormData({ ...formData, shipping_mode: 'air' })}
                className={`flex items-center justify-center space-x-2 py-2.5 rounded-xl border text-xs font-bold transition-all ${
                  formData.shipping_mode === 'air'
                    ? 'bg-sky-600 border-sky-500 text-white shadow-lg shadow-sky-500/20'
                    : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white'
                }`}
              >
                <Plane className="w-4 h-4" />
                <span>Air Express</span>
              </button>
            </div>
          </div>
        </div>

        {/* Output Calculation Table */}
        <div className="lg:col-span-6 space-y-6">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 glow-blue">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Landed Cost per Unit</span>
            <div className="text-4xl font-extrabold font-display text-sky-400 mt-2">
              ${result?.total_landed_usd ?? '--'} USD
            </div>
            <div className="text-sm font-semibold text-purple-400 mt-2">
              Equivalent: {result?.dest_currency_symbol}{result?.landed_cost_dest_currency} ({formData.dest_region})
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
            <h4 className="text-sm font-bold font-display text-white mb-4">Itemized Cost Structure</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="pb-3 font-semibold">Component</th>
                    <th className="pb-3 font-semibold text-right">Cost (USD)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-slate-200">
                  <tr>
                    <td className="py-3 font-medium">Base Sourcing Price</td>
                    <td className="py-3 text-right font-semibold">${result?.sourcing_cost_usd}</td>
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Freight Fee ({formData.shipping_mode.toUpperCase()})</td>
                    <td className="py-3 text-right font-semibold">${result?.freight_cost_usd}</td>
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Cargo Insurance (0.5%)</td>
                    <td className="py-3 text-right font-semibold">${result?.insurance_usd}</td>
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Import Customs Duty (6%)</td>
                    <td className="py-3 text-right font-semibold">${result?.customs_duty_usd}</td>
                  </tr>
                  <tr className="text-sky-400 font-bold">
                    <td className="py-3">Total Unit Landed Cost</td>
                    <td className="py-3 text-right">${result?.total_landed_usd}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}
