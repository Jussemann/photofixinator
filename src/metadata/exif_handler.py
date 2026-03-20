"""
EXIF metadata handling for images.

This module provides functions to read, modify, and save EXIF metadata,
particularly for managing image capture dates and camera settings.
"""

from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, Optional, Union

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


def set_exif_value(
    file_path: str,
    ifd_name: str,
    tag: Union[int, str],
    value: Any,
    value_type: str = "ascii",
) -> None:
    """
    Set a generic EXIF value in an image file.

    This is a general-purpose function for setting any EXIF field. It handles
    different data types (string, ratio, short int, etc.) based on the value_type.

    Args:
        file_path: Path to the image file to update.
        ifd_name: The IFD section name ("0th", "Exif", "GPS", or "1st").
        tag: The EXIF tag ID (int) or attribute name (str).
        value: The value to set (string, float, tuple, etc.).
        value_type: The data type for the value:
            - "ascii": ASCII string (encoded)
            - "ratio": Rational number (numerator, denominator)
            - "short": Unsigned short integer
            - "long": Unsigned long integer
            - "byte": Single byte

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
        ValueError: If the ifd_name or value_type is invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    if ifd_name not in ("0th", "Exif", "GPS", "1st"):
        raise ValueError(f"Invalid IFD name: {ifd_name}")

    try:
        # Read existing EXIF data or create new if none exists
        try:
            exif_dict = piexif.load(file_path)
        except piexif.InvalidImageDataError:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        # Encode value based on type
        if value_type == "ascii":
            encoded_value = str(value).encode() if isinstance(value, str) else value.encode()
        elif value_type == "ratio":
            # Convert float to (numerator, denominator) tuple
            if isinstance(value, (int, float)):
                frac = Fraction(value).limit_denominator()
                encoded_value = (frac.numerator, frac.denominator)
            else:
                encoded_value = value
        elif value_type == "short":
            encoded_value = int(value)
        elif value_type == "long":
            encoded_value = int(value)
        elif value_type == "byte":
            encoded_value = int(value)
        else:
            encoded_value = value

        # Set the value
        exif_dict[ifd_name][tag] = encoded_value

        # Dump EXIF data and save
        exif_bytes = piexif.dump(exif_dict)
        image = Image.open(file_path)
        image.save(file_path, exif=exif_bytes)

    except Exception as e:
        raise OSError(f"Failed to set EXIF value: {e}")


# Camera and settings specific functions

def set_camera_maker(file_path: str, maker: str) -> None:
    """
    Set the camera maker (manufacturer) in EXIF metadata.

    Args:
        file_path: Path to the image file to update.
        maker: The camera manufacturer name (e.g., "Canon", "Nikon").

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    set_exif_value(file_path, "0th", piexif.ImageIFD.Make, maker, "ascii")


def get_camera_maker(file_path: str) -> Optional[str]:
    """
    Retrieve the camera maker from EXIF metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        The camera maker name if found, None otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)
        if_0th = exif_dict.get("0th", {})
        if piexif.ImageIFD.Make in if_0th:
            return if_0th[piexif.ImageIFD.Make].decode()
        return None
    except piexif.InvalidImageDataError:
        return None
    except Exception as e:
        raise OSError(f"Failed to read camera maker: {e}")


def set_camera_model(file_path: str, model: str) -> None:
    """
    Set the camera model in EXIF metadata.

    Args:
        file_path: Path to the image file to update.
        model: The camera model name (e.g., "Canon EOS 5D Mark IV").

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    set_exif_value(file_path, "0th", piexif.ImageIFD.Model, model, "ascii")


def get_camera_model(file_path: str) -> Optional[str]:
    """
    Retrieve the camera model from EXIF metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        The camera model name if found, None otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)
        if_0th = exif_dict.get("0th", {})
        if piexif.ImageIFD.Model in if_0th:
            return if_0th[piexif.ImageIFD.Model].decode()
        return None
    except piexif.InvalidImageDataError:
        return None
    except Exception as e:
        raise OSError(f"Failed to read camera model: {e}")


def set_fstop(file_path: str, fstop: Union[int, float]) -> None:
    """
    Set the F-stop (aperture) in EXIF metadata.

    Args:
        file_path: Path to the image file to update.
        fstop: The F-stop value (e.g., 2.8, 5.6, 8.0).

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    set_exif_value(file_path, "Exif", piexif.ExifIFD.FNumber, fstop, "ratio")


def get_fstop(file_path: str) -> Optional[float]:
    """
    Retrieve the F-stop from EXIF metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        The F-stop value if found, None otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)
        exif_ifd = exif_dict.get("Exif", {})
        if piexif.ExifIFD.FNumber in exif_ifd:
            ratio = exif_ifd[piexif.ExifIFD.FNumber]
            return ratio[0] / ratio[1]
        return None
    except piexif.InvalidImageDataError:
        return None
    except Exception as e:
        raise OSError(f"Failed to read F-stop: {e}")


def set_exposure_time(file_path: str, exposure_time: Union[int, float, tuple]) -> None:
    """
    Set the exposure time in EXIF metadata.

    Args:
        file_path: Path to the image file to update.
        exposure_time: The exposure time as a fraction (e.g., 0.01 for 1/100s, or (1, 100)).

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    set_exif_value(file_path, "Exif", piexif.ExifIFD.ExposureTime, exposure_time, "ratio")


def get_exposure_time(file_path: str) -> Optional[float]:
    """
    Retrieve the exposure time from EXIF metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        The exposure time as a decimal (e.g., 0.01 for 1/100s), or None if not found.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)
        exif_ifd = exif_dict.get("Exif", {})
        if piexif.ExifIFD.ExposureTime in exif_ifd:
            ratio = exif_ifd[piexif.ExifIFD.ExposureTime]
            return ratio[0] / ratio[1]
        return None
    except piexif.InvalidImageDataError:
        return None
    except Exception as e:
        raise OSError(f"Failed to read exposure time: {e}")


def set_iso_speed(file_path: str, iso: int) -> None:
    """
    Set the ISO speed in EXIF metadata.

    Args:
        file_path: Path to the image file to update.
        iso: The ISO speed value (e.g., 100, 400, 1600).

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    set_exif_value(file_path, "Exif", piexif.ExifIFD.ISOSpeedRatings, iso, "short")


def get_iso_speed(file_path: str) -> Optional[int]:
    """
    Retrieve the ISO speed from EXIF metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        The ISO speed value if found, None otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)
        exif_ifd = exif_dict.get("Exif", {})
        if piexif.ExifIFD.ISOSpeedRatings in exif_ifd:
            return exif_ifd[piexif.ExifIFD.ISOSpeedRatings]
        return None
    except piexif.InvalidImageDataError:
        return None
    except Exception as e:
        raise OSError(f"Failed to read ISO speed: {e}")


def set_focal_length(file_path: str, focal_length: Union[int, float]) -> None:
    """
    Set the focal length in EXIF metadata.

    Args:
        file_path: Path to the image file to update.
        focal_length: The focal length in millimeters (e.g., 50.0, 85.0).

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read or written.
    """
    set_exif_value(file_path, "Exif", piexif.ExifIFD.FocalLength, focal_length, "ratio")


def get_focal_length(file_path: str) -> Optional[float]:
    """
    Retrieve the focal length from EXIF metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        The focal length in millimeters if found, None otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        exif_dict = piexif.load(file_path)
        exif_ifd = exif_dict.get("Exif", {})
        if piexif.ExifIFD.FocalLength in exif_ifd:
            ratio = exif_ifd[piexif.ExifIFD.FocalLength]
            return ratio[0] / ratio[1]
        return None
    except piexif.InvalidImageDataError:
        return None
    except Exception as e:
        raise OSError(f"Failed to read focal length: {e}")
