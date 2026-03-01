import { Route, Routes, Link, Navigate } from 'react-router-dom'
import { useState } from 'react'
import { DashboardPage } from './pages/DashboardPage'
import { LandingPage } from './pages/LandingPage'

export function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))

  const saveToken = (value: string | null) => {
    setToken(value)
    if (value) localStorage.setItem('token', value)
    else localStorage.removeItem('token')
  }

  return (
    <>
      <header className="top-nav">
        <h1>Rivinity Learning</h1>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          {token ? <button onClick={() => saveToken(null)}>Logout</button> : null}
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<LandingPage onAuth={saveToken} />} />
        <Route path="/dashboard" element={token ? <DashboardPage token={token} /> : <Navigate to="/" replace />} />
      </Routes>
    </>
  )
}
