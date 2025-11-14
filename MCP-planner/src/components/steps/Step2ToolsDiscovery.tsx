import React, { useState } from 'react';
import type { ToolSummary } from '../../types';

interface Step2Props {
  data: ToolSummary[];
  onChange: (data: ToolSummary[]) => void;
}

const Step2ToolsDiscovery: React.FC<Step2Props> = ({ data, onChange }) => {
  const [newTool, setNewTool] = useState({
    name: '',
    description: '',
    category: '',
  });

  const addTool = () => {
    if (newTool.name && newTool.description && newTool.category) {
      const tool: ToolSummary = {
        id: Date.now().toString(),
        ...newTool,
      };
      onChange([...data, tool]);
      setNewTool({ name: '', description: '', category: '' });
    }
  };

  const removeTool = (id: string) => {
    onChange(data.filter((tool) => tool.id !== id));
  };

  const updateTool = (id: string, updates: Partial<ToolSummary>) => {
    onChange(
      data.map((tool) => (tool.id === id ? { ...tool, ...updates } : tool))
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Tools Discovery
        </h2>
        <p className="text-gray-600">
          Define all the tools your MCP server will provide. We'll add detailed specifications in the next step.
        </p>
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Add New Tool
        </h3>
        <div className="space-y-3">
          <input
            type="text"
            value={newTool.name}
            onChange={(e) => setNewTool({ ...newTool, name: e.target.value })}
            placeholder="Tool name (e.g., get_weather, search_user)"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <input
            type="text"
            value={newTool.description}
            onChange={(e) =>
              setNewTool({ ...newTool, description: e.target.value })
            }
            placeholder="One-line description"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <input
            type="text"
            value={newTool.category}
            onChange={(e) =>
              setNewTool({ ...newTool, category: e.target.value })
            }
            placeholder="Category (e.g., Weather Data, User Management)"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="button"
            onClick={addTool}
            disabled={!newTool.name || !newTool.description || !newTool.category}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            + Add Tool
          </button>
        </div>
      </div>

      {data.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Tools ({data.length})
          </h3>
          {data.map((tool) => (
            <div
              key={tool.id}
              className="bg-white border border-gray-200 rounded-lg p-4 space-y-3"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1 space-y-2">
                  <input
                    type="text"
                    value={tool.name}
                    onChange={(e) =>
                      updateTool(tool.id, { name: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg font-medium"
                  />
                  <input
                    type="text"
                    value={tool.description}
                    onChange={(e) =>
                      updateTool(tool.id, { description: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  />
                  <input
                    type="text"
                    value={tool.category}
                    onChange={(e) =>
                      updateTool(tool.id, { category: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                    placeholder="Category"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => removeTool(tool.id)}
                  className="ml-4 text-red-600 hover:text-red-800 font-medium"
                >
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {data.length === 0 && (
        <div className="text-center py-12 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-gray-500">
            No tools added yet. Add your first tool above!
          </p>
        </div>
      )}
    </div>
  );
};

export default Step2ToolsDiscovery;
