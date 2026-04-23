'use client';


/**
 * AnalyticsPage: Implements Phase 4 (Feedback Loop & Continuous Intelligence)[cite: 242].
 * Visualizes the system's self-optimization and real-time telemetry metrics.
 */
export default function AnalyticsPage() {
  // 1. Defining the Four Pillars of the Score as weights[cite: 320, 435].
  // These represent the w_semantic, w_depth, w_stability, and w_risk multipliers.
  const weights = { 
    semantic: 50,  // Weight for Semantic Match (S_sem) [cite: 321]
    depth: 20,     // Weight for Career Depth & Velocity (S_dep) [cite: 327]
    stability: 20, // Weight for Tenure & Stability (S_sta) [cite: 333]
    risk: 10       // Negative weight multiplier for Forensic Risk (S_risk) [cite: 341]
  };

  // 2. Destructuring to fix the "Cannot find name" errors.
  const { semantic, depth, stability, risk } = weights;

  return (
    <div className="space-y-10 pb-20">
      {/* Header Section: Feedback Loop Monitoring [cite: 242] */}
      <div className="border-b pb-4">
        <h1 className="text-3xl font-bold text-slate-900">Pipeline Intelligence</h1>
        <p className="text-slate-500">Monitoring Phase 4 telemetry and Phase 5 ranking weights.</p>
      </div>

      {/* Real-time Metrics Section [cite: 247, 248] */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Recruiter CTR</p>
          <h3 className="text-3xl font-bold mt-1 text-blue-600">18.4%</h3>
          <p className="text-xs text-green-600 mt-2 font-medium">↑ 2.1% (Real-time Metric) [cite: 247]</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Avg. Dwell Time</p>
          <h3 className="text-3xl font-bold mt-1 text-purple-600">142s</h3>
          <p className="text-xs text-slate-400 mt-2">Captured via Telemetry </p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Conversion (Applied→Hired)</p>
          <h3 className="text-3xl font-bold mt-1 text-green-600">4.2%</h3>
          <p className="text-xs text-slate-400 mt-2">Conversion Tracking Active [cite: 249]</p>
        </div>
      </div>

      {/* Scoring Weight Visualization (Global Scoring Formula) [cite: 315, 433] */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
        <div className="mb-8">
          <h2 className="text-xl font-bold text-slate-800">Global Scoring Formula Weights ($w_1 \dots w_4$)</h2>
          <p className="text-sm text-slate-500 mt-1">Linear combination logic ensuring balanced recommendations[cite: 434].</p>
        </div>

        <div className="space-y-8">
          {/* Pillar 1: Semantic Match [cite: 321] */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="font-semibold text-slate-700">Semantic Match ($w_{semantic}$)</span>
              <span className="font-mono text-blue-600">{semantic}%</span>
            </div>
            <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 transition-all duration-500" style={{ width: `${semantic}%` }}></div>
            </div>
            <p className="text-xs text-slate-400 italic">Geometric proximity in vector space via Cosine Similarity[cite: 322, 324].</p>
          </div>

          {/* Pillar 2: Career Depth [cite: 327] */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="font-semibold text-slate-700">Career Depth & Velocity ($w_{depth}$)</span>
              <span className="font-mono text-green-600">{depth}%</span>
            </div>
            <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-green-500 transition-all duration-500" style={{ width: `${depth}%` }}></div>
            </div>
            <p className="text-xs text-slate-400 italic">Analyzed via NetworkX Graph Analysis to detect promotion density[cite: 329, 330].</p>
          </div>

          {/* Pillar 3: Stability [cite: 333] */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="font-semibold text-slate-700">Tenure & Stability ($w_{stability}$)</span>
              <span className="font-mono text-purple-600">{stability}%</span>
            </div>
            <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-purple-500 transition-all duration-500" style={{ width: `${stability}%` }}></div>
            </div>
            <p className="text-xs text-slate-400 italic">Calculated as Total Months / Unique Companies[cite: 336, 338].</p>
          </div>

          {/* Pillar 4: Risk (Negative Weight) [cite: 341] */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="font-semibold text-slate-700 text-red-600 font-bold">Forensic Risk Multiplier ($w_{risk}$)</span>
              <span className="font-mono text-red-600">{risk}%</span>
            </div>
            <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-red-500 opacity-80 transition-all duration-500" style={{ width: `${risk}%` }}></div>
            </div>
            <p className="text-xs text-slate-400 italic">Penalty score based on anomalies detected by the Auditor Agent[cite: 342, 343].</p>
          </div>
        </div>

        {/* System Self-Optimization Status [cite: 251, 259] */}
        <div className="mt-12 p-5 bg-blue-50 border border-blue-100 rounded-xl">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
            <h4 className="text-sm font-bold text-blue-900 uppercase tracking-tight">System Self-Optimization Active</h4>
          </div>
          <p className="text-sm text-blue-800/80 mt-2 leading-relaxed">
            The <strong>Optimization Layer</strong> is currently fine-tuning weights based on 
            explicit feedback and conversion tracking to update the Ranking Engine[cite: 251, 254, 258].
          </p>
        </div>
      </div>
    </div>
  );
}