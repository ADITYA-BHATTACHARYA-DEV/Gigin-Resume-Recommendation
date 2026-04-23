import { Briefcase, MapPin, User } from 'lucide-react';
import React from 'react';

interface CandidateCardProps {
  candidate: {
    candidate_id: string;
    score: number;
    pitch: string;
    metadata: {
      name: string;
      role: string;
      location: string;
    };
    score_breakdown: {
      s_sem: number;
      folder_boost: number;
      s_risk: number;
    };
  };
}

const CandidateCard: React.FC<CandidateCardProps> = ({ candidate }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-blue-500 transition-all shadow-lg mb-4">
      {/* Header: Name & Total Score */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <User className="text-blue-400" size={20} />
            {candidate.metadata.name.replace('.pdf', '')}
          </h3>
          <div className="flex gap-4 mt-1 text-slate-400 text-sm">
            <span className="flex items-center gap-1"><Briefcase size={14}/> {candidate.metadata.role}</span>
            <span className="flex items-center gap-1"><MapPin size={14}/> {candidate.metadata.location}</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-3xl font-black text-blue-500">{candidate.score}%</div>
          <div className="text-[10px] uppercase tracking-widest text-slate-500">Match Accuracy</div>
        </div>
      </div>

      {/* Phase 6: Agentic Pitch (The RAG Output) */}
      <div className="bg-slate-800/50 rounded-lg p-4 mb-4 border-l-4 border-blue-500">
        <p className="text-slate-300 italic text-sm leading-relaxed">
          "{candidate.pitch}"
        </p>
      </div>

      {/* Phase 5: The Mathematical Funnel (Score Breakdown) */}
      <div className="grid grid-cols-3 gap-4 border-t border-slate-800 pt-4">
        <div>
          <div className="text-[10px] text-slate-500 uppercase mb-1">Semantic Match</div>
          <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-green-500" 
              style={{ width: `${candidate.score_breakdown.s_sem}%` }}
            />
          </div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500 uppercase mb-1">Context Bonus</div>
          <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-blue-500" 
              style={{ width: `${candidate.score_breakdown.folder_boost * 10}%` }} 
            />
          </div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500 uppercase mb-1">Forensic Risk</div>
          <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-red-500" 
              style={{ width: `${candidate.score_breakdown.s_risk}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateCard;