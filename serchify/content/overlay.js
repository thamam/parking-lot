/**
 * Amazon Page Overlay
 * Injects "Find Cheaper" button on Amazon product pages
 */

(function() {
  'use strict';

  console.log('[Overlay] Script loaded');

  let overlayButton = null;
  let resultsBadge = null;
  let isSearching = false;

  /**
   * Create the floating "Find Cheaper" button
   */
  function createOverlayButton() {
    // Check if button already exists
    if (document.getElementById('serchify-overlay-btn')) {
      return;
    }

    // Create button
    const button = document.createElement('button');
    button.id = 'serchify-overlay-btn';
    button.className = 'serchify-floating-button';
    button.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span>Find Cheaper</span>
    `;
    button.title = 'Find this product on other marketplaces';

    // Create badge for results count
    const badge = document.createElement('span');
    badge.id = 'serchify-results-badge';
    badge.className = 'serchify-badge';
    badge.style.display = 'none';
    button.appendChild(badge);

    // Add click handler
    button.addEventListener('click', handleButtonClick);

    // Add to page
    document.body.appendChild(button);

    overlayButton = button;
    resultsBadge = badge;

    console.log('[Overlay] Button created');
  }

  /**
   * Handle button click
   */
  async function handleButtonClick() {
    if (isSearching) {
      return;
    }

    // Get product data from detector
    const productData = window.serchifyProductData;
    if (!productData) {
      showNotification('Could not extract product information', 'error');
      return;
    }

    isSearching = true;
    updateButtonState('searching');

    try {
      // Send search request to background
      const response = await chrome.runtime.sendMessage({
        type: 'SEARCH_PRODUCT',
        data: productData
      });

      if (response.success) {
        const results = response.data.results;
        updateButtonState('results', results.length);
        showResults(results, productData);
      } else {
        showNotification(`Search failed: ${response.error}`, 'error');
        updateButtonState('idle');
      }
    } catch (error) {
      console.error('[Overlay] Search error:', error);
      showNotification('An error occurred during search', 'error');
      updateButtonState('idle');
    } finally {
      isSearching = false;
    }
  }

  /**
   * Update button visual state
   */
  function updateButtonState(state, count) {
    if (!overlayButton) return;

    overlayButton.classList.remove('searching', 'has-results');

    switch (state) {
      case 'searching':
        overlayButton.classList.add('searching');
        overlayButton.innerHTML = `
          <div class="serchify-spinner"></div>
          <span>Searching...</span>
        `;
        break;

      case 'results':
        overlayButton.classList.add('has-results');
        overlayButton.innerHTML = `
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>Find Cheaper</span>
          <span class="serchify-badge">${count}</span>
        `;
        break;

      case 'idle':
      default:
        overlayButton.innerHTML = `
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>Find Cheaper</span>
        `;
        break;
    }
  }

  /**
   * Show results in a side panel or modal
   */
  function showResults(results, originalProduct) {
    // Remove existing results panel
    const existingPanel = document.getElementById('serchify-results-panel');
    if (existingPanel) {
      existingPanel.remove();
    }

    // Create results panel
    const panel = document.createElement('div');
    panel.id = 'serchify-results-panel';
    panel.className = 'serchify-panel';

    // Create header
    const header = document.createElement('div');
    header.className = 'serchify-panel-header';
    header.innerHTML = `
      <h3>Alternative Marketplaces</h3>
      <button class="serchify-close-btn" title="Close">&times;</button>
    `;

    // Create results container
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'serchify-results-container';

    if (results.length === 0) {
      resultsContainer.innerHTML = '<p class="serchify-no-results">No alternatives found</p>';
    } else {
      results.forEach(result => {
        const resultCard = createResultCard(result, originalProduct);
        resultsContainer.appendChild(resultCard);
      });
    }

    // Assemble panel
    panel.appendChild(header);
    panel.appendChild(resultsContainer);

    // Add close handler
    header.querySelector('.serchify-close-btn').addEventListener('click', () => {
      panel.classList.remove('visible');
      setTimeout(() => panel.remove(), 300);
    });

    // Add to page
    document.body.appendChild(panel);

    // Trigger animation
    setTimeout(() => panel.classList.add('visible'), 10);
  }

  /**
   * Create a result card element
   */
  function createResultCard(result, originalProduct) {
    const card = document.createElement('div');
    card.className = 'serchify-result-card';

    const priceDiff = originalProduct.price
      ? ((originalProduct.price - result.price) / originalProduct.price * 100).toFixed(0)
      : 0;

    const savings = priceDiff > 0 ? `<span class="serchify-savings">Save ${priceDiff}%</span>` : '';

    card.innerHTML = `
      <div class="serchify-result-image">
        <img src="${result.imageUrl}" alt="${result.title}" loading="lazy">
        <span class="serchify-platform-badge">${result.platform}</span>
      </div>
      <div class="serchify-result-info">
        <h4 class="serchify-result-title">${truncate(result.title, 80)}</h4>
        <div class="serchify-result-meta">
          <span class="serchify-price">$${result.price.toFixed(2)}</span>
          ${savings}
          <span class="serchify-confidence">${result.confidenceScore.toFixed(0)}% match</span>
        </div>
        <div class="serchify-result-details">
          <span class="serchify-rating">⭐ ${result.sellerRating.toFixed(1)}</span>
          <span class="serchify-reviews">${result.reviewCount} reviews</span>
          ${result.shippingCost > 0 ? `<span class="serchify-shipping">+$${result.shippingCost.toFixed(2)} shipping</span>` : '<span class="serchify-shipping">Free shipping</span>'}
        </div>
        <a href="${result.productUrl}" target="_blank" class="serchify-view-btn">View Product →</a>
      </div>
    `;

    return card;
  }

  /**
   * Show notification
   */
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `serchify-notification serchify-notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('visible'), 10);
    setTimeout(() => {
      notification.classList.remove('visible');
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  /**
   * Truncate text to specified length
   */
  function truncate(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }

  /**
   * Initialize overlay
   */
  function initialize() {
    // Listen for product detection
    window.addEventListener('serchify:product-detected', (event) => {
      console.log('[Overlay] Product detected, creating button');
      createOverlayButton();
    });

    // If product data already exists, create button immediately
    if (window.serchifyProductData) {
      createOverlayButton();
    }
  }

  // Start overlay
  initialize();

})();
