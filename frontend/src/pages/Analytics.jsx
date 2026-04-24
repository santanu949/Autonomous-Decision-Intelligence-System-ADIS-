import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import { TrendingUp, Activity, Target, Zap, AlertTriangle, GitBranch, BarChart3, Brain } from 'lucide-react';
import { analyzeData } from '../services/api';

const SAMPLE_TIMESERIES = [
  { period: 'W1', revenue: 12000, cost: 8400, profit: 3600, customers: 240 },
  { period: 'W2', revenue: 14200, cost: 8900, profit: 5300, customers: 280 },
  { period: 'W3', revenue: 13100, cost: 9200, profit: 3900, customers: 260 },
  { period: 'W4', revenue: 16800, cost: 9100, profit: 7700, customers: 340 },
  { period: 'W5', revenue: 18500, cost: 9500, profit: 9000, customers: 380 },
  { period: 'W6', revenue: 17200, cost: 10200, profit: 7000, customers: 350 },
  { period: 'W7', revenue: 21000, cost: 10800, profit: 10200, customers: 420 },
  { period: 'W8', revenue: 23400, cost: 11200, profit: 12200, customers: 460 },
];

const Analytics = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const runDeepAnalysis = async () => {
    setLoading(true);
    try {
      const res = await analyzeData(SAMPLE_TIMESERIES);
      setResults(res.data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const statCards = results ? [
    { label: 'Decisions Generated', val: results.decisions?.length || 0, icon: Target, color: 'text-indigo-600', bg: 'bg-indigo-50' },
    { label: 'Insights Discovered', val: results.insights?.length || 0, icon: Brain, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: 'Anomalies Detected', val: results.anomalies?.length || 0, icon: AlertTriangle, color: 'text-amber-600', bg: 'bg-amber-50' },
    { label: 'Processing Time', val: `${results.total_processing_ms?.toFixed(0)}ms`, icon: Zap, color: 'text-rose-600', bg: 'bg-rose-50' },
  ] : [
    { label: 'Model Accuracy', val: '—', icon: Target, color: 'text-indigo-600', bg: 'bg-indigo-50' },
    { label: 'Predictions', val: '—', icon: Activity, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: 'Processing Time', val: '—', icon: Zap, color: 'text-amber-600', bg: 'bg-amber-50' },
    { label: 'Impact Score', val: '—', icon: TrendingUp, color: 'text-rose-600', bg: 'bg-rose-50' },
  ];

  // Build correlation heatmap data
  const corrData = results?.correlations?.map(c => ({
    pair: `${c.var_a} ↔ ${c.var_b}`,
    value: Math.abs(c.coefficient),
    coefficient: c.coefficient,
    strength: c.strength,
  })) || [];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Deep Analytics</h1>
          <p className="text-slate-500 text-sm mt-1">Statistical profiling, correlations, and ML model insights.</p>
        </div>
        <button onClick={runDeepAnalysis} disabled={loading}
          className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white font-semibold py-2.5 px-5 rounded-xl shadow-lg hover:shadow-indigo-500/25 transition-all text-sm flex items-center gap-2 disabled:opacity-50">
          {loading ? <Activity className="animate-spin" size={16} /> : <><BarChart3 size={16} />Run Deep Analysis</>}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {statCards.map((s, i) => (
          <div key={i} className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex items-center hover:shadow-md transition-shadow">
            <div className={`p-3 rounded-xl ${s.bg} ${s.color} mr-4`}><s.icon size={22} /></div>
            <div>
              <p className="text-xs font-medium text-slate-500">{s.label}</p>
              <h3 className="text-xl font-bold text-slate-800">{s.val}</h3>
            </div>
          </div>
        ))}
      </div>

      {/* Time Series Chart */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-6">
        <h3 className="text-sm font-bold text-slate-700 mb-4">Multi-Variable Trend Analysis</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={SAMPLE_TIMESERIES} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="gRev" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} /><stop offset="95%" stopColor="#6366f1" stopOpacity={0} /></linearGradient>
                <linearGradient id="gProfit" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#10b981" stopOpacity={0.3} /><stop offset="95%" stopColor="#10b981" stopOpacity={0} /></linearGradient>
              </defs>
              <XAxis dataKey="period" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
              <Area type="monotone" dataKey="revenue" stroke="#6366f1" fill="url(#gRev)" strokeWidth={2} />
              <Area type="monotone" dataKey="profit" stroke="#10b981" fill="url(#gProfit)" strokeWidth={2} />
              <Area type="monotone" dataKey="cost" stroke="#f59e0b" fill="transparent" strokeWidth={2} strokeDasharray="5 5" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Correlations + ML Results */}
      {results && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Correlation Matrix */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h3 className="text-sm font-bold text-slate-700 mb-4 flex items-center gap-2"><GitBranch size={16} className="text-purple-500" />Correlation Analysis</h3>
            {corrData.length > 0 ? (
              <div className="space-y-2">
                {corrData.map((c, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <span className="text-xs text-slate-600 min-w-[140px] truncate">{c.pair}</span>
                    <div className="flex-1 bg-slate-100 rounded-full h-3 overflow-hidden">
                      <div className={`h-3 rounded-full ${c.coefficient > 0 ? 'bg-emerald-400' : 'bg-red-400'}`} style={{ width: `${c.value * 100}%` }} />
                    </div>
                    <span className={`text-xs font-mono font-bold min-w-[50px] text-right ${c.coefficient > 0 ? 'text-emerald-600' : 'text-red-600'}`}>{c.coefficient?.toFixed(3)}</span>
                  </div>
                ))}
              </div>
            ) : <p className="text-sm text-slate-400">Run analysis to see correlations</p>}
          </div>

          {/* ML Forecasts */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h3 className="text-sm font-bold text-slate-700 mb-4 flex items-center gap-2"><Brain size={16} className="text-indigo-500" />ML Model Results</h3>
            {results.ml_results?.length > 0 ? (
              <div className="space-y-3">
                {results.ml_results.map((ml, i) => (
                  <div key={i} className="bg-slate-50 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-semibold text-slate-700 capitalize">{ml.model_type}: {ml.target_variable}</span>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700">{ml.accuracy_metric}: {ml.accuracy_value?.toFixed(3)}</span>
                    </div>
                    {ml.forecasts?.map((f, j) => (
                      <div key={j} className="flex items-center justify-between text-xs text-slate-600 py-1 border-t border-slate-200">
                        <span>{f.period}</span>
                        <span className="font-mono">{f.predicted_value?.toFixed(1)} <span className="text-slate-400">({f.lower_bound?.toFixed(0)}–{f.upper_bound?.toFixed(0)})</span></span>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            ) : <p className="text-sm text-slate-400">Run analysis to see ML results</p>}
          </div>
        </div>
      )}
    </div>
  );
};

export default Analytics;
