'use client';

import { recruitmentService } from '@/services/api';
import { useState } from 'react';

export default function IngestPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'processing' | 'success'>('idle');
  const [stats, setStats] = useState<any>(null);

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    try {
      // Phase 1: PyPDFLoader -> Semantic Chunking -> HNSW Indexing
      const response = await recruitmentService.uploadResume(file);
      setStatus('processing');
      // Mock delay to simulate backend vectorization
      setTimeout(() => {
        setStats(response.data);
        setStatus('success');
      }, 1500);
    } catch (error) {
      console.error("Ingestion Error:", error);
      setStatus('idle');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="border-b pb-4">
        <h1 className="text-3xl font-bold">Phase 1: Knowledge Ingestion</h1>
        <p className="text-slate-500">Transforming unstructured PDFs into semantic professional DNA.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Upload Zone */}
        <div className="border-2 border-dashed border-slate-200 rounded-2xl p-12 flex flex-col items-center justify-center bg-white">
          <input 
            type="file" 
            accept=".pdf" 
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="mb-4 text-sm"
          />
          <button 
            onClick={handleUpload}
            disabled={!file || status !== 'idle'}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 transition-all"
          >
            {status === 'idle' ? 'Index Resume' : 'Processing Pipeline...'}
          </button>
        </div>

        {/* Pipeline Visualizer */}
        <div className="bg-slate-900 rounded-2xl p-6 text-slate-300 font-mono text-sm space-y-4">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${status !== 'idle' ? 'bg-green-500 animate-pulse' : 'bg-slate-700'}`}></div>
            <span>[1] PyPDFLoader: Document Extraction</span>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${status === 'processing' || status === 'success' ? 'bg-green-500 animate-pulse' : 'bg-slate-700'}`}></div>
            <span>[2] Semantic Chunking: Context Preservation</span>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${status === 'success' ? 'bg-green-500' : 'bg-slate-700'}`}></div>
            <span>[3] ChromaDB: HNSW Index Construction</span>
          </div>
          
          {status === 'success' && (
            <div className="mt-6 p-4 bg-green-500/10 border border-green-500/20 rounded text-green-400">
              Successfully indexed {stats?.chunks_processed} semantic vectors (384d).
            </div>
          )}
        </div>
      </div>
    </div>
  );
}