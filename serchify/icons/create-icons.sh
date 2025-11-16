#!/bin/bash
# Create placeholder icons using ImageMagick convert command
# If ImageMagick is not available, creates minimal PNG files

if command -v convert &> /dev/null; then
    # Use ImageMagick to create colored placeholder icons
    convert -size 16x16 xc:#667eea icon16.png
    convert -size 32x32 xc:#667eea icon32.png
    convert -size 48x48 xc:#667eea icon48.png
    convert -size 128x128 xc:#667eea icon128.png
    echo "Icons created with ImageMagick"
else
    # Create minimal 1x1 PNG files (base64 encoded)
    # This is a tiny red pixel PNG
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==" | base64 -d > icon16.png
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==" | base64 -d > icon32.png
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==" | base64 -d > icon48.png
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==" | base64 -d > icon128.png
    echo "Minimal placeholder icons created"
fi

ls -lh icon*.png
