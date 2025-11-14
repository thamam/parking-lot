import React, { useState } from 'react';
import { downloadPrompt } from '../utils/promptGenerator';

interface OutputModalProps {
  isOpen: boolean;
  onClose: () => void;
  prompt: string;
  serverName: string;
}

const OutputModal: React.FC<OutputModalProps> = ({
  isOpen,
  onClose,
  prompt,
  serverName,
}) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    downloadPrompt(prompt, serverName);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] flex flex-col">
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">
            MCP Server Specification
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="flex-1 overflow-auto p-6">
          <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono whitespace-pre-wrap">
            {prompt}
          </pre>
        </div>

        <div className="flex gap-4 p-6 border-t border-gray-200">
          <button
            onClick={handleCopy}
            className={`flex-1 px-6 py-3 rounded-lg font-medium transition-colors ${
              copied
                ? 'bg-green-600 text-white'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {copied ? '✓ Copied!' : '📋 Copy to Clipboard'}
          </button>
          <button
            onClick={handleDownload}
            className="flex-1 px-6 py-3 rounded-lg font-medium bg-purple-600 text-white hover:bg-purple-700 transition-colors"
          >
            ⬇ Download .md
          </button>
        </div>
      </div>
    </div>
  );
};

export default OutputModal;
