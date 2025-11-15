'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { formatDate, getRelativeTime, getStatusColor, getPriorityColor } from '@/lib/utils'

interface Project {
  id: string
  name: string
  description: string | null
  githubUrl: string | null
  status: string
  priority: string
  lastCommitDate: string | null
  openIssues: number
  openPRs: number
  stars: number
  language: string | null
  tags: string | null
  updatedAt: string
  researchNotes: any[]
}

export default function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState({
    status: '',
    priority: '',
    search: ''
  })
  const [syncing, setSyncing] = useState(false)

  useEffect(() => {
    fetchProjects()
  }, [filter])

  const fetchProjects = async () => {
    try {
      const params = new URLSearchParams()
      if (filter.status) params.append('status', filter.status)
      if (filter.priority) params.append('priority', filter.priority)
      if (filter.search) params.append('search', filter.search)

      const response = await fetch(`/api/projects?${params}`)
      const data = await response.json()
      setProjects(data)
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSync = async () => {
    try {
      setSyncing(true)
      const settingsResponse = await fetch('/api/settings')
      const settings = await settingsResponse.json()

      if (!settings.githubToken || !settings.githubUsername) {
        alert('Please configure GitHub settings first')
        window.location.href = '/settings'
        return
      }

      const response = await fetch('/api/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          githubToken: settings.githubToken,
          githubUsername: settings.githubUsername
        })
      })

      const result = await response.json()
      if (result.success) {
        alert(`Synced ${result.totalRepos} repositories (${result.created} new, ${result.updated} updated)`)
        fetchProjects()
      } else {
        alert(`Sync failed: ${result.error}`)
      }
    } catch (error) {
      console.error('Sync error:', error)
      alert('Failed to sync repositories')
    } finally {
      setSyncing(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-xl text-gray-600 dark:text-gray-400">Loading projects...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <nav className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white">
                Multi-Project Dashboard
              </Link>
              <Link href="/dashboard" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                Dashboard
              </Link>
              <Link href="/settings" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                Settings
              </Link>
            </div>
            <button
              onClick={handleSync}
              disabled={syncing}
              className="btn btn-primary disabled:opacity-50"
            >
              {syncing ? 'Syncing...' : 'Sync GitHub'}
            </button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-6 flex flex-wrap gap-4">
          <input
            type="text"
            placeholder="Search projects..."
            className="input flex-1 min-w-[200px]"
            value={filter.search}
            onChange={(e) => setFilter({ ...filter, search: e.target.value })}
          />
          <select
            className="input w-40"
            value={filter.status}
            onChange={(e) => setFilter({ ...filter, status: e.target.value })}
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="paused">Paused</option>
            <option value="completed">Completed</option>
            <option value="archived">Archived</option>
          </select>
          <select
            className="input w-40"
            value={filter.priority}
            onChange={(e) => setFilter({ ...filter, priority: e.target.value })}
          >
            <option value="">All Priority</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
          Showing {projects.length} project{projects.length !== 1 ? 's' : ''}
        </div>

        {projects.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              No projects found. Click "Sync GitHub" to import your repositories.
            </p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Link
                key={project.id}
                href={`/projects/${project.id}`}
                className="card hover:shadow-lg transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
                    {project.name}
                  </h3>
                  <div className="flex gap-2">
                    <span className={`badge ${getStatusColor(project.status)}`}>
                      {project.status}
                    </span>
                  </div>
                </div>

                {project.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                    {project.description}
                  </p>
                )}

                <div className="flex flex-wrap gap-2 mb-4">
                  <span className={`badge ${getPriorityColor(project.priority)}`}>
                    {project.priority}
                  </span>
                  {project.language && (
                    <span className="badge badge-info">{project.language}</span>
                  )}
                </div>

                <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
                  {project.githubUrl && (
                    <div className="flex items-center justify-between">
                      <span>GitHub:</span>
                      <span className="flex items-center gap-2">
                        <span>⭐ {project.stars}</span>
                        <span>Issues: {project.openIssues}</span>
                        <span>PRs: {project.openPRs}</span>
                      </span>
                    </div>
                  )}
                  {project.lastCommitDate && (
                    <div className="flex justify-between">
                      <span>Last commit:</span>
                      <span>{getRelativeTime(project.lastCommitDate)}</span>
                    </div>
                  )}
                  {project.researchNotes.length > 0 && (
                    <div className="flex justify-between">
                      <span>Research notes:</span>
                      <span>{project.researchNotes.length}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span>Updated:</span>
                    <span>{getRelativeTime(project.updatedAt)}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
