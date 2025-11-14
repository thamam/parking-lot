import React, { useState } from 'react';
import type { DataFlow, ExternalAPI } from '../../types';

interface Step6Props {
  data: DataFlow;
  onChange: (data: DataFlow) => void;
}

const Step6DataFlow: React.FC<Step6Props> = ({ data, onChange }) => {
  const [newAPI, setNewAPI] = useState({ name: '', endpoint: '' });

  const addAPI = () => {
    if (newAPI.name && newAPI.endpoint) {
      const api: ExternalAPI = {
        id: Date.now().toString(),
        ...newAPI,
      };
      onChange({
        ...data,
        externalAPIs: [...data.externalAPIs, api],
      });
      setNewAPI({ name: '', endpoint: '' });
    }
  };

  const removeAPI = (id: string) => {
    onChange({
      ...data,
      externalAPIs: data.externalAPIs.filter((api) => api.id !== id),
    });
  };

  const updateAPI = (id: string, updates: Partial<ExternalAPI>) => {
    onChange({
      ...data,
      externalAPIs: data.externalAPIs.map((api) =>
        api.id === id ? { ...api, ...updates } : api
      ),
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Data Flow Mapping
        </h2>
        <p className="text-gray-600">
          Configure how your MCP server connects to external services and transforms data.
        </p>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          External APIs / Services
        </h3>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={newAPI.name}
              onChange={(e) => setNewAPI({ ...newAPI, name: e.target.value })}
              placeholder="API name (e.g., OpenWeatherMap)"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={newAPI.endpoint}
              onChange={(e) =>
                setNewAPI({ ...newAPI, endpoint: e.target.value })
              }
              placeholder="Base endpoint URL"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="button"
              onClick={addAPI}
              disabled={!newAPI.name || !newAPI.endpoint}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              + Add
            </button>
          </div>
        </div>

        {data.externalAPIs.length > 0 && (
          <div className="space-y-2">
            {data.externalAPIs.map((api) => (
              <div
                key={api.id}
                className="bg-white border border-gray-200 rounded-lg p-3 flex gap-3"
              >
                <input
                  type="text"
                  value={api.name}
                  onChange={(e) => updateAPI(api.id, { name: e.target.value })}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                />
                <input
                  type="text"
                  value={api.endpoint}
                  onChange={(e) =>
                    updateAPI(api.id, { endpoint: e.target.value })
                  }
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                />
                <button
                  type="button"
                  onClick={() => removeAPI(api.id)}
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
          Authentication Method
        </label>
        <select
          value={data.authMethod}
          onChange={(e) =>
            onChange({
              ...data,
              authMethod: e.target.value as DataFlow['authMethod'],
            })
          }
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="none">None</option>
          <option value="api-key">API Key</option>
          <option value="oauth">OAuth</option>
          <option value="bearer">Bearer Token</option>
          <option value="custom">Custom</option>
        </select>
      </div>

      {data.authMethod !== 'none' && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            API Key Field Names / Auth Details
          </label>
          <input
            type="text"
            value={data.apiKeyFields}
            onChange={(e) =>
              onChange({ ...data, apiKeyFields: e.target.value })
            }
            placeholder="e.g., OPENWEATHER_API_KEY, GITHUB_TOKEN"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Rate Limits
        </label>
        <input
          type="text"
          value={data.rateLimits}
          onChange={(e) => onChange({ ...data, rateLimits: e.target.value })}
          placeholder="e.g., 60 requests per minute, 1000 per day"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Data Transformation Notes
        </label>
        <textarea
          value={data.dataTransformation}
          onChange={(e) =>
            onChange({ ...data, dataTransformation: e.target.value })
          }
          placeholder="Describe any data transformations, mappings, or conversions..."
          rows={4}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
    </div>
  );
};

export default Step6DataFlow;
