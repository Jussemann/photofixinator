"""
Base window classes for MetaCruncher.

Provides reusable base classes that implement common UI patterns,
reducing boilerplate in concrete window implementations.
"""

from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .image_loader import find_first_image, load_pixmap
from .image_display import ImagePane


class BaseImageWindow(QMainWindow):
    """
    Base class for windows that display and manage images.

    Subclasses should override _setup_metadata_fields() to add
    image-specific UI elements (text fields, buttons, etc.).

    This class handles:
      - Image discovery and loading
      - Common image pane setup
      - Layout management
    """

    # Configuration (can be overridden by subclasses)
    IMAGE_FOLDER: Path = Path(__file__).parent.parent.parent / "test_image"
    IMAGE_PANE_WIDTH: int = 600
    IMAGE_PANE_HEIGHT: int = 450

    def __init__(self, title: str = "MetaCruncher – Image Viewer") -> None:
        """
        Initialize the base image window.

        Args:
            title: Window title.
        """
        super().__init__()
        self.setWindowTitle(title)
        self._image_path: str | None = None
        self._layout: QVBoxLayout | None = None
        self.image_pane: ImagePane | None = None
        
        self._setup_ui()
        self._load_image()

    def _setup_ui(self) -> None:
        """
        Set up the main UI. Subclasses can override to customize layout.
        """
        # Create main layout
        layout = QVBoxLayout()

        # Add image pane
        self.image_pane = ImagePane(self.IMAGE_PANE_WIDTH, self.IMAGE_PANE_HEIGHT)
        layout.addWidget(self.image_pane)

        # Let subclasses add metadata fields
        self._setup_metadata_fields(layout)

        # Set layout spacing and margins
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        # Create container and set as central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self._layout = layout

    def _setup_metadata_fields(self, layout: QVBoxLayout) -> None:
        """
        Add metadata input fields to the layout.

        Subclasses should override this method to add fields like text input,
        buttons, labels, etc.

        Args:
            layout: The main QVBoxLayout to add widgets to.
        """
        # Base implementation: subclasses override this method
        pass

    def _load_image(self) -> None:
        """
        Find and display the first image in IMAGE_FOLDER.
        """
        self._image_path = find_first_image(self.IMAGE_FOLDER)

        if self._image_path is None:
            print(f"No images found in: {self.IMAGE_FOLDER}")
            return

        pixmap = load_pixmap(
            self._image_path,
            self.IMAGE_PANE_WIDTH,
            self.IMAGE_PANE_HEIGHT,
        )

        if pixmap is None:
            print(f"Failed to load: {self._image_path}")
            return

        if self.image_pane:
            self.image_pane.display_pixmap(pixmap)

        print(f"Loaded: {Path(self._image_path).name}")

    def get_current_image_path(self) -> str | None:
        """
        Get the path of the currently displayed image.

        Returns:
            Image file path, or None if no image is loaded.
        """
        return self._image_path
