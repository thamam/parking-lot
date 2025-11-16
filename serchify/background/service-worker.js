/**
 * Background Service Worker for Serchify Chrome Extension
 * Handles API calls, caching, and message passing
 */

// Import utilities (simulated - Chrome extensions don't use ES6 imports in service workers yet)
// In production, these would be injected via build process

/**
 * Message handler for communication with content scripts and popup
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Background] Received message:', request.type);

  switch (request.type) {
    case 'SEARCH_PRODUCT':
      handleProductSearch(request.data)
        .then(results => sendResponse({ success: true, data: results }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true; // Keep message channel open for async response

    case 'REVERSE_IMAGE_SEARCH':
      handleReverseImageSearch(request.data)
        .then(results => sendResponse({ success: true, data: results }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;

    case 'GET_SETTINGS':
      getSettings()
        .then(settings => sendResponse({ success: true, data: settings }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;

    case 'UPDATE_SETTINGS':
      updateSettings(request.data)
        .then(() => sendResponse({ success: true }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;

    case 'CLEAR_CACHE':
      clearCache()
        .then(() => sendResponse({ success: true }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;

    default:
      sendResponse({ success: false, error: 'Unknown message type' });
  }
});

/**
 * Handle product search across multiple platforms
 */
async function handleProductSearch(productData) {
  const { asin, title, imageUrl, price, brand } = productData;

  // Check cache first
  const cacheKey = `search_${asin}`;
  const cachedResults = await getFromCache(cacheKey);

  if (cachedResults) {
    console.log('[Background] Returning cached results');
    return cachedResults;
  }

  // Get user settings to determine which platforms to search
  const settings = await getSettings();
  const platforms = settings.preferredPlatforms || ['aliexpress', 'temu', 'wish'];

  // Search all platforms in parallel
  const searchPromises = platforms.map(platform =>
    searchPlatform(platform, { title, imageUrl, brand })
      .catch(error => {
        console.error(`[Background] Error searching ${platform}:`, error);
        return { platform, results: [], error: error.message };
      })
  );

  const allResults = await Promise.all(searchPromises);

  // Flatten and sort results by confidence score
  const combinedResults = allResults
    .filter(r => r.results && r.results.length > 0)
    .flatMap(r => r.results)
    .sort((a, b) => b.confidenceScore - a.confidenceScore);

  const response = {
    results: combinedResults,
    timestamp: Date.now(),
    platforms: platforms,
    originalProduct: productData
  };

  // Cache results for 24 hours
  await saveToCache(cacheKey, response, 24 * 60 * 60 * 1000);

  return response;
}

/**
 * Handle reverse image search
 */
async function handleReverseImageSearch(imageData) {
  const { imageUrl, dataUrl } = imageData;

  // Try platform-native image search first (AliExpress)
  try {
    const aliExpressResults = await reverseImageSearchAliExpress(imageUrl || dataUrl);
    if (aliExpressResults && aliExpressResults.length > 0) {
      return {
        results: aliExpressResults,
        method: 'aliexpress-native',
        timestamp: Date.now()
      };
    }
  } catch (error) {
    console.error('[Background] AliExpress image search failed:', error);
  }

  // Fallback to generic reverse image search (would use Google Lens API)
  try {
    const genericResults = await reverseImageSearchGeneric(imageUrl || dataUrl);
    return {
      results: genericResults,
      method: 'generic',
      timestamp: Date.now()
    };
  } catch (error) {
    console.error('[Background] Generic image search failed:', error);
    throw new Error('Image search unavailable');
  }
}

/**
 * Search a specific platform for products
 */
async function searchPlatform(platform, productInfo) {
  const { title, imageUrl, brand } = productInfo;

  switch (platform) {
    case 'aliexpress':
      return await searchAliExpress(title, imageUrl, brand);
    case 'temu':
      return await searchTemu(title, imageUrl, brand);
    case 'wish':
      return await searchWish(title, imageUrl, brand);
    case 'dhgate':
      return await searchDHGate(title, imageUrl, brand);
    case 'banggood':
      return await searchBanggood(title, imageUrl, brand);
    case 'ebay':
      return await searchEbay(title, imageUrl, brand);
    default:
      throw new Error(`Unknown platform: ${platform}`);
  }
}

/**
 * AliExpress search implementation
 */
async function searchAliExpress(title, imageUrl, brand) {
  // In production, this would use AliExpress API or web scraping
  // For now, this is a placeholder that demonstrates the structure

  const searchQuery = encodeURIComponent(`${brand} ${title}`.trim());
  const searchUrl = `https://www.aliexpress.com/wholesale?SearchText=${searchQuery}`;

  try {
    // Simulate API call - in production, would fetch and parse results
    const results = await simulatePlatformSearch('aliexpress', searchQuery);

    return {
      platform: 'aliexpress',
      results: results,
      searchUrl: searchUrl
    };
  } catch (error) {
    console.error('[Background] AliExpress search error:', error);
    return { platform: 'aliexpress', results: [], error: error.message };
  }
}

/**
 * Temu search implementation
 */
async function searchTemu(title, imageUrl, brand) {
  const searchQuery = encodeURIComponent(`${brand} ${title}`.trim());
  const searchUrl = `https://www.temu.com/search_result.html?search_key=${searchQuery}`;

  try {
    const results = await simulatePlatformSearch('temu', searchQuery);

    return {
      platform: 'temu',
      results: results,
      searchUrl: searchUrl
    };
  } catch (error) {
    console.error('[Background] Temu search error:', error);
    return { platform: 'temu', results: [], error: error.message };
  }
}

/**
 * Wish search implementation
 */
async function searchWish(title, imageUrl, brand) {
  const searchQuery = encodeURIComponent(`${brand} ${title}`.trim());
  const searchUrl = `https://www.wish.com/search/${searchQuery}`;

  try {
    const results = await simulatePlatformSearch('wish', searchQuery);

    return {
      platform: 'wish',
      results: results,
      searchUrl: searchUrl
    };
  } catch (error) {
    console.error('[Background] Wish search error:', error);
    return { platform: 'wish', results: [], error: error.message };
  }
}

/**
 * DHGate search implementation
 */
async function searchDHGate(title, imageUrl, brand) {
  const searchQuery = encodeURIComponent(`${brand} ${title}`.trim());
  const searchUrl = `https://www.dhgate.com/wholesale/search.do?act=search&searchkey=${searchQuery}`;

  try {
    const results = await simulatePlatformSearch('dhgate', searchQuery);

    return {
      platform: 'dhgate',
      results: results,
      searchUrl: searchUrl
    };
  } catch (error) {
    console.error('[Background] DHGate search error:', error);
    return { platform: 'dhgate', results: [], error: error.message };
  }
}

/**
 * Banggood search implementation
 */
async function searchBanggood(title, imageUrl, brand) {
  const searchQuery = encodeURIComponent(`${brand} ${title}`.trim());
  const searchUrl = `https://www.banggood.com/search/${searchQuery}.html`;

  try {
    const results = await simulatePlatformSearch('banggood', searchQuery);

    return {
      platform: 'banggood',
      results: results,
      searchUrl: searchUrl
    };
  } catch (error) {
    console.error('[Background] Banggood search error:', error);
    return { platform: 'banggood', results: [], error: error.message };
  }
}

/**
 * eBay search implementation
 */
async function searchEbay(title, imageUrl, brand) {
  const searchQuery = encodeURIComponent(`${brand} ${title}`.trim());
  const searchUrl = `https://www.ebay.com/sch/i.html?_nkw=${searchQuery}`;

  try {
    const results = await simulatePlatformSearch('ebay', searchQuery);

    return {
      platform: 'ebay',
      results: results,
      searchUrl: searchUrl
    };
  } catch (error) {
    console.error('[Background] eBay search error:', error);
    return { platform: 'ebay', results: [], error: error.message };
  }
}

/**
 * Simulate platform search (placeholder for actual implementation)
 * In production, this would make real API calls or perform web scraping
 */
async function simulatePlatformSearch(platform, query) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));

  // Return mock results
  return [
    {
      title: `Sample Product from ${platform}`,
      price: Math.random() * 50 + 10,
      currency: 'USD',
      imageUrl: 'https://via.placeholder.com/200',
      productUrl: `https://www.${platform}.com/item/123456`,
      confidenceScore: Math.random() * 40 + 60,
      matchType: 'similar',
      sellerRating: Math.random() * 2 + 3,
      reviewCount: Math.floor(Math.random() * 1000),
      shippingCost: Math.random() * 10,
      platform: platform
    }
  ];
}

/**
 * Reverse image search on AliExpress
 */
async function reverseImageSearchAliExpress(imageUrl) {
  // Placeholder - would use AliExpress image search API
  console.log('[Background] Performing AliExpress reverse image search');
  return [];
}

/**
 * Generic reverse image search (Google Lens or similar)
 */
async function reverseImageSearchGeneric(imageUrl) {
  // Placeholder - would use Google Lens API or SerpAPI
  console.log('[Background] Performing generic reverse image search');
  return [];
}

/**
 * Get user settings from storage
 */
async function getSettings() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['settings'], (result) => {
      const defaultSettings = {
        enableAffiliate: false,
        enableTracking: false,
        preferredPlatforms: ['aliexpress', 'temu', 'wish'],
        priceThreshold: 10 // minimum % savings
      };
      resolve(result.settings || defaultSettings);
    });
  });
}

/**
 * Update user settings
 */
async function updateSettings(newSettings) {
  return new Promise((resolve) => {
    chrome.storage.local.set({ settings: newSettings }, () => {
      resolve();
    });
  });
}

/**
 * Get data from cache
 */
async function getFromCache(key) {
  return new Promise((resolve) => {
    chrome.storage.local.get(['cache'], (result) => {
      const cache = result.cache || {};
      const cached = cache[key];

      if (cached && cached.expiresAt > Date.now()) {
        resolve(cached.data);
      } else {
        resolve(null);
      }
    });
  });
}

/**
 * Save data to cache with expiration
 */
async function saveToCache(key, data, ttlMs) {
  return new Promise((resolve) => {
    chrome.storage.local.get(['cache'], (result) => {
      const cache = result.cache || {};
      cache[key] = {
        data: data,
        expiresAt: Date.now() + ttlMs,
        timestamp: Date.now()
      };

      chrome.storage.local.set({ cache: cache }, () => {
        resolve();
      });
    });
  });
}

/**
 * Clear all cached data
 */
async function clearCache() {
  return new Promise((resolve) => {
    chrome.storage.local.set({ cache: {} }, () => {
      console.log('[Background] Cache cleared');
      resolve();
    });
  });
}

/**
 * Initialize extension on install
 */
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('[Background] Extension installed');

    // Set default settings
    const defaultSettings = {
      enableAffiliate: false,
      enableTracking: false,
      preferredPlatforms: ['aliexpress', 'temu', 'wish'],
      priceThreshold: 10
    };

    chrome.storage.local.set({ settings: defaultSettings });
  }
});

console.log('[Background] Service worker initialized');
