import React, { useState } from 'react';
import type { Examples, ExampleScenario, ToolSummary } from '../../types';

interface Step8Props {
  data: Examples;
  tools: ToolSummary[];
  onChange: (data: Examples) => void;
}

const Step8Examples: React.FC<Step8Props> = ({ data, tools, onChange }) => {
  const [newExample, setNewExample] = useState({
    description: '',
    inputExample: '',
    toolsUsed: [] as string[],
    expectedOutput: '',
  });

  const addExample = () => {
    if (newExample.description && newExample.inputExample) {
      const example: ExampleScenario = {
        id: Date.now().toString(),
        ...newExample,
      };
      onChange({
        ...data,
        scenarios: [...data.scenarios, example],
      });
      setNewExample({
        description: '',
        inputExample: '',
        toolsUsed: [],
        expectedOutput: '',
      });
    }
  };

  const removeExample = (id: string) => {
    onChange({
      ...data,
      scenarios: data.scenarios.filter((s) => s.id !== id),
    });
  };

  const updateExample = (id: string, updates: Partial<ExampleScenario>) => {
    onChange({
      ...data,
      scenarios: data.scenarios.map((s) =>
        s.id === id ? { ...s, ...updates } : s
      ),
    });
  };

  const toggleTool = (exampleId: string, toolId: string) => {
    const example = data.scenarios.find((s) => s.id === exampleId);
    if (!example) return;

    const toolsUsed = example.toolsUsed.includes(toolId)
      ? example.toolsUsed.filter((t) => t !== toolId)
      : [...example.toolsUsed, toolId];

    updateExample(exampleId, { toolsUsed });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Example Interactions
        </h2>
        <p className="text-gray-600">
          Provide concrete examples of how your MCP server will be used.
        </p>
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Add New Example
        </h3>
        <div className="space-y-3">
          <input
            type="text"
            value={newExample.description}
            onChange={(e) =>
              setNewExample({ ...newExample, description: e.target.value })
            }
            placeholder="Example description (e.g., Get current weather for Tokyo)"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <textarea
            value={newExample.inputExample}
            onChange={(e) =>
              setNewExample({ ...newExample, inputExample: e.target.value })
            }
            placeholder='Input example (JSON format):&#10;{&#10;  "location": "Tokyo",&#10;  "units": "metric"&#10;}'
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
          />
          <textarea
            value={newExample.expectedOutput}
            onChange={(e) =>
              setNewExample({ ...newExample, expectedOutput: e.target.value })
            }
            placeholder='Expected output (JSON format):&#10;{&#10;  "temperature": 18,&#10;  "conditions": "Cloudy"&#10;}'
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
          />
          <button
            type="button"
            onClick={addExample}
            disabled={!newExample.description || !newExample.inputExample}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            + Add Example
          </button>
        </div>
      </div>

      {data.scenarios.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Examples ({data.scenarios.length})
          </h3>
          {data.scenarios.map((example) => (
            <div
              key={example.id}
              className="bg-white border border-gray-200 rounded-lg p-4 space-y-3"
            >
              <div className="flex justify-between items-start">
                <input
                  type="text"
                  value={example.description}
                  onChange={(e) =>
                    updateExample(example.id, { description: e.target.value })
                  }
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg font-medium"
                />
                <button
                  type="button"
                  onClick={() => removeExample(example.id)}
                  className="ml-4 text-red-600 hover:text-red-800 font-medium"
                >
                  Remove
                </button>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Input Example
                </label>
                <textarea
                  value={example.inputExample}
                  onChange={(e) =>
                    updateExample(example.id, { inputExample: e.target.value })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                />
              </div>

              {tools.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tools Used
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {tools.map((tool) => (
                      <button
                        key={tool.id}
                        type="button"
                        onClick={() => toggleTool(example.id, tool.id)}
                        className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                          example.toolsUsed.includes(tool.id)
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                      >
                        {tool.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Expected Output
                </label>
                <textarea
                  value={example.expectedOutput}
                  onChange={(e) =>
                    updateExample(example.id, {
                      expectedOutput: e.target.value,
                    })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {data.scenarios.length === 0 && (
        <div className="text-center py-12 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-gray-500">
            No examples added yet. Add your first example above!
          </p>
        </div>
      )}
    </div>
  );
};

export default Step8Examples;
