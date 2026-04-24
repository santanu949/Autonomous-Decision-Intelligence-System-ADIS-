import React, { useState } from 'react';
import { HelpCircle, BookOpen, MessageCircle, FileQuestion, ChevronDown, ChevronUp, Code, Database, BrainCircuit, Zap, BarChart3, GitBranch } from 'lucide-react';

const faqs = [
  { q: 'What data formats does ADIS support?', a: 'ADIS accepts JSON arrays of objects. Each object represents a data record. Numeric, categorical, and temporal fields are automatically classified. CSV support is planned.' },
  { q: 'How are confidence scores calculated?', a: 'Confidence scores (0-100%) are computed from multiple signals: statistical significance, sample size, trend consistency, and ML model accuracy. Higher scores mean more data supports the decision.' },
  { q: 'What anomaly detection methods are used?', a: 'Three methods run in parallel: Z-score (standard deviation), IQR fences (interquartile range), and Modified Z-score (MAD-based, robust to outliers). Anomalies confirmed by multiple methods get higher severity.' },
  { q: 'Can I do what-if analysis?', a: 'Yes! Use the Scenario Simulator on the Dashboard. Adjust variable multipliers and the entire pipeline re-runs with modified data, showing how decisions change.' },
  { q: 'How does the ML pipeline work?', a: 'ADIS runs linear regression for forecasting and K-Means clustering for segmentation. Models are trained on your data in real-time with R² and silhouette scores for quality assessment.' },
  { q: 'Is my data stored anywhere?', a: 'Data is processed in-memory by default. MongoDB integration is available for persistent storage and audit trails. No data is sent to external services.' },
];

const architectureDocs = [
  { icon: Database, title: 'Ingestion Engine', desc: 'Adaptive parser with auto type inference, normalization, and quality scoring' },
  { icon: BarChart3, title: 'Statistical Engine', desc: 'Mean, median, std dev, quartiles, skewness, kurtosis for every numeric variable' },
  { icon: Zap, title: 'Anomaly Detector', desc: 'Multi-method detection: Z-score, IQR fences, Modified Z-score (MAD)' },
  { icon: GitBranch, title: 'Correlation Analyzer', desc: 'Pearson correlation with significance testing across all variable pairs' },
  { icon: BrainCircuit, title: 'Decision Synthesizer', desc: '5-signal aggregation: business heuristics, anomalies, trends, correlations, ML' },
  { icon: Code, title: 'Explainability Engine', desc: 'Dual-level: executive summary + technical detail with factor breakdowns' },
];

const Help = () => {
  const [openFaq, setOpenFaq] = useState(null);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold text-slate-800 tracking-tight mb-1">Help & Documentation</h1>
      <p className="text-slate-500 text-sm mb-8">Learn how the Autonomous Decision Intelligence System works.</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        {[
          { icon: BookOpen, title: 'Architecture', desc: 'Modular pipeline with 8 processing stages', color: 'text-indigo-500' },
          { icon: FileQuestion, title: 'FAQ', desc: 'Common questions about ADIS capabilities', color: 'text-emerald-500' },
          { icon: MessageCircle, title: 'Support', desc: 'Contact the engineering team', color: 'text-amber-500' },
        ].map((c, i) => (
          <div key={i} className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 text-center hover:shadow-md hover:border-indigo-200 transition-all cursor-pointer">
            <c.icon size={28} className={`mx-auto ${c.color} mb-3`} />
            <h3 className="font-bold text-slate-800 text-sm mb-1">{c.title}</h3>
            <p className="text-xs text-slate-500">{c.desc}</p>
          </div>
        ))}
      </div>

      {/* Architecture */}
      <div className="mb-10">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Pipeline Architecture</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {architectureDocs.map((doc, i) => (
            <div key={i} className="bg-white rounded-xl border border-slate-200 p-4 flex items-start gap-3 hover:shadow-sm transition-shadow">
              <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600"><doc.icon size={18} /></div>
              <div><h4 className="text-sm font-semibold text-slate-800">{doc.title}</h4><p className="text-xs text-slate-500 mt-0.5">{doc.desc}</p></div>
            </div>
          ))}
        </div>
      </div>

      {/* FAQ */}
      <div>
        <h2 className="text-lg font-bold text-slate-800 mb-4">Frequently Asked Questions</h2>
        <div className="space-y-2">
          {faqs.map((faq, i) => (
            <div key={i} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <button onClick={() => setOpenFaq(openFaq === i ? null : i)} className="w-full flex items-center justify-between px-5 py-4 text-left">
                <span className="text-sm font-medium text-slate-800">{faq.q}</span>
                {openFaq === i ? <ChevronUp size={16} className="text-slate-400" /> : <ChevronDown size={16} className="text-slate-400" />}
              </button>
              {openFaq === i && <div className="px-5 pb-4 text-sm text-slate-600 border-t border-slate-100 pt-3">{faq.a}</div>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Help;
