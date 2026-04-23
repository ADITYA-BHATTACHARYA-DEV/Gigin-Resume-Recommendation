import axios from 'axios';

const API = axios.create({
  // Ensure this points to the base + the version prefix
  baseURL: 'http://127.0.0.1:8000/api/v1', 
});

export const recruitmentService = {
  // Now this calls http://127.0.0.1:8000/api/v1/recommend
  getRecommendations: async (query: string) => {
    return API.get(`/recommend?jd_query=${encodeURIComponent(query)}`);
  },

  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return API.post('/ingest', formData);
  },
};