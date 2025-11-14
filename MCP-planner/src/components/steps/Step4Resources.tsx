import React from 'react';
import type { Resources } from '../../types';
import DynamicList from '../DynamicList';

interface Step4Props {
  data: Resources;
  onChange: (data: Resources) => void;
}

const Step4Resources: React.FC<Step4Props> = ({ data, onChange }) => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Resources</h2>
        <p className="text-gray-600">
          Resources allow clients to read data via URI patterns (optional).
        </p>
      </div>

      <div className="flex items-center gap-3 bg-gray-50 p-4 rounded-lg">
        <input
          type="checkbox"
          id="resources-enabled"
          checked={data.enabled}
          onChange={(e) => onChange({ ...data, enabled: e.target.checked })}
          className="w-5 h-5 rounded"
        />
        <label htmlFor="resources-enabled" className="text-lg font-medium">
          Does this MCP provide resources?
        </label>
      </div>

      {data.enabled && (
        <>
          <DynamicList
            items={data.uriPatterns}
            onChange={(uriPatterns) => onChange({ ...data, uriPatterns })}
            placeholder="e.g., weather://{location}/current"
            label="URI Patterns"
          />

          <DynamicList
            items={data.contentTypes}
            onChange={(contentTypes) => onChange({ ...data, contentTypes })}
            placeholder="e.g., application/json, text/plain"
            label="Content Types"
          />

          <DynamicList
            items={data.exampleUris}
            onChange={(exampleUris) => onChange({ ...data, exampleUris })}
            placeholder="e.g., weather://san-francisco/current"
            label="Example URIs"
          />

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">💡 About Resources</h4>
            <p className="text-sm text-blue-800">
              Resources provide a way for clients to read data using URIs. Use placeholders
              like {`{location}`} in patterns that will be replaced with actual values.
            </p>
          </div>
        </>
      )}

      {!data.enabled && (
        <div className="text-center py-12 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-gray-500">
            Resources are disabled. Enable them above if your MCP needs to provide URI-based data access.
          </p>
        </div>
      )}
    </div>
  );
};

export default Step4Resources;
