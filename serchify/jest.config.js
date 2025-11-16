/**
 * Jest Configuration for Serchify Chrome Extension
 */

module.exports = {
  // Test environment
  testEnvironment: 'jsdom',

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],

  // Test match patterns
  testMatch: [
    '**/tests/**/*.test.js',
    '**/tests/**/*.spec.js'
  ],

  // Coverage configuration
  collectCoverageFrom: [
    'lib/**/*.js',
    'background/**/*.js',
    'content/**/*.js',
    'popup/**/*.js',
    '!**/node_modules/**',
    '!**/tests/**'
  ],

  coverageThresholds: {
    global: {
      branches: 70,
      functions: 70,
      lines: 80,
      statements: 80
    }
  },

  // Module paths
  moduleDirectories: ['node_modules', '<rootDir>'],

  // Ignore patterns
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/'
  ],

  // Transform
  transform: {},

  // Verbose output
  verbose: true,

  // Timeout
  testTimeout: 10000
};
