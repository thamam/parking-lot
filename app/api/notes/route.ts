import { NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function POST(request: Request) {
  try {
    const data = await request.json()

    const note = await db.researchNote.create({
      data: {
        projectId: data.projectId,
        source: data.source,
        title: data.title,
        content: data.content,
        url: data.url,
        tags: data.tags ? JSON.stringify(data.tags) : null
      }
    })

    await db.activity.create({
      data: {
        projectId: data.projectId,
        type: 'note',
        description: `Research note added from ${data.source}`
      }
    })

    return NextResponse.json(note)
  } catch (error) {
    console.error('Error creating note:', error)
    return NextResponse.json(
      { error: 'Failed to create note' },
      { status: 500 }
    )
  }
}
