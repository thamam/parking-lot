/**
 * Amazon Product Detector Content Script
 * Detects Amazon product pages and extracts product information
 */

(function() {
  'use strict';

  console.log('[Amazon Detector] Content script loaded');

  /**
   * Check if current page is an Amazon product page
   */
  function isAmazonProductPage() {
    // Check URL pattern
    const url = window.location.href;
    const isProductPage = url.includes('/dp/') || url.includes('/gp/product/');

    // Additional check: look for product title element
    const hasProductTitle = document.querySelector('#productTitle') !== null;

    return isProductPage && hasProductTitle;
  }

  /**
   * Extract ASIN from URL or page
   */
  function extractASIN() {
    // Try URL first
    const urlMatch = window.location.href.match(/\/dp\/([A-Z0-9]{10})/);
    if (urlMatch) {
      return urlMatch[1];
    }

    // Try alternate URL pattern
    const altMatch = window.location.href.match(/\/gp\/product\/([A-Z0-9]{10})/);
    if (altMatch) {
      return altMatch[1];
    }

    // Try to find in page
    const asinInput = document.querySelector('input[name="ASIN"]');
    if (asinInput) {
      return asinInput.value;
    }

    return null;
  }

  /**
   * Extract product title
   */
  function extractTitle() {
    const titleElement = document.querySelector('#productTitle');
    if (titleElement) {
      return titleElement.textContent.trim();
    }
    return null;
  }

  /**
   * Extract product image URL
   */
  function extractImageUrl() {
    // Try main product image
    const mainImage = document.querySelector('#landingImage, #imgTagWrapperId img, #imageBlock img');
    if (mainImage && mainImage.src) {
      // Get high-resolution version
      let imageUrl = mainImage.src;
      // Replace thumbnail size with larger size
      imageUrl = imageUrl.replace(/\._[A-Z0-9_]+_\./, '.');
      return imageUrl;
    }

    // Fallback to any product image
    const anyImage = document.querySelector('[data-a-image-name="landingImage"]');
    if (anyImage && anyImage.src) {
      return anyImage.src;
    }

    return null;
  }

  /**
   * Extract product price
   */
  function extractPrice() {
    // Try various price selectors
    const priceSelectors = [
      '.a-price .a-offscreen',
      '#priceblock_ourprice',
      '#priceblock_dealprice',
      '.a-price-whole',
      '[data-a-color="price"] .a-offscreen'
    ];

    for (const selector of priceSelectors) {
      const priceElement = document.querySelector(selector);
      if (priceElement) {
        const priceText = priceElement.textContent.trim();
        // Extract number from price text
        const priceMatch = priceText.match(/[\d,.]+/);
        if (priceMatch) {
          return parseFloat(priceMatch[0].replace(',', ''));
        }
      }
    }

    return null;
  }

  /**
   * Extract product brand
   */
  function extractBrand() {
    // Try brand link
    const brandLink = document.querySelector('#bylineInfo');
    if (brandLink) {
      const brandText = brandLink.textContent.trim();
      // Remove "Visit the " or "Brand: " prefix
      return brandText.replace(/^(Visit the |Brand: )/i, '').replace(/ Store$/i, '');
    }

    // Try alternative selectors
    const brandSelectors = [
      'a[data-attribute="brand"]',
      '[data-feature-name="bylineInfo"] a',
      'tr:has(th:contains("Brand")) td'
    ];

    for (const selector of brandSelectors) {
      const brandElement = document.querySelector(selector);
      if (brandElement) {
        return brandElement.textContent.trim();
      }
    }

    return null;
  }

  /**
   * Extract product category
   */
  function extractCategory() {
    const breadcrumbs = document.querySelectorAll('#wayfinding-breadcrumbs_feature_div a');
    if (breadcrumbs.length > 0) {
      const categories = Array.from(breadcrumbs).map(el => el.textContent.trim());
      return categories[categories.length - 1]; // Return the most specific category
    }
    return null;
  }

  /**
   * Extract all product specifications
   */
  function extractSpecifications() {
    const specs = {};

    // Try product details table
    const detailRows = document.querySelectorAll('#productDetails_detailBullets_sections1 tr');
    detailRows.forEach(row => {
      const label = row.querySelector('th');
      const value = row.querySelector('td');
      if (label && value) {
        specs[label.textContent.trim()] = value.textContent.trim();
      }
    });

    // Try technical details
    const techRows = document.querySelectorAll('#productDetails_techSpec_section_1 tr');
    techRows.forEach(row => {
      const label = row.querySelector('th');
      const value = row.querySelector('td');
      if (label && value) {
        specs[label.textContent.trim()] = value.textContent.trim();
      }
    });

    return specs;
  }

  /**
   * Extract all product data
   */
  function extractProductData() {
    if (!isAmazonProductPage()) {
      return null;
    }

    const asin = extractASIN();
    if (!asin) {
      console.warn('[Amazon Detector] Could not extract ASIN');
      return null;
    }

    const productData = {
      asin: asin,
      title: extractTitle(),
      imageUrl: extractImageUrl(),
      price: extractPrice(),
      brand: extractBrand(),
      category: extractCategory(),
      specifications: extractSpecifications(),
      url: window.location.href,
      timestamp: Date.now()
    };

    console.log('[Amazon Detector] Extracted product data:', productData);
    return productData;
  }

  /**
   * Notify background script that product data is available
   */
  function notifyProductDetected() {
    const productData = extractProductData();
    if (productData) {
      // Store in page context for overlay access
      window.serchifyProductData = productData;

      // Notify background (if needed for other purposes)
      chrome.runtime.sendMessage({
        type: 'PRODUCT_DETECTED',
        data: productData
      });

      // Trigger overlay to show
      window.dispatchEvent(new CustomEvent('serchify:product-detected', {
        detail: productData
      }));
    }
  }

  /**
   * Initialize detector
   */
  function initialize() {
    // Check if we're on a product page
    if (isAmazonProductPage()) {
      console.log('[Amazon Detector] Product page detected');

      // Extract data after page load
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', notifyProductDetected);
      } else {
        // DOM already loaded
        notifyProductDetected();
      }

      // Also check after a short delay to ensure dynamic content is loaded
      setTimeout(notifyProductDetected, 1000);
    }
  }

  // Start detection
  initialize();

  // Expose extraction functions for testing
  window.serchifyDetector = {
    isAmazonProductPage,
    extractASIN,
    extractTitle,
    extractImageUrl,
    extractPrice,
    extractBrand,
    extractCategory,
    extractProductData
  };

})();
