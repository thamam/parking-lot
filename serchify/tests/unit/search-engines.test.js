/**
 * Unit Tests for Search Engines
 */

const SearchEngines = require('../../lib/search-engines');

describe('SearchEngines', () => {
  describe('buildSearchQuery', () => {
    test('should build query from brand and title', () => {
      const productData = {
        brand: 'Nike',
        title: 'Nike Air Max 90 Running Shoes'
      };

      const query = SearchEngines.buildSearchQuery(productData);

      expect(query).toContain('Nike');
      expect(query.length).toBeGreaterThan(0);
    });

    test('should exclude Generic brand', () => {
      const productData = {
        brand: 'Generic',
        title: 'Wireless Mouse'
      };

      const query = SearchEngines.buildSearchQuery(productData);

      expect(query).not.toContain('Generic');
      expect(query).toContain('wireless');
    });

    test('should handle missing brand', () => {
      const productData = {
        title: 'Bluetooth Speaker'
      };

      const query = SearchEngines.buildSearchQuery(productData);

      expect(query).toContain('bluetooth');
      expect(query).toContain('speaker');
    });
  });

  describe('extractKeywords', () => {
    test('should extract keywords and remove stop words', () => {
      const title = 'The Best Wireless Headphones for Music';

      const keywords = SearchEngines.extractKeywords(title);

      expect(keywords).toContain('best');
      expect(keywords).toContain('wireless');
      expect(keywords).toContain('headphones');
      expect(keywords).toContain('music');
      expect(keywords).not.toContain('the');
      expect(keywords).not.toContain('for');
    });

    test('should handle special characters', () => {
      const title = 'iPhone 13 Pro (256GB) - Blue';

      const keywords = SearchEngines.extractKeywords(title);

      expect(keywords).toContain('iphone');
      expect(keywords).toContain('pro');
      expect(keywords).toContain('256gb');
      expect(keywords).toContain('blue');
    });

    test('should filter short words', () => {
      const title = 'A USB C Cable for PC';

      const keywords = SearchEngines.extractKeywords(title);

      expect(keywords).toContain('usb');
      expect(keywords).toContain('cable');
      expect(keywords).not.toContain('a');
      expect(keywords).not.toContain('c'); // Too short
    });
  });

  describe('calculateConfidence', () => {
    test('should calculate high confidence for exact brand match', () => {
      const original = {
        brand: 'Apple',
        title: 'Apple iPhone 13',
        category: 'Electronics'
      };

      const match = {
        brand: 'Apple',
        title: 'Apple iPhone 13 Pro',
        category: 'Electronics'
      };

      const confidence = SearchEngines.calculateConfidence(original, match);

      expect(confidence).toBeGreaterThan(70);
    });

    test('should calculate lower confidence for different brands', () => {
      const original = {
        brand: 'Nike',
        title: 'Nike Running Shoes',
        category: 'Shoes'
      };

      const match = {
        brand: 'Adidas',
        title: 'Adidas Running Shoes',
        category: 'Shoes'
      };

      const confidence = SearchEngines.calculateConfidence(original, match);

      expect(confidence).toBeLessThan(80);
    });

    test('should handle missing data gracefully', () => {
      const original = { title: 'Product' };
      const match = { title: 'Product' };

      const confidence = SearchEngines.calculateConfidence(original, match);

      expect(confidence).toBeGreaterThanOrEqual(0);
      expect(confidence).toBeLessThanOrEqual(100);
    });
  });

  describe('stringSimilarity', () => {
    test('should return 1 for identical strings', () => {
      const similarity = SearchEngines.stringSimilarity('test', 'test');
      expect(similarity).toBe(1);
    });

    test('should return 0 for completely different strings', () => {
      const similarity = SearchEngines.stringSimilarity('apple', 'orange');
      expect(similarity).toBe(0);
    });

    test('should return value between 0 and 1 for partial matches', () => {
      const similarity = SearchEngines.stringSimilarity(
        'wireless bluetooth headphones',
        'wireless headphones'
      );

      expect(similarity).toBeGreaterThan(0);
      expect(similarity).toBeLessThan(1);
    });
  });

  describe('searchAll', () => {
    test('should search multiple platforms', async () => {
      const productData = {
        brand: 'Test',
        title: 'Test Product'
      };

      const platforms = ['aliexpress', 'temu'];
      const results = await SearchEngines.searchAll(productData, platforms);

      expect(results).toHaveLength(2);
      expect(results[0].platform).toBe('aliexpress');
      expect(results[1].platform).toBe('temu');
    });

    test('should handle search errors gracefully', async () => {
      // Mock search to throw error
      const originalSearch = SearchEngines.search;
      SearchEngines.search = jest.fn().mockRejectedValue(new Error('Search failed'));

      const productData = {
        brand: 'Test',
        title: 'Test Product'
      };

      const results = await SearchEngines.searchAll(productData, ['aliexpress']);

      expect(results).toHaveLength(1);
      expect(results[0].error).toBeDefined();

      // Restore original
      SearchEngines.search = originalSearch;
    });
  });

  describe('mockSearch', () => {
    test('should return array of results', async () => {
      const results = await SearchEngines.mockSearch('aliexpress', 'test query', {
        price: 50,
        brand: 'Test'
      });

      expect(Array.isArray(results)).toBe(true);
      expect(results.length).toBeGreaterThan(0);
      expect(results[0]).toHaveProperty('title');
      expect(results[0]).toHaveProperty('price');
      expect(results[0]).toHaveProperty('platform');
    });

    test('should include platform in results', async () => {
      const results = await SearchEngines.mockSearch('temu', 'test', { price: 30 });

      results.forEach(result => {
        expect(result.platform).toBe('temu');
      });
    });

    test('should calculate savings when original price provided', async () => {
      const results = await SearchEngines.mockSearch('wish', 'test', { price: 100 });

      results.forEach(result => {
        expect(result).toHaveProperty('savings');
      });
    });
  });

  describe('rate limiting', () => {
    beforeEach(() => {
      SearchEngines.rateLimit.requests = {};
    });

    test('should allow requests within limit', async () => {
      await expect(
        SearchEngines.rateLimit.checkLimit('test-platform', 5, 60000)
      ).resolves.not.toThrow();
    });

    test('should throw error when limit exceeded', async () => {
      const platform = 'test-platform-2';
      const maxRequests = 3;

      // Make requests up to limit
      for (let i = 0; i < maxRequests; i++) {
        await SearchEngines.rateLimit.checkLimit(platform, maxRequests, 60000);
      }

      // Next request should fail
      await expect(
        SearchEngines.rateLimit.checkLimit(platform, maxRequests, 60000)
      ).rejects.toThrow(/Rate limit exceeded/);
    });
  });
});
