#!/usr/bin/env python3
"""
Screen Automation Tool for Ubuntu 24.04

Fast, reliable screen automation combining screen capture, OCR/vision, and input control.
Supports both X11 and Wayland display servers.
"""

import time
import logging
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass

import mss
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ElementLocation:
    """Represents a located UI element."""
    x: int
    y: int
    width: int
    height: int
    confidence: float
    text: Optional[str] = None

    @property
    def center(self) -> Tuple[int, int]:
        """Get center coordinates of the element."""
        return (self.x + self.width // 2, self.y + self.height // 2)


class ScreenAutomation:
    """
    Main screen automation class providing screenshot, video recording,
    OCR, element detection, and input control capabilities.
    """

    def __init__(self,
                 default_save_dir: str = "./screenshots",
                 video_fps: int = 30,
                 video_codec: str = "mp4v"):
        """
        Initialize the ScreenAutomation instance.

        Args:
            default_save_dir: Default directory for saving screenshots/videos
            video_fps: Frames per second for video recording (default: 30)
            video_codec: Video codec to use (default: mp4v for H.264)
        """
        self.default_save_dir = Path(default_save_dir)
        self.default_save_dir.mkdir(parents=True, exist_ok=True)

        self.video_fps = video_fps
        self.video_codec = video_codec

        # Screen capture
        self.sct = mss.mss()

        # Input controllers
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()

        # Video recording state
        self._recording = False
        self._video_writer = None
        self._record_thread = None
        self._record_stop_event = threading.Event()

        # Display server detection
        self.display_server = self._detect_display_server()
        logger.info(f"Initialized ScreenAutomation on {self.display_server}")

    def _detect_display_server(self) -> str:
        """Detect whether running on X11 or Wayland."""
        session_type = subprocess.getoutput("echo $XDG_SESSION_TYPE").strip()
        if session_type in ["wayland", "x11"]:
            return session_type
        # Fallback detection
        if subprocess.getoutput("echo $WAYLAND_DISPLAY").strip():
            return "wayland"
        return "x11"

    # ============================================================================
    # SCREEN CAPTURE
    # ============================================================================

    def screenshot(self,
                   save_path: Optional[str] = None,
                   region: Optional[Tuple[int, int, int, int]] = None,
                   monitor: int = 1) -> np.ndarray:
        """
        Capture a screenshot with <100ms latency.

        Args:
            save_path: Path to save the screenshot (PNG format). If None, not saved.
            region: Tuple of (x, y, width, height) for partial capture
            monitor: Monitor number (1-indexed, 0 for all monitors)

        Returns:
            Screenshot as numpy array (BGR format)
        """
        start_time = time.time()

        try:
            # Select monitor
            if region:
                # Custom region
                monitor_spec = {
                    "top": region[1],
                    "left": region[0],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                # Use monitor index (0 = all monitors combined)
                monitor_spec = self.sct.monitors[monitor]

            # Capture screenshot
            sct_img = self.sct.grab(monitor_spec)

            # Convert to numpy array (BGR format for OpenCV compatibility)
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Save if path provided
            if save_path:
                save_path = self._resolve_path(save_path)
                cv2.imwrite(str(save_path), img)
                logger.info(f"Screenshot saved to {save_path}")

            elapsed = (time.time() - start_time) * 1000
            logger.debug(f"Screenshot captured in {elapsed:.2f}ms")

            return img

        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            raise

    def get_screen_size(self, monitor: int = 1) -> Tuple[int, int]:
        """
        Get the size of the specified monitor.

        Args:
            monitor: Monitor number (1-indexed)

        Returns:
            Tuple of (width, height)
        """
        mon = self.sct.monitors[monitor]
        return (mon["width"], mon["height"])

    # ============================================================================
    # VIDEO RECORDING
    # ============================================================================

    @contextmanager
    def record_video(self,
                     output_path: Optional[str] = None,
                     region: Optional[Tuple[int, int, int, int]] = None,
                     monitor: int = 1):
        """
        Context manager for video recording.

        Args:
            output_path: Path to save video file (default: auto-generated)
            region: Tuple of (x, y, width, height) for partial capture
            monitor: Monitor number to record

        Usage:
            with automation.record_video("output.mp4"):
                # perform actions
                pass
        """
        try:
            self.start_recording(output_path, region, monitor)
            yield
        finally:
            self.stop_recording()

    def start_recording(self,
                       output_path: Optional[str] = None,
                       region: Optional[Tuple[int, int, int, int]] = None,
                       monitor: int = 1):
        """
        Start video recording.

        Args:
            output_path: Path to save video file
            region: Tuple of (x, y, width, height) for partial capture
            monitor: Monitor number to record
        """
        if self._recording:
            logger.warning("Recording already in progress")
            return

        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.default_save_dir / f"recording_{timestamp}.mp4"
        else:
            output_path = self._resolve_path(output_path)

        # Determine capture region
        if region:
            capture_region = region
            width, height = region[2], region[3]
        else:
            mon = self.sct.monitors[monitor]
            capture_region = None
            width = mon["width"]
            height = mon["height"]

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*self.video_codec)
        self._video_writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            self.video_fps,
            (width, height)
        )

        if not self._video_writer.isOpened():
            raise RuntimeError(f"Failed to open video writer for {output_path}")

        # Start recording thread
        self._recording = True
        self._record_stop_event.clear()
        self._record_thread = threading.Thread(
            target=self._record_loop,
            args=(capture_region, monitor),
            daemon=True
        )
        self._record_thread.start()

        logger.info(f"Started recording to {output_path}")

    def stop_recording(self):
        """Stop video recording."""
        if not self._recording:
            logger.warning("No recording in progress")
            return

        # Signal stop and wait for thread
        self._recording = False
        self._record_stop_event.set()

        if self._record_thread:
            self._record_thread.join(timeout=5.0)

        # Release video writer
        if self._video_writer:
            self._video_writer.release()
            self._video_writer = None

        logger.info("Recording stopped")

    def _record_loop(self, region: Optional[Tuple[int, int, int, int]], monitor: int):
        """Internal recording loop running in separate thread."""
        frame_interval = 1.0 / self.video_fps

        try:
            while self._recording:
                frame_start = time.time()

                # Capture frame
                frame = self.screenshot(region=region, monitor=monitor)

                # Write frame
                self._video_writer.write(frame)

                # Maintain frame rate
                elapsed = time.time() - frame_start
                sleep_time = max(0, frame_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except Exception as e:
            logger.error(f"Recording error: {e}")
            self._recording = False

    # ============================================================================
    # VISUAL UNDERSTANDING - OCR & ELEMENT DETECTION
    # ============================================================================

    def ocr(self,
            image: Optional[np.ndarray] = None,
            region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """
        Perform OCR on image or screen region.

        Args:
            image: Image array (if None, captures current screen)
            region: Region to capture if image is None

        Returns:
            Extracted text as string
        """
        if image is None:
            image = self.screenshot(region=region)

        # Convert to PIL Image for pytesseract
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Perform OCR
        text = pytesseract.image_to_string(pil_image)
        return text.strip()

    def find_text(self,
                  text: str,
                  image: Optional[np.ndarray] = None,
                  fuzzy: bool = True,
                  case_sensitive: bool = False) -> List[ElementLocation]:
        """
        Find text on screen using OCR.

        Args:
            text: Text to search for
            image: Image to search in (if None, captures current screen)
            fuzzy: Allow partial/fuzzy matching
            case_sensitive: Whether to match case

        Returns:
            List of ElementLocation objects for found text
        """
        if image is None:
            image = self.screenshot()

        # Convert to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Get detailed OCR data with bounding boxes
        ocr_data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)

        locations = []
        search_text = text if case_sensitive else text.lower()

        # Search through OCR results
        for i in range(len(ocr_data['text'])):
            ocr_text = ocr_data['text'][i].strip()
            if not ocr_text:
                continue

            comparison_text = ocr_text if case_sensitive else ocr_text.lower()

            # Check for match
            matched = False
            if fuzzy:
                matched = search_text in comparison_text or comparison_text in search_text
            else:
                matched = search_text == comparison_text

            if matched and int(ocr_data['conf'][i]) > 0:
                location = ElementLocation(
                    x=ocr_data['left'][i],
                    y=ocr_data['top'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i],
                    confidence=float(ocr_data['conf'][i]) / 100.0,
                    text=ocr_text
                )
                locations.append(location)

        return locations

    def find_element(self,
                     description: str,
                     image: Optional[np.ndarray] = None,
                     method: str = "auto") -> Optional[ElementLocation]:
        """
        Find UI element by description.

        Args:
            description: Description of element (e.g., "Submit button", "username field")
            image: Image to search in (if None, captures current screen)
            method: Detection method - "ocr", "template", or "auto"

        Returns:
            ElementLocation if found, None otherwise
        """
        if image is None:
            image = self.screenshot()

        # Extract key terms from description
        description_lower = description.lower()

        # Try OCR-based detection first (most reliable for text elements)
        # Extract likely button text from description
        keywords = []
        for word in description.split():
            if word.lower() not in ['button', 'field', 'the', 'a', 'an', 'input', 'box']:
                keywords.append(word)

        # Search for each keyword
        for keyword in keywords:
            locations = self.find_text(keyword, image=image, fuzzy=True)
            if locations:
                # Return highest confidence match
                best_match = max(locations, key=lambda x: x.confidence)
                logger.info(f"Found '{description}' via OCR at {best_match.center}")
                return best_match

        # If OCR fails, try basic color/shape detection for buttons
        if "button" in description_lower:
            button_location = self._detect_button_heuristic(image, keywords)
            if button_location:
                logger.info(f"Found '{description}' via heuristic at {button_location.center}")
                return button_location

        logger.warning(f"Could not find element: {description}")
        return None

    def _detect_button_heuristic(self,
                                 image: np.ndarray,
                                 text_hints: List[str]) -> Optional[ElementLocation]:
        """
        Detect buttons using color/shape heuristics and nearby text.

        This is a basic implementation that looks for rectangular regions
        with text nearby (common button pattern).
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get OCR data for text proximity check
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ocr_data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)

        # Look for rectangular contours with appropriate size
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Filter by size (buttons typically 50-400px wide, 20-100px tall)
            if not (50 < w < 400 and 20 < h < 100):
                continue

            # Check if any text hints are nearby
            if text_hints:
                for i, ocr_text in enumerate(ocr_data['text']):
                    if not ocr_text.strip():
                        continue

                    for hint in text_hints:
                        if hint.lower() in ocr_text.lower():
                            # Check proximity
                            text_x = ocr_data['left'][i]
                            text_y = ocr_data['top'][i]

                            if abs(text_x - x) < 100 and abs(text_y - y) < 50:
                                return ElementLocation(
                                    x=x, y=y, width=w, height=h,
                                    confidence=0.6,
                                    text=ocr_text.strip()
                                )

        return None

    def find_template(self,
                      template_path: str,
                      image: Optional[np.ndarray] = None,
                      threshold: float = 0.8) -> Optional[ElementLocation]:
        """
        Find element using template matching.

        Args:
            template_path: Path to template image
            image: Image to search in (if None, captures current screen)
            threshold: Matching threshold (0-1, higher = more strict)

        Returns:
            ElementLocation if found with confidence >= threshold
        """
        if image is None:
            image = self.screenshot()

        # Load template
        template = cv2.imread(template_path)
        if template is None:
            raise ValueError(f"Could not load template: {template_path}")

        # Perform template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            return ElementLocation(
                x=max_loc[0],
                y=max_loc[1],
                width=w,
                height=h,
                confidence=float(max_val)
            )

        return None

    # ============================================================================
    # INPUT CONTROL - MOUSE
    # ============================================================================

    def click(self,
              coords: Optional[Tuple[int, int]] = None,
              element: Optional[ElementLocation] = None,
              button: str = "left",
              clicks: int = 1,
              delay: float = 0.1):
        """
        Click at specified coordinates or element.

        Args:
            coords: (x, y) coordinates to click
            element: ElementLocation to click (uses center)
            button: "left", "right", or "middle"
            clicks: Number of clicks (1=single, 2=double)
            delay: Delay between clicks in seconds
        """
        if element:
            coords = element.center

        if coords is None:
            raise ValueError("Must provide either coords or element")

        # Map button string to pynput Button
        button_map = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle
        }
        btn = button_map.get(button.lower(), Button.left)

        # Move to position
        self.mouse_controller.position = coords
        time.sleep(0.01)  # Small delay for position to register

        # Perform clicks
        for _ in range(clicks):
            self.mouse_controller.click(btn)
            if clicks > 1:
                time.sleep(delay)

        logger.debug(f"Clicked {button} button at {coords} ({clicks}x)")

    def double_click(self,
                     coords: Optional[Tuple[int, int]] = None,
                     element: Optional[ElementLocation] = None):
        """Double-click at specified coordinates or element."""
        self.click(coords=coords, element=element, clicks=2)

    def right_click(self,
                    coords: Optional[Tuple[int, int]] = None,
                    element: Optional[ElementLocation] = None):
        """Right-click at specified coordinates or element."""
        self.click(coords=coords, element=element, button="right")

    def move_mouse(self,
                   coords: Tuple[int, int],
                   smooth: bool = False,
                   duration: float = 0.5):
        """
        Move mouse to coordinates.

        Args:
            coords: (x, y) target coordinates
            smooth: Whether to move smoothly (human-like)
            duration: Duration of smooth movement in seconds
        """
        if smooth:
            # Smooth movement with multiple steps
            start_pos = self.mouse_controller.position
            steps = max(10, int(duration * 60))  # ~60 steps per second

            for i in range(steps + 1):
                t = i / steps
                # Ease-in-out interpolation
                t = t * t * (3 - 2 * t)
                x = int(start_pos[0] + (coords[0] - start_pos[0]) * t)
                y = int(start_pos[1] + (coords[1] - start_pos[1]) * t)
                self.mouse_controller.position = (x, y)
                time.sleep(duration / steps)
        else:
            self.mouse_controller.position = coords

        logger.debug(f"Moved mouse to {coords}")

    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return self.mouse_controller.position

    # ============================================================================
    # INPUT CONTROL - KEYBOARD
    # ============================================================================

    def type_text(self,
                  text: str,
                  delay_ms: int = 50,
                  human_like: bool = True):
        """
        Type text with realistic timing.

        Args:
            text: Text to type
            delay_ms: Base delay between keystrokes in milliseconds
            human_like: Add random variation to delay (more realistic)
        """
        import random

        for char in text:
            self.keyboard_controller.type(char)

            # Calculate delay
            if human_like:
                # Add ±30% random variation
                variation = random.uniform(0.7, 1.3)
                actual_delay = (delay_ms / 1000.0) * variation
            else:
                actual_delay = delay_ms / 1000.0

            time.sleep(actual_delay)

        logger.debug(f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}")

    def press_key(self, key: str):
        """
        Press and release a single key or key combination.

        Args:
            key: Key name (e.g., "enter", "tab", "ctrl+c", "shift+alt+f")
        """
        # Parse key combination
        parts = key.lower().split('+')

        # Map string names to Key objects
        key_map = {
            'enter': Key.enter,
            'return': Key.enter,
            'tab': Key.tab,
            'space': Key.space,
            'backspace': Key.backspace,
            'delete': Key.delete,
            'esc': Key.esc,
            'escape': Key.esc,
            'up': Key.up,
            'down': Key.down,
            'left': Key.left,
            'right': Key.right,
            'home': Key.home,
            'end': Key.end,
            'pageup': Key.page_up,
            'pagedown': Key.page_down,
            'ctrl': Key.ctrl,
            'control': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
            'cmd': Key.cmd,
            'command': Key.cmd,
            'win': Key.cmd,
        }

        # Separate modifiers from main key
        modifiers = []
        main_key = None

        for part in parts:
            part = part.strip()
            if part in ['ctrl', 'control', 'alt', 'shift', 'cmd', 'command', 'win']:
                modifiers.append(key_map[part])
            else:
                main_key = key_map.get(part, part)

        # Press modifiers
        for mod in modifiers:
            self.keyboard_controller.press(mod)

        # Press main key
        if main_key:
            if isinstance(main_key, str) and len(main_key) == 1:
                self.keyboard_controller.type(main_key)
            else:
                self.keyboard_controller.press(main_key)
                self.keyboard_controller.release(main_key)

        # Release modifiers
        for mod in reversed(modifiers):
            self.keyboard_controller.release(mod)

        logger.debug(f"Pressed key: {key}")

    def hold_key(self, key: str):
        """Press and hold a key (must call release_key to release)."""
        key_map = {
            'ctrl': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
        }
        k = key_map.get(key.lower(), key)
        self.keyboard_controller.press(k)

    def release_key(self, key: str):
        """Release a held key."""
        key_map = {
            'ctrl': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
        }
        k = key_map.get(key.lower(), key)
        self.keyboard_controller.release(k)

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def _resolve_path(self, path: str) -> Path:
        """Resolve path, using default save dir if relative."""
        p = Path(path)
        if not p.is_absolute():
            p = self.default_save_dir / p
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def wait(self, seconds: float):
        """Convenience method for waiting."""
        time.sleep(seconds)

    def cleanup(self):
        """Clean up resources."""
        if self._recording:
            self.stop_recording()
        if self.sct:
            self.sct.close()
        logger.info("Cleanup complete")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
        return False


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_automation(**kwargs) -> ScreenAutomation:
    """
    Factory function to create ScreenAutomation instance.

    Args:
        **kwargs: Arguments passed to ScreenAutomation.__init__

    Returns:
        ScreenAutomation instance
    """
    return ScreenAutomation(**kwargs)


if __name__ == "__main__":
    # Basic test/demo
    print("ScreenAutomation Library - Quick Test")
    print("=" * 50)

    with create_automation() as automation:
        print(f"Display server: {automation.display_server}")
        print(f"Screen size: {automation.get_screen_size()}")

        # Take a test screenshot
        print("\nTaking screenshot...")
        start = time.time()
        img = automation.screenshot(save_path="test_screenshot.png")
        elapsed = (time.time() - start) * 1000
        print(f"✓ Screenshot captured in {elapsed:.2f}ms")
        print(f"  Image shape: {img.shape}")
        print(f"  Saved to: {automation.default_save_dir}/test_screenshot.png")

        # Test OCR
        print("\nTesting OCR on screenshot...")
        text = automation.ocr(img)
        print(f"✓ Extracted {len(text)} characters")
        if text:
            preview = text[:100].replace('\n', ' ')
            print(f"  Preview: {preview}...")

        print("\n✓ All tests passed!")
