const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export async function searchByLawyer(name: string) {
  const res = await fetch(`${API_BASE}/cnj/lawyer-name?lawyer_name=${encodeURIComponent(name)}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function searchDeadlines(name: string, statuses?: string[], page = 1, page_size = 25, threshold_days?: number) {
  const params = new URLSearchParams({ lawyer_name: name, page: String(page), page_size: String(page_size) })
  if (statuses && statuses.length > 0) params.set('status', statuses.join(','))
  if (threshold_days !== undefined) params.set('threshold_days', String(threshold_days))
  const res = await fetch(`${API_BASE}/cnj/lawyer-name/deadlines?${params.toString()}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
} 
