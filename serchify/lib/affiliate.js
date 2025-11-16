/**
 * Affiliate Link Handler
 * Manages affiliate links with transparency and user control
 */

const AffiliateHandler = {
  /**
   * Affiliate configuration for different platforms
   */
  affiliateConfig: {
    aliexpress: {
      enabled: true,
      paramName: 'aff_trace_key',
      paramValue: 'serchify_affiliate_id', // Replace with actual affiliate ID
      additionalParams: {
        'aff_platform': 'serchify',
        'sk': 'serchify'
      }
    },
    temu: {
      enabled: true,
      paramName: 'refer_page_sn',
      paramValue: 'serchify_temu', // Replace with actual affiliate ID
      additionalParams: {}
    },
    wish: {
      enabled: true,
      paramName: 'share',
      paramValue: 'serchify', // Replace with actual affiliate ID
      additionalParams: {}
    },
    dhgate: {
      enabled: true,
      paramName: 'f',
      paramValue: 'serchify', // Replace with actual affiliate ID
      additionalParams: {}
    },
    banggood: {
      enabled: true,
      paramName: 'p',
      paramValue: 'serchify_affiliate', // Replace with actual affiliate ID
      additionalParams: {}
    },
    ebay: {
      enabled: true,
      paramName: 'mkcid',
      paramValue: '1', // eBay Partner Network ID
      additionalParams: {
        'mkrid': 'serchify',
        'campid': 'serchify_campaign'
      }
    }
  },

  /**
   * Add affiliate parameters to product URL
   */
  addAffiliateLink(url, platform, settings = { enableAffiliate: true }) {
    // Check if affiliate links are enabled in settings
    if (!settings.enableAffiliate) {
      return url;
    }

    // Get platform config
    const config = this.affiliateConfig[platform.toLowerCase()];
    if (!config || !config.enabled) {
      return url;
    }

    try {
      const urlObj = new URL(url);

      // Add main affiliate parameter
      urlObj.searchParams.set(config.paramName, config.paramValue);

      // Add additional parameters
      for (const [key, value] of Object.entries(config.additionalParams)) {
        urlObj.searchParams.set(key, value);
      }

      // Add tracking timestamp
      urlObj.searchParams.set('serchify_ts', Date.now().toString());

      return urlObj.toString();
    } catch (error) {
      console.error('[Affiliate] Error adding affiliate link:', error);
      return url; // Return original URL if error
    }
  },

  /**
   * Batch process URLs with affiliate links
   */
  processResults(results, settings = { enableAffiliate: true }) {
    return results.map(result => ({
      ...result,
      productUrl: this.addAffiliateLink(result.productUrl, result.platform, settings),
      isAffiliate: settings.enableAffiliate && this.affiliateConfig[result.platform.toLowerCase()]?.enabled,
      originalUrl: result.productUrl // Keep original for transparency
    }));
  },

  /**
   * Check if a URL contains affiliate parameters
   */
  isAffiliateLink(url) {
    try {
      const urlObj = new URL(url);
      const params = urlObj.searchParams;

      // Check for common affiliate parameters
      const affiliateParams = [
        'aff_trace_key',
        'refer_page_sn',
        'share',
        'mkcid',
        'mkrid',
        'serchify_ts'
      ];

      return affiliateParams.some(param => params.has(param));
    } catch (error) {
      return false;
    }
  },

  /**
   * Remove affiliate parameters from URL
   */
  removeAffiliateParams(url) {
    try {
      const urlObj = new URL(url);

      // List of affiliate parameters to remove
      const affiliateParams = [
        'aff_trace_key',
        'aff_platform',
        'sk',
        'refer_page_sn',
        'share',
        'f',
        'p',
        'mkcid',
        'mkrid',
        'campid',
        'serchify_ts'
      ];

      affiliateParams.forEach(param => {
        urlObj.searchParams.delete(param);
      });

      return urlObj.toString();
    } catch (error) {
      console.error('[Affiliate] Error removing affiliate params:', error);
      return url;
    }
  },

  /**
   * Get affiliate disclosure text
   */
  getDisclosureText(platform) {
    return {
      short: 'This link may include affiliate codes.',
      full: `This link includes affiliate tracking codes. When you make a purchase through this link, ${platform} may provide a small commission to Serchify at no extra cost to you. This helps support the development of this extension. You can disable affiliate links in settings.`,
      legal: 'As an affiliate partner, we may earn commissions from qualifying purchases. This does not affect the price you pay.'
    };
  },

  /**
   * Generate visual indicator for affiliate links
   */
  getAffiliateIndicator(isAffiliate) {
    if (!isAffiliate) {
      return null;
    }

    return {
      icon: '🔗',
      label: 'Affiliate Link',
      tooltip: 'This link supports Serchify development',
      color: '#10b981'
    };
  },

  /**
   * Track affiliate clicks (with user consent)
   */
  async trackClick(url, platform, settings = { enableTracking: false }) {
    if (!settings.enableTracking) {
      return; // Respect user privacy settings
    }

    try {
      // In production, this would send analytics to a backend
      const trackingData = {
        platform: platform,
        timestamp: Date.now(),
        isAffiliate: this.isAffiliateLink(url),
        sessionId: this.getSessionId()
      };

      // Store locally for privacy (not sent to server unless user consents)
      await this.storeTrackingData(trackingData);

      console.log('[Affiliate] Click tracked (locally only):', trackingData);
    } catch (error) {
      console.error('[Affiliate] Tracking error:', error);
    }
  },

  /**
   * Get or create session ID
   */
  getSessionId() {
    let sessionId = sessionStorage.getItem('serchify_session_id');
    if (!sessionId) {
      sessionId = this.generateSessionId();
      sessionStorage.setItem('serchify_session_id', sessionId);
    }
    return sessionId;
  },

  /**
   * Generate unique session ID
   */
  generateSessionId() {
    return `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  },

  /**
   * Store tracking data locally
   */
  async storeTrackingData(data) {
    return new Promise((resolve) => {
      chrome.storage.local.get(['affiliateTracking'], (result) => {
        const tracking = result.affiliateTracking || [];
        tracking.push(data);

        // Keep only last 100 entries
        const trimmed = tracking.slice(-100);

        chrome.storage.local.set({ affiliateTracking: trimmed }, resolve);
      });
    });
  },

  /**
   * Get affiliate statistics (for user transparency)
   */
  async getStatistics() {
    return new Promise((resolve) => {
      chrome.storage.local.get(['affiliateTracking'], (result) => {
        const tracking = result.affiliateTracking || [];

        const stats = {
          totalClicks: tracking.length,
          affiliateClicks: tracking.filter(t => t.isAffiliate).length,
          nonAffiliateClicks: tracking.filter(t => !t.isAffiliate).length,
          byPlatform: {},
          last7Days: 0,
          last30Days: 0
        };

        // Count by platform
        tracking.forEach(t => {
          if (!stats.byPlatform[t.platform]) {
            stats.byPlatform[t.platform] = 0;
          }
          stats.byPlatform[t.platform]++;
        });

        // Time-based stats
        const now = Date.now();
        const day = 24 * 60 * 60 * 1000;
        stats.last7Days = tracking.filter(t => now - t.timestamp < 7 * day).length;
        stats.last30Days = tracking.filter(t => now - t.timestamp < 30 * day).length;

        resolve(stats);
      });
    });
  },

  /**
   * Clear all tracking data
   */
  async clearTrackingData() {
    return new Promise((resolve) => {
      chrome.storage.local.set({ affiliateTracking: [] }, resolve);
    });
  },

  /**
   * Export tracking data (for GDPR compliance)
   */
  async exportTrackingData() {
    return new Promise((resolve) => {
      chrome.storage.local.get(['affiliateTracking'], (result) => {
        const tracking = result.affiliateTracking || [];
        const exportData = {
          exportDate: new Date().toISOString(),
          totalRecords: tracking.length,
          data: tracking
        };
        resolve(JSON.stringify(exportData, null, 2));
      });
    });
  },

  /**
   * Validate affiliate configuration
   */
  validateConfig() {
    const errors = [];

    for (const [platform, config] of Object.entries(this.affiliateConfig)) {
      if (config.enabled) {
        if (!config.paramName) {
          errors.push(`${platform}: Missing paramName`);
        }
        if (!config.paramValue || config.paramValue.includes('_affiliate_id')) {
          errors.push(`${platform}: Affiliate ID not configured (using placeholder)`);
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  },

  /**
   * Generate affiliate disclosure page content
   */
  getDisclosurePage() {
    const platforms = Object.keys(this.affiliateConfig)
      .filter(p => this.affiliateConfig[p].enabled)
      .join(', ');

    return `
# Affiliate Disclosure

## How Affiliate Links Work

Serchify uses affiliate links to support the development and maintenance of this extension. When you click on a product link and make a purchase, we may earn a small commission at no extra cost to you.

## Platforms Using Affiliate Links

We currently use affiliate links for the following platforms:
${platforms}

## Transparency

- **Clearly Marked**: All affiliate links are marked with a visual indicator
- **Original Links Available**: You can always view the original, non-affiliate link
- **Optional**: You can disable affiliate links entirely in Settings
- **No Price Markup**: Affiliate links do not affect the price you pay

## Your Control

You have full control over affiliate links:
1. **Disable in Settings**: Turn off affiliate links completely
2. **View Original URLs**: See the product URL without affiliate parameters
3. **Privacy First**: We only track clicks with your explicit consent

## Data Collection

When affiliate links are enabled, we collect:
- Platform clicked
- Timestamp of click
- Whether link was affiliate or regular

We DO NOT collect:
- Your personal information
- What you purchase
- How much you spend
- Your browsing history

## Questions?

If you have questions about our affiliate program, please contact us at support@serchify.example.com

Last updated: ${new Date().toLocaleDateString()}
    `;
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AffiliateHandler;
}
