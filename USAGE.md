# Usage Guide: Multi-Project Dashboard

## Quick Start Walkthrough

### Step 1: Initial Setup (5 minutes)

1. **Start the application**:
   ```bash
   npm run dev
   ```
   Open http://localhost:3000 in your browser.

2. **Get a GitHub Token**:
   - Visit https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Give it a name like "Multi-Project Dashboard"
   - Select scope: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

3. **Configure Settings**:
   - In the app, go to "Settings"
   - Enter your GitHub username (e.g., `thamam`)
   - Paste your GitHub Personal Access Token
   - Click "Save Settings"

### Step 2: Import Your Repositories (2 minutes)

1. Go to "Dashboard"
2. Click "Sync GitHub" button
3. Wait for the sync to complete (may take 30-60 seconds for 80 repos)
4. You'll see a success message with the number of repos synced
5. Your dashboard will now show all your repositories!

### Step 3: Organize Your Projects

#### Set Status

For each project, you can set its status:
- **Active**: Currently working on it
- **Paused**: Temporarily stopped
- **Completed**: Finished
- **Archived**: No longer maintained

#### Set Priority

Mark projects by importance:
- **Critical**: Urgent, high-impact projects
- **High**: Important projects
- **Medium**: Regular priority
- **Low**: Nice-to-have or experimental

#### Filter & Search

Use the dashboard filters to:
- Search by project name or description
- Filter by status (e.g., show only "Active" projects)
- Filter by priority (e.g., show only "Critical" and "High")
- Combine filters for powerful queries

### Step 4: Track Your Research

This is where the dashboard becomes powerful for multi-context work!

#### Adding Research Notes

1. Click on any project
2. Click "+ Add Note"
3. Select the source where you did the research:
   - **Claude**: Claude.ai conversations
   - **ChatGPT**: ChatGPT conversations
   - **Gemini**: Google Gemini chats
   - **Perplexity**: Perplexity AI searches
   - **Genspark**: Genspark research
   - **Notion**: Notion notes
   - **Files**: Local files or documents
   - **Other**: Any other source

4. Add a descriptive title
5. Paste or type your notes
6. Optionally add a URL (link to the AI chat, Notion page, etc.)
7. Click "Save Note"

#### Example Workflow

Let's say you're working on a React project:

1. **Day 1 - Research in Claude**:
   - Have a conversation with Claude about best practices
   - Go to your project in the dashboard
   - Add a note:
     - Source: Claude
     - Title: "React State Management Best Practices"
     - Content: [Key insights from the conversation]
     - URL: [Link to Claude chat if available]

2. **Day 2 - Research in Perplexity**:
   - Search for latest React hooks patterns
   - Add another note:
     - Source: Perplexity
     - Title: "Latest React Hooks Patterns 2024"
     - Content: [Summary of findings]
     - URL: [Perplexity search URL]

3. **Day 3 - Code in GitHub**:
   - Push commits to GitHub
   - Sync the dashboard to see updated commit info
   - All your research notes are still there!

Now you have a complete history of your research and development in one place.

## Advanced Usage

### Managing 80+ Repositories

With many repositories, organization is key:

1. **Initial Triage** (first time):
   - Sync all repos
   - Go through each one
   - Set accurate status (many are probably "Archived")
   - Set priorities
   - This takes time but only needs to be done once

2. **Daily Workflow**:
   - Filter by "Active" status to see current projects
   - Filter by "Critical" or "High" priority for important work
   - Use search to quickly find specific projects

3. **Weekly Review**:
   - Click "Sync GitHub" to update all repos
   - Review activity timeline
   - Update statuses as needed

### Cross-Project Research

Sometimes research applies to multiple projects:

1. Create research notes on each relevant project
2. Reference the same URL in all notes
3. Use consistent titles/tags
4. This way you can track which projects share common research

### Activity Timeline

Every project has an activity timeline showing:
- When it was synced from GitHub
- When notes were added
- When status/priority changed

This helps you see what you've been working on recently.

### Using with Notion

While Notion integration isn't built yet, you can still track Notion research:

1. When you write notes in Notion about a project
2. Add a research note with:
   - Source: Notion
   - Title: Same as Notion page title
   - Content: Summary or key points
   - URL: Link to Notion page

This creates a two-way reference between Notion and your dashboard.

## Tips & Best Practices

### Research Note Organization

- **Be specific in titles**: "React Context API pitfalls" not just "React notes"
- **Include dates if relevant**: "Migration plan - Nov 2024"
- **Always add URLs**: Makes it easy to revisit the original source
- **Use consistent source labeling**: Pick one name and stick with it

### Project Status Guidelines

- **Active**: Working on it this week/month
- **Paused**: Planning to resume, just not now
- **Completed**: It's done and deployed/released
- **Archived**: Not touching it anymore, but keep for reference

### Priority Guidelines

- **Critical**: Revenue-impacting or time-sensitive
- **High**: Important for growth or learning
- **Medium**: Regular work
- **Low**: Experiments or "someday" projects

### Syncing Strategy

- Sync GitHub weekly (or before important reviews)
- Don't sync too often (you'll see duplicate activities)
- Sync when you want updated commit/issue/PR counts

### Search Tips

The search box searches both:
- Project names
- Project descriptions

Make sure your GitHub repo descriptions are good!

## Common Workflows

### Starting a New Project

1. Create repo on GitHub
2. Sync dashboard
3. New project appears
4. Set status to "Active"
5. Set appropriate priority
6. Start adding research notes as you work

### Pausing a Project

1. Find the project
2. Click into it
3. Change status to "Paused"
4. Add a research note explaining why/when you'll resume

### Completing a Project

1. Change status to "Completed"
2. Add a final research note with:
   - Lessons learned
   - Final stats/metrics
   - Links to deployment, docs, etc.

### Reviewing Work

1. Filter by "Active" + "High" priority
2. Review each project's latest commits
3. Check if any need attention
4. Update priorities as needed

## Keyboard & Navigation Tips

- Use browser back/forward to navigate between projects
- Cmd/Ctrl+Click to open projects in new tabs
- Use browser find (Cmd/Ctrl+F) within long notes

## Data Export

Currently, data is in your local SQLite database at `prisma/dev.db`.

To backup or export:
```bash
# Backup database
cp prisma/dev.db prisma/backup-$(date +%Y%m%d).db

# Open in Prisma Studio to view/export
npm run db:studio
```

## Troubleshooting Common Issues

### "No projects found"

- Make sure you've configured GitHub settings
- Click "Sync GitHub"
- Check that your GitHub username is correct

### Sync takes a long time

- Normal for 80+ repos (may take 1-2 minutes)
- The app is fetching data for each repo
- Be patient, it will complete

### Research note didn't save

- Make sure all required fields are filled
- Title and content are required
- Try again or refresh the page

### Can't find a specific project

- Use the search box
- Try filtering by status
- Click "Sync GitHub" to import recent repos

## Getting Help

- Check the README.md for technical documentation
- Review this guide for usage questions
- Check your browser console for errors (F12)
- Verify your GitHub token is valid

## Next Steps

Once you're comfortable with the basics:
- Experiment with different filtering combinations
- Develop a consistent note-taking system
- Create a weekly review routine
- Consider customizing the code for your specific needs

Happy project tracking!
