import type { WizardData } from '../types';

const STORAGE_KEY = 'mcp-planner-data';
const CURRENT_STEP_KEY = 'mcp-planner-current-step';

export const saveWizardData = (data: WizardData): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (error) {
    console.error('Error saving wizard data:', error);
  }
};

export const loadWizardData = (): WizardData | null => {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Error loading wizard data:', error);
    return null;
  }
};

export const clearWizardData = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(CURRENT_STEP_KEY);
  } catch (error) {
    console.error('Error clearing wizard data:', error);
  }
};

export const saveCurrentStep = (step: number): void => {
  try {
    localStorage.setItem(CURRENT_STEP_KEY, step.toString());
  } catch (error) {
    console.error('Error saving current step:', error);
  }
};

export const loadCurrentStep = (): number => {
  try {
    const step = localStorage.getItem(CURRENT_STEP_KEY);
    return step ? parseInt(step, 10) : 1;
  } catch (error) {
    console.error('Error loading current step:', error);
    return 1;
  }
};

export const hasExistingData = (): boolean => {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return !!data;
  } catch (error) {
    return false;
  }
};

export const exportWizardData = (data: WizardData): void => {
  const dataStr = JSON.stringify(data, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `mcp-planner-${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export const importWizardData = (file: File): Promise<WizardData> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target?.result as string);
        resolve(data);
      } catch (error) {
        reject(new Error('Invalid JSON file'));
      }
    };
    reader.onerror = () => reject(new Error('Error reading file'));
    reader.readAsText(file);
  });
};

export const getExampleData = (): WizardData => {
  return {
    serverIdentity: {
      name: 'weather-mcp',
      description: 'A Model Context Protocol server that provides real-time weather information and forecasts',
      useCases: 'Get current weather conditions\nGet weather forecasts\nGet weather alerts\nSearch locations by coordinates',
      dataSources: ['OpenWeatherMap API', 'Weather.gov API', 'GeoNames'],
    },
    toolsSummary: [
      {
        id: '1',
        name: 'get_current_weather',
        description: 'Retrieves current weather conditions for a location',
        category: 'Weather Data',
      },
      {
        id: '2',
        name: 'get_forecast',
        description: 'Gets weather forecast for the next 7 days',
        category: 'Weather Data',
      },
      {
        id: '3',
        name: 'search_location',
        description: 'Searches for a location by name or coordinates',
        category: 'Location',
      },
    ],
    toolsDetails: {
      '1': {
        id: '1',
        detailedDescription: 'Fetches current weather data including temperature, humidity, wind speed, and conditions for a specified location. Uses OpenWeatherMap API for accurate real-time data.',
        parameters: [
          {
            id: 'p1',
            name: 'location',
            type: 'string',
            required: true,
            description: 'City name, zip code, or coordinates',
            constraints: 'Non-empty string, max 100 characters',
          },
          {
            id: 'p2',
            name: 'units',
            type: 'string',
            required: false,
            description: 'Temperature units (metric, imperial, kelvin)',
            constraints: 'Must be one of: metric, imperial, kelvin',
          },
        ],
        outputFormat: '{\n  "temperature": 72,\n  "conditions": "Clear",\n  "humidity": 65,\n  "windSpeed": 8.5,\n  "location": "San Francisco, CA"\n}',
        errorCases: [
          {
            id: 'e1',
            scenario: 'Location not found',
            handling: 'Return error with suggestions for similar locations',
          },
          {
            id: 'e2',
            scenario: 'API rate limit exceeded',
            handling: 'Return cached data if available, otherwise error message',
          },
        ],
      },
      '2': {
        id: '2',
        detailedDescription: 'Provides a 7-day weather forecast with daily high/low temperatures and conditions.',
        parameters: [
          {
            id: 'p3',
            name: 'location',
            type: 'string',
            required: true,
            description: 'City name or coordinates',
            constraints: 'Non-empty string',
          },
        ],
        outputFormat: '{\n  "forecast": [\n    {\n      "date": "2025-11-15",\n      "high": 75,\n      "low": 62,\n      "conditions": "Sunny"\n    }\n  ]\n}',
        errorCases: [],
      },
      '3': {
        id: '3',
        detailedDescription: 'Searches for locations by name and returns coordinates and metadata.',
        parameters: [
          {
            id: 'p4',
            name: 'query',
            type: 'string',
            required: true,
            description: 'Location search query',
            constraints: 'Min 2 characters',
          },
        ],
        outputFormat: '{\n  "results": [\n    {\n      "name": "San Francisco",\n      "country": "US",\n      "lat": 37.7749,\n      "lon": -122.4194\n    }\n  ]\n}',
        errorCases: [],
      },
    },
    resources: {
      enabled: true,
      uriPatterns: ['weather://{location}/current', 'weather://{location}/forecast'],
      contentTypes: ['application/json'],
      exampleUris: ['weather://san-francisco/current', 'weather://london/forecast'],
    },
    prompts: {
      enabled: true,
      templates: [
        {
          id: 't1',
          name: 'weather_summary',
          template: 'Provide a natural language summary of the weather in {location}',
          arguments: 'location: string',
          useCase: 'Generate human-readable weather summaries',
        },
      ],
    },
    dataFlow: {
      externalAPIs: [
        {
          id: 'api1',
          name: 'OpenWeatherMap',
          endpoint: 'https://api.openweathermap.org/data/2.5',
        },
      ],
      authMethod: 'api-key',
      apiKeyFields: 'OPENWEATHER_API_KEY',
      rateLimits: '60 calls per minute, 1000 calls per day',
      dataTransformation: 'Convert Kelvin to requested units, normalize condition codes to human-readable strings',
    },
    errorHandling: {
      errorScenarios: [
        {
          id: 's1',
          scenario: 'Network timeout',
          fallback: 'Return cached data with warning',
        },
      ],
      validationRules: [
        {
          id: 'v1',
          rule: 'Validate location string is not empty',
        },
      ],
      timeout: '5000ms',
      retryStrategy: 'Exponential backoff: 1s, 2s, 4s',
    },
    examples: {
      scenarios: [
        {
          id: 'ex1',
          description: 'Get current weather for a city',
          inputExample: '{\n  "location": "Tokyo",\n  "units": "metric"\n}',
          toolsUsed: ['get_current_weather'],
          expectedOutput: '{\n  "temperature": 18,\n  "conditions": "Cloudy",\n  "humidity": 70,\n  "windSpeed": 12.3\n}',
        },
      ],
    },
    configuration: {
      envVariables: [
        {
          id: 'env1',
          name: 'OPENWEATHER_API_KEY',
          description: 'API key for OpenWeatherMap service',
        },
      ],
      dependencies: [
        {
          id: 'dep1',
          packageName: 'axios',
          version: '^1.6.0',
        },
      ],
      installationRequirements: 'Node.js 18+, npm or yarn',
      setupSteps: [
        {
          id: 'step1',
          step: 'Install dependencies: npm install',
        },
        {
          id: 'step2',
          step: 'Set OPENWEATHER_API_KEY environment variable',
        },
      ],
    },
    testing: {
      testCases: [
        {
          id: 'test1',
          toolName: 'get_current_weather',
          testDescription: 'Should return weather data for valid location',
          inputData: '{ "location": "London", "units": "metric" }',
          expectedOutput: 'Object with temperature, conditions, humidity, windSpeed fields',
        },
      ],
      successCriteria: 'All tools return expected data formats. Error handling works for invalid inputs. API rate limits are respected.',
    },
  };
};
