export type Suggestion = { title: string; reason: string; type: string }
export type Course = {
  id: number
  title: string
  field: string
  level: string
  generated_outline: {
    modules: Array<{ name: string; topics: string[]; practical: string; assessment: string }>
  }
  created_at: string
}
export type User = {
  id: number
  email: string
  full_name: string
  role: string
  interests: string[]
  class_level: string
  target_track: string
}
