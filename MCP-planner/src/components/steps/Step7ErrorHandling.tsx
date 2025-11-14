import React, { useState } from 'react';
import type { ErrorHandling, ErrorScenario, ValidationRule } from '../../types';

interface Step7Props {
  data: ErrorHandling;
  onChange: (data: ErrorHandling) => void;
}

const Step7ErrorHandling: React.FC<Step7Props> = ({ data, onChange }) => {
  const [newScenario, setNewScenario] = useState({ scenario: '', fallback: '' });
  const [newRule, setNewRule] = useState('');

  const addScenario = () => {
    if (newScenario.scenario && newScenario.fallback) {
      const scenario: ErrorScenario = {
        id: Date.now().toString(),
        ...newScenario,
      };
      onChange({
        ...data,
        errorScenarios: [...data.errorScenarios, scenario],
      });
      setNewScenario({ scenario: '', fallback: '' });
    }
  };

  const removeScenario = (id: string) => {
    onChange({
      ...data,
      errorScenarios: data.errorScenarios.filter((s) => s.id !== id),
    });
  };

  const updateScenario = (id: string, updates: Partial<ErrorScenario>) => {
    onChange({
      ...data,
      errorScenarios: data.errorScenarios.map((s) =>
        s.id === id ? { ...s, ...updates } : s
      ),
    });
  };

  const addRule = () => {
    if (newRule.trim()) {
      const rule: ValidationRule = {
        id: Date.now().toString(),
        rule: newRule.trim(),
      };
      onChange({
        ...data,
        validationRules: [...data.validationRules, rule],
      });
      setNewRule('');
    }
  };

  const removeRule = (id: string) => {
    onChange({
      ...data,
      validationRules: data.validationRules.filter((r) => r.id !== id),
    });
  };

  const updateRule = (id: string, ruleText: string) => {
    onChange({
      ...data,
      validationRules: data.validationRules.map((r) =>
        r.id === id ? { ...r, rule: ruleText } : r
      ),
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Error Handling & Edge Cases
        </h2>
        <p className="text-gray-600">
          Define how your MCP server should handle errors and validate inputs.
        </p>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Error Scenarios
        </h3>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
          <div className="space-y-3">
            <input
              type="text"
              value={newScenario.scenario}
              onChange={(e) =>
                setNewScenario({ ...newScenario, scenario: e.target.value })
              }
              placeholder="Error scenario (e.g., Network timeout, API rate limit)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={newScenario.fallback}
              onChange={(e) =>
                setNewScenario({ ...newScenario, fallback: e.target.value })
              }
              placeholder="Fallback behavior (e.g., Return cached data)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="button"
              onClick={addScenario}
              disabled={!newScenario.scenario || !newScenario.fallback}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              + Add Error Scenario
            </button>
          </div>
        </div>

        {data.errorScenarios.length > 0 && (
          <div className="space-y-2">
            {data.errorScenarios.map((scenario) => (
              <div
                key={scenario.id}
                className="bg-white border border-gray-200 rounded-lg p-3 space-y-2"
              >
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={scenario.scenario}
                    onChange={(e) =>
                      updateScenario(scenario.id, { scenario: e.target.value })
                    }
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => removeScenario(scenario.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </div>
                <input
                  type="text"
                  value={scenario.fallback}
                  onChange={(e) =>
                    updateScenario(scenario.id, { fallback: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  placeholder="Fallback behavior"
                />
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Validation Rules
        </h3>
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={newRule}
            onChange={(e) => setNewRule(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addRule()}
            placeholder="Validation rule (e.g., Email must be valid format)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="button"
            onClick={addRule}
            disabled={!newRule.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            + Add
          </button>
        </div>

        {data.validationRules.length > 0 && (
          <div className="space-y-2">
            {data.validationRules.map((rule) => (
              <div
                key={rule.id}
                className="bg-white border border-gray-200 rounded-lg p-3 flex gap-3"
              >
                <input
                  type="text"
                  value={rule.rule}
                  onChange={(e) => updateRule(rule.id, e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                />
                <button
                  type="button"
                  onClick={() => removeRule(rule.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Timeout Settings
        </label>
        <input
          type="text"
          value={data.timeout}
          onChange={(e) => onChange({ ...data, timeout: e.target.value })}
          placeholder="e.g., 5000ms, 30 seconds"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Retry Strategy
        </label>
        <input
          type="text"
          value={data.retryStrategy}
          onChange={(e) =>
            onChange({ ...data, retryStrategy: e.target.value })
          }
          placeholder="e.g., Exponential backoff: 1s, 2s, 4s, max 3 retries"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <h4 className="font-medium text-yellow-900 mb-2">⚠️ Important</h4>
        <p className="text-sm text-yellow-800">
          Good error handling is crucial for a robust MCP server. Consider all
          possible failure scenarios including network issues, invalid inputs,
          and API failures.
        </p>
      </div>
    </div>
  );
};

export default Step7ErrorHandling;
