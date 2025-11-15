'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    githubToken: '',
    githubUsername: '',
    notionToken: '',
    defaultView: 'grid'
  })
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const response = await fetch('/api/settings')
      const data = await response.json()
      setSettings({
        githubToken: data.githubToken || '',
        githubUsername: data.githubUsername || '',
        notionToken: data.notionToken || '',
        defaultView: data.defaultView || 'grid'
      })
    } catch (error) {
      console.error('Error fetching settings:', error)
    }
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setMessage('')

    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      })

      if (response.ok) {
        setMessage('Settings saved successfully!')
      } else {
        setMessage('Failed to save settings')
      }
    } catch (error) {
      console.error('Error saving settings:', error)
      setMessage('Failed to save settings')
    } finally {
      setSaving(false)
    }
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
            <Link href="/settings" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
              Settings
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <h1 className="text-3xl font-bold mb-8 text-gray-900 dark:text-white">Settings</h1>

        <form onSubmit={handleSave} className="space-y-6">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">GitHub Configuration</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  GitHub Username
                </label>
                <input
                  type="text"
                  className="input"
                  value={settings.githubUsername}
                  onChange={(e) => setSettings({ ...settings, githubUsername: e.target.value })}
                  placeholder="your-github-username"
                />
                <p className="mt-1 text-xs text-gray-500">Your GitHub username for syncing repositories</p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  GitHub Personal Access Token
                </label>
                <input
                  type="password"
                  className="input"
                  value={settings.githubToken}
                  onChange={(e) => setSettings({ ...settings, githubToken: e.target.value })}
                  placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Create a token at{' '}
                  <a
                    href="https://github.com/settings/tokens"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    github.com/settings/tokens
                  </a>
                  {' '}with 'repo' scope
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              Notion Integration (Optional)
            </h2>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                Notion Integration Token
              </label>
              <input
                type="password"
                className="input"
                value={settings.notionToken}
                onChange={(e) => setSettings({ ...settings, notionToken: e.target.value })}
                placeholder="secret_xxxxxxxxxxxxxxxxxxxx"
              />
              <p className="mt-1 text-xs text-gray-500">
                For future Notion integration (coming soon)
              </p>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Display Preferences</h2>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                Default View
              </label>
              <select
                className="input"
                value={settings.defaultView}
                onChange={(e) => setSettings({ ...settings, defaultView: e.target.value })}
              >
                <option value="grid">Grid</option>
                <option value="list">List</option>
                <option value="kanban">Kanban (Coming Soon)</option>
              </select>
            </div>
          </div>

          {message && (
            <div className={`p-4 rounded-md ${
              message.includes('success')
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
            }`}>
              {message}
            </div>
          )}

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={saving}
              className="btn btn-primary flex-1 disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Settings'}
            </button>
            <Link href="/dashboard" className="btn btn-secondary flex-1 text-center">
              Cancel
            </Link>
          </div>
        </form>

        <div className="mt-8 card bg-blue-50 dark:bg-blue-900">
          <h3 className="font-semibold mb-2 text-blue-900 dark:text-blue-100">Getting Started</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm text-blue-800 dark:text-blue-200">
            <li>Create a GitHub Personal Access Token</li>
            <li>Enter your GitHub username and token above</li>
            <li>Click "Save Settings"</li>
            <li>Go to Dashboard and click "Sync GitHub"</li>
            <li>Your repositories will be imported automatically</li>
          </ol>
        </div>
      </div>
    </div>
  )
}
