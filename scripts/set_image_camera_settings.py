"""
Script to set comprehensive camera and image metadata on an image.

This script demonstrates setting multiple EXIF fields including date taken,
camera maker, camera model, F-stop, exposure time, ISO speed, focal length,
and GPS location.
"""

from datetime import datetime
import importlib
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
    set_gps_location,
    get_exif_date,
    get_camera_maker,
    get_camera_model,
    get_fstop,
    get_exposure_time,
    get_iso_speed,
    get_focal_length,
    get_gps_location,
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

# GPS location preset selection. Use one of the names in data/gps_locations.yaml,
# or set to "custom" to use the coordinates below.
GPS_LOCATION_CHOICE = "Mo i Rana"

# Custom GPS location used when GPS_LOCATION_CHOICE is set to "custom"
CUSTOM_GPS_LOCATION_NAME = "Custom location"
CUSTOM_GPS_LATITUDE = 66.0
CUSTOM_GPS_LONGITUDE = 14.0

# ============================================================================
# SINGLE FILE MODE
# ============================================================================
# Path to the image file to modify (used when BULK_SWITCH is False)
IMAGE_PATH = Path(__file__).parent.parent / "test_image" / "sample.jpg"

# Path to the YAML file containing preset GPS locations
GPS_LOCATIONS_FILE = Path(__file__).parent.parent / "data" / "gps_locations.yaml"

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


def load_gps_locations(config_path: Path) -> dict[str, dict[str, float]]:
    """
    Load preset GPS locations from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Mapping of location names to latitude/longitude pairs.

    Raises:
        FileNotFoundError: If the YAML file does not exist.
        ValueError: If the YAML structure is invalid.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"GPS locations file not found: {config_path}")

    yaml_module = importlib.import_module("ruamel.yaml")
    yaml = yaml_module.YAML(typ="safe")
    with config_path.open("r", encoding="utf-8") as file_handle:
        data = yaml.load(file_handle) or {}

    locations = data.get("locations")
    if not isinstance(locations, dict):
        raise ValueError("GPS locations YAML must contain a 'locations' mapping.")

    validated_locations: dict[str, dict[str, float]] = {}
    for name, coordinates in locations.items():
        if not isinstance(coordinates, dict):
            raise ValueError(f"GPS location '{name}' must be a mapping.")

        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")
        if latitude is None or longitude is None:
            raise ValueError(
                f"GPS location '{name}' must define both latitude and longitude."
            )

        validated_locations[str(name)] = {
            "latitude": float(latitude),
            "longitude": float(longitude),
        }

    return validated_locations


def get_selected_gps_location() -> tuple[str, float, float]:
    """
    Resolve the selected GPS location from presets or custom coordinates.

    Returns:
        Tuple containing location name, latitude, and longitude.

    Raises:
        ValueError: If the configured preset does not exist.
    """
    if GPS_LOCATION_CHOICE.lower() == "custom":
        return (
            CUSTOM_GPS_LOCATION_NAME,
            float(CUSTOM_GPS_LATITUDE),
            float(CUSTOM_GPS_LONGITUDE),
        )

    locations = load_gps_locations(GPS_LOCATIONS_FILE)
    if GPS_LOCATION_CHOICE not in locations:
        available_locations = ", ".join(sorted(locations))
        raise ValueError(
            f"Unknown GPS location '{GPS_LOCATION_CHOICE}'. "
            f"Available presets: {available_locations}, custom"
        )

    selected_location = locations[GPS_LOCATION_CHOICE]
    return (
        GPS_LOCATION_CHOICE,
        selected_location["latitude"],
        selected_location["longitude"],
    )


def format_gps_coordinates(latitude: float, longitude: float) -> str:
    """
    Format latitude and longitude for readable console output.

    Args:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.

    Returns:
        Formatted coordinate string.
    """
    return f"{latitude:.6f}, {longitude:.6f}"


def apply_metadata_to_image(
    image_path: str,
    gps_location_name: str,
    gps_latitude: float,
    gps_longitude: float,
) -> bool:
    """
    Apply all configured metadata to a single image file.

    Args:
        image_path: Path to the image file to update.
        gps_location_name: Display name of the GPS location.
        gps_latitude: Latitude in decimal degrees.
        gps_longitude: Longitude in decimal degrees.

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
        set_gps_location(image_path, gps_latitude, gps_longitude)

        print(
            "  ✓ Metadata updated successfully "
            f"({gps_location_name}: {format_gps_coordinates(gps_latitude, gps_longitude)})"
        )
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
    gps_location = get_gps_location(image_path)
    if gps_location is None:
        print("GPS Location: Not set")
    else:
        print(f"GPS Location: {format_gps_coordinates(*gps_location)}")


def process_single_image() -> None:
    """
    Process a single image file with metadata updates.
    """
    gps_location_name, gps_latitude, gps_longitude = get_selected_gps_location()

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
    print(f"Focal Length: {FOCAL_LENGTH}mm")
    print(
        f"GPS Location: {gps_location_name} "
        f"({format_gps_coordinates(gps_latitude, gps_longitude)})\n"
    )

    if apply_metadata_to_image(
        str(IMAGE_PATH),
        gps_location_name,
        gps_latitude,
        gps_longitude,
    ):
        # Verify the changes
        print("\n=== Updated EXIF Metadata ===")
        display_metadata(str(IMAGE_PATH))


def process_bulk_images() -> None:
    """
    Process all image files in a folder with metadata updates.
    """
    gps_location_name, gps_latitude, gps_longitude = get_selected_gps_location()

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
    print(f"Focal Length: {FOCAL_LENGTH}mm")
    print(
        f"GPS Location: {gps_location_name} "
        f"({format_gps_coordinates(gps_latitude, gps_longitude)})\n"
    )

    successful = 0
    failed = 0

    for image_file in image_files:
        if apply_metadata_to_image(
            str(image_file),
            gps_location_name,
            gps_latitude,
            gps_longitude,
        ):
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
