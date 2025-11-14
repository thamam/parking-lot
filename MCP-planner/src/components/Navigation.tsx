import React from 'react';

interface NavigationProps {
  currentStep: number;
  totalSteps: number;
  onNext: () => void;
  onPrevious: () => void;
  onSaveExit: () => void;
  canProceed: boolean;
}

const Navigation: React.FC<NavigationProps> = ({
  currentStep,
  totalSteps,
  onNext,
  onPrevious,
  onSaveExit,
  canProceed,
}) => {
  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === totalSteps;

  return (
    <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
      <button
        onClick={onPrevious}
        disabled={isFirstStep}
        className={`px-6 py-2 rounded-lg font-medium transition-colors ${
          isFirstStep
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        ← Previous
      </button>

      <button
        onClick={onSaveExit}
        className="px-6 py-2 rounded-lg font-medium bg-yellow-500 text-white hover:bg-yellow-600 transition-colors"
      >
        Save & Exit
      </button>

      <button
        onClick={onNext}
        disabled={!canProceed && !isLastStep}
        className={`px-6 py-2 rounded-lg font-medium transition-colors ${
          !canProceed && !isLastStep
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : isLastStep
            ? 'bg-green-600 text-white hover:bg-green-700'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        }`}
      >
        {isLastStep ? '✓ Review & Generate' : 'Next →'}
      </button>
    </div>
  );
};

export default Navigation;
