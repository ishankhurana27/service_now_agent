import React, { useState } from 'react'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'
import { useAuth } from '../contexts/AuthContext'

interface AuthWrapperProps {
  children: React.ReactNode
}

const AuthWrapper: React.FC<AuthWrapperProps> = ({ children }) => {
  const { isAuthenticated, isLoading, logout } = useAuth()
  const [showRegister, setShowRegister] = useState(false)

  const handleLoginSuccess = () => {
    // Login success is handled by the context
  }

  const handleRegisterSuccess = () => {
    // Registration success is handled by the context
  }

  const handleLogout = () => {
    logout()
  }

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Checking authentication...</p>
        </div>
      </div>
    )
  }

  // Show authentication forms if not authenticated
  if (!isAuthenticated) {
    if (showRegister) {
      return (
        <RegisterForm
          onSwitchToLogin={() => setShowRegister(false)}
          onRegisterSuccess={handleRegisterSuccess}
        />
      )
    }

    return (
      <LoginForm
        onSwitchToRegister={() => setShowRegister(true)}
        onLoginSuccess={handleLoginSuccess}
      />
    )
  }

  // Show main app if authenticated
  return (
    <div className="auth-wrapper">
      {React.cloneElement(children as React.ReactElement, { onLogout: handleLogout })}
    </div>
  )
}

export default AuthWrapper
