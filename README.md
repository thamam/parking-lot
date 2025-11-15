# Multi-Project Dashboard

A comprehensive dashboard for managing multiple GitHub repositories and research notes across various AI platforms and tools.

## Features

- **GitHub Integration**: Automatically sync all your GitHub repositories
- **Multi-Source Research Tracking**: Track research and notes from:
  - Claude
  - ChatGPT
  - Gemini
  - Perplexity
  - Genspark
  - Notion
  - Local files
  - Other sources
- **Project Management**:
  - Status tracking (Active, Paused, Completed, Archived)
  - Priority levels (Critical, High, Medium, Low)
  - Custom tags
- **GitHub Metrics**:
  - Stars, issues, and pull requests
  - Last commit information
  - Repository language
- **Activity Timeline**: Track all changes and updates to your projects
- **Advanced Filtering**: Filter by status, priority, language, or search
- **Responsive UI**: Clean, modern interface with dark mode support

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Database**: SQLite with Prisma ORM
- **Styling**: Tailwind CSS
- **API Integration**: GitHub REST API

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- GitHub account
- GitHub Personal Access Token

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd parking-lot
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Initialize the database:
   ```bash
   npm run db:push
   ```

4. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

### Configuration

1. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes:
     - `repo` (for private repos) or `public_repo` (for public repos only)
   - Copy the token

2. Configure the application:
   - Start the development server: `npm run dev`
   - Open http://localhost:3000
   - Navigate to Settings
   - Enter your GitHub username
   - Paste your GitHub Personal Access Token
   - Click "Save Settings"

3. Sync your repositories:
   - Go to Dashboard
   - Click "Sync GitHub"
   - Wait for the sync to complete
   - Your repositories will now appear on the dashboard

## Usage

### Dashboard

The main dashboard displays all your projects with:
- Project name and description
- Status and priority badges
- GitHub metrics (stars, issues, PRs)
- Last commit information
- Research notes count

**Filtering**: Use the filters at the top to filter by status, priority, or search for specific projects.

### Project Details

Click on any project to view:
- Full project information
- All research notes
- Activity timeline
- Quick status/priority updates

### Adding Research Notes

On any project page:
1. Click "+ Add Note"
2. Select the source (Claude, ChatGPT, etc.)
3. Enter a title and content
4. Optionally add a URL reference
5. Click "Save Note"

This is perfect for tracking:
- AI-generated insights
- Research findings
- Meeting notes
- Development decisions
- Links to relevant resources

### Syncing Repositories

The dashboard doesn't automatically sync. To update your repositories:
1. Go to Dashboard
2. Click "Sync GitHub"
3. The sync will:
   - Import new repositories
   - Update existing repositories
   - Fetch latest commit information
   - Update issue and PR counts

## Database Schema

The application uses SQLite with the following models:

- **Project**: Main project information and GitHub data
- **ResearchNote**: Research notes from various sources
- **Activity**: Timeline of project activities
- **Settings**: User configuration

## API Routes

- `POST /api/sync` - Sync GitHub repositories
- `GET /api/projects` - Get all projects (with filters)
- `POST /api/projects` - Create a new project
- `GET /api/projects/[id]` - Get project details
- `PATCH /api/projects/[id]` - Update project
- `DELETE /api/projects/[id]` - Delete project
- `POST /api/notes` - Create research note
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings

## Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Open Prisma Studio (database GUI)
npm run db:studio
```

## Project Structure

```
parking-lot/
├── app/                      # Next.js app directory
│   ├── api/                  # API routes
│   │   ├── notes/           # Research notes endpoints
│   │   ├── projects/        # Project endpoints
│   │   ├── settings/        # Settings endpoints
│   │   └── sync/            # GitHub sync endpoint
│   ├── dashboard/           # Dashboard page
│   ├── projects/[id]/       # Project detail page
│   ├── settings/            # Settings page
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── lib/                      # Utility libraries
│   ├── db.ts                # Prisma client
│   ├── github.ts            # GitHub API wrapper
│   └── utils.ts             # Helper functions
├── prisma/                   # Database
│   ├── schema.prisma        # Database schema
│   └── dev.db               # SQLite database
└── package.json             # Dependencies
```

## Future Enhancements

- [ ] Notion API integration for bi-directional sync
- [ ] Kanban board view
- [ ] Advanced analytics and charts
- [ ] Export projects to various formats
- [ ] Team collaboration features
- [ ] Webhook support for real-time GitHub updates
- [ ] Custom automation rules
- [ ] Multi-user support
- [ ] Mobile app

## Troubleshooting

### Sync Fails

- Verify your GitHub token is valid
- Check that you have the correct scopes (repo or public_repo)
- Ensure your GitHub username is correct

### Database Issues

Reset the database:
```bash
rm prisma/dev.db
npm run db:push
```

### Build Errors

Clear cache and reinstall:
```bash
rm -rf .next node_modules
npm install
npm run dev
```

## Security

- Never commit your `.env` file
- Keep your GitHub token secure
- The token is stored in the local SQLite database
- Consider using environment variables for production deployments

## Contributing

This is a POC project. Feel free to fork and customize for your needs!

## License

MIT