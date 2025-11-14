import React, { useState } from 'react';

interface DynamicListProps {
  items: string[];
  onChange: (items: string[]) => void;
  placeholder?: string;
  label?: string;
}

const DynamicList: React.FC<DynamicListProps> = ({
  items,
  onChange,
  placeholder = 'Enter item...',
  label,
}) => {
  const [inputValue, setInputValue] = useState('');

  const addItem = () => {
    if (inputValue.trim()) {
      onChange([...items, inputValue.trim()]);
      setInputValue('');
    }
  };

  const removeItem = (index: number) => {
    onChange(items.filter((_, i) => i !== index));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addItem();
    }
  };

  return (
    <div className="space-y-3">
      {label && (
        <label className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}

      <div className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="button"
          onClick={addItem}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          + Add
        </button>
      </div>

      {items.length > 0 && (
        <div className="space-y-2">
          {items.map((item, index) => (
            <div
              key={index}
              className="flex items-center justify-between bg-gray-50 px-4 py-2 rounded-lg"
            >
              <span className="text-gray-700">{item}</span>
              <button
                type="button"
                onClick={() => removeItem(index)}
                className="text-red-600 hover:text-red-800 font-medium"
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DynamicList;
