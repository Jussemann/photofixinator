"""
Reusable image display widget for MetaCruncher.

Provides the ImagePane widget which encapsulates image display,
scaling, and styling. Can be used in any PySide6 application.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ImagePane(QLabel):
    """
    A reusable image display widget with fixed dimensions and styled background.

    Features:
      - Fixed size display area
      - Centered alignment
      - Dark theme styling with border
      - Accept QPixmap for display

    Example:
        pane = ImagePane(width=600, height=450)
        pane.setPixmap(some_pixmap)
    """

    def __init__(self, width: int = 600, height: int = 450) -> None:
        """
        Initialize the image pane.

        Args:
            width: Display width in pixels.
            height: Display height in pixels.
        """
        super().__init__()
        self.setFixedSize(width, height)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444;")

    def display_pixmap(self, pixmap: QPixmap | None) -> None:
        """
        Display a pixmap, or clear the display if pixmap is None.

        Args:
            pixmap: QPixmap to display, or None to clear.
        """
        if pixmap is None:
            self.clear()
        else:
            self.setPixmap(pixmap)
