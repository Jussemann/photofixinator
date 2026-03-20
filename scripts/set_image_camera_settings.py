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

# Enable bulk mode: when True, process all images in BULK_FOLDER
# When False, process only the single image at IMAGE_PATH
BULK_SWITCH = True

# Date taken (format: year, month, day, hour, minute, second)
DATE_TAKEN = datetime(2025, 3, 10, 14, 30, 1)

# Camera manufacturer
CAMERA_MAKER = "Minolta"

# Camera model
CAMERA_MODEL = "Minolta XG-2"

# F-stop (aperture)
FSTOP = 2.4

# Exposure time (as a fraction: e.g., 0.01 for 1/100 seconds, or use tuple (1, 100))
EXPOSURE_TIME = (1, 60)  # 1/260 seconds

# ISO speed rating
ISO_SPEED = 400

# Focal length in millimeters
FOCAL_LENGTH = 35.0

# ============================================================================
# SINGLE FILE MODE
# ============================================================================
# Path to the image file to modify (used when BULK_SWITCH is False)
IMAGE_PATH = Path(__file__).parent.parent / "test_image" / "sample.jpg"

# ============================================================================
# BULK MODE
# ============================================================================
# Path to the folder containing images to process (used when BULK_SWITCH is True)
BULK_FOLDER = Path(__file__).parent.parent / "test_image"

# Image file extensions to process in bulk mode
IMAGE_FORMATS = [".jpg", ".jpeg", ".JPG", ".JPEG"]

# ============================================================================
# END CONFIGURATION
# ============================================================================


def apply_metadata_to_image(image_path: str) -> bool:
    """
    Apply all configured metadata to a single image file.

    Args:
        image_path: Path to the image file to update.

    Returns:
        True if successful, False if an error occurred.
    """
    try:
        # Load the image
        image = load_image(image_path)
        print(f"  ✓ Loaded: {image_path} ({image.size}, {image.format})")

        # Set all metadata
        set_exif_date(image_path, DATE_TAKEN)
        set_camera_maker(image_path, CAMERA_MAKER)
        set_camera_model(image_path, CAMERA_MODEL)
        set_fstop(image_path, FSTOP)
        set_exposure_time(image_path, EXPOSURE_TIME)
        set_iso_speed(image_path, ISO_SPEED)
        set_focal_length(image_path, FOCAL_LENGTH)

        print(f"  ✓ Metadata updated successfully")
        return True

    except Exception as e:
        print(f"  ✗ Error processing image: {e}")
        return False


def display_metadata(image_path: str) -> None:
    """
    Display all current EXIF metadata for an image.

    Args:
        image_path: Path to the image file.
    """
    current_date = get_exif_date(image_path)
    print(f"Date Taken: {current_date if current_date else 'Not set'}")
    print(f"Camera Maker: {get_camera_maker(image_path) or 'Not set'}")
    print(f"Camera Model: {get_camera_model(image_path) or 'Not set'}")
    print(f"F-stop: {get_fstop(image_path) or 'Not set'}")
    print(f"Exposure Time: {get_exposure_time(image_path) or 'Not set'}")
    print(f"ISO Speed: {get_iso_speed(image_path) or 'Not set'}")
    print(f"Focal Length: {get_focal_length(image_path) or 'Not set'}")


def process_single_image() -> None:
    """
    Process a single image file with metadata updates.
    """
    if not IMAGE_PATH.exists():
        print(f"Error: Test image not found at {IMAGE_PATH}")
        print("Please provide a JPEG image in the test_image folder.")
        return

    print(f"\n{'='*70}")
    print("SINGLE IMAGE MODE")
    print(f"{'='*70}\n")

    print(f"Processing: {IMAGE_PATH}")

    # Display current metadata
    print("\n=== Current EXIF Metadata ===")
    display_metadata(str(IMAGE_PATH))

    # Apply metadata
    print("\n=== Applying New EXIF Metadata ===")
    print(f"Date Taken: {DATE_TAKEN}")
    print(f"Camera Maker: {CAMERA_MAKER}")
    print(f"Camera Model: {CAMERA_MODEL}")
    print(f"F-stop: {FSTOP}")
    print(f"Exposure Time: {EXPOSURE_TIME}")
    print(f"ISO Speed: {ISO_SPEED}")
    print(f"Focal Length: {FOCAL_LENGTH}mm\n")

    if apply_metadata_to_image(str(IMAGE_PATH)):
        # Verify the changes
        print("\n=== Updated EXIF Metadata ===")
        display_metadata(str(IMAGE_PATH))


def process_bulk_images() -> None:
    """
    Process all image files in a folder with metadata updates.
    """
    if not BULK_FOLDER.exists():
        print(f"Error: Bulk folder not found at {BULK_FOLDER}")
        print("Please create the folder or update BULK_FOLDER path.")
        return

    # Find all image files (use a set to avoid duplicates across case-insensitive patterns)
    image_files_set = set()
    for ext in IMAGE_FORMATS:
        for file_path in BULK_FOLDER.glob(f"*{ext}"):
            image_files_set.add(file_path.resolve())
    
    image_files = sorted(image_files_set)

    if not image_files:
        print(f"Error: No image files found in {BULK_FOLDER}")
        print(f"Looking for: {', '.join(IMAGE_FORMATS)}")
        return

    print(f"\n{'='*70}")
    print("BULK PROCESSING MODE")
    print(f"{'='*70}\n")

    print(f"Folder: {BULK_FOLDER}")
    print(f"Found {len(image_files)} image(s) to process\n")

    print("=== Applying Metadata ===")
    print(f"Date Taken: {DATE_TAKEN}")
    print(f"Camera Maker: {CAMERA_MAKER}")
    print(f"Camera Model: {CAMERA_MODEL}")
    print(f"F-stop: {FSTOP}")
    print(f"Exposure Time: {EXPOSURE_TIME}")
    print(f"ISO Speed: {ISO_SPEED}")
    print(f"Focal Length: {FOCAL_LENGTH}mm\n")

    successful = 0
    failed = 0

    for image_file in image_files:
        if apply_metadata_to_image(str(image_file)):
            successful += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'='*70}")
    print("PROCESSING SUMMARY")
    print(f"{'='*70}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(image_files)}")


def main():
    """
    Main entry point: process either a single image or bulk images based on BULK_SWITCH.
    """
    try:
        if BULK_SWITCH:
            process_bulk_images()
        else:
            process_single_image()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
