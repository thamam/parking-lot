/**
 * Unit Tests for Affiliate Handler
 */

const AffiliateHandler = require('../../lib/affiliate');

describe('AffiliateHandler', () => {
  describe('addAffiliateLink', () => {
    test('should add affiliate parameters when enabled', () => {
      const url = 'https://www.aliexpress.com/item/123456.html';
      const settings = { enableAffiliate: true };

      const affiliateUrl = AffiliateHandler.addAffiliateLink(url, 'aliexpress', settings);

      expect(affiliateUrl).toContain('aff_trace_key');
      expect(affiliateUrl).toContain('serchify');
      expect(affiliateUrl).not.toBe(url);
    });

    test('should not add affiliate parameters when disabled', () => {
      const url = 'https://www.aliexpress.com/item/123456.html';
      const settings = { enableAffiliate: false };

      const affiliateUrl = AffiliateHandler.addAffiliateLink(url, 'aliexpress', settings);

      expect(affiliateUrl).toBe(url);
    });

    test('should handle different platforms', () => {
      const settings = { enableAffiliate: true };

      const platforms = ['aliexpress', 'temu', 'wish', 'ebay'];

      platforms.forEach(platform => {
        const url = `https://www.${platform}.com/item/123`;
        const affiliateUrl = AffiliateHandler.addAffiliateLink(url, platform, settings);

        expect(affiliateUrl).not.toBe(url);
        expect(affiliateUrl).toContain(url.split('?')[0]);
      });
    });

    test('should preserve existing query parameters', () => {
      const url = 'https://www.aliexpress.com/item/123456.html?color=red&size=L';
      const settings = { enableAffiliate: true };

      const affiliateUrl = AffiliateHandler.addAffiliateLink(url, 'aliexpress', settings);

      expect(affiliateUrl).toContain('color=red');
      expect(affiliateUrl).toContain('size=L');
      expect(affiliateUrl).toContain('aff_trace_key');
    });

    test('should handle invalid URLs gracefully', () => {
      const invalidUrl = 'not-a-valid-url';
      const settings = { enableAffiliate: true };

      const result = AffiliateHandler.addAffiliateLink(invalidUrl, 'aliexpress', settings);

      expect(result).toBe(invalidUrl);
    });
  });

  describe('isAffiliateLink', () => {
    test('should identify affiliate links', () => {
      const affiliateUrl = 'https://www.aliexpress.com/item/123?aff_trace_key=test';

      expect(AffiliateHandler.isAffiliateLink(affiliateUrl)).toBe(true);
    });

    test('should identify non-affiliate links', () => {
      const normalUrl = 'https://www.aliexpress.com/item/123';

      expect(AffiliateHandler.isAffiliateLink(normalUrl)).toBe(false);
    });

    test('should detect various affiliate parameters', () => {
      const urls = [
        'https://example.com?aff_trace_key=123',
        'https://example.com?refer_page_sn=456',
        'https://example.com?mkcid=1',
        'https://example.com?serchify_ts=789'
      ];

      urls.forEach(url => {
        expect(AffiliateHandler.isAffiliateLink(url)).toBe(true);
      });
    });
  });

  describe('removeAffiliateParams', () => {
    test('should remove affiliate parameters', () => {
      const affiliateUrl = 'https://www.example.com/item?aff_trace_key=test&color=red&serchify_ts=123';

      const cleanUrl = AffiliateHandler.removeAffiliateParams(affiliateUrl);

      expect(cleanUrl).not.toContain('aff_trace_key');
      expect(cleanUrl).not.toContain('serchify_ts');
      expect(cleanUrl).toContain('color=red');
    });

    test('should handle URLs without affiliate params', () => {
      const normalUrl = 'https://www.example.com/item?color=red';

      const result = AffiliateHandler.removeAffiliateParams(normalUrl);

      expect(result).toContain('color=red');
    });

    test('should remove all known affiliate parameters', () => {
      const url = 'https://example.com?aff_trace_key=1&refer_page_sn=2&mkcid=3&share=4';

      const cleanUrl = AffiliateHandler.removeAffiliateParams(url);

      expect(cleanUrl).not.toContain('aff_trace_key');
      expect(cleanUrl).not.toContain('refer_page_sn');
      expect(cleanUrl).not.toContain('mkcid');
      expect(cleanUrl).not.toContain('share');
    });
  });

  describe('processResults', () => {
    test('should add affiliate links to all results when enabled', () => {
      const results = [
        { productUrl: 'https://www.aliexpress.com/item/1', platform: 'aliexpress' },
        { productUrl: 'https://www.temu.com/item/2', platform: 'temu' }
      ];

      const settings = { enableAffiliate: true };

      const processed = AffiliateHandler.processResults(results, settings);

      expect(processed[0].isAffiliate).toBe(true);
      expect(processed[1].isAffiliate).toBe(true);
      expect(processed[0].productUrl).not.toBe(results[0].productUrl);
      expect(processed[0].originalUrl).toBe(results[0].productUrl);
    });

    test('should not modify URLs when affiliate disabled', () => {
      const results = [
        { productUrl: 'https://www.aliexpress.com/item/1', platform: 'aliexpress' }
      ];

      const settings = { enableAffiliate: false };

      const processed = AffiliateHandler.processResults(results, settings);

      expect(processed[0].productUrl).toBe(results[0].productUrl);
    });
  });

  describe('getDisclosureText', () => {
    test('should return disclosure text for platform', () => {
      const disclosure = AffiliateHandler.getDisclosureText('aliexpress');

      expect(disclosure).toHaveProperty('short');
      expect(disclosure).toHaveProperty('full');
      expect(disclosure).toHaveProperty('legal');
      expect(disclosure.full).toContain('aliexpress');
    });
  });

  describe('getAffiliateIndicator', () => {
    test('should return indicator for affiliate links', () => {
      const indicator = AffiliateHandler.getAffiliateIndicator(true);

      expect(indicator).toHaveProperty('icon');
      expect(indicator).toHaveProperty('label');
      expect(indicator).toHaveProperty('tooltip');
      expect(indicator).toHaveProperty('color');
    });

    test('should return null for non-affiliate links', () => {
      const indicator = AffiliateHandler.getAffiliateIndicator(false);

      expect(indicator).toBeNull();
    });
  });

  describe('generateSessionId', () => {
    test('should generate unique session IDs', () => {
      const id1 = AffiliateHandler.generateSessionId();
      const id2 = AffiliateHandler.generateSessionId();

      expect(id1).not.toBe(id2);
      expect(id1).toContain('sess_');
      expect(id2).toContain('sess_');
    });
  });

  describe('validateConfig', () => {
    test('should validate affiliate configuration', () => {
      const validation = AffiliateHandler.validateConfig();

      expect(validation).toHaveProperty('valid');
      expect(validation).toHaveProperty('errors');
      expect(Array.isArray(validation.errors)).toBe(true);
    });

    test('should detect missing affiliate IDs', () => {
      const validation = AffiliateHandler.validateConfig();

      // Should have warnings about placeholder affiliate IDs
      const hasPlaceholderWarnings = validation.errors.some(
        error => error.includes('placeholder') || error.includes('not configured')
      );

      expect(hasPlaceholderWarnings).toBe(true);
    });
  });

  describe('getDisclosurePage', () => {
    test('should generate disclosure page content', () => {
      const content = AffiliateHandler.getDisclosurePage();

      expect(content).toContain('Affiliate Disclosure');
      expect(content).toContain('How Affiliate Links Work');
      expect(content).toContain('Privacy');
      expect(content.length).toBeGreaterThan(100);
    });
  });
});
