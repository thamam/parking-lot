import type { WizardData, ToolSummary } from '../types';

export const generatePrompt = (data: WizardData): string => {
  let prompt = `# MCP Server Implementation Specification

You are tasked with implementing an MCP (Model Context Protocol) server with the following complete specification.

## Server Overview

**Name:** ${data.serverIdentity.name}

**Description:** ${data.serverIdentity.description}

**Primary Use Cases:**
${data.serverIdentity.useCases.split('\n').map(uc => `- ${uc}`).join('\n')}

**Data Sources:**
${data.serverIdentity.dataSources.map(ds => `- ${ds}`).join('\n')}

---

## Tools Implementation

`;

  // Add each tool's details
  data.toolsSummary.forEach((tool: ToolSummary) => {
    const details = data.toolsDetails[tool.id];

    prompt += `### Tool: ${tool.name}

**Category:** ${tool.category}

**Description:** ${details?.detailedDescription || tool.description}

**Input Schema:**
\`\`\`typescript
{
${details?.parameters.map(p =>
  `  ${p.name}: {
    type: "${p.type}",
    required: ${p.required},
    description: "${p.description}",
    constraints: "${p.constraints}"
  }`
).join(',\n')}
}
\`\`\`

**Output Schema:**
\`\`\`json
${details?.outputFormat || '{}'}
\`\`\`

${details?.errorCases && details.errorCases.length > 0 ? `**Error Handling:**
${details.errorCases.map(ec => `- **${ec.scenario}:** ${ec.handling}`).join('\n')}
` : ''}
---

`;
  });

  // Resources section
  if (data.resources.enabled) {
    prompt += `## Resources

This MCP server provides resources accessible via URI patterns.

**URI Patterns:**
${data.resources.uriPatterns.map(pattern => `- \`${pattern}\``).join('\n')}

**Content Types:**
${data.resources.contentTypes.map(ct => `- ${ct}`).join('\n')}

**Example URIs:**
${data.resources.exampleUris.map(uri => `- \`${uri}\``).join('\n')}

---

`;
  }

  // Prompts section
  if (data.prompts.enabled && data.prompts.templates.length > 0) {
    prompt += `## Prompt Templates

${data.prompts.templates.map(pt => `### ${pt.name}

**Template:** ${pt.template}

**Arguments:** ${pt.arguments}

**Use Case:** ${pt.useCase}
`).join('\n')}

---

`;
  }

  // Integration Details
  prompt += `## Integration Details

### External APIs

${data.dataFlow.externalAPIs.map(api => `- **${api.name}:** \`${api.endpoint}\``).join('\n')}

### Authentication

**Method:** ${data.dataFlow.authMethod}
${data.dataFlow.apiKeyFields ? `\n**API Key Fields:** ${data.dataFlow.apiKeyFields}` : ''}

### Rate Limits

${data.dataFlow.rateLimits}

### Data Transformations

${data.dataFlow.dataTransformation}

---

## Configuration

### Environment Variables

${data.configuration.envVariables.map(env => `- **${env.name}:** ${env.description}`).join('\n')}

### Dependencies

\`\`\`json
{
${data.configuration.dependencies.map(dep => `  "${dep.packageName}": "${dep.version}"`).join(',\n')}
}
\`\`\`

### Installation Requirements

${data.configuration.installationRequirements}

### Setup Instructions

${data.configuration.setupSteps.map((step, idx) => `${idx + 1}. ${step.step}`).join('\n')}

---

## Error Handling Strategy

### Error Scenarios

${data.errorHandling.errorScenarios.map(es => `- **${es.scenario}:** ${es.fallback}`).join('\n')}

### Validation Rules

${data.errorHandling.validationRules.map(vr => `- ${vr.rule}`).join('\n')}

### Timeout Settings

${data.errorHandling.timeout}

### Retry Strategy

${data.errorHandling.retryStrategy}

---

## Example Interactions

${data.examples.scenarios.map(scenario => `### ${scenario.description}

**Input:**
\`\`\`json
${scenario.inputExample}
\`\`\`

**Tools Used:** ${scenario.toolsUsed.map(toolId => {
  const tool = data.toolsSummary.find(t => t.id === toolId);
  return tool ? tool.name : toolId;
}).join(', ')}

**Expected Output:**
\`\`\`json
${scenario.expectedOutput}
\`\`\`
`).join('\n')}

---

## Test Suite

### Test Cases

${data.testing.testCases.map(tc => `#### ${tc.testDescription}

**Tool:** ${tc.toolName}

**Input:**
\`\`\`json
${tc.inputData}
\`\`\`

**Expected Output:**
${tc.expectedOutput}
`).join('\n')}

### Success Criteria

${data.testing.successCriteria}

---

## Implementation Instructions

Please implement this MCP server using **FastMCP (Python)** or **MCP SDK (TypeScript)** based on your preference and the project requirements.

Ensure the implementation includes:

1. **Complete error handling** for all specified error scenarios
2. **Comprehensive logging** for debugging and monitoring
3. **Input validation** according to the specified rules
4. **Rate limiting** and retry logic as specified
5. **All test cases** passing
6. **Proper MCP protocol compliance**
7. **Clear documentation** for setup and usage

Follow MCP best practices and ensure the server is production-ready.
`;

  return prompt;
};

export const downloadPrompt = (prompt: string, serverName: string): void => {
  const blob = new Blob([prompt], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  const fileName = serverName || 'mcp-server';
  link.download = `${fileName}-specification-${new Date().toISOString().split('T')[0]}.md`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
