export function formatDate(date: Date | string | null): string {
  if (!date) return 'Never'
  const d = new Date(date)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export function formatDateTime(date: Date | string | null): string {
  if (!date) return 'Never'
  const d = new Date(date)
  return d.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export function getRelativeTime(date: Date | string | null): string {
  if (!date) return 'Never'

  const now = new Date()
  const then = new Date(date)
  const seconds = Math.floor((now.getTime() - then.getTime()) / 1000)

  if (seconds < 60) return 'just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`
  if (seconds < 2592000) return `${Math.floor(seconds / 604800)}w ago`
  if (seconds < 31536000) return `${Math.floor(seconds / 2592000)}mo ago`
  return `${Math.floor(seconds / 31536000)}y ago`
}

export function parseGitHubUrl(url: string): { owner: string; repo: string } | null {
  try {
    const match = url.match(/github\.com\/([^\/]+)\/([^\/]+)/)
    if (match) {
      return { owner: match[1], repo: match[2].replace(/\.git$/, '') }
    }
  } catch (e) {
    // ignore
  }
  return null
}

export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'active': return 'badge-success'
    case 'paused': return 'badge-warning'
    case 'completed': return 'badge-info'
    case 'archived': return 'badge-danger'
    default: return 'badge-info'
  }
}

export function getPriorityColor(priority: string): string {
  switch (priority.toLowerCase()) {
    case 'critical': return 'badge-danger'
    case 'high': return 'badge-warning'
    case 'medium': return 'badge-info'
    case 'low': return 'badge-success'
    default: return 'badge-info'
  }
}
