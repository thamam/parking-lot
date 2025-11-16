/**
 * Build Script for Serchify Extension
 * Creates a production-ready ZIP file for Chrome Web Store
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BUILD_DIR = 'dist';
const OUTPUT_ZIP = 'serchify-extension.zip';

// Files and directories to include in build
const INCLUDE = [
  'manifest.json',
  'background',
  'content',
  'popup',
  'lib',
  'icons',
  'docs/PRIVACY.md',
  'docs/AFFILIATE-DISCLOSURE.md'
];

// Files and directories to exclude
const EXCLUDE = [
  'node_modules',
  'tests',
  'scripts',
  'dist',
  '.git',
  '.gitignore',
  'jest.config.js',
  'package.json',
  'package-lock.json',
  'README.md' // Use store description instead
];

console.log('🔨 Building Serchify extension...\n');

// Clean previous build
if (fs.existsSync(BUILD_DIR)) {
  console.log('🧹 Cleaning previous build...');
  fs.rmSync(BUILD_DIR, { recursive: true, force: true });
}

// Create build directory
fs.mkdirSync(BUILD_DIR, { recursive: true });
console.log('✅ Build directory created\n');

// Copy files
console.log('📦 Copying files...');
INCLUDE.forEach(item => {
  const src = path.join(__dirname, '..', item);
  const dest = path.join(__dirname, '..', BUILD_DIR, item);

  if (!fs.existsSync(src)) {
    console.warn(`⚠️  Warning: ${item} not found, skipping`);
    return;
  }

  // Create parent directory if needed
  const destDir = path.dirname(dest);
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  // Copy file or directory
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.cpSync(src, dest, { recursive: true });
    console.log(`  ✓ ${item}/`);
  } else {
    fs.copyFileSync(src, dest);
    console.log(`  ✓ ${item}`);
  }
});

console.log('\n✅ Files copied\n');

// Validate manifest
console.log('🔍 Validating manifest.json...');
const manifestPath = path.join(__dirname, '..', BUILD_DIR, 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

if (manifest.manifest_version !== 3) {
  console.error('❌ Error: Must use Manifest V3');
  process.exit(1);
}

console.log(`  ✓ Version: ${manifest.version}`);
console.log(`  ✓ Name: ${manifest.name}`);
console.log(`  ✓ Manifest V${manifest.manifest_version}`);
console.log('✅ Manifest validated\n');

// Create ZIP
console.log('📦 Creating ZIP archive...');
const zipPath = path.join(__dirname, '..', OUTPUT_ZIP);

try {
  // Remove old ZIP if exists
  if (fs.existsSync(zipPath)) {
    fs.unlinkSync(zipPath);
  }

  // Create new ZIP (using system zip command)
  const cwd = path.join(__dirname, '..', BUILD_DIR);
  execSync(`zip -r ../${OUTPUT_ZIP} .`, { cwd, stdio: 'inherit' });

  console.log(`✅ ZIP created: ${OUTPUT_ZIP}\n`);
} catch (error) {
  console.error('❌ Error creating ZIP:', error.message);
  process.exit(1);
}

// Get file size
const stats = fs.statSync(zipPath);
const fileSizeMB = (stats.size / (1024 * 1024)).toFixed(2);
console.log(`📊 Package size: ${fileSizeMB} MB`);

if (stats.size > 5 * 1024 * 1024) {
  console.warn('⚠️  Warning: Package exceeds 5MB (Chrome Web Store limit)');
}

console.log('\n✨ Build complete!\n');
console.log('Next steps:');
console.log('1. Test the extension by loading the dist/ folder in Chrome');
console.log('2. Upload serchify-extension.zip to Chrome Web Store');
console.log('3. Fill out store listing with screenshots and description\n');
