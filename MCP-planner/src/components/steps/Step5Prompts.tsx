import React, { useState } from 'react';
import type { Prompts, PromptTemplate } from '../../types';

interface Step5Props {
  data: Prompts;
  onChange: (data: Prompts) => void;
}

const Step5Prompts: React.FC<Step5Props> = ({ data, onChange }) => {
  const [newPrompt, setNewPrompt] = useState({
    name: '',
    template: '',
    arguments: '',
    useCase: '',
  });

  const addPrompt = () => {
    if (newPrompt.name && newPrompt.template) {
      const prompt: PromptTemplate = {
        id: Date.now().toString(),
        ...newPrompt,
      };
      onChange({
        ...data,
        templates: [...data.templates, prompt],
      });
      setNewPrompt({ name: '', template: '', arguments: '', useCase: '' });
    }
  };

  const removePrompt = (id: string) => {
    onChange({
      ...data,
      templates: data.templates.filter((p) => p.id !== id),
    });
  };

  const updatePrompt = (id: string, updates: Partial<PromptTemplate>) => {
    onChange({
      ...data,
      templates: data.templates.map((p) =>
        p.id === id ? { ...p, ...updates } : p
      ),
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Prompts/Templates
        </h2>
        <p className="text-gray-600">
          Define reusable prompt templates for common interactions (optional).
        </p>
      </div>

      <div className="flex items-center gap-3 bg-gray-50 p-4 rounded-lg">
        <input
          type="checkbox"
          id="prompts-enabled"
          checked={data.enabled}
          onChange={(e) => onChange({ ...data, enabled: e.target.checked })}
          className="w-5 h-5 rounded"
        />
        <label htmlFor="prompts-enabled" className="text-lg font-medium">
          Does this MCP provide prompt templates?
        </label>
      </div>

      {data.enabled && (
        <>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Add New Prompt Template
            </h3>
            <div className="space-y-3">
              <input
                type="text"
                value={newPrompt.name}
                onChange={(e) =>
                  setNewPrompt({ ...newPrompt, name: e.target.value })
                }
                placeholder="Template name (e.g., weather_summary)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <textarea
                value={newPrompt.template}
                onChange={(e) =>
                  setNewPrompt({ ...newPrompt, template: e.target.value })
                }
                placeholder="Template text (use {variable} for arguments)"
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                value={newPrompt.arguments}
                onChange={(e) =>
                  setNewPrompt({ ...newPrompt, arguments: e.target.value })
                }
                placeholder="Arguments (e.g., location: string, date: string)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                value={newPrompt.useCase}
                onChange={(e) =>
                  setNewPrompt({ ...newPrompt, useCase: e.target.value })
                }
                placeholder="Use case description"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={addPrompt}
                disabled={!newPrompt.name || !newPrompt.template}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                + Add Prompt Template
              </button>
            </div>
          </div>

          {data.templates.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Templates ({data.templates.length})
              </h3>
              {data.templates.map((prompt) => (
                <div
                  key={prompt.id}
                  className="bg-white border border-gray-200 rounded-lg p-4 space-y-3"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1 space-y-2">
                      <input
                        type="text"
                        value={prompt.name}
                        onChange={(e) =>
                          updatePrompt(prompt.id, { name: e.target.value })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg font-medium"
                      />
                      <textarea
                        value={prompt.template}
                        onChange={(e) =>
                          updatePrompt(prompt.id, { template: e.target.value })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        rows={2}
                      />
                      <input
                        type="text"
                        value={prompt.arguments}
                        onChange={(e) =>
                          updatePrompt(prompt.id, { arguments: e.target.value })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        placeholder="Arguments"
                      />
                      <input
                        type="text"
                        value={prompt.useCase}
                        onChange={(e) =>
                          updatePrompt(prompt.id, { useCase: e.target.value })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        placeholder="Use case"
                      />
                    </div>
                    <button
                      type="button"
                      onClick={() => removePrompt(prompt.id)}
                      className="ml-4 text-red-600 hover:text-red-800 font-medium"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">💡 About Prompts</h4>
            <p className="text-sm text-blue-800">
              Prompt templates help standardize common interactions. Use {`{variable}`}
              syntax for dynamic values that will be filled in at runtime.
            </p>
          </div>
        </>
      )}

      {!data.enabled && (
        <div className="text-center py-12 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-gray-500">
            Prompt templates are disabled. Enable them if you want to provide reusable prompts.
          </p>
        </div>
      )}
    </div>
  );
};

export default Step5Prompts;
