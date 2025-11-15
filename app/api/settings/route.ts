import { NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET() {
  try {
    let settings = await db.settings.findUnique({
      where: { id: 'settings' }
    })

    if (!settings) {
      settings = await db.settings.create({
        data: { id: 'settings' }
      })
    }

    return NextResponse.json(settings)
  } catch (error) {
    console.error('Error fetching settings:', error)
    return NextResponse.json(
      { error: 'Failed to fetch settings' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const data = await request.json()

    const settings = await db.settings.upsert({
      where: { id: 'settings' },
      update: {
        githubToken: data.githubToken,
        githubUsername: data.githubUsername,
        notionToken: data.notionToken,
        defaultView: data.defaultView
      },
      create: {
        id: 'settings',
        githubToken: data.githubToken,
        githubUsername: data.githubUsername,
        notionToken: data.notionToken,
        defaultView: data.defaultView || 'grid'
      }
    })

    return NextResponse.json(settings)
  } catch (error) {
    console.error('Error updating settings:', error)
    return NextResponse.json(
      { error: 'Failed to update settings' },
      { status: 500 }
    )
  }
}
