/*
 * Demonstration Platform - Profile Page
 * ======================================
 * Educational Demo – OAuth Token Theft Simulation
 * 
 * This page demonstrates:
 * 1. How a valid access token grants access to protected resources
 * 2. What happens when a token expires
 * 3. The importance of keeping tokens secure
 */

'use client'

import { useState, useEffect, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'

const API_BASE = 'http://localhost:5000'

interface ProfileData {
  username: string
  role: string
  access_level: string
  protected_data: {
    type: string
    description: string
    records: number
    format: string
    sensitivity: string
  }
  token_info: {
    issued_at: string
    expires_at: string
    expires_in_seconds: number
    token_prefix: string
  }
  security_notice: string
  attack_scenario: string
}

interface ProfileError {
  error: string
  message: string
}

function ProfileContent() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const token = searchParams.get('token')

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [profileData, setProfileData] = useState<ProfileData | null>(null)
  const [countdown, setCountdown] = useState(0)

  useEffect(() => {
    if (!token) {
      setError('No token provided. Please log in first.')
      setIsLoading(false)
      return
    }

    const fetchProfile = async () => {
      try {
        // Send request with token in Authorization header
        const response = await fetch(`${API_BASE}/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })

        const data: ProfileData | ProfileError = await response.json()

        if (!response.ok) {
          setError((data as ProfileError).message || 'Failed to fetch profile')
          setIsLoading(false)
          return
        }

        setProfileData(data as ProfileData)
        setCountdown((data as ProfileData).token_info.expires_in_seconds)
        setIsLoading(false)
      } catch (err) {
        console.error('[DEMO] Network error:', err)
        setError('Unable to connect to the server. Is the Flask backend running?')
        setIsLoading(false)
      }
    }

    fetchProfile()
  }, [token])

  // Countdown timer
  useEffect(() => {
    if (countdown <= 0 || !profileData) return

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          setError('Token has expired. Please log in again.')
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [countdown, profileData])

  const handleLogout = () => {
    router.push('/login')
  }

  if (!token) {
    return (
      <main>
        <div className="card">
          <div className="error-state">
            <h2 className="error-title">Authentication Required</h2>
            <p className="error-message">{error || 'No token found in URL'}</p>
            <button onClick={handleLogout} className="btn btn-primary">
              Go to Login
            </button>
          </div>
        </div>
      </main>
    )
  }

  if (isLoading) {
    return (
      <main>
        <div className="card">
          <div className="loading">
            <div className="loading-spinner"></div>
          </div>
        </div>
      </main>
    )
  }

  if (error) {
    return (
      <main>
        <div className="card">
          <div className="error-state">
            <h2 className="error-title">Error</h2>
            <p className="error-message">{error}</p>
            <button onClick={handleLogout} className="btn btn-primary">
              Go to Login
            </button>
          </div>
        </div>
      </main>
    )
  }

  if (!profileData) {
    return null
  }

  return (
    <main>
      <div className="card">
        <div className="profile-header">
          <h1 className="profile-welcome">
            Welcome, {profileData.username}
          </h1>
          <p className="profile-role">Role: {profileData.role}</p>
        </div>

        {/* Token Expiry Countdown */}
        <div className="countdown">
          <div className="countdown-number">{countdown}s</div>
          <div className="countdown-label">Token Expires In</div>
        </div>

        {/* Protected Data Section */}
        <div className="data-section">
          <div className="data-title">Protected Data</div>
          <div className="data-item">
            <span className="data-key">Type</span>
            <span className="data-value">{profileData.protected_data.type}</span>
          </div>
          <div className="data-item">
            <span className="data-key">Description</span>
            <span className="data-value">{profileData.protected_data.description}</span>
          </div>
          <div className="data-item">
            <span className="data-key">Records</span>
            <span className="data-value">{profileData.protected_data.records.toLocaleString()}</span>
          </div>
          <div className="data-item">
            <span className="data-key">Format</span>
            <span className="data-value">{profileData.protected_data.format}</span>
          </div>
          <div className="data-item">
            <span className="data-key">Sensitivity</span>
            <span className="data-value">{profileData.protected_data.sensitivity}</span>
          </div>
        </div>

        {/* Access Level Section */}
        <div className="data-section">
          <div className="data-title">Access Level</div>
          <div className="data-item">
            <span className="data-key">Level</span>
            <span className="data-value">{profileData.access_level}</span>
          </div>
        </div>

        {/* Token Info Section */}
        <div className="data-section">
          <div className="data-title">Token Information</div>
          <div className="data-item">
            <span className="data-key">Token Prefix</span>
            <span className="data-value" style={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
              {profileData.token_info.token_prefix}
            </span>
          </div>
          <div className="data-item">
            <span className="data-key">Issued At</span>
            <span className="data-value">{new Date(profileData.token_info.issued_at).toLocaleString()}</span>
          </div>
          <div className="data-item">
            <span className="data-key">Expires At</span>
            <span className="data-value">{new Date(profileData.token_info.expires_at).toLocaleString()}</span>
          </div>
          <div className="token-preview">
            Full token: {token?.slice(0, 20)}...{token?.slice(-20)}
          </div>
        </div>

        {/* Warning Box - Security Education */}
        <div className="warning-box">
          <div className="warning-title">
            <span>⚠️</span>
            <span>Security Warning - Token Theft Demo</span>
          </div>
          <div className="warning-content">
            <p>
              <strong>What just happened?</strong><br />
              You successfully accessed protected data using an access token.
              This is how OAuth-based authentication works in real applications.
            </p>
            <p>
              <strong>Token Theft Risk:</strong><br />
              If an attacker obtained this token (e.g., via XSS, MITM attack,
              or insecure storage), they could access this data WITHOUT knowing
              your username or password. This is called a <em>Token Replay Attack</em>.
            </p>
            <p>
              <strong>Mitigation in Production:</strong><br />
              • Use short-lived tokens (like this 60-second demo)<br />
              • Implement token rotation with refresh tokens<br />
              • Store tokens securely (httpOnly cookies, encrypted storage)<br />
              • Use TLS/HTTPS to prevent interception<br />
              • Implement token binding to devices
            </p>
            <p style={{ color: 'var(--error)', marginTop: '0.5rem' }}>
              <strong>Demo Note:</strong> Check the <code>leaked_token.txt</code> file on the
              Flask server. It contains the token that was "stolen" during login!
            </p>
          </div>
        </div>

        {/* Attack Scenario Notice */}
        <div className="alert alert-warning" style={{ marginTop: '1.5rem' }}>
          <strong>Token Replay Attack Scenario:</strong><br />
          {profileData.attack_scenario}
        </div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="btn btn-primary"
          style={{ marginTop: '1.5rem' }}
        >
          Logout
        </button>
      </div>
    </main>
  )
}

// Wrap with Suspense for useSearchParams
export default function ProfilePage() {
  return (
    <Suspense fallback={
      <main>
        <div className="card">
          <div className="loading">
            <div className="loading-spinner"></div>
          </div>
        </div>
      </main>
    }>
      <ProfileContent />
    </Suspense>
  )
}
