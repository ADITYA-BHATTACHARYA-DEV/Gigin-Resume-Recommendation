// src/components/Ingest/UploadZone.tsx
'use client';
import { recruitmentService } from '@/services/api';
import { useState } from 'react';

export default function UploadZone() {
  const [status, setStatus] = useState<'idle' | 'uploading' | 'done'>('idle');

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    setStatus('uploading');
    try {
      // Phase 1: PyPDFLoader + Semantic Chunking happens on the backend
      await recruitmentService.uploadResume(e.target.files[0]);
      setStatus('done');
    } catch (err) {
      console.error(err);
      setStatus('idle');
    }
  };

  return (
    <div className="border-2 border-dashed p-10 text-center rounded-lg bg-gray-50">
      <input type="file" onChange={handleUpload} className="hidden" id="resume-upload" />
      <label htmlFor="resume-upload" className="cursor-pointer">
        {status === 'uploading' ? 'Vectorizing...' : 'Upload PDF Resume (Phase 1)'}
      </label>
    </div>
  );
}