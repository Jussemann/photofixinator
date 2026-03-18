"""
EXIF metadata handling for images.

This module provides functions to read, modify, and save EXIF metadata,
particularly for managing image capture dates.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import piexif
from PIL import Image


def load_image(file_path: str) -> Image.Image:
    """
    Load an image file from disk.

    Args:
        file_path: Path to the image file (JPEG or other PIL-supported format).

    Returns:
        A PIL Image object.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be opened as an image.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        image = Image.open(file_path)
        return image
    except Exception as e:
        raise IOError(f"Failed to load image: {e}")


def set_exif_date(file_path: str, date: datetime) -> None:
    """
    Set the EXIF date metadata for an image and save it.

    Updates the following EXIF fields:
    - DateTime (0th IFD)
    - DateTimeOriginal (Exif IFD)
    - DateTimeDigitized (Exif IFD)

    Args:
        file_path: Path to the image file to update.
        date: The datetime object representing when the image was taken.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    # Format date as EXIF expects: "YYYY:MM:DD HH:MM:SS"
    exif_date_str = date.strftime("%Y:%m:%d %H:%M:%S")

    try:
        # Read existing EXIF data or create new if none exists
        try:
            exif_dict = piexif.load(file_path)
        except piexif.InvalidImageDataError:
            # No EXIF data exists, create a new one
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        # Update DateTime (0th IFD)
        exif_dict["0th"][piexif.ImageIFD.DateTime] = exif_date_str.encode()

        # Update DateTimeOriginal (Exif IFD)
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = exif_date_str.encode()

        # Update DateTimeDigitized (Exif IFD)
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = exif_date_str.encode()

        # Dump EXIF data and save
        exif_bytes = piexif.dump(exif_dict)

        # Load image and save with new EXIF
        image = Image.open(file_path)
        image.save(file_path, exif=exif_bytes)

    except Exception as e:
        raise OSError(f"Failed to set EXIF date: {e}")


def get_exif_date(file_path: str) -> Optional[datetime]:
    """
    Retrieve the EXIF date metadata from an image.

    Attempts to read DateTimeOriginal, DateTime, or DateTimeDigitized in that order.

    Args:
        file_path: Path to the image file.

    Returns:
        A datetime object if found, None otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)

        # Try DateTimeOriginal first
        exif_ifd = exif_dict.get("Exif", {})
        if piexif.ExifIFD.DateTimeOriginal in exif_ifd:
            date_str = exif_ifd[piexif.ExifIFD.DateTimeOriginal].decode()
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

        # Fall back to DateTime
        if_0th = exif_dict.get("0th", {})
        if piexif.ImageIFD.DateTime in if_0th:
            date_str = if_0th[piexif.ImageIFD.DateTime].decode()
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

        # Fall back to DateTimeDigitized
        if piexif.ExifIFD.DateTimeDigitized in exif_ifd:
            date_str = exif_ifd[piexif.ExifIFD.DateTimeDigitized].decode()
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

        return None

    except piexif.InvalidImageDataError:
        # No EXIF data in the image
        return None
    except Exception as e:
        raise OSError(f"Failed to read EXIF date: {e}")
