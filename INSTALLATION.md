# Screen Automation Tool - Installation Guide

Complete setup instructions for Ubuntu 24.04 (Noble Numbat)

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Install System Dependencies](#install-system-dependencies)
3. [Install Python Dependencies](#install-python-dependencies)
4. [Display Server Configuration](#display-server-configuration)
5. [Permissions and Access](#permissions-and-access)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

- **OS**: Ubuntu 24.04 LTS (Noble Numbat) or compatible
- **Python**: 3.11 or higher
- **Display Server**: X11 or Wayland (both supported)
- **RAM**: Minimum 2GB (4GB+ recommended for video recording)
- **Disk Space**: ~500MB for dependencies, plus storage for recordings

---

## Install System Dependencies

### Step 1: Update Package Lists

```bash
sudo apt update
```

### Step 2: Install Core Dependencies

```bash
# Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv

# Tesseract OCR engine and language data
sudo apt install -y tesseract-ocr tesseract-ocr-eng

# Image and video processing libraries
sudo apt install -y libopencv-dev python3-opencv

# X11 libraries (needed even on Wayland for compatibility)
sudo apt install -y python3-xlib libxtst-dev libx11-dev

# FFmpeg for video encoding (optional but recommended)
sudo apt install -y ffmpeg libavcodec-dev libavformat-dev libswscale-dev

# Development tools
sudo apt install -y build-essential pkg-config
```

### Step 3: Additional OCR Languages (Optional)

If you need to recognize text in languages other than English:

```bash
# Examples:
sudo apt install -y tesseract-ocr-spa  # Spanish
sudo apt install -y tesseract-ocr-fra  # French
sudo apt install -y tesseract-ocr-deu  # German
sudo apt install -y tesseract-ocr-chi-sim  # Simplified Chinese

# List all available languages:
apt-cache search tesseract-ocr
```

---

## Install Python Dependencies

### Step 1: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### Step 2: Install Python Packages

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individually:
pip install mss>=9.0.0
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
pip install Pillow>=10.0.0
pip install pytesseract>=0.3.10
pip install pynput>=1.7.6
```

### Step 3: Verify Installation

```bash
python3 -c "import mss, cv2, pytesseract, pynput; print('✓ All imports successful')"
```

---

## Display Server Configuration

The tool supports both X11 and Wayland display servers.

### Check Your Display Server

```bash
echo $XDG_SESSION_TYPE
# Output: "x11" or "wayland"
```

### X11 Configuration (Default on Ubuntu Desktop)

No additional configuration needed. X11 works out of the box.

### Wayland Configuration

Wayland has stricter security policies. You may need to grant permissions:

#### For GNOME on Wayland:

```bash
# Install required packages
sudo apt install -y python3-dbus

# Grant screen capture permission (may require user confirmation via GUI)
# The first screenshot will trigger a permission dialog
```

#### For Testing (Temporary X11 Session):

If you encounter issues on Wayland, you can temporarily switch to X11:

1. Log out
2. On login screen, click the gear icon
3. Select "Ubuntu on Xorg"
4. Log in

### Screen Recording Permissions

For video recording, ensure you have:

```bash
# Write permissions to output directory
mkdir -p ~/videos
chmod 755 ~/videos

# Check available disk space (recordings can be large)
df -h ~
```

---

## Permissions and Access

### Input Control Permissions

The tool needs to control mouse and keyboard. On some systems:

```bash
# Add user to input group (may require logout/login)
sudo usermod -a -G input $USER

# For X11, ensure DISPLAY is set
echo $DISPLAY  # Should show something like ":0" or ":1"
```

### Screen Capture Permissions

```bash
# Ensure you have read access to /dev/fb0 (framebuffer) if needed
# Usually automatic for desktop users

# Check current permissions
ls -l /dev/fb0
```

### Directory Permissions

```bash
# Create default screenshot directory
mkdir -p ./screenshots
chmod 755 ./screenshots
```

---

## Verification

### Step 1: Run Quick Test

```bash
# Run built-in test
python3 screen_automation.py
```

Expected output:
```
ScreenAutomation Library - Quick Test
==================================================
Display server: x11
Screen size: (1920, 1080)

Taking screenshot...
✓ Screenshot captured in 45.23ms
  Image shape: (1080, 1920, 3)
  Saved to: ./screenshots/test_screenshot.png

Testing OCR on screenshot...
✓ Extracted 1234 characters
  Preview: ...

✓ All tests passed!
```

### Step 2: Run Examples

```bash
# Run all examples (safe - no actual clicks)
python3 examples.py
```

### Step 3: Performance Benchmarks

```bash
# Run performance tests
python3 test_performance.py
```

Expected performance:
- Screenshot capture: **<100ms** ✓
- OCR extraction: **<1000ms** ✓
- Element detection: **<2000ms** ✓
- Mouse/keyboard actions: **<50ms** ✓

---

## Troubleshooting

### Issue: "ImportError: No module named 'mss'"

**Solution**: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Issue: "TesseractNotFoundError"

**Solution**: Install tesseract
```bash
sudo apt install -y tesseract-ocr
# Verify installation
which tesseract  # Should show: /usr/bin/tesseract
```

### Issue: "Screenshot is black/empty"

**Possible causes**:
1. **Wayland permissions**: First screenshot may trigger permission dialog
2. **Multi-monitor setup**: Try specifying monitor: `automation.screenshot(monitor=1)`
3. **Graphics driver**: Update graphics drivers

**Solution**:
```bash
# Check monitors
python3 -c "import mss; print(mss.mss().monitors)"

# Try different monitor
automation.screenshot(monitor=2)
```

### Issue: "Mouse/keyboard control not working"

**Solution**: Check permissions and display server
```bash
# Verify DISPLAY variable (X11)
echo $DISPLAY

# Add to input group
sudo usermod -a -G input $USER
# Then logout and login

# Test manually
python3 -c "from pynput.mouse import Controller; m = Controller(); print(m.position)"
```

### Issue: "Video recording fails"

**Solution**: Check codec and dependencies
```bash
# Install FFmpeg
sudo apt install -y ffmpeg

# Try different codec
automation = ScreenAutomation(video_codec="XVID")
```

### Issue: "OCR not detecting text"

**Solution**: Improve OCR accuracy
```bash
# Install better language data
sudo apt install -y tesseract-ocr-eng tesseract-ocr-osd

# Pre-process image (in your code):
import cv2
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
text = automation.ocr(thresh)
```

### Issue: "Permission denied on Wayland"

**Solution**: Grant screen capture permissions
```bash
# First run will show permission dialog
# Click "Share" to allow

# Or switch to X11 session temporarily:
# Logout → Login screen → Gear icon → "Ubuntu on Xorg"
```

### Issue: "Slow performance"

**Optimization tips**:
```bash
# 1. Use region capture instead of full screen
automation.screenshot(region=(0, 0, 800, 600))

# 2. Lower video FPS
automation = ScreenAutomation(video_fps=15)

# 3. Use smaller OCR regions
automation.ocr(region=(100, 100, 500, 300))

# 4. Close other applications
# 5. Check system resources
top
```

---

## Testing the Installation

### Quick Functionality Test

Create a file `test_install.py`:

```python
#!/usr/bin/env python3
from screen_automation import ScreenAutomation
import time

print("Testing Screen Automation Installation...")

automation = ScreenAutomation()

# Test 1: Screenshot
print("1. Testing screenshot...", end=" ")
img = automation.screenshot()
print(f"✓ ({img.shape[1]}x{img.shape[0]})")

# Test 2: Screen size
print("2. Testing screen size...", end=" ")
size = automation.get_screen_size()
print(f"✓ ({size[0]}x{size[1]})")

# Test 3: OCR
print("3. Testing OCR...", end=" ")
text = automation.ocr(img)
print(f"✓ ({len(text)} chars)")

# Test 4: Mouse position
print("4. Testing mouse control...", end=" ")
pos = automation.get_mouse_position()
print(f"✓ (at {pos})")

# Test 5: Display server
print(f"5. Display server: {automation.display_server}")

automation.cleanup()
print("\n✓ All tests passed! Installation successful.")
```

Run it:
```bash
python3 test_install.py
```

---

## Next Steps

1. **Read the examples**: `python3 examples.py`
2. **Run performance tests**: `python3 test_performance.py`
3. **Check the API documentation**: See docstrings in `screen_automation.py`
4. **Create your first automation**: Start with simple screenshot and OCR

---

## Additional Resources

- **Tesseract Documentation**: https://tesseract-ocr.github.io/
- **OpenCV Tutorials**: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- **pynput Documentation**: https://pynput.readthedocs.io/
- **MSS (Screenshot library)**: https://python-mss.readthedocs.io/

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Run the verification tests
3. Check system logs: `journalctl -xe`
4. Verify all dependencies are installed
5. Test on X11 session if using Wayland

---

**Installation complete!** You're ready to automate your Ubuntu desktop.
