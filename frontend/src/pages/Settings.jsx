import React, { useState } from 'react';
import { Settings as SettingsIcon, Database, Shield, Zap, Save, Bell, User, Globe, Cpu } from 'lucide-react';

const Settings = () => {
  const [activeSection, setActiveSection] = useState('engine');
  const [config, setConfig] = useState({
    confidenceThreshold: 75, enableML: true, enableClustering: true,
    anomalyZThreshold: 2.0, forecastPeriods: 3, maxDecisions: 5,
    notifyAnomalies: true, notifyDecisions: true, darkMode: false,
  });

  const sections = [
    { id: 'engine', label: 'Engine Parameters', icon: Zap },
    { id: 'data', label: 'Data Sources', icon: Database },
    { id: 'security', label: 'Security & Access', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
  ];

  const Toggle = ({ checked, onChange }) => (
    <button onClick={() => onChange(!checked)} className={`w-10 h-5 rounded-full transition-colors relative ${checked ? 'bg-indigo-600' : 'bg-slate-300'}`}>
      <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5 transition-transform shadow-sm ${checked ? 'translate-x-5' : 'translate-x-0.5'}`} />
    </button>
  );

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold text-slate-800 tracking-tight mb-1">System Configuration</h1>
      <p className="text-slate-500 text-sm mb-8">Manage ADIS engine parameters, data sources, and preferences.</p>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="space-y-1">
          {sections.map(s => (
            <button key={s.id} onClick={() => setActiveSection(s.id)}
              className={`w-full text-left px-4 py-3 rounded-xl font-medium flex items-center text-sm transition-all ${activeSection === s.id ? 'bg-indigo-50 text-indigo-700' : 'text-slate-600 hover:bg-slate-100'}`}>
              <s.icon size={16} className="mr-3" />{s.label}
            </button>
          ))}
        </div>

        <div className="col-span-3 bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
          {activeSection === 'engine' && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-800">Engine Parameters</h2>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Confidence Threshold: {config.confidenceThreshold}%</label>
                <input type="range" className="w-full accent-indigo-600" min="30" max="95" value={config.confidenceThreshold}
                  onChange={e => setConfig({ ...config, confidenceThreshold: +e.target.value })} />
                <div className="flex justify-between text-[10px] text-slate-500 mt-1"><span>More Decisions</span><span>Higher Accuracy</span></div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Anomaly Z-Score Threshold: {config.anomalyZThreshold}</label>
                <input type="range" className="w-full accent-amber-600" min="1" max="4" step="0.5" value={config.anomalyZThreshold}
                  onChange={e => setConfig({ ...config, anomalyZThreshold: +e.target.value })} />
                <div className="flex justify-between text-[10px] text-slate-500 mt-1"><span>More Sensitive</span><span>Less Sensitive</span></div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Forecast Periods: {config.forecastPeriods}</label>
                <input type="range" className="w-full accent-emerald-600" min="1" max="10" value={config.forecastPeriods}
                  onChange={e => setConfig({ ...config, forecastPeriods: +e.target.value })} />
              </div>
              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                <div><p className="text-sm font-medium text-slate-700">Enable ML Models</p><p className="text-xs text-slate-500">Use regression and clustering alongside rules</p></div>
                <Toggle checked={config.enableML} onChange={v => setConfig({ ...config, enableML: v })} />
              </div>
              <div className="flex items-center justify-between">
                <div><p className="text-sm font-medium text-slate-700">Enable Clustering</p><p className="text-xs text-slate-500">K-Means segmentation analysis</p></div>
                <Toggle checked={config.enableClustering} onChange={v => setConfig({ ...config, enableClustering: v })} />
              </div>
              <div className="pt-4">
                <select className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 mb-4">
                  <option>ADIS Core v2.0 (Rules + ML)</option>
                  <option>ADIS Core v1.0 (Rules Only)</option>
                </select>
                <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-6 rounded-lg transition-colors flex items-center gap-2 text-sm">
                  <Save size={16} />Save Configuration
                </button>
              </div>
            </div>
          )}

          {activeSection === 'data' && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-800">Data Sources</h2>
              <div className="space-y-3">
                {['JSON Input (Active)', 'CSV Upload (Active)', 'REST API (Coming Soon)', 'Database Connector (Coming Soon)'].map((src, i) => (
                  <div key={i} className={`flex items-center justify-between p-4 rounded-xl border ${i < 2 ? 'border-emerald-200 bg-emerald-50/50' : 'border-slate-200 bg-slate-50'}`}>
                    <div className="flex items-center gap-3">
                      <Globe size={16} className={i < 2 ? 'text-emerald-600' : 'text-slate-400'} />
                      <span className="text-sm font-medium text-slate-700">{src}</span>
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${i < 2 ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-200 text-slate-500'}`}>{i < 2 ? 'CONNECTED' : 'PLANNED'}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeSection === 'security' && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-800">Security & Access</h2>
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                <p className="text-sm text-amber-800 font-medium">Enterprise Feature</p>
                <p className="text-xs text-amber-600 mt-1">Authentication, role-based access, and SSO are planned for the enterprise release.</p>
              </div>
              <div className="space-y-3">
                {[{ role: 'Admin', desc: 'Full system access', color: 'bg-red-100 text-red-700' },
                  { role: 'Analyst', desc: 'Analysis & reports', color: 'bg-blue-100 text-blue-700' },
                  { role: 'Viewer', desc: 'Read-only access', color: 'bg-green-100 text-green-700' }
                ].map((r, i) => (
                  <div key={i} className="flex items-center justify-between p-4 rounded-xl border border-slate-200">
                    <div className="flex items-center gap-3"><User size={16} className="text-slate-500" /><span className="text-sm font-medium">{r.role}</span><span className="text-xs text-slate-500">{r.desc}</span></div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${r.color}`}>{r.role.toUpperCase()}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeSection === 'notifications' && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-800">Notifications</h2>
              <div className="flex items-center justify-between"><div><p className="text-sm font-medium text-slate-700">Anomaly Alerts</p><p className="text-xs text-slate-500">Get notified when anomalies are detected</p></div>
                <Toggle checked={config.notifyAnomalies} onChange={v => setConfig({ ...config, notifyAnomalies: v })} /></div>
              <div className="flex items-center justify-between"><div><p className="text-sm font-medium text-slate-700">Decision Updates</p><p className="text-xs text-slate-500">Notifications for new critical decisions</p></div>
                <Toggle checked={config.notifyDecisions} onChange={v => setConfig({ ...config, notifyDecisions: v })} /></div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;
