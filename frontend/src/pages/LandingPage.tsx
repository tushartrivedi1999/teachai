import { FormEvent, useState } from 'react'
import { api, setToken } from '../api/client'

export function LandingPage({ onAuth }: { onAuth: (token: string) => void }) {
  const [form, setForm] = useState({ full_name: '', email: '', password: '' })
  const [mode, setMode] = useState<'login' | 'register'>('register')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const endpoint = mode === 'login' ? '/auth/login' : '/auth/register'
      const payload = mode === 'login' ? { email: form.email, password: form.password } : form
      const { data } = await api.post(endpoint, payload)
      setToken(data.access_token)
      onAuth(data.access_token)
    } catch {
      setError('Unable to authenticate. Please verify your details and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="grid hero">
      <section>
        <h2>AI tutor for school students, engineers, and researchers</h2>
        <p>Generate dynamic module-wise learning paths, practical projects, proctored tests, and certificates.</p>
      </section>
      <section className="card">
        <h3>{mode === 'login' ? 'Login' : 'Get Started'}</h3>
        <form onSubmit={submit} className="stack">
          {mode === 'register' ? (
            <input placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          ) : null}
          <input placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          {error ? <p className="error">{error}</p> : null}
          <button type="submit" disabled={loading}>{loading ? 'Please wait...' : mode === 'login' ? 'Login' : 'Create account'}</button>
          <button type="button" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
            Switch to {mode === 'login' ? 'Register' : 'Login'}
          </button>
        </form>
      </section>
    </main>
  )
}
