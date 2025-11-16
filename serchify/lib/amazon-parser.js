/**
 * Amazon Product Parser
 * Utility functions for parsing Amazon product pages
 */

const AmazonParser = {
  /**
   * Check if a URL is an Amazon product page
   */
  isAmazonProductUrl(url) {
    if (!url) return false;
    return url.includes('amazon.com') && (url.includes('/dp/') || url.includes('/gp/product/'));
  },

  /**
   * Extract ASIN from URL
   */
  extractASIN(url) {
    if (!url) return null;

    // Try standard pattern
    const dpMatch = url.match(/\/dp\/([A-Z0-9]{10})/);
    if (dpMatch) return dpMatch[1];

    // Try product pattern
    const productMatch = url.match(/\/gp\/product\/([A-Z0-9]{10})/);
    if (productMatch) return productMatch[1];

    // Try offer listing pattern
    const offerMatch = url.match(/\/offer-listing\/([A-Z0-9]{10})/);
    if (offerMatch) return offerMatch[1];

    return null;
  },

  /**
   * Extract product data from Amazon page DOM
   */
  extractProductData(document) {
    return {
      asin: this.extractASINFromPage(document),
      title: this.extractTitle(document),
      imageUrl: this.extractMainImage(document),
      price: this.extractPrice(document),
      brand: this.extractBrand(document),
      category: this.extractCategory(document),
      specifications: this.extractSpecifications(document),
      rating: this.extractRating(document),
      reviewCount: this.extractReviewCount(document),
      availability: this.extractAvailability(document)
    };
  },

  /**
   * Extract ASIN from page DOM
   */
  extractASINFromPage(doc) {
    // Try input field
    const asinInput = doc.querySelector('input[name="ASIN"]');
    if (asinInput) return asinInput.value;

    // Try data attribute
    const productElement = doc.querySelector('[data-asin]');
    if (productElement) return productElement.dataset.asin;

    // Try URL
    return this.extractASIN(window.location.href);
  },

  /**
   * Extract product title
   */
  extractTitle(doc) {
    const selectors = [
      '#productTitle',
      '#title',
      'h1.product-title',
      '[data-feature-name="title"] h1'
    ];

    for (const selector of selectors) {
      const element = doc.querySelector(selector);
      if (element) {
        return element.textContent.trim();
      }
    }

    return null;
  },

  /**
   * Extract main product image
   */
  extractMainImage(doc) {
    const selectors = [
      '#landingImage',
      '#imgTagWrapperId img',
      '#imageBlock img',
      '[data-a-image-name="landingImage"]',
      '.imgTagWrapper img'
    ];

    for (const selector of selectors) {
      const img = doc.querySelector(selector);
      if (img && img.src) {
        // Get high-resolution version by removing size parameters
        let imageUrl = img.src;
        imageUrl = imageUrl.replace(/\._[A-Z0-9_,]+_\./, '.');
        return imageUrl;
      }
    }

    return null;
  },

  /**
   * Extract product price
   */
  extractPrice(doc) {
    const selectors = [
      '.a-price .a-offscreen',
      '#priceblock_ourprice',
      '#priceblock_dealprice',
      '#priceblock_saleprice',
      '.a-price-whole',
      '[data-a-color="price"] .a-offscreen',
      '.apexPriceToPay .a-offscreen'
    ];

    for (const selector of selectors) {
      const element = doc.querySelector(selector);
      if (element) {
        const priceText = element.textContent.trim();
        const priceMatch = priceText.match(/[\d,.]+/);
        if (priceMatch) {
          return parseFloat(priceMatch[0].replace(/,/g, ''));
        }
      }
    }

    return null;
  },

  /**
   * Extract brand
   */
  extractBrand(doc) {
    // Try byline info
    const byline = doc.querySelector('#bylineInfo');
    if (byline) {
      let brandText = byline.textContent.trim();
      brandText = brandText.replace(/^(Visit the |Brand: )/i, '');
      brandText = brandText.replace(/ Store$/i, '');
      return brandText;
    }

    // Try brand link
    const brandLink = doc.querySelector('a[data-attribute="brand"]');
    if (brandLink) {
      return brandLink.textContent.trim();
    }

    // Try product details
    const brandRow = Array.from(doc.querySelectorAll('th')).find(
      th => th.textContent.trim().toLowerCase() === 'brand'
    );
    if (brandRow) {
      const brandCell = brandRow.nextElementSibling;
      if (brandCell) return brandCell.textContent.trim();
    }

    return null;
  },

  /**
   * Extract category
   */
  extractCategory(doc) {
    // Try breadcrumbs
    const breadcrumbs = doc.querySelectorAll('#wayfinding-breadcrumbs_feature_div a');
    if (breadcrumbs.length > 0) {
      const categories = Array.from(breadcrumbs).map(el => el.textContent.trim());
      return categories[categories.length - 1];
    }

    // Try department
    const department = doc.querySelector('[data-feature-name="department"]');
    if (department) {
      return department.textContent.trim();
    }

    return null;
  },

  /**
   * Extract product specifications
   */
  extractSpecifications(doc) {
    const specs = {};

    // Try product details section
    const detailRows = doc.querySelectorAll('#productDetails_detailBullets_sections1 tr');
    detailRows.forEach(row => {
      const label = row.querySelector('th');
      const value = row.querySelector('td');
      if (label && value) {
        const key = label.textContent.trim().replace(/\s+/g, ' ');
        specs[key] = value.textContent.trim().replace(/\s+/g, ' ');
      }
    });

    // Try technical specifications
    const techRows = doc.querySelectorAll('#productDetails_techSpec_section_1 tr');
    techRows.forEach(row => {
      const cells = row.querySelectorAll('td, th');
      if (cells.length >= 2) {
        const key = cells[0].textContent.trim().replace(/\s+/g, ' ');
        const value = cells[1].textContent.trim().replace(/\s+/g, ' ');
        specs[key] = value;
      }
    });

    // Try detail bullets
    const bullets = doc.querySelectorAll('#detailBullets_feature_div li');
    bullets.forEach(bullet => {
      const text = bullet.textContent.trim();
      const parts = text.split(':');
      if (parts.length >= 2) {
        const key = parts[0].trim().replace(/\s+/g, ' ');
        const value = parts.slice(1).join(':').trim().replace(/\s+/g, ' ');
        specs[key] = value;
      }
    });

    return specs;
  },

  /**
   * Extract product rating
   */
  extractRating(doc) {
    const ratingElement = doc.querySelector('[data-hook="rating-out-of-text"]');
    if (ratingElement) {
      const ratingText = ratingElement.textContent.trim();
      const match = ratingText.match(/[\d.]+/);
      if (match) {
        return parseFloat(match[0]);
      }
    }

    // Try alternate selectors
    const ratingSpan = doc.querySelector('.a-icon-star .a-icon-alt');
    if (ratingSpan) {
      const match = ratingSpan.textContent.match(/[\d.]+/);
      if (match) {
        return parseFloat(match[0]);
      }
    }

    return null;
  },

  /**
   * Extract review count
   */
  extractReviewCount(doc) {
    const reviewElement = doc.querySelector('#acrCustomerReviewText');
    if (reviewElement) {
      const reviewText = reviewElement.textContent.trim();
      const match = reviewText.match(/[\d,]+/);
      if (match) {
        return parseInt(match[0].replace(/,/g, ''));
      }
    }

    return null;
  },

  /**
   * Extract availability
   */
  extractAvailability(doc) {
    const availabilityElement = doc.querySelector('#availability');
    if (availabilityElement) {
      const text = availabilityElement.textContent.trim().toLowerCase();
      if (text.includes('in stock')) return 'in_stock';
      if (text.includes('out of stock')) return 'out_of_stock';
      if (text.includes('temporarily out')) return 'temporarily_unavailable';
    }

    return 'unknown';
  },

  /**
   * Generate search keywords from product data
   */
  generateSearchKeywords(productData) {
    const keywords = [];

    if (productData.brand) {
      keywords.push(productData.brand);
    }

    if (productData.title) {
      // Extract key terms from title (exclude common words)
      const stopWords = ['the', 'a', 'an', 'and', 'or', 'but', 'for', 'with', 'pack', 'of'];
      const titleWords = productData.title
        .toLowerCase()
        .split(/\s+/)
        .filter(word => word.length > 3 && !stopWords.includes(word));

      keywords.push(...titleWords.slice(0, 5)); // Take first 5 significant words
    }

    // Remove duplicates
    return [...new Set(keywords)];
  },

  /**
   * Calculate product hash for caching
   */
  generateProductHash(productData) {
    const key = `${productData.asin}_${productData.title}`;
    // Simple hash function
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      const char = key.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(36);
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AmazonParser;
}
