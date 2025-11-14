// Step 1: Server Identity & Purpose
export interface ServerIdentity {
  name: string;
  description: string;
  useCases: string;
  dataSources: string[];
}

// Step 2: Tools Discovery
export interface ToolSummary {
  id: string;
  name: string;
  description: string;
  category: string;
}

// Step 3: Tool Details
export interface ToolParameter {
  id: string;
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array' | 'object';
  required: boolean;
  description: string;
  constraints: string;
}

export interface ErrorCase {
  id: string;
  scenario: string;
  handling: string;
}

export interface ToolDetails {
  id: string;
  detailedDescription: string;
  parameters: ToolParameter[];
  outputFormat: string;
  errorCases: ErrorCase[];
}

// Step 4: Resources
export interface Resources {
  enabled: boolean;
  uriPatterns: string[];
  contentTypes: string[];
  exampleUris: string[];
}

// Step 5: Prompts/Templates
export interface PromptTemplate {
  id: string;
  name: string;
  template: string;
  arguments: string;
  useCase: string;
}

export interface Prompts {
  enabled: boolean;
  templates: PromptTemplate[];
}

// Step 6: Data Flow Mapping
export interface ExternalAPI {
  id: string;
  name: string;
  endpoint: string;
}

export interface DataFlow {
  externalAPIs: ExternalAPI[];
  authMethod: 'none' | 'api-key' | 'oauth' | 'bearer' | 'custom';
  apiKeyFields: string;
  rateLimits: string;
  dataTransformation: string;
}

// Step 7: Error Handling & Edge Cases
export interface ErrorScenario {
  id: string;
  scenario: string;
  fallback: string;
}

export interface ValidationRule {
  id: string;
  rule: string;
}

export interface ErrorHandling {
  errorScenarios: ErrorScenario[];
  validationRules: ValidationRule[];
  timeout: string;
  retryStrategy: string;
}

// Step 8: Example Interactions
export interface ExampleScenario {
  id: string;
  description: string;
  inputExample: string;
  toolsUsed: string[];
  expectedOutput: string;
}

export interface Examples {
  scenarios: ExampleScenario[];
}

// Step 9: Configuration & Setup
export interface EnvVariable {
  id: string;
  name: string;
  description: string;
}

export interface Dependency {
  id: string;
  packageName: string;
  version: string;
}

export interface SetupStep {
  id: string;
  step: string;
}

export interface Configuration {
  envVariables: EnvVariable[];
  dependencies: Dependency[];
  installationRequirements: string;
  setupSteps: SetupStep[];
}

// Step 10: Testing & Validation
export interface TestCase {
  id: string;
  toolName: string;
  testDescription: string;
  inputData: string;
  expectedOutput: string;
}

export interface Testing {
  testCases: TestCase[];
  successCriteria: string;
}

// Complete wizard data
export interface WizardData {
  serverIdentity: ServerIdentity;
  toolsSummary: ToolSummary[];
  toolsDetails: { [toolId: string]: ToolDetails };
  resources: Resources;
  prompts: Prompts;
  dataFlow: DataFlow;
  errorHandling: ErrorHandling;
  examples: Examples;
  configuration: Configuration;
  testing: Testing;
}

// Initial empty state
export const initialWizardData: WizardData = {
  serverIdentity: {
    name: '',
    description: '',
    useCases: '',
    dataSources: [],
  },
  toolsSummary: [],
  toolsDetails: {},
  resources: {
    enabled: false,
    uriPatterns: [],
    contentTypes: [],
    exampleUris: [],
  },
  prompts: {
    enabled: false,
    templates: [],
  },
  dataFlow: {
    externalAPIs: [],
    authMethod: 'none',
    apiKeyFields: '',
    rateLimits: '',
    dataTransformation: '',
  },
  errorHandling: {
    errorScenarios: [],
    validationRules: [],
    timeout: '',
    retryStrategy: '',
  },
  examples: {
    scenarios: [],
  },
  configuration: {
    envVariables: [],
    dependencies: [],
    installationRequirements: '',
    setupSteps: [],
  },
  testing: {
    testCases: [],
    successCriteria: '',
  },
};
