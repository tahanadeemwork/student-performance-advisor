// ============================================
// API Service
// Handles all communication with Flask backend
// ============================================

import axios from 'axios'

const BASE_URL = import.meta.env.DEV 
  ? 'http://localhost:5000/api'  // Development
  : 'http://localhost:5000/api'  // Production

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

// Check if API is running
export const checkHealth = async () => {
  const res = await api.get('/health')
  return res.data
}

// Analyze a student
export const analyzeStudent = async (studentData) => {
  const res = await api.post('/analyze', studentData)
  return res.data
}

// Get sample profiles
export const getSamples = async () => {
  const res = await api.get('/samples')
  return res.data
}

export default api