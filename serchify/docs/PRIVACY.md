# Privacy Policy

**Last Updated: November 16, 2025**

## Introduction

Serchify ("we", "our", or "the extension") is committed to protecting your privacy. This Privacy Policy explains what data we collect, how we use it, and your rights regarding your information.

## TL;DR (Quick Summary)

- ✅ We collect minimal data
- ✅ Everything is stored locally on your device
- ✅ No personal information collected
- ✅ No browsing history tracking
- ✅ Analytics are optional (opt-in)
- ✅ You can delete all data anytime

## Data We Collect

### 1. Product Search Data

**What:**
- Amazon product URLs you search
- Search queries you enter
- Products you click on

**Why:**
- To perform marketplace searches
- To cache results for faster performance
- To show recent searches

**Where Stored:**
- Locally on your device (Chrome local storage)
- Never sent to external servers (except marketplace APIs)

**Retention:**
- Cached results: 24 hours
- Search history: Until you clear it
- Can be deleted anytime via Settings

### 2. Settings & Preferences

**What:**
- Which marketplaces you prefer
- Whether affiliate links are enabled
- Display preferences (price threshold, etc.)
- Privacy preferences (tracking consent)

**Why:**
- To personalize your experience
- To respect your choices

**Where Stored:**
- Locally on your device

### 3. Anonymous Usage Analytics (Optional)

**What** (only if you opt-in):
- Number of searches performed
- Which platforms are searched
- Click-through rates
- Error rates
- Extension version

**What NOT collected:**
- Your identity
- Specific products searched
- Purchase information
- Browsing history outside Amazon
- Personal information

**Why:**
- To improve the extension
- To identify and fix bugs
- To understand which features are useful

**Where Stored:**
- Locally, then aggregated anonymously

**Opt-out:**
- Analytics are OFF by default
- Enable in Settings only if you want to help improve Serchify
- Can be disabled anytime

### 4. Affiliate Click Tracking (Optional)

**What** (only if affiliate links enabled):
- Platform clicked
- Timestamp of click
- Whether link was affiliate or regular

**What NOT collected:**
- What you purchase
- How much you spend
- Product details
- Your account information

**Why:**
- To measure if affiliate links are used
- For transparency in reporting

**Where Stored:**
- Locally on your device
- Last 100 clicks only

**Opt-out:**
- Disable affiliate links in Settings

## Data We DO NOT Collect

- ❌ Your name, email, or contact information
- ❌ Your browsing history (outside Amazon product pages)
- ❌ Your purchase history
- ❌ Payment information
- ❌ Passwords or credentials
- ❌ IP address
- ❌ Device identifiers
- ❌ Location data
- ❌ Personal identifiers

## How We Use Your Data

### Local Processing Only

All product searches and data processing happen locally on your device. We don't run servers that collect your data.

### Third-Party Services

When you search for products, we query:

1. **Marketplace APIs/Websites**:
   - AliExpress, Temu, Wish, etc.
   - We send search queries (product title, brand)
   - They return product listings
   - Subject to their privacy policies

2. **Image Search Services** (for reverse image search):
   - May use Google Lens API or similar
   - Images uploaded for matching only
   - Not stored permanently
   - Subject to their privacy policies

### No Sale of Data

We **never** sell your data to third parties. Ever.

## Your Rights & Controls

### Access Your Data

All data is stored locally. You can view it using Chrome Developer Tools:
1. Right-click extension icon → Inspect
2. Go to Application → Storage → Local Storage

### Delete Your Data

**Delete Search History:**
- Settings → Data Management → Clear Search History

**Delete Cache:**
- Settings → Data Management → Clear Cache

**Delete Everything:**
- Chrome Extensions → Serchify → Remove

### Export Your Data

To export your data:
1. Open Chrome Developer Tools (F12)
2. Console tab
3. Run: `chrome.storage.local.get(null, console.log)`
4. Copy the output

### Disable Tracking

1. Open Settings
2. Uncheck "Enable anonymous usage analytics"
3. Uncheck "Enable affiliate links"
4. Save Settings

## Children's Privacy

Serchify is not intended for children under 13. We do not knowingly collect data from children.

## Permissions Explained

### Required Permissions

**storage**
- Why: Store your settings and cache locally
- What: Settings, recent searches, cached results
- Where: Your device only

**activeTab**
- Why: Detect Amazon product pages
- What: Current tab URL when you click the extension
- Not Used For: Tracking browsing history

**scripting**
- Why: Inject the "Find Cheaper" button on Amazon pages
- What: Add our overlay to Amazon product pages
- Not Used For: Modifying page content or stealing data

### Host Permissions

**amazon.com**
- Why: Detect and extract product information
- What: Read product title, price, image, ASIN
- Not Used For: Accessing your account or purchase history

**aliexpress.com, temu.com, wish.com, etc.**
- Why: Search for matching products
- What: Send search queries, receive product listings
- Not Used For: Tracking or data collection

## Security

### Data Protection

- All data stored locally (not on servers)
- HTTPS enforced for all external communications
- No storage of sensitive information
- Regular security audits

### Extension Security

- Open-source code (auditable)
- No code obfuscation
- Minimal permissions
- Manifest V3 (latest Chrome security standard)

## Changes to Privacy Policy

We may update this policy occasionally. Changes will be:
- Posted on this page
- Dated at the top
- Highlighted in extension updates

Continued use after changes means you accept the updated policy.

## GDPR Compliance (EU Users)

If you're in the EU, you have additional rights:

- **Right to Access**: You can access all your data (it's local)
- **Right to Deletion**: Delete via Settings or uninstall
- **Right to Portability**: Export via Developer Tools
- **Right to Object**: Disable tracking in Settings
- **Right to Rectification**: Manually edit via Settings

**Legal Basis for Processing:**
- Consent: You install and use the extension
- Legitimate Interest: Provide the core functionality

**Data Controller:**
- Serchify Extension Team
- Contact: privacy@serchify.example.com

## CCPA Compliance (California Users)

California residents have the right to:

- Know what data is collected: See "Data We Collect" above
- Delete data: Settings → Clear Data or uninstall
- Opt-out of sale: We don't sell data (never have, never will)

**Do Not Sell My Personal Information:**
We don't sell personal information. This extension is funded through optional affiliate commissions, not data sales.

## Cookies

Serchify does not use cookies. We use Chrome's local storage API to save data locally on your device.

## Contact Us

Questions about privacy?

- **Email**: privacy@serchify.example.com
- **GitHub**: [Open an issue](https://github.com/serchify/serchify/issues)

## Data Breach Policy

In the unlikely event of a data breach:
1. We will investigate immediately
2. Affected users will be notified within 72 hours
3. Steps to protect yourself will be provided
4. Regulatory authorities will be notified if required

## Third-Party Privacy Policies

When you use Serchify, you may interact with:

- **Amazon**: [Amazon Privacy Policy](https://www.amazon.com/gp/help/customer/display.html?nodeId=468496)
- **AliExpress**: [AliExpress Privacy Policy](https://www.aliexpress.com/p/privacy-policy/index.html)
- **Temu**: Check Temu website for their policy
- **Wish**: Check Wish website for their policy
- Other marketplaces: See their respective privacy policies

We are not responsible for their privacy practices.

## Transparency Report

We believe in transparency. Here's what we track:

| Data Type | Collected | Stored Locally | Sent to Server | Can Be Deleted |
|-----------|-----------|----------------|----------------|----------------|
| Search queries | Yes | Yes | No | Yes |
| Product URLs | Yes | Yes | No | Yes |
| Settings | Yes | Yes | No | Yes |
| Usage stats (opt-in) | Optional | Yes | Aggregated only | Yes |
| Personal info | No | No | No | N/A |
| Browsing history | No | No | No | N/A |

---

**Bottom Line:** Serchify is designed to be privacy-friendly. We collect minimal data, store everything locally, and give you full control. If you have concerns, please reach out.
