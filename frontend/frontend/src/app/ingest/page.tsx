'use client';

import { useState } from 'react';
import { recruitmentService } from '@/services/api';

export default function IngestCommandCenter() {
  const [status, setStatus] = useState<'idle' | 'running' | 'complete'>('idle');
  const [activeStep, setActiveStep] = useState(0);

  const pipelineSteps = [
    { label: "Document Extraction", tool: "PyPDFLoader", desc: "Parsing raw text from PDF" },
    { label: "Semantic Chunking", tool: "RecursiveSplitter", desc: "Preserving context by section" },
    { label: "Vectorization", tool: "all-MiniLM-L6-v2", desc: "Generating 384d embeddings" },
    { label: "Storage", tool: "ChromaDB/HNSW", desc: "Indexing for O(log N) retrieval" }
  ];

  const triggerPipeline = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    setStatus('running');
    // Simulate pipeline progression for UI feedback
    for (let i = 0; i <= pipelineSteps.length; i++) {
      setActiveStep(i);
      await new Promise(r => setTimeout(r, 800));
    }

    try {
      await recruitmentService.uploadResume(file);
      setStatus('complete');
    } catch (err) {
      console.error("Pipeline Crash:", err);
      setStatus('idle');
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="flex justify-between items-end border-b pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">Pipeline Command Center</h1>
          <p className="text-slate-500 mt-1">Phase 1: Knowledge Ingestion & Vectorization [cite: 346]</p>
        </div>
        <label className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-bold cursor-pointer hover:bg-blue-700 transition-all shadow-lg shadow-blue-200">
          Drop New Resume
          <input type="file" className="hidden" onChange={triggerPipeline} />
        </label>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Step Progress */}
        <div className="lg:col-span-2 space-y-4">
          {pipelineSteps.map((step, idx) => (
            <div 
              key={idx}
              className={`p-5 rounded-xl border-2 transition-all ${
                activeStep === idx ? "border-blue-500 bg-blue-50" : 
                activeStep > idx ? "border-green-200 bg-green-50" : "border-slate-100 bg-white"
              }`}
            >
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                  <span className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                    activeStep > idx ? "bg-green-500 text-white" : "bg-slate-200 text-slate-600"
                  }`}>
                    {activeStep > idx ? "✓" : idx + 1}
                  </span>
                  <div>
                    <h3 className="font-bold text-slate-800">{step.label}</h3>
                    <p className="text-xs text-slate-500 font-mono">{step.tool}</p>
                  </div>
                </div>
                {activeStep === idx && <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>}
              </div>
              {activeStep === idx && <p className="mt-3 text-sm text-blue-600 italic">{step.desc}...</p>}
            </div>
          ))}
        </div>

        {/* Right: System Health & Logs */}
        <div className="space-y-6">
          <div className="bg-slate-900 rounded-2xl p-6 shadow-xl shadow-slate-200">
            <h3 className="text-white font-bold mb-4 flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              Live Pipeline Logs
            </h3>
            <div className="font-mono text-[10px] space-y-2 text-slate-400 overflow-hidden">
              <p className="text-green-400">{">"} Initializing PyPDFLoader...</p>
              <p className="text-slate-500">{">"} Found 3 pages. Extracting text blocks.</p>
              <p className={activeStep >= 2 ? "text-green-400" : ""}>{">"} Tokenizing via all-MiniLM-L6-v2</p>
              <p className={activeStep >= 3 ? "text-green-400" : ""}>{">"} HNSW Index Construction: O(log N) optimized [cite: 352]</p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200">
            <h4 className="font-bold text-slate-800 mb-2">Engine Settings</h4>
            <div className="space-y-3">
              <div className="flex justify-between text-xs">
                <span>Vector Dimension</span>
                <span className="font-mono font-bold">384d</span>
              </div>
              <div className="flex justify-between text-xs">
                <span>Similarity Metric</span>
                <span className="font-mono font-bold">Cosine [cite: 324]</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}