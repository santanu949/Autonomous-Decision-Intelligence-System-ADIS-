import React, { useState } from 'react';
import { FileText, Download, Calendar, CheckCircle, Clock, BarChart3, AlertTriangle, Brain } from 'lucide-react';
import { analyzeData } from '../services/api';

const SAMPLE_DATA = [
  {"quarter":"Q1","revenue":125000,"expenses":89000,"customers":1200,"churn_rate":5.2},
  {"quarter":"Q2","revenue":138000,"expenses":92000,"customers":1380,"churn_rate":4.8},
  {"quarter":"Q3","revenue":115000,"expenses":98000,"customers":1150,"churn_rate":7.1},
  {"quarter":"Q4","revenue":152000,"expenses":95000,"customers":1520,"churn_rate":3.9},
];

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [generating, setGenerating] = useState(false);

  const generateReport = async () => {
    setGenerating(true);
    try {
      const res = await analyzeData(SAMPLE_DATA);
      const data = res.data;
      const report = {
        id: Date.now(),
        name: `ADIS Analysis Report #${reports.length + 1}`,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        decisions: data.decisions?.length || 0,
        insights: data.insights?.length || 0,
        anomalies: data.anomalies?.length || 0,
        confidence: data.decisions?.[0]?.confidence || 0,
        processingTime: data.total_processing_ms,
        data: data,
      };
      setReports([report, ...reports]);
    } catch (e) {
      console.error(e);
    }
    setGenerating(false);
  };

  const exportJSON = (report) => {
    const blob = new Blob([JSON.stringify(report.data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `adis-report-${report.id}.json`; a.click();
    URL.revokeObjectURL(url);
  };

  const exportCSV = (report) => {
    if (!report.data?.chart_data?.length) return;
    const headers = Object.keys(report.data.chart_data[0]).join(',');
    const rows = report.data.chart_data.map(r => Object.values(r).join(','));
    const csv = [headers, ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `adis-data-${report.id}.csv`; a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Reports & Export</h1>
          <p className="text-slate-500 text-sm mt-1">Generate analysis reports and export data in multiple formats.</p>
        </div>
        <button onClick={generateReport} disabled={generating}
          className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white font-semibold py-2.5 px-5 rounded-xl shadow-lg hover:shadow-indigo-500/25 transition-all text-sm flex items-center gap-2 disabled:opacity-50">
          {generating ? <Clock className="animate-spin" size={16} /> : <><FileText size={16} />Generate Report</>}
        </button>
      </div>

      {reports.length === 0 ? (
        <div className="rounded-2xl border-2 border-dashed border-slate-300 bg-white/50 flex flex-col items-center justify-center p-16 text-center">
          <FileText size={48} className="text-slate-300 mb-4" />
          <h3 className="text-lg font-bold text-slate-600 mb-2">No Reports Yet</h3>
          <p className="text-slate-400 text-sm">Click "Generate Report" to create an analysis report from sample data.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {reports.map(r => (
            <div key={r.id} className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-xl bg-indigo-50 text-indigo-600"><FileText size={22} /></div>
                  <div>
                    <h3 className="font-bold text-slate-800">{r.name}</h3>
                    <p className="text-xs text-slate-500 flex items-center gap-1 mt-1"><Calendar size={12} />{r.date} · {r.processingTime?.toFixed(0)}ms</p>
                    <div className="flex gap-3 mt-3">
                      <span className="text-[11px] bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-full font-semibold flex items-center gap-1"><CheckCircle size={12} />{r.decisions} Decisions</span>
                      <span className="text-[11px] bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded-full font-semibold flex items-center gap-1"><Brain size={12} />{r.insights} Insights</span>
                      <span className="text-[11px] bg-amber-50 text-amber-700 px-2.5 py-1 rounded-full font-semibold flex items-center gap-1"><AlertTriangle size={12} />{r.anomalies} Anomalies</span>
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => exportJSON(r)} className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-2 rounded-lg transition-colors flex items-center gap-1"><Download size={14} />JSON</button>
                  <button onClick={() => exportCSV(r)} className="text-xs font-semibold text-emerald-600 hover:text-emerald-800 bg-emerald-50 hover:bg-emerald-100 px-3 py-2 rounded-lg transition-colors flex items-center gap-1"><Download size={14} />CSV</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Reports;
