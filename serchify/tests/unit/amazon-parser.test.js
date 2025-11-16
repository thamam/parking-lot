/**
 * Unit Tests for Amazon Parser
 */

const AmazonParser = require('../../lib/amazon-parser');

describe('AmazonParser', () => {
  describe('isAmazonProductUrl', () => {
    test('should identify valid Amazon product URLs', () => {
      expect(AmazonParser.isAmazonProductUrl('https://www.amazon.com/dp/B08XYZ123')).toBe(true);
      expect(AmazonParser.isAmazonProductUrl('https://www.amazon.com/gp/product/B08ABC456')).toBe(true);
      expect(AmazonParser.isAmazonProductUrl('https://amazon.com/dp/B08XYZ123?tag=test')).toBe(true);
    });

    test('should reject invalid URLs', () => {
      expect(AmazonParser.isAmazonProductUrl('https://www.google.com')).toBe(false);
      expect(AmazonParser.isAmazonProductUrl('https://www.amazon.com')).toBe(false);
      expect(AmazonParser.isAmazonProductUrl('')).toBe(false);
      expect(AmazonParser.isAmazonProductUrl(null)).toBe(false);
    });
  });

  describe('extractASIN', () => {
    test('should extract ASIN from /dp/ URLs', () => {
      expect(AmazonParser.extractASIN('https://www.amazon.com/dp/B08XYZ1234')).toBe('B08XYZ1234');
      expect(AmazonParser.extractASIN('https://www.amazon.com/product-name/dp/B08ABC5678/ref=123')).toBe('B08ABC5678');
    });

    test('should extract ASIN from /gp/product/ URLs', () => {
      expect(AmazonParser.extractASIN('https://www.amazon.com/gp/product/B08DEF9012')).toBe('B08DEF9012');
    });

    test('should return null for invalid URLs', () => {
      expect(AmazonParser.extractASIN('https://www.amazon.com')).toBe(null);
      expect(AmazonParser.extractASIN('')).toBe(null);
      expect(AmazonParser.extractASIN(null)).toBe(null);
    });

    test('should handle ASINs with different formats', () => {
      expect(AmazonParser.extractASIN('https://www.amazon.com/dp/B08XYZ1234')).toBe('B08XYZ1234');
      expect(AmazonParser.extractASIN('https://www.amazon.com/dp/0123456789')).toBe('0123456789');
    });
  });

  describe('extractTitle', () => {
    test('should extract title from product page', () => {
      const mockDoc = {
        querySelector: jest.fn((selector) => {
          if (selector === '#productTitle') {
            return { textContent: '  Sample Product Title  ' };
          }
          return null;
        })
      };

      expect(AmazonParser.extractTitle(mockDoc)).toBe('Sample Product Title');
    });

    test('should return null when title not found', () => {
      const mockDoc = {
        querySelector: jest.fn(() => null)
      };

      expect(AmazonParser.extractTitle(mockDoc)).toBe(null);
    });
  });

  describe('extractPrice', () => {
    test('should extract price from offscreen element', () => {
      const mockDoc = {
        querySelector: jest.fn((selector) => {
          if (selector === '.a-price .a-offscreen') {
            return { textContent: '$29.99' };
          }
          return null;
        })
      };

      expect(AmazonParser.extractPrice(mockDoc)).toBe(29.99);
    });

    test('should handle prices with commas', () => {
      const mockDoc = {
        querySelector: jest.fn((selector) => {
          if (selector === '.a-price .a-offscreen') {
            return { textContent: '$1,299.99' };
          }
          return null;
        })
      };

      expect(AmazonParser.extractPrice(mockDoc)).toBe(1299.99);
    });

    test('should return null when price not found', () => {
      const mockDoc = {
        querySelector: jest.fn(() => null)
      };

      expect(AmazonParser.extractPrice(mockDoc)).toBe(null);
    });
  });

  describe('generateSearchKeywords', () => {
    test('should generate keywords from product data', () => {
      const productData = {
        brand: 'SampleBrand',
        title: 'SampleBrand Wireless Headphones with Noise Cancellation'
      };

      const keywords = AmazonParser.generateSearchKeywords(productData);

      expect(keywords).toContain('SampleBrand');
      expect(keywords).toContain('wireless');
      expect(keywords).toContain('headphones');
      expect(keywords.length).toBeGreaterThan(0);
    });

    test('should filter out stop words', () => {
      const productData = {
        brand: 'TestBrand',
        title: 'The Best Product for Your Home'
      };

      const keywords = AmazonParser.generateSearchKeywords(productData);

      expect(keywords).not.toContain('the');
      expect(keywords).not.toContain('for');
      expect(keywords).toContain('TestBrand');
    });

    test('should handle empty data', () => {
      const productData = {};
      const keywords = AmazonParser.generateSearchKeywords(productData);

      expect(Array.isArray(keywords)).toBe(true);
    });
  });

  describe('generateProductHash', () => {
    test('should generate consistent hash for same product', () => {
      const productData = {
        asin: 'B08XYZ1234',
        title: 'Sample Product'
      };

      const hash1 = AmazonParser.generateProductHash(productData);
      const hash2 = AmazonParser.generateProductHash(productData);

      expect(hash1).toBe(hash2);
    });

    test('should generate different hashes for different products', () => {
      const product1 = {
        asin: 'B08XYZ1234',
        title: 'Product 1'
      };

      const product2 = {
        asin: 'B08ABC5678',
        title: 'Product 2'
      };

      const hash1 = AmazonParser.generateProductHash(product1);
      const hash2 = AmazonParser.generateProductHash(product2);

      expect(hash1).not.toBe(hash2);
    });
  });
});
