/*
 * Demonstration Platform - Login Page
 * ====================================
 * Educational Demo – OAuth Token Theft Simulation
 * 
 * This page simulates a login form that would be part of an OAuth flow.
 * In a real OAuth implementation, this would redirect to an authorization
 * server, but for this demo we have a simplified direct login.
 */

'use client'

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'

const API_BASE = 'http://localhost:5002'

interface LoginResponse {
  access_token: string
  expires_in: number
  token_type: string
  message?: string
}

interface LoginError {
  error: string
}

export default function LoginPage() {
  const router = useRouter()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })

      const data: LoginResponse | LoginError = await response.json()

      if (!response.ok) {
        setError((data as LoginError).error || 'Login failed')
        setIsLoading(false)
        return
      }

      const loginData = data as LoginResponse
      
      // Store token in localStorage (simulating OAuth token storage)
      // In real OAuth, tokens are stored securely (httpOnly cookies, encrypted storage, etc.)
      localStorage.setItem('access_token', loginData.access_token)
      localStorage.setItem('token_expiry', String(loginData.expires_in))
      
      console.log('[DEMO] Login successful!')
      console.log('[DEMO] Token stored in localStorage')
      console.log('[DEMO] Token saved to leaked_token.txt on server (simulating theft)')
      console.log('[DEMO] In real apps, tokens in localStorage can be stolen via XSS!')
      
      // Redirect to profile page
      router.push('/profile')
    } catch (err) {
      console.error('[DEMO] Network error:', err)
      setError('Unable to connect to the server. Is the Flask backend running?')
      setIsLoading(false)
    }
  }

  return (
    <main>
      <div className="card">
        <div className="card-header">
          <h1 className="card-title">Demonstration Platform</h1>
          <p className="card-subtitle">Educational Demo – OAuth Token Theft Simulation</p>
        </div>

        {error && (
          <div className="alert alert-danger">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username" className="form-label">
              Username
            </label>
            <input
              type="text"
              id="username"
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={isLoading}
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="demo-notice">
          <p className="demo-notice-text">
            Demo only. No real accounts are used.
          </p>
        </div>
      </div>

      <div className="alert alert-info" style={{ marginTop: '1.5rem', textAlign: 'center' }}>
        <strong>Demo Credentials:</strong><br />
        Username: <code>student</code> | Password: <code>1234</code>
      </div>

      <div className="alert alert-warning" style={{ marginTop: '1rem', textAlign: 'center' }}>
        <strong>⚠️ Security Note:</strong><br />
        After login, open Dev Tools (F12) → Application → Local Storage<br />
        You will see the token stored there (simulating how XSS attacks steal tokens!)
      </div>
    </main>
  )
}
