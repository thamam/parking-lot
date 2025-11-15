'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { formatDateTime, getRelativeTime, getStatusColor, getPriorityColor } from '@/lib/utils'

interface ResearchNote {
  id: string
  source: string
  title: string
  content: string
  url: string | null
  createdAt: string
}

interface Activity {
  id: string
  type: string
  description: string
  createdAt: string
}

interface Project {
  id: string
  name: string
  description: string | null
  githubUrl: string | null
  status: string
  priority: string
  lastCommitDate: string | null
  lastCommitSha: string | null
  openIssues: number
  openPRs: number
  stars: number
  language: string | null
  researchNotes: ResearchNote[]
  activities: Activity[]
}

export default function ProjectPage() {
  const params = useParams()
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const [showNoteForm, setShowNoteForm] = useState(false)
  const [noteForm, setNoteForm] = useState({
    source: 'claude',
    title: '',
    content: '',
    url: ''
  })

  useEffect(() => {
    if (params.id) {
      fetchProject()
    }
  }, [params.id])

  const fetchProject = async () => {
    try {
      const response = await fetch(`/api/projects/${params.id}`)
      const data = await response.json()
      setProject(data)
    } catch (error) {
      console.error('Error fetching project:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const response = await fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId: params.id,
          ...noteForm
        })
      })

      if (response.ok) {
        setNoteForm({ source: 'claude', title: '', content: '', url: '' })
        setShowNoteForm(false)
        fetchProject()
      }
    } catch (error) {
      console.error('Error adding note:', error)
    }
  }

  const handleUpdateProject = async (updates: Partial<Project>) => {
    try {
      const response = await fetch(`/api/projects/${params.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      })

      if (response.ok) {
        fetchProject()
      }
    } catch (error) {
      console.error('Error updating project:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-xl text-gray-600 dark:text-gray-400">Loading project...</div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl text-gray-600 dark:text-gray-400 mb-4">Project not found</div>
          <Link href="/dashboard" className="btn btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <nav className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white">
              Multi-Project Dashboard
            </Link>
            <Link href="/dashboard" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
              Dashboard
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link href="/dashboard" className="text-blue-600 hover:underline text-sm">
            ← Back to Dashboard
          </Link>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="card">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {project.name}
                  </h1>
                  {project.description && (
                    <p className="text-gray-600 dark:text-gray-400">{project.description}</p>
                  )}
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-4">
                <select
                  className="badge cursor-pointer"
                  value={project.status}
                  onChange={(e) => handleUpdateProject({ status: e.target.value })}
                >
                  <option value="active">Active</option>
                  <option value="paused">Paused</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>

                <select
                  className="badge cursor-pointer"
                  value={project.priority}
                  onChange={(e) => handleUpdateProject({ priority: e.target.value })}
                >
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>

                {project.language && (
                  <span className="badge badge-info">{project.language}</span>
                )}
              </div>

              {project.githubUrl && (
                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">GitHub:</span>
                    <a
                      href={project.githubUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      View Repository →
                    </a>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Stars:</span>
                    <span className="text-gray-900 dark:text-white">⭐ {project.stars}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Open Issues:</span>
                    <span className="text-gray-900 dark:text-white">{project.openIssues}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Open PRs:</span>
                    <span className="text-gray-900 dark:text-white">{project.openPRs}</span>
                  </div>
                  {project.lastCommitDate && (
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Last Commit:</span>
                      <span className="text-gray-900 dark:text-white">
                        {getRelativeTime(project.lastCommitDate)}
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Research Notes ({project.researchNotes.length})
                </h2>
                <button
                  onClick={() => setShowNoteForm(!showNoteForm)}
                  className="btn btn-primary text-sm"
                >
                  {showNoteForm ? 'Cancel' : '+ Add Note'}
                </button>
              </div>

              {showNoteForm && (
                <form onSubmit={handleAddNote} className="mb-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg space-y-3">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
                      Source
                    </label>
                    <select
                      className="input"
                      value={noteForm.source}
                      onChange={(e) => setNoteForm({ ...noteForm, source: e.target.value })}
                      required
                    >
                      <option value="claude">Claude</option>
                      <option value="chatgpt">ChatGPT</option>
                      <option value="gemini">Gemini</option>
                      <option value="perplexity">Perplexity</option>
                      <option value="genspark">Genspark</option>
                      <option value="notion">Notion</option>
                      <option value="files">Files</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
                      Title
                    </label>
                    <input
                      type="text"
                      className="input"
                      value={noteForm.title}
                      onChange={(e) => setNoteForm({ ...noteForm, title: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
                      Content
                    </label>
                    <textarea
                      className="input"
                      rows={4}
                      value={noteForm.content}
                      onChange={(e) => setNoteForm({ ...noteForm, content: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
                      URL (optional)
                    </label>
                    <input
                      type="url"
                      className="input"
                      value={noteForm.url}
                      onChange={(e) => setNoteForm({ ...noteForm, url: e.target.value })}
                    />
                  </div>
                  <button type="submit" className="btn btn-primary w-full">
                    Save Note
                  </button>
                </form>
              )}

              {project.researchNotes.length === 0 ? (
                <p className="text-gray-600 dark:text-gray-400 text-center py-8">
                  No research notes yet. Add your first note!
                </p>
              ) : (
                <div className="space-y-4">
                  {project.researchNotes.map((note) => (
                    <div key={note.id} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-gray-900 dark:text-white">{note.title}</h3>
                        <span className="badge badge-info text-xs">{note.source}</span>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2 whitespace-pre-wrap">
                        {note.content}
                      </p>
                      {note.url && (
                        <a
                          href={note.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-600 hover:underline"
                        >
                          View source →
                        </a>
                      )}
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                        {formatDateTime(note.createdAt)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="space-y-6">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                Recent Activity
              </h2>
              {project.activities.length === 0 ? (
                <p className="text-gray-600 dark:text-gray-400 text-sm">No recent activity</p>
              ) : (
                <div className="space-y-3">
                  {project.activities.map((activity) => (
                    <div key={activity.id} className="pb-3 border-b border-gray-200 dark:border-gray-700 last:border-0">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {activity.description}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {getRelativeTime(activity.createdAt)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
