export interface GitHubRepo {
  id: number
  name: string
  full_name: string
  description: string | null
  html_url: string
  language: string | null
  stargazers_count: number
  open_issues_count: number
  updated_at: string
  pushed_at: string
  owner: {
    login: string
  }
}

export interface GitHubCommit {
  sha: string
  commit: {
    message: string
    author: {
      name: string
      date: string
    }
  }
}

export interface GitHubPullRequest {
  id: number
  number: number
  title: string
  state: string
  html_url: string
}

export class GitHubAPI {
  private token: string
  private baseUrl = 'https://api.github.com'

  constructor(token: string) {
    this.token = token
  }

  private async fetch(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText }))
      throw new Error(`GitHub API error: ${error.message || response.statusText}`)
    }

    return response.json()
  }

  async getUserRepos(username: string, page = 1, perPage = 100): Promise<GitHubRepo[]> {
    return this.fetch(`/users/${username}/repos?page=${page}&per_page=${perPage}&sort=updated`)
  }

  async getAllUserRepos(username: string): Promise<GitHubRepo[]> {
    const repos: GitHubRepo[] = []
    let page = 1
    const perPage = 100

    while (true) {
      const pageRepos = await this.getUserRepos(username, page, perPage)
      repos.push(...pageRepos)

      if (pageRepos.length < perPage) {
        break
      }
      page++
    }

    return repos
  }

  async getRepoCommits(owner: string, repo: string, perPage = 1): Promise<GitHubCommit[]> {
    return this.fetch(`/repos/${owner}/${repo}/commits?per_page=${perPage}`)
  }

  async getRepoPullRequests(owner: string, repo: string, state = 'open'): Promise<GitHubPullRequest[]> {
    return this.fetch(`/repos/${owner}/${repo}/pulls?state=${state}`)
  }

  async getRepo(owner: string, repo: string): Promise<GitHubRepo> {
    return this.fetch(`/repos/${owner}/${repo}`)
  }
}
