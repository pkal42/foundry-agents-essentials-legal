import { useState, useEffect } from 'react'
import './App.css'

interface Note {
  id: string
  text: string
  created_at: string
}

interface Onboarding {
  id: string
  client_name: string
  engagement_type: string
  description: string
  status: string
  contact_email: string
  created_at: string
  notes: Note[]
}

const statusColors: Record<string, string> = {
  'pending': '#f59e0b',
  'in-review': '#3b82f6',
  'approved': '#10b981',
  'active': '#8b5cf6',
  'completed': '#6b7280',
  'on-hold': '#ef4444',
}

function App() {
  const [onboardings, setOnboardings] = useState<Onboarding[]>([])
  const [selected, setSelected] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = () => {
      fetch('/api/onboardings')
        .then(r => r.json())
        .then(setOnboardings)
        .catch(() => {})
    }
    fetchData()
    const interval = setInterval(fetchData, 3000)
    return () => clearInterval(interval)
  }, [])

  const detail = onboardings.find(o => o.id === selected)

  return (
    <div className="app">
      <header>
        <h1>📋 Client Onboarding Tracker</h1>
        <p className="subtitle">Powered by Microsoft Foundry Agent</p>
      </header>

      <div className="dashboard">
        <div className="stats">
          {['pending', 'in-review', 'approved', 'active'].map(status => (
            <div key={status} className="stat-card" style={{ borderLeftColor: statusColors[status] }}>
              <div className="stat-count">{onboardings.filter(o => o.status === status).length}</div>
              <div className="stat-label">{status}</div>
            </div>
          ))}
        </div>

        <div className="content">
          <div className="list">
            <h2>Onboardings</h2>
            {onboardings.length === 0 ? (
              <p className="empty">No onboardings yet. Use the Foundry agent to create one!</p>
            ) : (
              onboardings.map(ob => (
                <div
                  key={ob.id}
                  className={`card ${selected === ob.id ? 'selected' : ''}`}
                  onClick={() => setSelected(ob.id)}
                >
                  <div className="card-header">
                    <span className="client-name">{ob.client_name}</span>
                    <span className="status-badge" style={{ backgroundColor: statusColors[ob.status] }}>
                      {ob.status}
                    </span>
                  </div>
                  <div className="card-type">{ob.engagement_type}</div>
                  <div className="card-id">{ob.id}</div>
                </div>
              ))
            )}
          </div>

          <div className="detail">
            {detail ? (
              <>
                <h2>{detail.client_name}</h2>
                <div className="detail-grid">
                  <div className="detail-label">ID</div>
                  <div>{detail.id}</div>
                  <div className="detail-label">Type</div>
                  <div>{detail.engagement_type}</div>
                  <div className="detail-label">Status</div>
                  <div>
                    <span className="status-badge" style={{ backgroundColor: statusColors[detail.status] }}>
                      {detail.status}
                    </span>
                  </div>
                  <div className="detail-label">Contact</div>
                  <div>{detail.contact_email || '—'}</div>
                  <div className="detail-label">Created</div>
                  <div>{new Date(detail.created_at).toLocaleDateString()}</div>
                  <div className="detail-label">Description</div>
                  <div>{detail.description}</div>
                </div>
                <h3>Notes ({detail.notes.length})</h3>
                {detail.notes.length === 0 ? (
                  <p className="empty">No notes yet.</p>
                ) : (
                  <div className="notes">
                    {detail.notes.map(note => (
                      <div key={note.id} className="note">
                        <div className="note-text">{note.text}</div>
                        <div className="note-date">{new Date(note.created_at).toLocaleString()}</div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="empty-detail">
                <p>Select an onboarding to view details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
