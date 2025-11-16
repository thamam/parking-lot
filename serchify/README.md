# Serchify - Cross-Platform Product Finder

A Chrome extension that helps you find Amazon products on alternative marketplaces like AliExpress, Temu, Wish, and more. Save money by comparing prices across multiple platforms with just one click.

## Features

- **Automatic Detection**: Automatically detects Amazon product pages
- **Multi-Platform Search**: Searches AliExpress, Temu, Wish, DHGate, Banggood, and eBay
- **Reverse Image Search**: Find products using images for better accuracy
- **Price Comparison**: See price differences and potential savings
- **Privacy Focused**: Minimal data collection with full transparency
- **Affiliate Transparency**: Clear disclosure and control over affiliate links
- **Smart Caching**: Fast results with intelligent caching

## Installation

### From Source (Development)

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/serchify.git
   cd serchify
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `serchify` directory

### From Chrome Web Store

Coming soon!

## Usage

### Method 1: Automatic Detection

1. Visit any Amazon product page
2. Look for the "Find Cheaper" floating button in the bottom-right corner
3. Click the button to search for alternatives
4. Browse results in the side panel

### Method 2: Manual URL Search

1. Click the Serchify extension icon
2. Paste an Amazon product URL
3. Click "Search"
4. View results

### Method 3: Image Search

1. Click the Serchify extension icon
2. Switch to "Image Search" tab
3. Upload a product image or drag & drop
4. Click "Search by Image"
5. View visually similar products

## Settings

Access settings by clicking the gear icon in the extension popup:

### Marketplaces
- Choose which platforms to search
- Enable/disable individual marketplaces

### Privacy & Data
- **Anonymous Analytics**: Opt-in to help improve the extension
- **Affiliate Links**: Choose whether to support development via affiliate links
- **Data Management**: Clear cache and search history anytime

### Display
- **Minimum Savings**: Set threshold for which alternatives to show
- Filter results by percentage savings

## Privacy

Serchify respects your privacy:

- ✅ Only collects data you explicitly consent to
- ✅ No personal information collected
- ✅ No browsing history tracking outside Amazon
- ✅ All data stored locally on your device
- ✅ Optional anonymous analytics (opt-in)
- ✅ Full control to clear all data

Read our [Privacy Policy](docs/PRIVACY.md) for details.

## Affiliate Disclosure

Serchify may use affiliate links to support development. This means:

- When you purchase through our links, we may earn a small commission
- **No extra cost to you** - prices remain the same
- Clearly marked with visual indicators
- **Completely optional** - can be disabled in settings
- Original URLs always available

Read our [Affiliate Disclosure](docs/AFFILIATE-DISCLOSURE.md) for full details.

## Development

### Project Structure

```
serchify/
├── manifest.json           # Extension manifest (V3)
├── background/
│   └── service-worker.js   # Background service worker
├── content/
│   ├── amazon-detector.js  # Amazon page detection
│   ├── overlay.js          # Floating button overlay
│   └── overlay.css         # Overlay styles
├── popup/
│   ├── popup.html          # Extension popup UI
│   ├── popup.css           # Popup styles
│   └── popup.js            # Popup logic
├── lib/
│   ├── amazon-parser.js    # Amazon product parser
│   ├── search-engines.js   # Marketplace search
│   ├── reverse-image.js    # Image search
│   └── affiliate.js        # Affiliate link handler
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
└── docs/                   # Documentation
```

### Running Tests

```bash
# Run all tests
npm test

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration

# Run E2E tests
npm run test:e2e

# Generate coverage report
npm run test:coverage
```

### Building

```bash
# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Submit a pull request

## Testing

The extension includes comprehensive test coverage:

- **Unit Tests**: 80%+ code coverage
- **Integration Tests**: Component interaction testing
- **E2E Tests**: Full user flow validation
- **Performance Tests**: Response time and memory usage
- **Security Tests**: XSS prevention and HTTPS enforcement

## Roadmap

- [ ] Mobile companion app
- [ ] Support for more marketplaces
- [ ] Price history tracking
- [ ] Product alerts and notifications
- [ ] Browser extension for Firefox and Edge
- [ ] Advanced filtering and sorting options

## FAQ

### Is this extension safe to use?

Yes! Serchify is open-source, auditable, and follows Chrome extension best practices. We use minimal permissions and are transparent about data usage.

### Does it work on mobile?

Chrome extensions don't work on mobile Chrome browsers. We're planning a companion mobile app.

### Why do some searches return no results?

Not all products are available on all platforms. Generic or brand-specific items may not have exact matches on alternative marketplaces.

### How accurate is the reverse image search?

Accuracy varies by product type. Items with distinctive visual features (electronics, clothing with unique designs) typically have better match rates (60-80%).

### Can I disable affiliate links?

Yes! Go to Settings and uncheck "Enable affiliate links". All product links will then be clean URLs without any affiliate parameters.

## Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/serchify/serchify/issues)
- **Questions**: Check our [FAQ](https://github.com/serchify/serchify/wiki/FAQ)
- **Email**: support@serchify.example.com

## License

MIT License - see [LICENSE](LICENSE) file for details

## Disclaimer

Serchify is an independent tool and is not affiliated with, endorsed by, or sponsored by Amazon, AliExpress, Temu, Wish, or any other marketplace mentioned. All trademarks belong to their respective owners.

## Acknowledgments

- Built with Chrome Extension Manifest V3
- Tested with Jest and Playwright
- Icons from [source] (placeholder)

---

Made with ❤️ by the Serchify team
