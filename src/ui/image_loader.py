"""
Image loading utilities for MetaCruncher.

Provides functions for discovering images in folders and loading them
as scalable QPixmap objects. This module is decoupled from UI logic
and can be reused across different UI implementations.
"""

from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


# Supported image extensions (can be extended for PNG, TIFF, etc.)
DEFAULT_SUPPORTED_EXTENSIONS: tuple[str, ...] = (".jpg", ".jpeg")


def find_first_image(
    folder: str | Path,
    extensions: tuple[str, ...] = DEFAULT_SUPPORTED_EXTENSIONS,
) -> str | None:
    """
    Return the absolute path of the first supported image in *folder*,
    or None if the folder is empty / contains no supported files.

    Args:
        folder: Path to the directory to search (str or Path object).
        extensions: Tuple of file extensions to search for (lowercase, e.g., ".jpg").

    Returns:
        Absolute path string, or None.
    """
    folder_path = Path(folder)
    if not folder_path.is_dir():
        return None

    for entry in sorted(folder_path.iterdir()):
        if entry.suffix.lower() in extensions:
            return str(entry)

    return None


def load_pixmap(
    image_path: str,
    max_width: int,
    max_height: int,
) -> QPixmap | None:
    """
    Load an image file into a QPixmap, scaled to fit within the given
    dimensions while preserving the aspect ratio.

    Args:
        image_path: Absolute path to the image file.
        max_width:  Maximum display width in pixels.
        max_height: Maximum display height in pixels.

    Returns:
        Scaled QPixmap, or None if loading fails.
    """
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        return None

    scaled = pixmap.scaled(
        max_width,
        max_height,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    return scaled
