import React, { useState } from 'react';
import type {
  Configuration,
  EnvVariable,
  Dependency,
  SetupStep,
} from '../../types';

interface Step9Props {
  data: Configuration;
  onChange: (data: Configuration) => void;
}

const Step9Configuration: React.FC<Step9Props> = ({ data, onChange }) => {
  const [newEnvVar, setNewEnvVar] = useState({ name: '', description: '' });
  const [newDep, setNewDep] = useState({ packageName: '', version: '' });
  const [newStep, setNewStep] = useState('');

  const addEnvVar = () => {
    if (newEnvVar.name && newEnvVar.description) {
      const envVar: EnvVariable = {
        id: Date.now().toString(),
        ...newEnvVar,
      };
      onChange({
        ...data,
        envVariables: [...data.envVariables, envVar],
      });
      setNewEnvVar({ name: '', description: '' });
    }
  };

  const removeEnvVar = (id: string) => {
    onChange({
      ...data,
      envVariables: data.envVariables.filter((v) => v.id !== id),
    });
  };

  const updateEnvVar = (id: string, updates: Partial<EnvVariable>) => {
    onChange({
      ...data,
      envVariables: data.envVariables.map((v) =>
        v.id === id ? { ...v, ...updates } : v
      ),
    });
  };

  const addDep = () => {
    if (newDep.packageName && newDep.version) {
      const dep: Dependency = {
        id: Date.now().toString(),
        ...newDep,
      };
      onChange({
        ...data,
        dependencies: [...data.dependencies, dep],
      });
      setNewDep({ packageName: '', version: '' });
    }
  };

  const removeDep = (id: string) => {
    onChange({
      ...data,
      dependencies: data.dependencies.filter((d) => d.id !== id),
    });
  };

  const updateDep = (id: string, updates: Partial<Dependency>) => {
    onChange({
      ...data,
      dependencies: data.dependencies.map((d) =>
        d.id === id ? { ...d, ...updates } : d
      ),
    });
  };

  const addStep = () => {
    if (newStep.trim()) {
      const step: SetupStep = {
        id: Date.now().toString(),
        step: newStep.trim(),
      };
      onChange({
        ...data,
        setupSteps: [...data.setupSteps, step],
      });
      setNewStep('');
    }
  };

  const removeStep = (id: string) => {
    onChange({
      ...data,
      setupSteps: data.setupSteps.filter((s) => s.id !== id),
    });
  };

  const updateStep = (id: string, stepText: string) => {
    onChange({
      ...data,
      setupSteps: data.setupSteps.map((s) =>
        s.id === id ? { ...s, step: stepText } : s
      ),
    });
  };

  const moveStep = (id: string, direction: 'up' | 'down') => {
    const index = data.setupSteps.findIndex((s) => s.id === id);
    if (
      (direction === 'up' && index > 0) ||
      (direction === 'down' && index < data.setupSteps.length - 1)
    ) {
      const newSteps = [...data.setupSteps];
      const swapIndex = direction === 'up' ? index - 1 : index + 1;
      [newSteps[index], newSteps[swapIndex]] = [
        newSteps[swapIndex],
        newSteps[index],
      ];
      onChange({ ...data, setupSteps: newSteps });
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Configuration & Setup
        </h2>
        <p className="text-gray-600">
          Define environment variables, dependencies, and setup instructions.
        </p>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Environment Variables
        </h3>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
          <div className="flex gap-3 mb-3">
            <input
              type="text"
              value={newEnvVar.name}
              onChange={(e) =>
                setNewEnvVar({ ...newEnvVar, name: e.target.value })
              }
              placeholder="Variable name (e.g., API_KEY)"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={newEnvVar.description}
              onChange={(e) =>
                setNewEnvVar({ ...newEnvVar, description: e.target.value })
              }
              placeholder="Description"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="button"
              onClick={addEnvVar}
              disabled={!newEnvVar.name || !newEnvVar.description}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              + Add
            </button>
          </div>
        </div>

        {data.envVariables.length > 0 && (
          <div className="space-y-2 mb-6">
            {data.envVariables.map((envVar) => (
              <div
                key={envVar.id}
                className="bg-white border border-gray-200 rounded-lg p-3 flex gap-3"
              >
                <input
                  type="text"
                  value={envVar.name}
                  onChange={(e) =>
                    updateEnvVar(envVar.id, { name: e.target.value })
                  }
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                />
                <input
                  type="text"
                  value={envVar.description}
                  onChange={(e) =>
                    updateEnvVar(envVar.id, { description: e.target.value })
                  }
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
                <button
                  type="button"
                  onClick={() => removeEnvVar(envVar.id)}
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
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Dependencies
        </h3>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={newDep.packageName}
              onChange={(e) =>
                setNewDep({ ...newDep, packageName: e.target.value })
              }
              placeholder="Package name (e.g., axios, express)"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={newDep.version}
              onChange={(e) =>
                setNewDep({ ...newDep, version: e.target.value })
              }
              placeholder="Version (e.g., ^1.0.0)"
              className="w-40 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="button"
              onClick={addDep}
              disabled={!newDep.packageName || !newDep.version}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              + Add
            </button>
          </div>
        </div>

        {data.dependencies.length > 0 && (
          <div className="space-y-2 mb-6">
            {data.dependencies.map((dep) => (
              <div
                key={dep.id}
                className="bg-white border border-gray-200 rounded-lg p-3 flex gap-3"
              >
                <input
                  type="text"
                  value={dep.packageName}
                  onChange={(e) =>
                    updateDep(dep.id, { packageName: e.target.value })
                  }
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                />
                <input
                  type="text"
                  value={dep.version}
                  onChange={(e) =>
                    updateDep(dep.id, { version: e.target.value })
                  }
                  className="w-40 px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                />
                <button
                  type="button"
                  onClick={() => removeDep(dep.id)}
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
          Installation Requirements
        </label>
        <textarea
          value={data.installationRequirements}
          onChange={(e) =>
            onChange({ ...data, installationRequirements: e.target.value })
          }
          placeholder="e.g., Node.js 18+, Python 3.9+, Docker"
          rows={3}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Setup Steps (ordered)
        </h3>
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={newStep}
            onChange={(e) => setNewStep(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addStep()}
            placeholder="Setup step (e.g., Run npm install)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="button"
            onClick={addStep}
            disabled={!newStep.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            + Add
          </button>
        </div>

        {data.setupSteps.length > 0 && (
          <div className="space-y-2">
            {data.setupSteps.map((step, index) => (
              <div
                key={step.id}
                className="bg-white border border-gray-200 rounded-lg p-3 flex gap-3 items-center"
              >
                <span className="text-gray-500 font-medium w-8">
                  {index + 1}.
                </span>
                <input
                  type="text"
                  value={step.step}
                  onChange={(e) => updateStep(step.id, e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                />
                <div className="flex gap-1">
                  <button
                    type="button"
                    onClick={() => moveStep(step.id, 'up')}
                    disabled={index === 0}
                    className="px-2 py-1 text-gray-600 hover:text-gray-800 disabled:text-gray-300"
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    onClick={() => moveStep(step.id, 'down')}
                    disabled={index === data.setupSteps.length - 1}
                    className="px-2 py-1 text-gray-600 hover:text-gray-800 disabled:text-gray-300"
                  >
                    ↓
                  </button>
                </div>
                <button
                  type="button"
                  onClick={() => removeStep(step.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Step9Configuration;
