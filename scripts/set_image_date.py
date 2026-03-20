"""
Simple script to load an image, set its capture date, and save it.

This script demonstrates basic image loading and EXIF date modification.
"""

from datetime import datetime
from pathlib import Path
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from metadata.exif_handler import load_image, set_exif_date, get_exif_date


def main():
    """
    Load a test image, set its date, and save it.
    """
    # Example usage: modify this path to point to your test image
    image_path = Path(__file__).parent.parent / "test_image" / "sample.jpg"

    if not image_path.exists():
        print(f"Error: Test image not found at {image_path}")
        print("Please provide a JPEG image in the test_image folder.")
        return

    try:
        # Load the image
        print(f"Loading image from: {image_path}")
        image = load_image(str(image_path))
        print(f"Image loaded successfully. Size: {image.size}, Format: {image.format}")

        # Get the current EXIF date if it exists
        current_date = get_exif_date(str(image_path))
        if current_date:
            print(f"Current EXIF date: {current_date}")
        else:
            print("No existing EXIF date found.")

        # Set a new date (example: March 18, 2026, 14:30:00)
        new_date = datetime(2026, 3, 18, 14, 30, 0)
        print(f"\nSetting image date to: {new_date}")
        set_exif_date(str(image_path), new_date)
        print("Date saved successfully!")

        # Verify the change
        updated_date = get_exif_date(str(image_path))
        print(f"Verified EXIF date: {updated_date}")

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except OSError as e:
        print(f"Operation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
