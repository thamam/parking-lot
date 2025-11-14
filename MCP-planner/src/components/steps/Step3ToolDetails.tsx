import React, { useState } from 'react';
import type { ToolSummary, ToolDetails, ToolParameter, ErrorCase } from '../../types';

interface Step3Props {
  tools: ToolSummary[];
  toolsDetails: { [toolId: string]: ToolDetails };
  onChange: (toolsDetails: { [toolId: string]: ToolDetails }) => void;
}

const Step3ToolDetails: React.FC<Step3Props> = ({
  tools,
  toolsDetails,
  onChange,
}) => {
  const [currentToolIndex, setCurrentToolIndex] = useState(0);

  if (tools.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">
          No tools to configure. Please add tools in Step 2 first.
        </p>
      </div>
    );
  }

  const currentTool = tools[currentToolIndex];
  const details = toolsDetails[currentTool.id] || {
    id: currentTool.id,
    detailedDescription: '',
    parameters: [],
    outputFormat: '',
    errorCases: [],
  };

  const updateDetails = (updates: Partial<ToolDetails>) => {
    onChange({
      ...toolsDetails,
      [currentTool.id]: { ...details, ...updates },
    });
  };

  const addParameter = () => {
    const newParam: ToolParameter = {
      id: Date.now().toString(),
      name: '',
      type: 'string',
      required: false,
      description: '',
      constraints: '',
    };
    updateDetails({ parameters: [...details.parameters, newParam] });
  };

  const updateParameter = (id: string, updates: Partial<ToolParameter>) => {
    updateDetails({
      parameters: details.parameters.map((p) =>
        p.id === id ? { ...p, ...updates } : p
      ),
    });
  };

  const removeParameter = (id: string) => {
    updateDetails({
      parameters: details.parameters.filter((p) => p.id !== id),
    });
  };

  const addErrorCase = () => {
    const newError: ErrorCase = {
      id: Date.now().toString(),
      scenario: '',
      handling: '',
    };
    updateDetails({ errorCases: [...details.errorCases, newError] });
  };

  const updateErrorCase = (id: string, updates: Partial<ErrorCase>) => {
    updateDetails({
      errorCases: details.errorCases.map((e) =>
        e.id === id ? { ...e, ...updates } : e
      ),
    });
  };

  const removeErrorCase = (id: string) => {
    updateDetails({
      errorCases: details.errorCases.filter((e) => e.id !== id),
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Tool Details</h2>
        <p className="text-gray-600">
          Configuring: <strong>{currentTool.name}</strong>
        </p>
        <p className="text-sm text-gray-500 mt-1">
          Tool {currentToolIndex + 1} of {tools.length}
        </p>
      </div>

      {tools.length > 1 && (
        <div className="flex gap-2 flex-wrap">
          {tools.map((tool, index) => (
            <button
              key={tool.id}
              onClick={() => setCurrentToolIndex(index)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                index === currentToolIndex
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {tool.name}
            </button>
          ))}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Detailed Description <span className="text-red-500">*</span>
        </label>
        <textarea
          value={details.detailedDescription}
          onChange={(e) =>
            updateDetails({ detailedDescription: e.target.value })
          }
          placeholder="Provide a comprehensive description of what this tool does, how it works, and any important details..."
          rows={4}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg font-semibold text-gray-900">Parameters</h3>
          <button
            type="button"
            onClick={addParameter}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            + Add Parameter
          </button>
        </div>

        {details.parameters.length > 0 ? (
          <div className="space-y-3">
            {details.parameters.map((param) => (
              <div
                key={param.id}
                className="bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-3"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1 grid grid-cols-2 gap-3">
                    <input
                      type="text"
                      value={param.name}
                      onChange={(e) =>
                        updateParameter(param.id, { name: e.target.value })
                      }
                      placeholder="Parameter name"
                      className="px-3 py-2 border border-gray-300 rounded-lg"
                    />
                    <select
                      value={param.type}
                      onChange={(e) =>
                        updateParameter(param.id, {
                          type: e.target.value as ToolParameter['type'],
                        })
                      }
                      className="px-3 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="string">String</option>
                      <option value="number">Number</option>
                      <option value="boolean">Boolean</option>
                      <option value="array">Array</option>
                      <option value="object">Object</option>
                    </select>
                    <input
                      type="text"
                      value={param.description}
                      onChange={(e) =>
                        updateParameter(param.id, {
                          description: e.target.value,
                        })
                      }
                      placeholder="Description"
                      className="px-3 py-2 border border-gray-300 rounded-lg"
                    />
                    <input
                      type="text"
                      value={param.constraints}
                      onChange={(e) =>
                        updateParameter(param.id, {
                          constraints: e.target.value,
                        })
                      }
                      placeholder="Constraints (e.g., max 100 chars)"
                      className="px-3 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div className="ml-4 flex flex-col gap-2">
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={param.required}
                        onChange={(e) =>
                          updateParameter(param.id, {
                            required: e.target.checked,
                          })
                        }
                        className="rounded"
                      />
                      <span className="text-sm">Required</span>
                    </label>
                    <button
                      type="button"
                      onClick={() => removeParameter(param.id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">No parameters added yet.</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Output Format (JSON example)
        </label>
        <textarea
          value={details.outputFormat}
          onChange={(e) => updateDetails({ outputFormat: e.target.value })}
          placeholder={'{\n  "result": "...",\n  "data": {...}\n}'}
          rows={6}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
        />
      </div>

      <div>
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg font-semibold text-gray-900">Error Cases</h3>
          <button
            type="button"
            onClick={addErrorCase}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            + Add Error Case
          </button>
        </div>

        {details.errorCases.length > 0 ? (
          <div className="space-y-3">
            {details.errorCases.map((error) => (
              <div
                key={error.id}
                className="bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-3"
              >
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={error.scenario}
                    onChange={(e) =>
                      updateErrorCase(error.id, { scenario: e.target.value })
                    }
                    placeholder="Error scenario"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => removeErrorCase(error.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </div>
                <input
                  type="text"
                  value={error.handling}
                  onChange={(e) =>
                    updateErrorCase(error.id, { handling: e.target.value })
                  }
                  placeholder="How to handle this error"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">No error cases defined yet.</p>
        )}
      </div>
    </div>
  );
};

export default Step3ToolDetails;
