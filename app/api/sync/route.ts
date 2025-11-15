import { NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { GitHubAPI } from '@/lib/github'
import { parseGitHubUrl } from '@/lib/utils'

export async function POST(request: Request) {
  try {
    const { githubToken, githubUsername } = await request.json()

    if (!githubToken || !githubUsername) {
      return NextResponse.json(
        { error: 'GitHub token and username are required' },
        { status: 400 }
      )
    }

    const github = new GitHubAPI(githubToken)
    const repos = await github.getAllUserRepos(githubUsername)

    let createdCount = 0
    let updatedCount = 0

    for (const repo of repos) {
      try {
        // Get latest commit
        const commits = await github.getRepoCommits(repo.owner.login, repo.name, 1)
        const latestCommit = commits[0]

        // Get open PRs
        const openPRs = await github.getRepoPullRequests(repo.owner.login, repo.name, 'open')

        const projectData = {
          name: repo.name,
          description: repo.description,
          githubUrl: repo.html_url,
          githubOwner: repo.owner.login,
          githubRepo: repo.name,
          lastCommitDate: latestCommit ? new Date(latestCommit.commit.author.date) : null,
          lastCommitSha: latestCommit?.sha,
          openIssues: repo.open_issues_count,
          openPRs: openPRs.length,
          stars: repo.stargazers_count,
          language: repo.language,
          lastSyncedAt: new Date(),
        }

        // Check if project exists
        const existingProject = await db.project.findFirst({
          where: {
            OR: [
              { githubUrl: repo.html_url },
              {
                AND: [
                  { githubOwner: repo.owner.login },
                  { githubRepo: repo.name }
                ]
              }
            ]
          }
        })

        if (existingProject) {
          await db.project.update({
            where: { id: existingProject.id },
            data: projectData
          })

          // Log activity
          await db.activity.create({
            data: {
              projectId: existingProject.id,
              type: 'sync',
              description: 'Project synced from GitHub'
            }
          })

          updatedCount++
        } else {
          const newProject = await db.project.create({
            data: projectData
          })

          // Log activity
          await db.activity.create({
            data: {
              projectId: newProject.id,
              type: 'sync',
              description: 'Project created from GitHub'
            }
          })

          createdCount++
        }
      } catch (error) {
        console.error(`Error syncing repo ${repo.name}:`, error)
        // Continue with other repos
      }
    }

    return NextResponse.json({
      success: true,
      totalRepos: repos.length,
      created: createdCount,
      updated: updatedCount
    })
  } catch (error) {
    console.error('Sync error:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to sync repositories' },
      { status: 500 }
    )
  }
}
