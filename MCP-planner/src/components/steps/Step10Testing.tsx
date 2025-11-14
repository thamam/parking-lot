import React, { useState } from 'react';
import type { Testing, TestCase, ToolSummary, WizardData } from '../../types';

interface Step10Props {
  data: Testing;
  tools: ToolSummary[];
  wizardData: WizardData;
  onChange: (data: Testing) => void;
  onGeneratePrompt: () => void;
}

const Step10Testing: React.FC<Step10Props> = ({
  data,
  tools,
  wizardData,
  onChange,
  onGeneratePrompt,
}) => {
  const [newTest, setNewTest] = useState({
    toolName: '',
    testDescription: '',
    inputData: '',
    expectedOutput: '',
  });
  const [activeTab, setActiveTab] = useState<'tests' | 'review'>('tests');

  const addTest = () => {
    if (newTest.toolName && newTest.testDescription) {
      const test: TestCase = {
        id: Date.now().toString(),
        ...newTest,
      };
      onChange({
        ...data,
        testCases: [...data.testCases, test],
      });
      setNewTest({
        toolName: '',
        testDescription: '',
        inputData: '',
        expectedOutput: '',
      });
    }
  };

  const removeTest = (id: string) => {
    onChange({
      ...data,
      testCases: data.testCases.filter((t) => t.id !== id),
    });
  };

  const updateTest = (id: string, updates: Partial<TestCase>) => {
    onChange({
      ...data,
      testCases: data.testCases.map((t) =>
        t.id === id ? { ...t, ...updates } : t
      ),
    });
  };

  const getSummary = () => {
    const summary = {
      serverName: wizardData.serverIdentity.name,
      tools: wizardData.toolsSummary.length,
      dataSources: wizardData.serverIdentity.dataSources.length,
      hasResources: wizardData.resources.enabled,
      hasPrompts: wizardData.prompts.enabled,
      externalAPIs: wizardData.dataFlow.externalAPIs.length,
      errorScenarios: wizardData.errorHandling.errorScenarios.length,
      examples: wizardData.examples.scenarios.length,
      envVariables: wizardData.configuration.envVariables.length,
      dependencies: wizardData.configuration.dependencies.length,
      testCases: data.testCases.length,
    };
    return summary;
  };

  const summary = getSummary();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Testing & Review
        </h2>
        <p className="text-gray-600">
          Add test cases and review your complete MCP specification.
        </p>
      </div>

      <div className="flex gap-4 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('tests')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'tests'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Test Cases
        </button>
        <button
          onClick={() => setActiveTab('review')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'review'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Review Summary
        </button>
      </div>

      {activeTab === 'tests' && (
        <>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Add New Test Case
            </h3>
            <div className="space-y-3">
              <select
                value={newTest.toolName}
                onChange={(e) =>
                  setNewTest({ ...newTest, toolName: e.target.value })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select a tool...</option>
                {tools.map((tool) => (
                  <option key={tool.id} value={tool.name}>
                    {tool.name}
                  </option>
                ))}
              </select>
              <input
                type="text"
                value={newTest.testDescription}
                onChange={(e) =>
                  setNewTest({ ...newTest, testDescription: e.target.value })
                }
                placeholder="Test description (e.g., Should return weather data for valid location)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <textarea
                value={newTest.inputData}
                onChange={(e) =>
                  setNewTest({ ...newTest, inputData: e.target.value })
                }
                placeholder='Input data (JSON):&#10;{ "location": "London" }'
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
              />
              <textarea
                value={newTest.expectedOutput}
                onChange={(e) =>
                  setNewTest({ ...newTest, expectedOutput: e.target.value })
                }
                placeholder="Expected output description"
                rows={2}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={addTest}
                disabled={!newTest.toolName || !newTest.testDescription}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                + Add Test Case
              </button>
            </div>
          </div>

          {data.testCases.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Test Cases ({data.testCases.length})
              </h3>
              {data.testCases.map((test) => (
                <div
                  key={test.id}
                  className="bg-white border border-gray-200 rounded-lg p-4 space-y-3"
                >
                  <div className="flex justify-between items-start">
                    <select
                      value={test.toolName}
                      onChange={(e) =>
                        updateTest(test.id, { toolName: e.target.value })
                      }
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      {tools.map((tool) => (
                        <option key={tool.id} value={tool.name}>
                          {tool.name}
                        </option>
                      ))}
                    </select>
                    <button
                      type="button"
                      onClick={() => removeTest(test.id)}
                      className="ml-4 text-red-600 hover:text-red-800 font-medium"
                    >
                      Remove
                    </button>
                  </div>
                  <input
                    type="text"
                    value={test.testDescription}
                    onChange={(e) =>
                      updateTest(test.id, {
                        testDescription: e.target.value,
                      })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <textarea
                    value={test.inputData}
                    onChange={(e) =>
                      updateTest(test.id, { inputData: e.target.value })
                    }
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                  />
                  <textarea
                    value={test.expectedOutput}
                    onChange={(e) =>
                      updateTest(test.id, { expectedOutput: e.target.value })
                    }
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  />
                </div>
              ))}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Success Criteria
            </label>
            <textarea
              value={data.successCriteria}
              onChange={(e) =>
                onChange({ ...data, successCriteria: e.target.value })
              }
              placeholder="Define what success looks like (e.g., All tools return expected formats, Error handling works correctly, API rate limits are respected)"
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </>
      )}

      {activeTab === 'review' && (
        <>
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              {summary.serverName || 'Unnamed MCP Server'}
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-blue-600">
                  {summary.tools}
                </div>
                <div className="text-sm text-gray-600">Tools</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-green-600">
                  {summary.dataSources}
                </div>
                <div className="text-sm text-gray-600">Data Sources</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-purple-600">
                  {summary.examples}
                </div>
                <div className="text-sm text-gray-600">Examples</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-orange-600">
                  {summary.testCases}
                </div>
                <div className="text-sm text-gray-600">Test Cases</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-red-600">
                  {summary.errorScenarios}
                </div>
                <div className="text-sm text-gray-600">Error Scenarios</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-indigo-600">
                  {summary.dependencies}
                </div>
                <div className="text-sm text-gray-600">Dependencies</div>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">Features</h4>
              <ul className="space-y-1 text-sm text-gray-600">
                <li>
                  {summary.hasResources ? '✅' : '❌'} Resources enabled
                </li>
                <li>
                  {summary.hasPrompts ? '✅' : '❌'} Prompt templates
                </li>
                <li>
                  {summary.externalAPIs > 0 ? '✅' : '❌'} External API integration
                </li>
                <li>
                  {summary.envVariables > 0 ? '✅' : '❌'} Environment configuration
                </li>
              </ul>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">
                Quick Summary
              </h4>
              <p className="text-sm text-gray-600">
                {wizardData.serverIdentity.description ||
                  'No description provided'}
              </p>
            </div>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-green-900 mb-3">
              Ready to Generate! 🎉
            </h3>
            <p className="text-green-800 mb-4">
              Your MCP specification is complete. Click the button below to
              generate a comprehensive implementation prompt.
            </p>
            <button
              onClick={onGeneratePrompt}
              className="w-full px-6 py-4 bg-green-600 text-white text-lg font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-lg"
            >
              🚀 Generate Implementation Prompt
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Step10Testing;
