import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Home from './pages/Home'
import Landing from './pages/Landing'
import ProtectedRoute from './components/ProtectedRoute'
import DemoSite from './pages/DemoSite'
import SaveActionGallery from './pages/SaveActionGallery'
import DemoNarrative from './pages/DemoNarrative'

function App() {
  const { isAuthenticated, initializeAuth } = useAuthStore()

  // Initialize auth on app load
  useEffect(() => {
    initializeAuth()
  }, [initializeAuth])

  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />
      } />
      <Route path="/signup" element={
        isAuthenticated ? <Navigate to="/dashboard" replace /> : <Signup />
      } />
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Home />
        </ProtectedRoute>
      } />
      <Route path="/demo" element={<DemoSite />} />
      <Route path="/save-actions" element={<SaveActionGallery />} />
      <Route path="/demo-narrative" element={<DemoNarrative />} />
      <Route path="/" element={<Landing />} />
    </Routes>
  )
}

export default App

