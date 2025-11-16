# Extension Icons

This directory contains the extension icons in various sizes required by Chrome.

## Required Sizes

- **icon16.png**: 16x16 - Small icon for extension toolbar
- **icon32.png**: 32x32 - Medium icon for extension management
- **icon48.png**: 48x48 - Standard icon for extension management
- **icon128.png**: 128x128 - Large icon for Chrome Web Store

## Current Status

**TODO**: Replace placeholder icons with actual designed icons

## Design Guidelines

1. **Simple and Recognizable**: Should be identifiable at 16x16 pixels
2. **Consistent Branding**: Use brand colors (purple/blue gradient)
3. **Clear Symbol**: Search magnifying glass or shopping bag icon
4. **Professional**: High-quality, scalable graphics

## Temporary Solution

For development, you can create placeholder PNGs using ImageMagick:

```bash
# Install ImageMagick (if not already installed)
# Ubuntu/Debian: sudo apt-get install imagemagick
# macOS: brew install imagemagick

# Create placeholder icons
convert -size 16x16 xc:#667eea icon16.png
convert -size 32x32 xc:#667eea icon32.png
convert -size 48x48 xc:#667eea icon48.png
convert -size 128x128 xc:#667eea icon128.png
```

## Design Tools

Recommended tools for creating icons:
- **Figma**: Free, browser-based design tool
- **Inkscape**: Free, open-source vector graphics editor
- **GIMP**: Free, open-source image editor

## Exporting

When exporting final icons:
1. Use PNG format
2. Ensure exact pixel dimensions
3. Use transparent background
4. Optimize file size with tools like TinyPNG
