"""
Script to set comprehensive camera and image metadata on an image.

This script demonstrates setting multiple EXIF fields including date taken,
camera maker, camera model, F-stop, exposure time, ISO speed, and focal length.
"""

from datetime import datetime
from pathlib import Path
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from metadata.exif_handler import (
    load_image,
    set_exif_date,
    set_camera_maker,
    set_camera_model,
    set_fstop,
    set_exposure_time,
    set_iso_speed,
    set_focal_length,
    get_exif_date,
    get_camera_maker,
    get_camera_model,
    get_fstop,
    get_exposure_time,
    get_iso_speed,
    get_focal_length,
)

# ============================================================================
# CONFIGURATION: Modify these variables to set your desired metadata values
# ============================================================================

# Date taken (format: year, month, day, hour, minute, second)
DATE_TAKEN = datetime(2025, 3, 10, 14, 30, 1)

# Camera manufacturer
CAMERA_MAKER = "Minolta"

# Camera model
CAMERA_MODEL = "Minolta XG-2"

# F-stop (aperture)
FSTOP = 2.4

# Exposure time (as a fraction: e.g., 0.01 for 1/100 seconds, or use tuple (1, 100))
EXPOSURE_TIME = (1, 60)  # 1/250 seconds

# ISO speed rating
ISO_SPEED = 400

# Focal length in millimeters
FOCAL_LENGTH = 35.0

# Path to the image file to modify
IMAGE_PATH = Path(__file__).parent.parent / "test_image" / "sample.jpg"

# ============================================================================
# END CONFIGURATION
# ============================================================================


def main():
    """
    Load an image and set all specified camera and image metadata.
    """
    if not IMAGE_PATH.exists():
        print(f"Error: Test image not found at {IMAGE_PATH}")
        print("Please provide a JPEG image in the test_image folder.")
        return

    try:
        # Load the image
        print(f"Loading image from: {IMAGE_PATH}")
        image = load_image(str(IMAGE_PATH))
        print(f"Image loaded successfully. Size: {image.size}, Format: {image.format}\n")

        # Display current metadata
        print("=== Current EXIF Metadata ===")
        current_date = get_exif_date(str(IMAGE_PATH))
        print(f"Date Taken: {current_date if current_date else 'Not set'}")
        print(f"Camera Maker: {get_camera_maker(str(IMAGE_PATH)) or 'Not set'}")
        print(f"Camera Model: {get_camera_model(str(IMAGE_PATH)) or 'Not set'}")
        print(f"F-stop: {get_fstop(str(IMAGE_PATH)) or 'Not set'}")
        print(f"Exposure Time: {get_exposure_time(str(IMAGE_PATH)) or 'Not set'}")
        print(f"ISO Speed: {get_iso_speed(str(IMAGE_PATH)) or 'Not set'}")
        print(f"Focal Length: {get_focal_length(str(IMAGE_PATH)) or 'Not set'}")
        print()

        # Set all metadata
        print("=== Setting New EXIF Metadata ===")
        print(f"Setting Date Taken to: {DATE_TAKEN}")
        set_exif_date(str(IMAGE_PATH), DATE_TAKEN)

        print(f"Setting Camera Maker to: {CAMERA_MAKER}")
        set_camera_maker(str(IMAGE_PATH), CAMERA_MAKER)

        print(f"Setting Camera Model to: {CAMERA_MODEL}")
        set_camera_model(str(IMAGE_PATH), CAMERA_MODEL)

        print(f"Setting F-stop to: {FSTOP}")
        set_fstop(str(IMAGE_PATH), FSTOP)

        print(f"Setting Exposure Time to: {EXPOSURE_TIME}")
        set_exposure_time(str(IMAGE_PATH), EXPOSURE_TIME)

        print(f"Setting ISO Speed to: {ISO_SPEED}")
        set_iso_speed(str(IMAGE_PATH), ISO_SPEED)

        print(f"Setting Focal Length to: {FOCAL_LENGTH}mm")
        set_focal_length(str(IMAGE_PATH), FOCAL_LENGTH)
        print("\nAll metadata saved successfully!")

        # Verify the changes
        print("\n=== Updated EXIF Metadata ===")
        updated_date = get_exif_date(str(IMAGE_PATH))
        print(f"Date Taken: {updated_date}")
        print(f"Camera Maker: {get_camera_maker(str(IMAGE_PATH))}")
        print(f"Camera Model: {get_camera_model(str(IMAGE_PATH))}")
        print(f"F-stop: {get_fstop(str(IMAGE_PATH))}")
        print(f"Exposure Time: {get_exposure_time(str(IMAGE_PATH))}")
        print(f"ISO Speed: {get_iso_speed(str(IMAGE_PATH))}")
        print(f"Focal Length: {get_focal_length(str(IMAGE_PATH))}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
