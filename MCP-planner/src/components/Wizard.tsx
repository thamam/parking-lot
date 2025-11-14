import React, { useState, useEffect } from 'react';
import type { WizardData } from '../types';
import { initialWizardData } from '../types';
import {
  saveWizardData,
  loadWizardData,
  saveCurrentStep,
  loadCurrentStep,
  clearWizardData,
  hasExistingData,
  exportWizardData,
  importWizardData,
  getExampleData,
} from '../utils/storage';
import { generatePrompt } from '../utils/promptGenerator';
import ProgressBar from './ProgressBar';
import Navigation from './Navigation';
import OutputModal from './OutputModal';
import Step1ServerIdentity from './steps/Step1ServerIdentity';
import Step2ToolsDiscovery from './steps/Step2ToolsDiscovery';
import Step3ToolDetails from './steps/Step3ToolDetails';
import Step4Resources from './steps/Step4Resources';
import Step5Prompts from './steps/Step5Prompts';
import Step6DataFlow from './steps/Step6DataFlow';
import Step7ErrorHandling from './steps/Step7ErrorHandling';
import Step8Examples from './steps/Step8Examples';
import Step9Configuration from './steps/Step9Configuration';
import Step10Testing from './steps/Step10Testing';

const TOTAL_STEPS = 10;

const Wizard: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [wizardData, setWizardData] = useState<WizardData>(initialWizardData);
  const [showOutputModal, setShowOutputModal] = useState(false);
  const [generatedPrompt, setGeneratedPrompt] = useState('');
  const [showLoadDialog, setShowLoadDialog] = useState(false);

  useEffect(() => {
    if (hasExistingData()) {
      setShowLoadDialog(true);
    }
  }, []);

  useEffect(() => {
    saveWizardData(wizardData);
    saveCurrentStep(currentStep);
  }, [wizardData, currentStep]);

  const loadPreviousSession = () => {
    const data = loadWizardData();
    if (data) {
      setWizardData(data);
      setCurrentStep(loadCurrentStep());
    }
    setShowLoadDialog(false);
  };

  const startFresh = () => {
    clearWizardData();
    setShowLoadDialog(false);
  };

  const loadExample = () => {
    const exampleData = getExampleData();
    setWizardData(exampleData);
    setShowLoadDialog(false);
  };

  const handleNext = () => {
    if (currentStep < TOTAL_STEPS) {
      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleSaveExit = () => {
    alert('Your progress has been saved! You can return anytime to continue.');
  };

  const handleGeneratePrompt = () => {
    const prompt = generatePrompt(wizardData);
    setGeneratedPrompt(prompt);
    setShowOutputModal(true);
  };

  const handleClearAll = () => {
    if (
      window.confirm(
        'Are you sure you want to clear all data? This cannot be undone.'
      )
    ) {
      clearWizardData();
      setWizardData(initialWizardData);
      setCurrentStep(1);
    }
  };

  const handleExport = () => {
    exportWizardData(wizardData);
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      importWizardData(file)
        .then((data) => {
          setWizardData(data);
          alert('Data imported successfully!');
        })
        .catch((error) => {
          alert('Error importing data: ' + error.message);
        });
    }
  };

  const canProceedToNext = (): boolean => {
    switch (currentStep) {
      case 1:
        return !!(
          wizardData.serverIdentity.name &&
          wizardData.serverIdentity.description &&
          wizardData.serverIdentity.useCases
        );
      case 2:
        return wizardData.toolsSummary.length > 0;
      case 3:
        return wizardData.toolsSummary.every(
          (tool) =>
            wizardData.toolsDetails[tool.id]?.detailedDescription?.trim()
        );
      default:
        return true;
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <Step1ServerIdentity
            data={wizardData.serverIdentity}
            onChange={(data) =>
              setWizardData({ ...wizardData, serverIdentity: data })
            }
          />
        );
      case 2:
        return (
          <Step2ToolsDiscovery
            data={wizardData.toolsSummary}
            onChange={(data) =>
              setWizardData({ ...wizardData, toolsSummary: data })
            }
          />
        );
      case 3:
        return (
          <Step3ToolDetails
            tools={wizardData.toolsSummary}
            toolsDetails={wizardData.toolsDetails}
            onChange={(data) =>
              setWizardData({ ...wizardData, toolsDetails: data })
            }
          />
        );
      case 4:
        return (
          <Step4Resources
            data={wizardData.resources}
            onChange={(data) =>
              setWizardData({ ...wizardData, resources: data })
            }
          />
        );
      case 5:
        return (
          <Step5Prompts
            data={wizardData.prompts}
            onChange={(data) => setWizardData({ ...wizardData, prompts: data })}
          />
        );
      case 6:
        return (
          <Step6DataFlow
            data={wizardData.dataFlow}
            onChange={(data) =>
              setWizardData({ ...wizardData, dataFlow: data })
            }
          />
        );
      case 7:
        return (
          <Step7ErrorHandling
            data={wizardData.errorHandling}
            onChange={(data) =>
              setWizardData({ ...wizardData, errorHandling: data })
            }
          />
        );
      case 8:
        return (
          <Step8Examples
            data={wizardData.examples}
            tools={wizardData.toolsSummary}
            onChange={(data) =>
              setWizardData({ ...wizardData, examples: data })
            }
          />
        );
      case 9:
        return (
          <Step9Configuration
            data={wizardData.configuration}
            onChange={(data) =>
              setWizardData({ ...wizardData, configuration: data })
            }
          />
        );
      case 10:
        return (
          <Step10Testing
            data={wizardData.testing}
            tools={wizardData.toolsSummary}
            wizardData={wizardData}
            onChange={(data) => setWizardData({ ...wizardData, testing: data })}
            onGeneratePrompt={handleGeneratePrompt}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {showLoadDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Welcome Back!
            </h2>
            <p className="text-gray-600 mb-6">
              We found a previous session. Would you like to continue where you
              left off?
            </p>
            <div className="space-y-3">
              <button
                onClick={loadPreviousSession}
                className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Continue Previous Session
              </button>
              <button
                onClick={loadExample}
                className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
              >
                Load Example Data
              </button>
              <button
                onClick={startFresh}
                className="w-full px-4 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
              >
                Start Fresh
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">MCP Planner</h1>
            <p className="text-sm text-gray-600">
              Plan and generate MCP server specifications
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleExport}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm"
            >
              Export
            </button>
            <label className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm cursor-pointer">
              Import
              <input
                type="file"
                accept=".json"
                onChange={handleImport}
                className="hidden"
              />
            </label>
            <button
              onClick={() => loadExample()}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
            >
              Load Example
            </button>
            <button
              onClick={handleClearAll}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
            >
              Clear All
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-8">
        <ProgressBar currentStep={currentStep} totalSteps={TOTAL_STEPS} />

        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          {renderStep()}
        </div>

        <Navigation
          currentStep={currentStep}
          totalSteps={TOTAL_STEPS}
          onNext={handleNext}
          onPrevious={handlePrevious}
          onSaveExit={handleSaveExit}
          canProceed={canProceedToNext()}
        />
      </div>

      <OutputModal
        isOpen={showOutputModal}
        onClose={() => setShowOutputModal(false)}
        prompt={generatedPrompt}
        serverName={wizardData.serverIdentity.name}
      />

      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <p className="text-sm">
            MCP Planner - A comprehensive tool for planning Model Context Protocol servers
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Built with React, TypeScript, and Tailwind CSS
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Wizard;
