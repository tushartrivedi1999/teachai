import { FormEvent, useEffect, useState } from 'react'
import { api, setToken } from '../api/client'
import type { Course, Suggestion, User } from '../types'

const menuItems = ['AI Tutor', 'Certificates', 'Interview Prep', 'Leaderboard', 'Tools Directory']

export function DashboardPage({ token }: { token: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [suggestions, setSuggestions] = useState<Suggestion[]>([])
  const [courses, setCourses] = useState<Course[]>([])
  const [courseForm, setCourseForm] = useState({ title: '', field: '', level: '', objectives: '' })
  const [showCourseModal, setShowCourseModal] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setToken(token)
    Promise.all([api.get('/users/me'), api.get('/suggestions'), api.get('/courses')])
      .then(([u, s, c]) => {
        setUser(u.data)
        setSuggestions(s.data)
        setCourses(c.data)
      })
      .catch(() => setError('Failed to load dashboard data.'))
  }, [token])

  const createCourse = async (event: FormEvent) => {
    event.preventDefault()
    const payload = {
      ...courseForm,
      objectives: courseForm.objectives.split(',').map((x) => x.trim()).filter(Boolean)
    }
    try {
      const { data } = await api.post('/courses', payload)
      setCourses((prev) => [data, ...prev])
      setCourseForm({ title: '', field: '', level: '', objectives: '' })
      setShowCourseModal(false)
    } catch {
      setError('Could not generate course. Please try again.')
    }
  }

  return (
    <main className="dashboard">
      <aside className="sidebar card">
        <h3>Menu</h3>
        <ul>{menuItems.map((item) => <li key={item}>{item}</li>)}</ul>
      </aside>
      <section className="content stack">
        <article className="card">
          <h2>Welcome, {user?.full_name ?? 'Learner'}</h2>
          <p>Class level: {user?.class_level} • Target track: {user?.target_track}</p>
          <button onClick={() => setShowCourseModal(true)}>Create Course</button>
        </article>
        {error ? <article className="card"><p className="error">{error}</p></article> : null}
        <article className="card">
          <h3>Dynamic Suggestions</h3>
          <ul>{suggestions.map((s) => <li key={s.title}><strong>{s.title}</strong> — {s.reason}</li>)}</ul>
        </article>
        <article className="card">
          <h3>Your Courses</h3>
          {courses.map((course) => (
            <details key={course.id}>
              <summary>{course.title} ({course.field}/{course.level})</summary>
              <ul>{course.generated_outline.modules.map((m) => <li key={m.name}>{m.name}: {m.practical}</li>)}</ul>
            </details>
          ))}
        </article>
      </section>
      <aside className="card">
        <h3>Calendar & Reminders</h3>
        <p>Upcoming weekly quiz reminder is generated based on your active courses.</p>
      </aside>

      {showCourseModal ? (
        <div className="modal-overlay" onClick={() => setShowCourseModal(false)}>
          <div className="card modal" onClick={(e) => e.stopPropagation()}>
            <h3>Create Dynamic Course</h3>
            <form onSubmit={createCourse} className="stack">
              <input value={courseForm.title} placeholder="Course title" onChange={(e) => setCourseForm({ ...courseForm, title: e.target.value })} />
              <input value={courseForm.field} placeholder="Field" onChange={(e) => setCourseForm({ ...courseForm, field: e.target.value })} />
              <input value={courseForm.level} placeholder="Level" onChange={(e) => setCourseForm({ ...courseForm, level: e.target.value })} />
              <input value={courseForm.objectives} placeholder="Objectives (comma separated)" onChange={(e) => setCourseForm({ ...courseForm, objectives: e.target.value })} />
              <button type="submit">Generate Course</button>
            </form>
          </div>
        </div>
      ) : null}
    </main>
  )
}
