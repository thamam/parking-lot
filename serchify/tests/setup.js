/**
 * Jest Setup File
 * Mocks Chrome APIs and sets up test environment
 */

// Mock Chrome APIs
global.chrome = {
  runtime: {
    sendMessage: jest.fn((message, callback) => {
      if (callback) {
        callback({ success: true, data: {} });
      }
      return Promise.resolve({ success: true, data: {} });
    }),
    onMessage: {
      addListener: jest.fn()
    },
    onInstalled: {
      addListener: jest.fn()
    },
    getURL: jest.fn((path) => `chrome-extension://mock-id/${path}`)
  },

  storage: {
    local: {
      get: jest.fn((keys, callback) => {
        const mockData = {
          settings: {
            enableAffiliate: false,
            enableTracking: false,
            preferredPlatforms: ['aliexpress', 'temu', 'wish'],
            priceThreshold: 10
          },
          cache: {},
          searchHistory: []
        };

        if (callback) {
          callback(mockData);
        }
        return Promise.resolve(mockData);
      }),
      set: jest.fn((data, callback) => {
        if (callback) {
          callback();
        }
        return Promise.resolve();
      }),
      remove: jest.fn((keys, callback) => {
        if (callback) {
          callback();
        }
        return Promise.resolve();
      }),
      clear: jest.fn((callback) => {
        if (callback) {
          callback();
        }
        return Promise.resolve();
      })
    },
    sync: {
      get: jest.fn((keys, callback) => {
        if (callback) {
          callback({});
        }
        return Promise.resolve({});
      }),
      set: jest.fn((data, callback) => {
        if (callback) {
          callback();
        }
        return Promise.resolve();
      })
    }
  },

  tabs: {
    query: jest.fn((queryInfo, callback) => {
      const mockTabs = [{
        id: 1,
        url: 'https://www.amazon.com/dp/B08XYZ123',
        active: true
      }];

      if (callback) {
        callback(mockTabs);
      }
      return Promise.resolve(mockTabs);
    }),
    create: jest.fn((createProperties, callback) => {
      const mockTab = { id: 2, url: createProperties.url };
      if (callback) {
        callback(mockTab);
      }
      return Promise.resolve(mockTab);
    })
  },

  scripting: {
    executeScript: jest.fn()
  }
};

// Mock sessionStorage
global.sessionStorage = {
  getItem: jest.fn((key) => null),
  setItem: jest.fn((key, value) => {}),
  removeItem: jest.fn((key) => {}),
  clear: jest.fn()
};

// Mock localStorage
global.localStorage = {
  getItem: jest.fn((key) => null),
  setItem: jest.fn((key, value) => {}),
  removeItem: jest.fn((key) => {}),
  clear: jest.fn()
};

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve('')
  })
);

// Mock console to reduce noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
};

// Setup DOM if needed
if (typeof document === 'undefined') {
  const { JSDOM } = require('jsdom');
  const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
  global.document = dom.window.document;
  global.window = dom.window;
}

// Mock URL if not available
if (typeof URL === 'undefined') {
  global.URL = require('url').URL;
}

// Mock atob and btoa
if (typeof atob === 'undefined') {
  global.atob = (str) => Buffer.from(str, 'base64').toString('binary');
}

if (typeof btoa === 'undefined') {
  global.btoa = (str) => Buffer.from(str, 'binary').toString('base64');
}

// Reset mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
});
