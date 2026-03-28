/*
 * Demonstration Platform - Profile Page
 * ======================================
 * Educational Demo – OAuth Token Theft Simulation
 * 
 * This page demonstrates:
 * 1. How a valid access token grants access to protected resources
 * 2. What happens when a token expires
 * 3. The importance of keeping tokens secure
 * 
 * TOKEN THEFT SCENARIO:
 * - Tokens stored in localStorage can be stolen via XSS attacks
 * - An attacker could use the stolen token to access protected resources
 */

'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

const API_BASE = 'http://localhost:5002'

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

export default function ProfilePage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [profileData, setProfileData] = useState<ProfileData | null>(null)

  const [manualToken, setManualToken] = useState('')
  const [useManualToken, setUseManualToken] = useState(false)

  // Get token from localStorage (set during login)
  const getToken = () => {
    if (useManualToken && manualToken) {
      return manualToken
    }
    return localStorage.getItem('access_token')
  }

  useEffect(() => {
    const fetchProfile = async () => {
      const token = getToken()

      if (!token) {
        setError('You are not authorized to view this page')
        setIsLoading(false)
        return
      }

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
        setIsLoading(false)
      } catch (err) {
        console.error('[DEMO] Network error:', err)
        setError('Unable to connect to the server. Is the Flask backend running?')
        setIsLoading(false)
      }
    }

    fetchProfile()
  }, [useManualToken, manualToken])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('token_expiry')
    router.push('/login')
  }

  const handleManualTokenSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    setUseManualToken(true)
  }

  // If no token available, show unauthorized error
  if (!localStorage.getItem('access_token') && !error) {
    return (
      <main>
        <div className="card">
          <div className="card-header">
            <h1 className="card-title">Access Denied</h1>
            <p className="card-subtitle">You are not authorized to view this page</p>
          </div>

          <div className="alert alert-danger">
            <strong>401 Unauthorized</strong><br />
            Valid access token is required to view this resource.
          </div>

          <button
            onClick={() => router.push('/login')}
            className="btn btn-primary"
          >
            Go to Login
          </button>
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
        </div>

        {/* User Settings Section */}
        <div className="data-section">
          <div className="data-title">User Settings</div>
          <div className="data-item">
            <span className="data-key">Theme</span>
            <span className="data-value">Dark Mode</span>
          </div>
          <div className="data-item">
            <span className="data-key">Language</span>
            <span className="data-value">English (US)</span>
          </div>
          <div className="data-item">
            <span className="data-key">Timezone</span>
            <span className="data-value">UTC+3</span>
          </div>
          <div className="data-item">
            <span className="data-key">2FA Enabled</span>
            <span className="data-value" style={{ color: 'var(--success)' }}>✓ Yes</span>
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="data-section">
          <div className="data-title">Recent Activity</div>
          <div className="data-item">
            <span className="data-key">Last Login</span>
            <span className="data-value">Today, 22:30 UTC</span>
          </div>
          <div className="data-item">
            <span className="data-key">IP Address</span>
            <span className="data-value">192.168.1.xxx</span>
          </div>
          <div className="data-item">
            <span className="data-key">Active Sessions</span>
            <span className="data-value">2 devices</span>
          </div>
        </div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="btn btn-primary"
          style={{ marginTop: '1rem' }}
        >
          Logout
        </button>
      </div>
    </main>
  )
}
