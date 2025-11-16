/**
 * Serchify Popup Script
 * Handles all popup interactions and communication with background script
 */

(function() {
  'use strict';

  // State
  let currentSettings = null;
  let searchResults = [];
  let recentSearches = [];

  // DOM Elements
  const elements = {
    // Tabs
    tabs: document.querySelectorAll('.tab'),
    urlTab: document.getElementById('urlTab'),
    imageTab: document.getElementById('imageTab'),

    // URL Search
    urlInput: document.getElementById('urlInput'),
    searchBtn: document.getElementById('searchBtn'),

    // Image Search
    uploadArea: document.getElementById('uploadArea'),
    imageInput: document.getElementById('imageInput'),
    imagePreview: document.getElementById('imagePreview'),
    previewImg: document.getElementById('previewImg'),
    removeImageBtn: document.getElementById('removeImageBtn'),
    imageSearchBtn: document.getElementById('imageSearchBtn'),

    // Results
    loadingState: document.getElementById('loadingState'),
    resultsSection: document.getElementById('resultsSection'),
    resultsCount: document.getElementById('resultsCount'),
    resultsList: document.getElementById('resultsList'),
    sortSelect: document.getElementById('sortSelect'),

    // Recent
    recentList: document.getElementById('recentList'),

    // Settings
    settingsBtn: document.getElementById('settingsBtn'),
    settingsPanel: document.getElementById('settingsPanel'),
    closeSettingsBtn: document.getElementById('closeSettingsBtn'),
    saveSettingsBtn: document.getElementById('saveSettingsBtn'),
    clearCacheBtn: document.getElementById('clearCacheBtn'),
    clearHistoryBtn: document.getElementById('clearHistoryBtn'),
    platformCheckboxes: document.querySelectorAll('.platform-checkbox'),
    enableTracking: document.getElementById('enableTracking'),
    enableAffiliate: document.getElementById('enableAffiliate'),
    priceThreshold: document.getElementById('priceThreshold'),

    // Links
    privacyLink: document.getElementById('privacyLink'),
    supportLink: document.getElementById('supportLink'),
    affiliateDisclosureLink: document.getElementById('affiliateDisclosureLink')
  };

  /**
   * Initialize popup
   */
  async function initialize() {
    console.log('[Popup] Initializing...');

    // Load settings
    await loadSettings();

    // Load recent searches
    await loadRecentSearches();

    // Setup event listeners
    setupEventListeners();

    // Check if we're on an Amazon page
    checkCurrentPage();
  }

  /**
   * Setup all event listeners
   */
  function setupEventListeners() {
    // Tab switching
    elements.tabs.forEach(tab => {
      tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // URL search
    elements.searchBtn.addEventListener('click', handleUrlSearch);
    elements.urlInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleUrlSearch();
    });

    // Image upload
    elements.uploadArea.addEventListener('click', () => elements.imageInput.click());
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('drop', handleDrop);
    elements.imageInput.addEventListener('change', handleImageSelect);
    elements.removeImageBtn.addEventListener('click', removeImage);
    elements.imageSearchBtn.addEventListener('click', handleImageSearch);

    // Sort
    elements.sortSelect.addEventListener('change', handleSort);

    // Settings
    elements.settingsBtn.addEventListener('click', openSettings);
    elements.closeSettingsBtn.addEventListener('click', closeSettings);
    elements.saveSettingsBtn.addEventListener('click', saveSettings);
    elements.clearCacheBtn.addEventListener('click', clearCache);
    elements.clearHistoryBtn.addEventListener('click', clearHistory);

    // Links
    elements.privacyLink.addEventListener('click', (e) => {
      e.preventDefault();
      chrome.tabs.create({ url: 'https://github.com/serchify/privacy' });
    });

    elements.supportLink.addEventListener('click', (e) => {
      e.preventDefault();
      chrome.tabs.create({ url: 'https://github.com/serchify/support' });
    });

    elements.affiliateDisclosureLink.addEventListener('click', (e) => {
      e.preventDefault();
      chrome.tabs.create({ url: 'https://github.com/serchify/affiliate-disclosure' });
    });
  }

  /**
   * Switch between tabs
   */
  function switchTab(tabName) {
    elements.tabs.forEach(tab => {
      tab.classList.toggle('active', tab.dataset.tab === tabName);
    });

    elements.urlTab.classList.toggle('active', tabName === 'url');
    elements.imageTab.classList.toggle('active', tabName === 'image');
  }

  /**
   * Handle URL search
   */
  async function handleUrlSearch() {
    const url = elements.urlInput.value.trim();

    if (!url) {
      showNotification('Please enter an Amazon product URL', 'error');
      return;
    }

    if (!isAmazonUrl(url)) {
      showNotification('Please enter a valid Amazon product URL', 'error');
      return;
    }

    // Extract ASIN from URL
    const asin = extractAsinFromUrl(url);
    if (!asin) {
      showNotification('Could not extract product ID from URL', 'error');
      return;
    }

    // Show loading state
    showLoading();

    try {
      // In a real implementation, we would fetch product data from Amazon
      // For now, simulate with basic data
      const productData = {
        asin: asin,
        title: 'Product from Amazon',
        imageUrl: '',
        price: 0,
        brand: '',
        url: url
      };

      const response = await chrome.runtime.sendMessage({
        type: 'SEARCH_PRODUCT',
        data: productData
      });

      if (response.success) {
        searchResults = response.data.results;
        displayResults(searchResults);
        addToRecentSearches(url);
      } else {
        showNotification(`Search failed: ${response.error}`, 'error');
        hideLoading();
      }
    } catch (error) {
      console.error('[Popup] Search error:', error);
      showNotification('An error occurred during search', 'error');
      hideLoading();
    }
  }

  /**
   * Handle image selection
   */
  function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file) {
      displayImagePreview(file);
    }
  }

  /**
   * Handle drag over
   */
  function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
  }

  /**
   * Handle drop
   */
  function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();

    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      displayImagePreview(file);
    }
  }

  /**
   * Display image preview
   */
  function displayImagePreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      elements.previewImg.src = e.target.result;
      elements.uploadArea.style.display = 'none';
      elements.imagePreview.style.display = 'block';
      elements.imageSearchBtn.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  /**
   * Remove image
   */
  function removeImage() {
    elements.previewImg.src = '';
    elements.uploadArea.style.display = 'block';
    elements.imagePreview.style.display = 'none';
    elements.imageSearchBtn.style.display = 'none';
    elements.imageInput.value = '';
  }

  /**
   * Handle image search
   */
  async function handleImageSearch() {
    const imageDataUrl = elements.previewImg.src;

    if (!imageDataUrl) {
      showNotification('Please upload an image first', 'error');
      return;
    }

    showLoading();

    try {
      const response = await chrome.runtime.sendMessage({
        type: 'REVERSE_IMAGE_SEARCH',
        data: { dataUrl: imageDataUrl }
      });

      if (response.success) {
        searchResults = response.data.results;
        displayResults(searchResults);
      } else {
        showNotification(`Image search failed: ${response.error}`, 'error');
        hideLoading();
      }
    } catch (error) {
      console.error('[Popup] Image search error:', error);
      showNotification('An error occurred during image search', 'error');
      hideLoading();
    }
  }

  /**
   * Display search results
   */
  function displayResults(results) {
    hideLoading();

    elements.resultsSection.style.display = 'block';
    elements.resultsCount.textContent = results.length;
    elements.resultsList.innerHTML = '';

    if (results.length === 0) {
      elements.resultsList.innerHTML = '<p class="empty-state">No alternatives found</p>';
      return;
    }

    results.forEach(result => {
      const resultElement = createResultElement(result);
      elements.resultsList.appendChild(resultElement);
    });
  }

  /**
   * Create result element
   */
  function createResultElement(result) {
    const div = document.createElement('div');
    div.className = 'result-item';

    const savings = result.savings > 0
      ? `<span class="result-savings">Save ${result.savings}%</span>`
      : '';

    div.innerHTML = `
      <div class="result-image">
        <img src="${result.imageUrl}" alt="${result.title}" loading="lazy">
      </div>
      <div class="result-info">
        <div class="result-title" title="${result.title}">${truncate(result.title, 50)}</div>
        <div class="result-meta">
          <span class="result-price">$${result.price.toFixed(2)}</span>
          ${savings}
          <span class="result-platform">${result.platform}</span>
        </div>
        <a href="${getProductLink(result)}" target="_blank" class="result-link">View Product →</a>
      </div>
    `;

    return div;
  }

  /**
   * Get product link with affiliate code if enabled
   */
  function getProductLink(result) {
    if (currentSettings && currentSettings.enableAffiliate) {
      // Append affiliate parameters based on platform
      // This is a placeholder - actual implementation would vary by platform
      return result.productUrl + '?ref=serchify';
    }
    return result.productUrl;
  }

  /**
   * Handle sort
   */
  function handleSort() {
    const sortBy = elements.sortSelect.value;

    const sorted = [...searchResults].sort((a, b) => {
      switch (sortBy) {
        case 'price':
          return a.price - b.price;
        case 'price-desc':
          return b.price - a.price;
        case 'rating':
          return b.sellerRating - a.sellerRating;
        case 'confidence':
        default:
          return b.confidenceScore - a.confidenceScore;
      }
    });

    displayResults(sorted);
  }

  /**
   * Load settings
   */
  async function loadSettings() {
    try {
      const response = await chrome.runtime.sendMessage({ type: 'GET_SETTINGS' });
      if (response.success) {
        currentSettings = response.data;
        applySettings(currentSettings);
      }
    } catch (error) {
      console.error('[Popup] Error loading settings:', error);
    }
  }

  /**
   * Apply settings to UI
   */
  function applySettings(settings) {
    // Platform checkboxes
    elements.platformCheckboxes.forEach(checkbox => {
      checkbox.checked = settings.preferredPlatforms.includes(checkbox.value);
    });

    // Privacy settings
    elements.enableTracking.checked = settings.enableTracking;
    elements.enableAffiliate.checked = settings.enableAffiliate;

    // Display settings
    elements.priceThreshold.value = settings.priceThreshold;
  }

  /**
   * Open settings panel
   */
  function openSettings() {
    elements.settingsPanel.style.display = 'flex';
  }

  /**
   * Close settings panel
   */
  function closeSettings() {
    elements.settingsPanel.style.display = 'none';
  }

  /**
   * Save settings
   */
  async function saveSettings() {
    const selectedPlatforms = Array.from(elements.platformCheckboxes)
      .filter(cb => cb.checked)
      .map(cb => cb.value);

    const newSettings = {
      preferredPlatforms: selectedPlatforms,
      enableTracking: elements.enableTracking.checked,
      enableAffiliate: elements.enableAffiliate.checked,
      priceThreshold: parseInt(elements.priceThreshold.value)
    };

    try {
      const response = await chrome.runtime.sendMessage({
        type: 'UPDATE_SETTINGS',
        data: newSettings
      });

      if (response.success) {
        currentSettings = newSettings;
        showNotification('Settings saved successfully', 'success');
        closeSettings();
      } else {
        showNotification('Failed to save settings', 'error');
      }
    } catch (error) {
      console.error('[Popup] Error saving settings:', error);
      showNotification('An error occurred while saving settings', 'error');
    }
  }

  /**
   * Clear cache
   */
  async function clearCache() {
    try {
      const response = await chrome.runtime.sendMessage({ type: 'CLEAR_CACHE' });
      if (response.success) {
        showNotification('Cache cleared successfully', 'success');
      } else {
        showNotification('Failed to clear cache', 'error');
      }
    } catch (error) {
      console.error('[Popup] Error clearing cache:', error);
      showNotification('An error occurred while clearing cache', 'error');
    }
  }

  /**
   * Clear search history
   */
  function clearHistory() {
    chrome.storage.local.set({ searchHistory: [] }, () => {
      recentSearches = [];
      renderRecentSearches();
      showNotification('Search history cleared', 'success');
    });
  }

  /**
   * Load recent searches
   */
  async function loadRecentSearches() {
    chrome.storage.local.get(['searchHistory'], (result) => {
      recentSearches = result.searchHistory || [];
      renderRecentSearches();
    });
  }

  /**
   * Render recent searches
   */
  function renderRecentSearches() {
    elements.recentList.innerHTML = '';

    if (recentSearches.length === 0) {
      elements.recentList.innerHTML = '<p class="empty-state">No recent searches</p>';
      return;
    }

    recentSearches.slice(0, 5).forEach(search => {
      const div = document.createElement('div');
      div.className = 'recent-item';
      div.textContent = truncate(search.query, 50);
      div.addEventListener('click', () => {
        elements.urlInput.value = search.query;
        switchTab('url');
      });
      elements.recentList.appendChild(div);
    });
  }

  /**
   * Add to recent searches
   */
  function addToRecentSearches(query) {
    const search = {
      query: query,
      timestamp: Date.now()
    };

    recentSearches.unshift(search);
    recentSearches = recentSearches.slice(0, 10); // Keep only last 10

    chrome.storage.local.set({ searchHistory: recentSearches }, () => {
      renderRecentSearches();
    });
  }

  /**
   * Check current page
   */
  async function checkCurrentPage() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab && tab.url && isAmazonUrl(tab.url)) {
        elements.urlInput.value = tab.url;
        elements.urlInput.placeholder = 'Current Amazon page detected';
      }
    } catch (error) {
      console.error('[Popup] Error checking current page:', error);
    }
  }

  /**
   * Show loading state
   */
  function showLoading() {
    elements.loadingState.style.display = 'block';
    elements.resultsSection.style.display = 'none';
  }

  /**
   * Hide loading state
   */
  function hideLoading() {
    elements.loadingState.style.display = 'none';
  }

  /**
   * Show notification
   */
  function showNotification(message, type = 'info') {
    // Simple alert for now - could be enhanced with a better notification system
    alert(message);
  }

  /**
   * Check if URL is an Amazon URL
   */
  function isAmazonUrl(url) {
    return url.includes('amazon.com') && (url.includes('/dp/') || url.includes('/gp/product/'));
  }

  /**
   * Extract ASIN from Amazon URL
   */
  function extractAsinFromUrl(url) {
    const match = url.match(/\/dp\/([A-Z0-9]{10})|\/gp\/product\/([A-Z0-9]{10})/);
    return match ? (match[1] || match[2]) : null;
  }

  /**
   * Truncate text
   */
  function truncate(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }

})();
