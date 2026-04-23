'use client';

import { recruitmentService } from "@/services/api";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [candidates, setCandidates] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setIsLoading(true);
    try {
      // Phase 2 & 3: Retrieval (Top 50) -> MMR Diversification (Top 15)
      // The backend now filters by folder names if keywords like "Bangalore" are found.
      const response = await recruitmentService.getRecommendations(query);
      console.log("Raw Response from Backend:", response.data);
      setCandidates(response.data);
    } catch (error) {
      console.error("Discovery Engine Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-10 pb-20">
      {/* Search Section: The Discovery Entry Point */}
      <section className="text-center space-y-4">
        <h1 className="text-4xl font-extrabold tracking-tight text-slate-900">
          Discovery Engine
        </h1>
        <p className="text-slate-500 max-w-2xl mx-auto">
          Type a job description or location (e.g., "Telesales in Bangalore") to 
          query the <strong>HNSW Vector Index</strong> on the F: drive.
        </p>
        <div className="flex max-w-2xl mx-auto gap-2 mt-8">
          <input
            type="text"
            placeholder="Search roles, locations, or skills..."
            className="flex-1 px-5 py-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button 
            onClick={handleSearch}
            disabled={isLoading}
            className="px-8 py-4 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-all disabled:opacity-50 shadow-lg shadow-blue-100"
          >
            {isLoading ? "Querying..." : "Search"}
          </button>
        </div>
      </section>

      {/* Results Section: The Top 15 Unique Shortlist */}
      <section>
        <div className="flex items-center justify-between mb-8 border-b pb-4">
          <h2 className="text-xl font-bold text-slate-800">Unique Talent Shortlist</h2>
          <div className="flex gap-4 items-center">
             <span className="text-xs font-mono text-slate-400">λ: 0.5</span>
             <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded font-bold">
               {candidates.length} Profiles Found
             </span>
          </div>
        </div>

        {candidates.length === 0 && !isLoading ? (
          <div className="text-center py-32 border-2 border-dashed rounded-3xl text-slate-400 bg-white/50">
            No candidates retrieved. Type a query to start the pipeline.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {candidates.map((candidate, idx) => (
              <div key={idx} className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all flex flex-col">
                {/* Header: Filename & Match Score */}
                <div className="flex justify-between items-start mb-4">
                  <div className="space-y-1">
                    <h3 className="font-bold text-slate-900 truncate max-w-[150px]" title={candidate.metadata?.name}>
                      {candidate.metadata?.name}
                    </h3>
                    <div className="flex gap-1">
                      <span className="text-[10px] uppercase font-bold px-2 py-0.5 bg-blue-50 text-blue-600 rounded">
                        {candidate.metadata?.role}
                      </span>
                      <span className="text-[10px] uppercase font-bold px-2 py-0.5 bg-slate-100 text-slate-600 rounded">
                        {candidate.metadata?.location}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-black text-blue-600">{Math.round(candidate.score)}</div>
                    <div className="text-[10px] text-slate-400 font-bold uppercase">Rank Score</div>
                  </div>
                </div>

                {/* Phase 5: The Four Pillars Visualization */}
                <div className="space-y-3 my-6">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Scoring Pillars</div>
                  
                  {/* Semantic Bar */}
                  <div className="space-y-1">
                    <div className="flex justify-between text-[10px] font-medium">
                      <span>Semantic Match</span>
                      <span>{candidate.score_breakdown?.s_sem}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500" style={{ width: `${candidate.score_breakdown?.s_sem}%` }}></div>
                    </div>
                  </div>

                  {/* Career Velocity Bar */}
                  <div className="space-y-1">
                    <div className="flex justify-between text-[10px] font-medium">
                      <span>Career Velocity</span>
                      <span>{candidate.score_breakdown?.s_dep}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-green-500" style={{ width: `${candidate.score_breakdown?.s_dep}%` }}></div>
                    </div>
                  </div>

                  {/* Stability Bar */}
                  <div className="space-y-1">
                    <div className="flex justify-between text-[10px] font-medium">
                      <span>Tenure Stability</span>
                      <span>{candidate.score_breakdown?.s_sta}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-purple-500" style={{ width: `${candidate.score_breakdown?.s_sta}%` }}></div>
                    </div>
                  </div>
                </div>

                {/* Phase 6: Agentic Explanation */}
                <div className="flex-1 p-4 bg-slate-50 rounded-xl border border-slate-100 text-sm text-slate-600 leading-relaxed relative">
                  <span className="absolute -top-2 left-3 bg-white px-2 text-[10px] font-bold text-slate-400 uppercase">Pitch</span>
                  "{candidate.pitch || "This candidate shows strong technical alignment with your requirements and a verified growth trajectory."}"
                </div>
                
                {/* PDF Action */}
                <div className="mt-6 pt-4 border-t flex gap-2">
                  <a 
                    href={`http://localhost:8000/resumes/${candidate.metadata?.role}/${candidate.metadata?.location}/${candidate.metadata?.name}${candidate.metadata?.name.endsWith('.pdf') ? '' : '.pdf'}`}
                    target="_blank"
                    className="flex-1 text-center py-2.5 bg-white border border-slate-200 text-slate-700 rounded-lg font-bold hover:bg-slate-50 transition-colors text-xs"
                  >
                    Preview PDF
                  </a>
                  <button className="px-4 py-2.5 bg-blue-50 text-blue-600 rounded-lg font-bold hover:bg-blue-100 transition-colors text-xs">
                    Graph
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}