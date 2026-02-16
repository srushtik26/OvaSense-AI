/**
 * API Client for OvaSense AI Backend
 * Centralized axios instance with all API endpoints
 */

import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor (for future auth tokens)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token here when implemented
    // const token = localStorage.getItem('token')
    // if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// ===== HEALTH SCORE API =====
export const healthScoreAPI = {
  getScore: (userId: string) => 
    apiClient.get(`/health-score/${userId}`),
}

// ===== PERIOD TRACKER API =====
export const periodAPI = {
  addLog: (data: any) => 
    apiClient.post('/period/add', data),
  
  getHistory: (userId: string) => 
    apiClient.get(`/period/history/${userId}`),
  
  getPrediction: (userId: string) => 
    apiClient.get(`/period/prediction/${userId}`),
}

// ===== MENTAL HEALTH API =====
export const mentalHealthAPI = {
  addLog: (data: any) => 
    apiClient.post('/mental-health/add', data),
  
  getHistory: (userId: string) => 
    apiClient.get(`/mental-health/history/${userId}`),
  
  getInsights: (userId: string) => 
    apiClient.get(`/mental-health/insights/${userId}`),
}

// ===== DIET PLAN API =====
export const dietAPI = {
  getPlan: (userId: string) => 
    apiClient.get(`/diet-plan/${userId}`),
}

// ===== QUIZ API =====
export const quizAPI = {
  getQuestions: () => 
    apiClient.get('/quiz/questions'),
  
  submitQuiz: (data: any) => 
    apiClient.post('/quiz/submit', data),
}

// ===== REPORTS API =====
export const reportsAPI = {
  getMonthlyReport: (userId: string) => 
    apiClient.get(`/report/monthly/${userId}`),
}

// ===== ASSESSMENT API (Existing) =====
export const assessmentAPI = {
  create: (data: any) => 
    apiClient.post('/assessments/', data),
  
  getById: (assessmentId: number) => 
    apiClient.get(`/assessments/${assessmentId}`),
  
  getByUser: (userId: string) => 
    apiClient.get(`/assessments/user/${userId}`),
}

export default apiClient
