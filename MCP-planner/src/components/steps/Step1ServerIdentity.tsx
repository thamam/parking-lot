import React from 'react';
import type { ServerIdentity } from '../../types';
import DynamicList from '../DynamicList';

interface Step1Props {
  data: ServerIdentity;
  onChange: (data: ServerIdentity) => void;
}

const Step1ServerIdentity: React.FC<Step1Props> = ({ data, onChange }) => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Server Identity & Purpose
        </h2>
        <p className="text-gray-600">
          Let's start by defining the basic identity and purpose of your MCP server.
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Server Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={data.name}
          onChange={(e) => onChange({ ...data, name: e.target.value })}
          placeholder="e.g., weather-mcp, github-mcp, database-query-mcp"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Description <span className="text-red-500">*</span>
        </label>
        <textarea
          value={data.description}
          onChange={(e) => onChange({ ...data, description: e.target.value })}
          placeholder="Briefly describe what this MCP server does..."
          rows={3}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Primary Use Cases <span className="text-red-500">*</span>
        </label>
        <textarea
          value={data.useCases}
          onChange={(e) => onChange({ ...data, useCases: e.target.value })}
          placeholder="One use case per line:&#10;- Get weather forecasts&#10;- Search locations&#10;- Track weather alerts"
          rows={5}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
        />
        <p className="mt-1 text-sm text-gray-500">
          Enter one use case per line
        </p>
      </div>

      <DynamicList
        items={data.dataSources}
        onChange={(dataSources) => onChange({ ...data, dataSources })}
        placeholder="e.g., OpenWeatherMap API, PostgreSQL Database"
        label="Data Sources / APIs"
      />

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">💡 Tip</h4>
        <p className="text-sm text-blue-800">
          Be specific about your server's purpose. This helps generate more accurate
          implementation code. Think about what problems this MCP server will solve.
        </p>
      </div>
    </div>
  );
};

export default Step1ServerIdentity;
