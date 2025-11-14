# MCP Planner

A comprehensive web application for planning and generating Model Context Protocol (MCP) server specifications through an interactive 10-step wizard.

## Overview

MCP Planner helps you systematically capture all information needed to build a complete MCP server. It guides you through defining tools, resources, prompts, error handling, configuration, and testing - then generates a detailed specification document ready for implementation.

## Features

### Interactive 10-Step Wizard

1. **Server Identity & Purpose** - Define your MCP server's name, description, use cases, and data sources
2. **Tools Discovery** - List all tools your server will provide
3. **Tool Details** - Configure parameters, output formats, and error handling for each tool
4. **Resources** - Define URI patterns and resource types (optional)
5. **Prompts/Templates** - Create reusable prompt templates (optional)
6. **Data Flow Mapping** - Configure external APIs, authentication, and rate limits
7. **Error Handling** - Define error scenarios, validation rules, timeouts, and retry strategies
8. **Example Interactions** - Provide concrete usage examples with expected outputs
9. **Configuration & Setup** - Specify environment variables, dependencies, and setup steps
10. **Testing & Review** - Add test cases and review your complete specification

### Key Capabilities

- **Auto-save to localStorage** - Never lose your progress
- **Import/Export** - Save your work as JSON and share with others
- **Example Data** - Load a pre-filled weather MCP example to see how it works
- **Prompt Generation** - Generate a comprehensive markdown specification document
- **Copy & Download** - Copy to clipboard or download as `.md` file
- **Validation** - Required fields ensure you don't miss critical information
- **Responsive Design** - Works on desktop and mobile

## Getting Started

### Installation

```bash
# Navigate to the MCP-planner directory
cd MCP-planner

# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for fast development and building
- **localStorage API** for data persistence
- No backend required - fully client-side

## Project Structure

```
MCP-planner/
├── src/
│   ├── components/
│   │   ├── Wizard.tsx              # Main orchestrator
│   │   ├── Navigation.tsx          # Navigation controls
│   │   ├── ProgressBar.tsx         # Progress indicator
│   │   ├── DynamicList.tsx         # Reusable list component
│   │   ├── OutputModal.tsx         # Display generated prompt
│   │   └── steps/
│   │       ├── Step1ServerIdentity.tsx
│   │       ├── Step2ToolsDiscovery.tsx
│   │       ├── Step3ToolDetails.tsx
│   │       ├── Step4Resources.tsx
│   │       ├── Step5Prompts.tsx
│   │       ├── Step6DataFlow.tsx
│   │       ├── Step7ErrorHandling.tsx
│   │       ├── Step8Examples.tsx
│   │       ├── Step9Configuration.tsx
│   │       └── Step10Testing.tsx
│   ├── utils/
│   │   ├── storage.ts              # localStorage helpers
│   │   └── promptGenerator.ts      # Generate specification
│   ├── types.ts                    # TypeScript interfaces
│   ├── App.tsx
│   └── main.tsx
├── package.json
└── README.md
```

## Usage Guide

### Starting a New Project

1. Launch the application
2. Click "Start Fresh" if prompted about previous session
3. Fill in each step of the wizard
4. Use "Next" and "Previous" buttons to navigate
5. Click "Save & Exit" to save your progress at any time

### Loading an Example

Click "Load Example Data" to see a complete weather MCP server specification. This is helpful for understanding how to structure your own MCP server.

### Generating the Specification

1. Complete all 10 steps
2. On Step 10, click "Review Summary" to see an overview
3. Click "Generate Implementation Prompt"
4. Copy to clipboard or download the markdown file
5. Use this specification to implement your MCP server

### Tips

- **Be Specific**: Detailed descriptions generate better implementation code
- **Add Examples**: Concrete examples help clarify expected behavior
- **Define Error Cases**: Think through what can go wrong
- **Test Cases**: Add comprehensive test cases for quality assurance

## Generated Output

The wizard generates a complete markdown specification including:

- Server overview and purpose
- Complete tool definitions with input/output schemas
- Resource URI patterns and examples
- Prompt templates
- External API integration details
- Authentication configuration
- Error handling strategies
- Example interactions
- Environment setup instructions
- Test suite with success criteria
- Implementation instructions

## Data Persistence

All data is automatically saved to your browser's localStorage:

- **Auto-save** on every change
- **Resume sessions** when you return
- **Export to JSON** for backup
- **Import from JSON** to restore or share

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

Requires localStorage support.

## Contributing

This is a standalone web application. To make improvements:

1. Make your changes
2. Test with `npm run dev`
3. Build with `npm run build`
4. Commit and push

## License

This project is part of the parking-lot repository.

## About MCP

Model Context Protocol (MCP) is a protocol for providing context to AI models. An MCP server exposes:

- **Tools** - Functions the AI can call
- **Resources** - Data accessible via URIs
- **Prompts** - Reusable templates

Learn more at: https://modelcontextprotocol.io

---

Built with ❤️ using React, TypeScript, and Tailwind CSS
