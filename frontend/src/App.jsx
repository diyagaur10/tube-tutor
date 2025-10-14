import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './hooks/useAuth'
import Layout from './components/common/Layout'
import Home from './pages/Home'
import VideoPage from './pages/VideoPage'
import AdminDashboard from './pages/AdminDashboard'
import Profile from './pages/Profile'
import LoginForm from './components/auth/LoginForm'
import RegisterForm from './components/auth/RegisterForm'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/" element={<Layout />}>
              <Route index element={<Home />} />
              <Route path="video/:id" element={<VideoPage />} />
              <Route path="admin" element={<AdminDashboard />} />
              <Route path="profile" element={<Profile />} />
            </Route>
          </Routes>
          <Toaster position="top-right" />
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
