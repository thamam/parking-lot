#!/usr/bin/env python3
"""
Usage Examples for Screen Automation Tool

Demonstrates practical use cases for screen capture, OCR, element detection,
and input control on Ubuntu 24.04.
"""

import time
from screen_automation import ScreenAutomation


def example_1_basic_screenshot():
    """Example 1: Take a screenshot and save it"""
    print("=" * 60)
    print("Example 1: Basic Screenshot Capture")
    print("=" * 60)

    automation = ScreenAutomation()

    # Take a screenshot of the entire screen
    print("Taking full screen screenshot...")
    automation.screenshot(save_path="full_screen.png")
    print("✓ Saved to ./screenshots/full_screen.png")

    # Take a screenshot of a specific region (x, y, width, height)
    print("\nTaking partial screenshot (top-left 800x600)...")
    automation.screenshot(
        save_path="partial_screen.png",
        region=(0, 0, 800, 600)
    )
    print("✓ Saved to ./screenshots/partial_screen.png")

    # Capture without saving (get numpy array for processing)
    print("\nCapturing to memory for processing...")
    img_array = automation.screenshot()
    print(f"✓ Captured {img_array.shape[1]}x{img_array.shape[0]} image")

    automation.cleanup()
    print("\n")


def example_2_ocr_text_extraction():
    """Example 2: Extract text from screen using OCR"""
    print("=" * 60)
    print("Example 2: OCR Text Extraction")
    print("=" * 60)

    automation = ScreenAutomation()

    # Extract all text from current screen
    print("Extracting text from entire screen...")
    text = automation.ocr()
    print(f"✓ Extracted {len(text)} characters")
    print(f"\nFirst 200 characters:\n{text[:200]}...")

    # Extract text from a specific region
    print("\n\nExtracting text from specific region...")
    text = automation.ocr(region=(100, 100, 600, 400))
    print(f"✓ Extracted text from region")
    if text:
        print(f"Text preview: {text[:100]}...")

    automation.cleanup()
    print("\n")


def example_3_find_and_click():
    """Example 3: Find an element by description and click it"""
    print("=" * 60)
    print("Example 3: Find and Click UI Element")
    print("=" * 60)

    automation = ScreenAutomation()

    # Find element by text description
    print("Searching for 'Submit' button...")
    element = automation.find_element("Submit button")

    if element:
        print(f"✓ Found element at {element.center}")
        print(f"  Confidence: {element.confidence:.2%}")
        print(f"  Text: {element.text}")

        # Click the element (commented out to avoid accidental clicks)
        # automation.click(element=element)
        print("\n(Click commented out - uncomment to actually click)")
    else:
        print("✗ Element not found")

    # Alternative: Find specific text and click
    print("\n\nSearching for 'Login' text...")
    locations = automation.find_text("Login", fuzzy=True)

    if locations:
        print(f"✓ Found {len(locations)} matches")
        for i, loc in enumerate(locations):
            print(f"  Match {i+1}: {loc.center} (confidence: {loc.confidence:.2%})")

        # Click the first match (commented out)
        # automation.click(element=locations[0])
        print("\n(Click commented out - uncomment to actually click)")
    else:
        print("✗ Text not found")

    automation.cleanup()
    print("\n")


def example_4_automated_typing():
    """Example 4: Automated form filling with realistic typing"""
    print("=" * 60)
    print("Example 4: Automated Typing with Human-like Timing")
    print("=" * 60)

    automation = ScreenAutomation()

    print("This example demonstrates typing text with realistic timing")
    print("(Commented out to avoid interfering with your system)")
    print()

    # Example workflow (commented to avoid accidental execution):
    """
    # Click on username field
    username_field = automation.find_element("username field")
    if username_field:
        automation.click(element=username_field)
        automation.wait(0.2)  # Wait for field to focus

        # Type username with human-like timing (50ms ± 30% variation)
        automation.type_text("john.doe@example.com", delay_ms=50, human_like=True)

        # Move to next field using Tab
        automation.press_key("tab")
        automation.wait(0.2)

        # Type password
        automation.type_text("SecurePassword123!", delay_ms=60, human_like=True)

        # Submit form
        automation.press_key("enter")
    """

    print("Code example:")
    print("""
    # Click username field and type
    automation.click(element=username_field)
    automation.type_text("user@example.com", delay_ms=50, human_like=True)

    # Press Tab to move to next field
    automation.press_key("tab")

    # Type password
    automation.type_text("password123", delay_ms=60, human_like=True)

    # Submit with Enter
    automation.press_key("enter")
    """)

    automation.cleanup()
    print("\n")


def example_5_video_recording():
    """Example 5: Record video of screen actions"""
    print("=" * 60)
    print("Example 5: Video Recording")
    print("=" * 60)

    automation = ScreenAutomation(video_fps=30)

    # Method 1: Using context manager (recommended)
    print("Recording 5 seconds of screen activity...")
    print("(Using context manager for automatic cleanup)")

    with automation.record_video("demo_recording.mp4"):
        # Perform actions while recording
        for i in range(5):
            print(f"  Recording... {i+1}/5 seconds")
            time.sleep(1.0)

    print("✓ Recording saved to ./screenshots/demo_recording.mp4")

    # Method 2: Manual start/stop
    print("\n\nAlternative method - manual start/stop:")
    print("""
    automation.start_recording("output.mp4")
    # ... perform actions ...
    automation.stop_recording()
    """)

    # Record specific region
    print("\n\nRecording specific region (top-left 800x600) for 3 seconds...")
    with automation.record_video("region_recording.mp4", region=(0, 0, 800, 600)):
        for i in range(3):
            print(f"  Recording region... {i+1}/3 seconds")
            time.sleep(1.0)

    print("✓ Region recording saved")

    automation.cleanup()
    print("\n")


def example_6_mouse_control():
    """Example 6: Mouse movement and clicking"""
    print("=" * 60)
    print("Example 6: Mouse Control")
    print("=" * 60)

    automation = ScreenAutomation()

    # Get current mouse position
    current_pos = automation.get_mouse_position()
    print(f"Current mouse position: {current_pos}")

    # Get screen size for safe coordinates
    width, height = automation.get_screen_size()
    print(f"Screen size: {width}x{height}")

    print("\n(Mouse movements commented out to avoid interference)")
    print()

    # Example mouse operations (commented to avoid accidental execution):
    """
    # Move mouse to center of screen (smooth movement)
    center = (width // 2, height // 2)
    automation.move_mouse(center, smooth=True, duration=1.0)

    # Click at specific coordinates
    automation.click(coords=(100, 100))

    # Double-click
    automation.double_click(coords=(200, 200))

    # Right-click
    automation.right_click(coords=(300, 300))

    # Click an element found by OCR
    button = automation.find_element("OK button")
    if button:
        automation.click(element=button)
    """

    print("Code examples:")
    print("""
    # Smooth mouse movement to center
    automation.move_mouse((width//2, height//2), smooth=True, duration=1.0)

    # Click at coordinates
    automation.click(coords=(100, 100))

    # Double-click
    automation.double_click(coords=(200, 200))

    # Right-click
    automation.right_click(coords=(300, 300))
    """)

    automation.cleanup()
    print("\n")


def example_7_keyboard_shortcuts():
    """Example 7: Keyboard shortcuts and key combinations"""
    print("=" * 60)
    print("Example 7: Keyboard Shortcuts and Key Combinations")
    print("=" * 60)

    automation = ScreenAutomation()

    print("(Keyboard commands commented out to avoid interference)")
    print()

    # Example keyboard operations (commented):
    """
    # Press single keys
    automation.press_key("enter")
    automation.press_key("tab")
    automation.press_key("esc")

    # Press key combinations
    automation.press_key("ctrl+c")      # Copy
    automation.press_key("ctrl+v")      # Paste
    automation.press_key("ctrl+s")      # Save
    automation.press_key("alt+tab")     # Switch window
    automation.press_key("ctrl+shift+t")  # Complex combination

    # Type text followed by Enter
    automation.type_text("search query")
    automation.press_key("enter")

    # Select all and delete
    automation.press_key("ctrl+a")
    automation.press_key("delete")
    """

    print("Code examples:")
    print("""
    # Single keys
    automation.press_key("enter")
    automation.press_key("tab")
    automation.press_key("esc")

    # Key combinations
    automation.press_key("ctrl+c")       # Copy
    automation.press_key("ctrl+v")       # Paste
    automation.press_key("alt+tab")      # Switch window
    automation.press_key("ctrl+shift+t") # Reopen closed tab

    # Type and submit
    automation.type_text("Hello World")
    automation.press_key("enter")
    """)

    automation.cleanup()
    print("\n")


def example_8_complete_workflow():
    """Example 8: Complete automation workflow"""
    print("=" * 60)
    print("Example 8: Complete Automation Workflow")
    print("=" * 60)
    print("This demonstrates a typical automation sequence:")
    print("  1. Take a screenshot")
    print("  2. Find an element using OCR")
    print("  3. Click the element")
    print("  4. Type some text")
    print("  5. Submit with Enter")
    print()

    automation = ScreenAutomation()

    print("Workflow (demonstration - no actual clicks):")
    print()

    # Step 1: Take initial screenshot
    print("Step 1: Capturing initial state...")
    initial_img = automation.screenshot(save_path="workflow_initial.png")
    print("✓ Screenshot saved")

    # Step 2: Find search box
    print("\nStep 2: Looking for search input...")
    search_box = automation.find_element("search")
    if search_box:
        print(f"✓ Found search box at {search_box.center}")

        # Step 3 & 4: Click and type (commented out)
        print("\nStep 3 & 4: Would click and type 'screen automation'")
        # automation.click(element=search_box)
        # automation.wait(0.3)
        # automation.type_text("screen automation", delay_ms=50, human_like=True)

        # Step 5: Submit (commented out)
        print("\nStep 5: Would press Enter to search")
        # automation.press_key("enter")
        # automation.wait(2.0)

        # Take final screenshot
        print("\nStep 6: Would capture final state")
        # automation.screenshot(save_path="workflow_final.png")
    else:
        print("✗ Search box not found - workflow cannot continue")

    automation.cleanup()
    print("\n✓ Workflow demonstration complete")
    print("\n")


def example_9_template_matching():
    """Example 9: Find elements using template matching"""
    print("=" * 60)
    print("Example 9: Template Matching")
    print("=" * 60)

    automation = ScreenAutomation()

    print("Template matching allows finding UI elements by image reference")
    print()

    # Example (requires a template image):
    """
    # Save a small screenshot of the element you want to find
    # (e.g., a button, icon, etc.) as 'template_button.png'

    # Then find it on screen:
    element = automation.find_template(
        template_path="template_button.png",
        threshold=0.8  # 80% similarity required
    )

    if element:
        print(f"Found template at {element.center}")
        automation.click(element=element)
    """

    print("Code example:")
    print("""
    # Find element using a saved template image
    element = automation.find_template(
        template_path="my_button_template.png",
        threshold=0.8
    )

    if element:
        automation.click(element=element)
    else:
        print("Template not found")
    """)

    print("\nTo create a template:")
    print("  1. Capture a screenshot: automation.screenshot('screen.png')")
    print("  2. Crop the element you want (using image editor)")
    print("  3. Save as template: 'template_name.png'")
    print("  4. Use find_template() to locate it")

    automation.cleanup()
    print("\n")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SCREEN AUTOMATION TOOL - EXAMPLES" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    examples = [
        ("Basic Screenshot", example_1_basic_screenshot),
        ("OCR Text Extraction", example_2_ocr_text_extraction),
        ("Find and Click", example_3_find_and_click),
        ("Automated Typing", example_4_automated_typing),
        ("Video Recording", example_5_video_recording),
        ("Mouse Control", example_6_mouse_control),
        ("Keyboard Shortcuts", example_7_keyboard_shortcuts),
        ("Complete Workflow", example_8_complete_workflow),
        ("Template Matching", example_9_template_matching),
    ]

    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n" + "-" * 60)
    print("Running all examples...")
    print("-" * 60 + "\n")

    for name, example_func in examples:
        try:
            example_func()
            time.sleep(0.5)  # Brief pause between examples
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            break
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}\n")

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
