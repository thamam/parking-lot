/**
 * Real-world Integration Tests for Amazon Parser
 * Tests against actual Amazon HTML structure (from saved fixtures)
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const AmazonParser = require('../../lib/amazon-parser');

describe('Amazon Parser - Real HTML Integration', () => {
  let document;

  beforeAll(() => {
    // Load the real Amazon HTML fixture
    const htmlPath = path.join(__dirname, '../fixtures/amazon-product-sample.html');
    const html = fs.readFileSync(htmlPath, 'utf8');

    const dom = new JSDOM(html);
    document = dom.window.document;
  });

  test('should extract ASIN from real Amazon page', () => {
    const asin = AmazonParser.extractASINFromPage(document);

    expect(asin).toBe('B08N5WRWNW');
  });

  test('should extract product title from real Amazon page', () => {
    const title = AmazonParser.extractTitle(document);

    expect(title).toBeTruthy();
    expect(title).toContain('Apple AirPods Pro');
    expect(title).toContain('2nd Generation');
  });

  test('should extract price from real Amazon page', () => {
    const price = AmazonParser.extractPrice(document);

    expect(price).toBe(189.99);
  });

  test('should extract brand from real Amazon page', () => {
    const brand = AmazonParser.extractBrand(document);

    expect(brand).toBe('Apple');
  });

  test('should extract category from real Amazon page', () => {
    const category = AmazonParser.extractCategory(document);

    expect(category).toBeTruthy();
    expect(category).toContain('Earbuds');
  });

  test('should extract image URL from real Amazon page', () => {
    const imageUrl = AmazonParser.extractImageUrl(document);

    expect(imageUrl).toBeTruthy();
    expect(imageUrl).toContain('media-amazon.com');
    expect(imageUrl).toContain('.jpg');
  });

  test('should extract rating from real Amazon page', () => {
    const rating = AmazonParser.extractRating(document);

    expect(rating).toBe(4.6);
  });

  test('should extract review count from real Amazon page', () => {
    const reviewCount = AmazonParser.extractReviewCount(document);

    expect(reviewCount).toBe(87234);
  });

  test('should extract specifications from real Amazon page', () => {
    const specs = AmazonParser.extractSpecifications(document);

    expect(specs).toBeTruthy();
    expect(Object.keys(specs).length).toBeGreaterThan(0);
    expect(specs['Brand']).toBe('Apple');
    expect(specs['Color']).toBe('White');
    expect(specs['Form Factor']).toBe('In Ear');
  });

  test('should extract availability from real Amazon page', () => {
    const availability = AmazonParser.extractAvailability(document);

    expect(availability).toBe('in_stock');
  });

  test('should extract complete product data from real Amazon page', () => {
    const productData = AmazonParser.extractProductData(document);

    expect(productData).toEqual({
      asin: 'B08N5WRWNW',
      title: expect.stringContaining('Apple AirPods Pro'),
      imageUrl: expect.stringContaining('media-amazon.com'),
      price: 189.99,
      brand: 'Apple',
      category: expect.stringContaining('Earbuds'),
      specifications: expect.any(Object),
      rating: 4.6,
      reviewCount: 87234,
      availability: 'in_stock'
    });
  });

  test('should generate search keywords from real product data', () => {
    const productData = AmazonParser.extractProductData(document);
    const keywords = AmazonParser.generateSearchKeywords(productData);

    expect(keywords).toBeTruthy();
    expect(keywords.length).toBeGreaterThan(0);
    expect(keywords).toContain('Apple');

    // Should extract meaningful terms from title
    const keywordString = keywords.join(' ').toLowerCase();
    expect(keywordString).toMatch(/airpods|wireless|ear|buds/);
  });
});
