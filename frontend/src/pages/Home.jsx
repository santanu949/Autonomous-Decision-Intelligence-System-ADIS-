import React, { useState, useEffect } from 'react';
import { analyzeData, sendChatMessage } from '../services/api';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid } from 'recharts';
import { Activity, AlertTriangle, BarChart3, BrainCircuit, CheckCircle2, ChevronRight, Database, Sparkles, MessageSquare, Sliders, TrendingUp, TrendingDown, Shield, Zap, Target, ArrowUpRight, ArrowDownRight, Info, ChevronDown, ChevronUp } from 'lucide-react';

const EXAMPLES = {
  business: [
    {"month":"Jan","sales":4000,"expenses":2400},
    {"month":"Feb","sales":3000,"expenses":1398},
    {"month":"Mar","sales":2000,"expenses":9800},
    {"month":"Apr","sales":2780,"expenses":3908},
    {"month":"May","sales":1890,"expenses":4800},
    {"month":"Jun","sales":2390,"expenses":3800}
  ],
  healthcare: [
    {"day":"Mon","patients":120,"wait_time":18,"staff":8},
    {"day":"Tue","patients":185,"wait_time":42,"staff":8},
    {"day":"Wed","patients":140,"wait_time":22,"staff":10},
    {"day":"Thu","patients":160,"wait_time":30,"staff":9},
    {"day":"Fri","patients":130,"wait_time":20,"staff":10}
  ],
  supply: [
    {"sku":"A100","inventory":450,"demand":45,"lead_time":14},
    {"sku":"B200","inventory":120,"demand":60,"lead_time":7},
    {"sku":"C300","inventory":800,"demand":20,"lead_time":21},
    {"sku":"D400","inventory":50,"demand":80,"lead_time":10}
  ]
};

const ConfidenceGauge = ({ value, size = 64 }) => {
  const r = (size - 8) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  const color = value >= 80 ? '#10b981' : value >= 60 ? '#f59e0b' : '#ef4444';
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="currentColor" className="text-slate-200" strokeWidth="4" />
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth="4"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1s ease' }} />
      </svg>
      <span className="absolute text-xs font-bold" style={{ color }}>{Math.round(value)}%</span>
    </div>
  );
};

const RiskBadge = ({ level }) => {
  const styles = {
    severe: 'bg-red-100 text-red-700 border-red-200',
    high: 'bg-orange-100 text-orange-700 border-orange-200',
    moderate: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    low: 'bg-green-100 text-green-700 border-green-200',
    minimal: 'bg-slate-100 text-slate-600 border-slate-200'
  };
  return <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${styles[level] || styles.moderate}`}>{level?.toUpperCase()}</span>;
};

const DecisionCard = ({ decision, idx }) => {
  const [expanded, setExpanded] = useState(false);
  const iconMap = { growth: TrendingUp, cost: TrendingDown, risk: Shield, operational: Zap, strategic: Target };
  const Icon = iconMap[decision.category] || BrainCircuit;
  const borderColors = { 1: 'border-l-indigo-500', 2: 'border-l-emerald-500', 3: 'border-l-amber-500' };

  return (
    <div className={`border-l-4 ${borderColors[decision.rank] || 'border-l-slate-400'} rounded-r-xl bg-white shadow-sm hover:shadow-md transition-all p-5`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600 mt-0.5"><Icon size={18} /></div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className="text-[10px] font-bold text-indigo-500 bg-indigo-50 px-2 py-0.5 rounded-full">#{decision.rank}</span>
              <h3 className="font-bold text-slate-800 text-sm">{decision.action}</h3>
            </div>
            <p className="text-xs text-slate-500 mb-2">{decision.executive_summary || decision.explanation}</p>
            <div className="flex items-center gap-3 flex-wrap">
              <ConfidenceGauge value={decision.confidence} size={40} />
              <RiskBadge level={decision.risk_level} />
              {decision.expected_impact && <span className="text-[10px] text-slate-400">{decision.expected_impact.slice(0, 80)}</span>}
            </div>
          </div>
        </div>
      </div>
      {decision.contributing_factors?.length > 0 && (
        <div className="mt-3 pt-3 border-t border-slate-100">
          <button onClick={() => setExpanded(!expanded)} className="flex items-center gap-1 text-xs font-medium text-indigo-500 hover:text-indigo-700">
            {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            {expanded ? 'Hide' : 'Show'} Factor Breakdown ({decision.contributing_factors.length})
          </button>
          {expanded && (
            <div className="mt-2 space-y-1.5 animate-in fade-in">
              {decision.contributing_factors.map((f, i) => (
                <div key={i} className="flex items-center gap-2 text-xs">
                  <span className={`w-1.5 h-1.5 rounded-full ${f.direction === 'positive' ? 'bg-emerald-500' : f.direction === 'negative' ? 'bg-red-500' : 'bg-slate-400'}`} />
                  <span className="font-medium text-slate-700 min-w-[80px]">{f.factor}</span>
                  <div className="flex-1 bg-slate-100 rounded-full h-1.5">
                    <div className={`h-1.5 rounded-full ${f.direction === 'positive' ? 'bg-emerald-400' : f.direction === 'negative' ? 'bg-red-400' : 'bg-slate-400'}`}
                      style={{ width: `${Math.min(100, f.contribution_pct)}%` }} />
                  </div>
                  <span className="text-slate-500 min-w-[35px] text-right">{f.contribution_pct?.toFixed(0)}%</span>
                </div>
              ))}
              {decision.reasoning_chain?.length > 0 && (
                <div className="mt-2 p-2 bg-slate-50 rounded-lg">
                  <p className="text-[10px] font-semibold text-slate-500 mb-1">REASONING CHAIN</p>
                  {decision.reasoning_chain.map((s, i) => (
                    <p key={i} className="text-[11px] text-slate-600">→ {s}</p>
                  ))}
                </div>
              )}
              {decision.alternatives?.length > 0 && (
                <p className="text-[10px] text-slate-400 mt-1">Alternatives: {decision.alternatives.join(' · ')}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const Home = () => {
  const [inputData, setInputData] = useState(JSON.stringify(EXAMPLES.business, null, 2));
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('decisions');
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { role: 'ai', text: 'Hello! I analyze your data and provide actionable insights. Run an analysis first, then ask me anything.' }
  ]);
  const [chatLoading, setChatLoading] = useState(false);
  const [selectedExample, setSelectedExample] = useState('business');

  const handleAnalyze = async () => {
    try {
      setLoading(true);
      setError('');
      const parsed = JSON.parse(inputData);
      const res = await analyzeData(parsed);
      setResults(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    const userMsg = chatInput;
    setChatHistory(h => [...h, { role: 'user', text: userMsg }]);
    setChatInput('');
    setChatLoading(true);
    try {
      const res = await sendChatMessage(userMsg);
      setChatHistory(h => [...h, { role: 'ai', text: res.data.response }]);
    } catch {
      setChatHistory(h => [...h, { role: 'ai', text: 'Sorry, I encountered an error.' }]);
    }
    setChatLoading(false);
  };

  const loadExample = (key) => {
    setSelectedExample(key);
    setInputData(JSON.stringify(EXAMPLES[key], null, 2));
  };

  return (
    <div className="w-full font-sans">
      <main className="max-w-screen-2xl mx-auto py-4 grid grid-cols-1 xl:grid-cols-12 gap-6">

        {/* Left: Data Input */}
        <div className="xl:col-span-3 space-y-5">
          <div className="rounded-2xl border border-slate-200 bg-white/80 backdrop-blur shadow-sm overflow-hidden">
            <div className="px-5 py-3 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white flex items-center">
              <Database size={16} className="text-indigo-500 mr-2" /><h2 className="font-semibold text-sm">Data Ingestion</h2>
            </div>
            <div className="p-4">
              <div className="flex gap-1.5 mb-3">
                {Object.keys(EXAMPLES).map(k => (
                  <button key={k} onClick={() => loadExample(k)}
                    className={`text-[10px] font-semibold px-2.5 py-1 rounded-full transition-all ${selectedExample === k ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}>
                    {k.charAt(0).toUpperCase() + k.slice(1)}
                  </button>
                ))}
              </div>
              <textarea value={inputData} onChange={e => setInputData(e.target.value)}
                className="w-full h-48 p-3 font-mono text-[11px] rounded-xl bg-slate-50 border border-slate-200 text-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none resize-none"
                placeholder="Paste JSON data..." />
              {error && <p className="text-xs text-red-500 mt-2 flex items-center gap-1"><AlertTriangle size={12} />{error}</p>}
              <button onClick={handleAnalyze} disabled={loading}
                className="mt-3 w-full bg-gradient-to-r from-indigo-600 to-indigo-700 text-white font-semibold py-2.5 px-4 rounded-xl flex items-center justify-center shadow-lg hover:shadow-indigo-500/25 transition-all text-sm disabled:opacity-50">
                {loading ? <Activity className="animate-spin" size={16} /> : <><Zap size={14} className="mr-1.5" />Run Analysis</>}
              </button>
            </div>
          </div>

          {/* Pipeline Performance */}
          {results && (
            <div className="rounded-2xl border border-slate-200 bg-white/80 backdrop-blur shadow-sm p-4">
              <h3 className="text-xs font-semibold text-slate-500 mb-3 flex items-center gap-1.5"><Activity size={14} className="text-emerald-500" />PIPELINE METRICS</h3>
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-slate-50 rounded-lg p-2.5 text-center">
                  <p className="text-lg font-bold text-indigo-600">{results.total_processing_ms?.toFixed(0)}ms</p>
                  <p className="text-[10px] text-slate-500">Total Time</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-2.5 text-center">
                  <p className="text-lg font-bold text-emerald-600">{results.data_profile?.quality_score?.toFixed(0)}/100</p>
                  <p className="text-[10px] text-slate-500">Data Quality</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-2.5 text-center">
                  <p className="text-lg font-bold text-amber-600">{results.anomalies?.length || 0}</p>
                  <p className="text-[10px] text-slate-500">Anomalies</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-2.5 text-center">
                  <p className="text-lg font-bold text-purple-600">{results.correlations?.length || 0}</p>
                  <p className="text-[10px] text-slate-500">Correlations</p>
                </div>
              </div>
              {results.pipeline_stages && (
                <div className="mt-3 space-y-1">
                  {Object.entries(results.pipeline_stages).map(([k, v]) => (
                    <div key={k} className="flex items-center gap-2 text-[10px]">
                      <span className="text-slate-500 min-w-[80px]">{k}</span>
                      <div className="flex-1 bg-slate-100 rounded-full h-1"><div className="bg-indigo-400 h-1 rounded-full" style={{ width: `${Math.min(100, (v / results.total_processing_ms) * 100)}%` }} /></div>
                      <span className="text-slate-400">{v?.toFixed(1)}ms</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Center: Results */}
        <div className="xl:col-span-6 space-y-5">
          {!results ? (
            <div className="rounded-2xl border-2 border-dashed border-slate-300 bg-white/50 flex flex-col items-center justify-center p-16 text-center min-h-[500px]">
              <BrainCircuit size={56} className="text-indigo-300 mb-6" />
              <h3 className="text-xl font-bold text-slate-600 mb-2">Decision Engine Ready</h3>
              <p className="text-slate-400 text-sm max-w-sm">Select a dataset example or paste your own JSON data, then run the analysis to generate AI-driven decisions.</p>
            </div>
          ) : (
            <>
              {/* Tab Navigation */}
              <div className="flex gap-1 bg-slate-100 p-1 rounded-xl">
                {[
                  { id: 'decisions', label: 'Decisions', icon: CheckCircle2, count: results.decisions?.length },
                  { id: 'insights', label: 'Insights', icon: Sparkles, count: results.insights?.length },
                  { id: 'viz', label: 'Charts', icon: BarChart3 },
                  { id: 'audit', label: 'Audit', icon: Shield, count: results.audit_trail?.length }
                ].map(tab => (
                  <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-semibold transition-all ${activeTab === tab.id ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>
                    <tab.icon size={14} />{tab.label}
                    {tab.count != null && <span className="bg-indigo-100 text-indigo-600 text-[10px] px-1.5 rounded-full">{tab.count}</span>}
                  </button>
                ))}
              </div>

              {/* Decisions Tab */}
              {activeTab === 'decisions' && (
                <div className="space-y-3">
                  {results.decisions?.map((d, i) => <DecisionCard key={i} decision={d} idx={i} />)}
                </div>
              )}

              {/* Insights Tab */}
              {activeTab === 'insights' && (
                <div className="space-y-2">
                  {results.insights?.map((ins, i) => (
                    <div key={i} className={`rounded-xl p-4 border-l-4 bg-white shadow-sm ${ins.severity === 'critical' ? 'border-l-red-500' : ins.severity === 'warning' ? 'border-l-amber-500' : 'border-l-blue-400'}`}>
                      <div className="flex items-start gap-2">
                        <Sparkles size={14} className={ins.severity === 'critical' ? 'text-red-500' : ins.severity === 'warning' ? 'text-amber-500' : 'text-blue-500'} />
                        <div>
                          <h4 className="text-sm font-semibold text-slate-800">{ins.title}</h4>
                          <p className="text-xs text-slate-500 mt-0.5">{ins.description}</p>
                          <div className="flex gap-2 mt-2">
                            <span className="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">{ins.category}</span>
                            <span className="text-[10px] bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full">{ins.confidence?.toFixed(0)}% confidence</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Charts Tab */}
              {activeTab === 'viz' && (
                <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                  <h3 className="text-sm font-bold text-slate-700 mb-4">Data Visualization</h3>
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={results.chart_data}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis dataKey={Object.keys(results.chart_data?.[0] || {}).find(k => typeof results.chart_data[0][k] === 'string') || 'index'} axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
                        <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }} />
                        {Object.keys(results.chart_data?.[0] || {}).filter(k => typeof results.chart_data[0][k] === 'number').slice(0, 3).map((k, i) => (
                          <Bar key={k} dataKey={k} fill={['#6366f1', '#10b981', '#f59e0b'][i]} radius={[6, 6, 0, 0]} />
                        ))}
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  {/* Variable profiles */}
                  {results.variable_profiles && (
                    <div className="mt-4 grid grid-cols-2 gap-2">
                      {Object.entries(results.variable_profiles).filter(([_, v]) => v.var_type === 'numeric').map(([k, v]) => (
                        <div key={k} className="bg-slate-50 rounded-lg p-3">
                          <p className="text-xs font-semibold text-slate-700 mb-1">{k}</p>
                          <div className="grid grid-cols-3 gap-1 text-[10px] text-slate-500">
                            <span>μ {v.mean?.toFixed(1)}</span>
                            <span>σ {v.std_dev?.toFixed(1)}</span>
                            <span className={v.trend_direction === 'increasing' ? 'text-emerald-600' : v.trend_direction === 'decreasing' ? 'text-red-500' : ''}>
                              {v.trend_direction === 'increasing' ? '↑' : v.trend_direction === 'decreasing' ? '↓' : '→'} {v.trend_pct_change?.toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Audit Tab */}
              {activeTab === 'audit' && (
                <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                  <div className="px-5 py-3 border-b border-slate-100 bg-slate-50">
                    <h3 className="text-xs font-semibold text-slate-500">FULL AUDIT TRAIL</h3>
                  </div>
                  <div className="divide-y divide-slate-100">
                    {results.audit_trail?.map((entry, i) => (
                      <div key={i} className="px-5 py-3 flex items-center gap-3 text-xs">
                        <span className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-[10px] font-bold">{i + 1}</span>
                        <div className="flex-1">
                          <span className="font-semibold text-slate-700">{entry.action}</span>
                          <span className="text-slate-400 ml-2">[{entry.stage}]</span>
                        </div>
                        <span className="text-slate-400">{entry.duration_ms?.toFixed(1)}ms</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Right: Chat */}
        <div className="xl:col-span-3">
          <div className="rounded-2xl border border-slate-200 bg-white/80 backdrop-blur shadow-sm flex flex-col h-[calc(100vh-12rem)]">
            <div className="px-5 py-3 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white flex items-center">
              <MessageSquare size={16} className="text-purple-500 mr-2" /><h2 className="font-semibold text-sm">ADIS Assistant</h2>
            </div>
            <div className="flex-1 p-3 overflow-y-auto space-y-3">
              {chatHistory.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[90%] rounded-2xl p-3 text-xs leading-relaxed ${msg.role === 'user' ? 'bg-indigo-600 text-white rounded-br-sm' : 'bg-slate-100 text-slate-700 rounded-bl-sm'}`}>
                    {msg.text.split('\n').map((line, j) => <p key={j} className={j > 0 ? 'mt-1' : ''}>{line}</p>)}
                  </div>
                </div>
              ))}
              {chatLoading && <div className="flex justify-start"><div className="bg-slate-100 rounded-2xl p-3 text-xs text-slate-400 animate-pulse">Thinking...</div></div>}
            </div>
            <div className="p-3 border-t border-slate-200">
              <form onSubmit={handleChat} className="flex gap-1.5">
                <input type="text" value={chatInput} onChange={e => setChatInput(e.target.value)}
                  placeholder="Ask about your data..." className="flex-1 rounded-xl px-3 py-2 text-xs bg-slate-50 border border-slate-200 outline-none focus:ring-2 focus:ring-indigo-300" />
                <button type="submit" className="bg-purple-600 hover:bg-purple-700 text-white px-3 rounded-xl transition-colors"><ChevronRight size={14} /></button>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
