import api from './api'

export const authService = {
  async login(email, password) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },
}

export const videoService = {
  async getVideos() {
    const response = await api.get('/videos/')
    return response.data
  },

  async getVideo(id) {
    const response = await api.get(`/videos/${id}`)
    return response.data
  },

  async uploadVideo(formData) {
    const response = await api.post('/videos/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async getVideoQuestions(videoId) {
    const response = await api.get(`/videos/${videoId}/questions`)
    return response.data
  },
}

export const questionService = {
  async submitAnswer(questionId, answer, currentTimestamp) {
    const response = await api.post(`/questions/${questionId}/answer`, {
      answer,
      current_timestamp: currentTimestamp,
    })
    return response.data
  },
}

export const progressService = {
  async getProgress(videoId) {
    const response = await api.get(`/progress/${videoId}`)
    return response.data
  },

  async updateProgress(videoId, currentTimestamp) {
    const response = await api.put(`/progress/${videoId}`, {
      current_timestamp: currentTimestamp,
    })
    return response.data
  },
}
