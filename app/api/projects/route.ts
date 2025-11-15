import { NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const status = searchParams.get('status')
    const priority = searchParams.get('priority')
    const search = searchParams.get('search')
    const language = searchParams.get('language')

    const where: any = {}

    if (status) where.status = status
    if (priority) where.priority = priority
    if (language) where.language = language
    if (search) {
      where.OR = [
        { name: { contains: search, mode: 'insensitive' } },
        { description: { contains: search, mode: 'insensitive' } },
      ]
    }

    const projects = await db.project.findMany({
      where,
      include: {
        researchNotes: {
          orderBy: { createdAt: 'desc' },
          take: 5
        },
        activities: {
          orderBy: { createdAt: 'desc' },
          take: 5
        }
      },
      orderBy: { updatedAt: 'desc' }
    })

    return NextResponse.json(projects)
  } catch (error) {
    console.error('Error fetching projects:', error)
    return NextResponse.json(
      { error: 'Failed to fetch projects' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const data = await request.json()

    const project = await db.project.create({
      data: {
        name: data.name,
        description: data.description,
        githubUrl: data.githubUrl,
        status: data.status || 'active',
        priority: data.priority || 'medium',
        tags: data.tags ? JSON.stringify(data.tags) : null
      }
    })

    await db.activity.create({
      data: {
        projectId: project.id,
        type: 'note',
        description: 'Project created'
      }
    })

    return NextResponse.json(project)
  } catch (error) {
    console.error('Error creating project:', error)
    return NextResponse.json(
      { error: 'Failed to create project' },
      { status: 500 }
    )
  }
}
