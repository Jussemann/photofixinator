"""
image_viewer_demo.py
--------------------
MetaCruncher experiment: Display images and edit metadata.

This script demonstrates the refactored UI architecture using:
  - BaseImageWindow: reusable window base class
  - ImagePane: reusable image display widget
  - Image loader utilities: decoupled image discovery/loading

Dependencies:
  pip install PySide6 Pillow

Usage:
  Run: python scripts/GUI_test.py
"""

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ui.base_window import BaseImageWindow


class MainWindow(BaseImageWindow):
    """
    Main application window demonstrating image viewing and metadata editing.

    Layout (top to bottom):
      - Image pane      : displays the first image from test_image folder
      - Status label    : shows the filename
      - Text field      : editable title/name for the image
      - Save button     : saves metadata (demo hook)
    """

    def __init__(self) -> None:
        super().__init__(title="MetaCruncher – Image Viewer Demo")
        self.status_label: QLabel | None = None
        self.text_field: QLineEdit | None = None
        self.save_button: QPushButton | None = None

    def _setup_metadata_fields(self, layout: QVBoxLayout) -> None:
        """
        Add metadata input fields to the layout.

        Args:
            layout: The main QVBoxLayout to add widgets to.
        """
        # --- Status / filename label ---
        self.status_label = QLabel("No image loaded.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # --- Editable text field ---
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("Enter a title or name for this image…")
        layout.addWidget(self.text_field)

        # --- Save button ---
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._on_save)
        layout.addWidget(self.save_button)

        # Update status label after UI is set up
        self._update_status()

    def _update_status(self) -> None:
        """Update the status label with the current image filename."""
        if not self.status_label:
            return

        image_path = self.get_current_image_path()
        if image_path is None:
            self.status_label.setText("No image loaded.")
            self.text_field.setText("")
        else:
            filename = Path(image_path).name
            self.status_label.setText(filename)
            # Pre-fill the text field with the filename stem (no extension)
            if self.text_field:
                self.text_field.setText(Path(image_path).stem)

    def _on_save(self) -> None:
        """
        Triggered when the user clicks Save.

        Currently prints the values to the console.
        In the full app: pass these to the database layer for persistence.
        """
        if not self.text_field:
            return

        title = self.text_field.text().strip()
        path = self.get_current_image_path() or "N/A"

        # Placeholder: replace with a database.save_image_metadata() call later
        print(f"[SAVE] path='{path}'  title='{title}'")

        QMessageBox.information(
            self,
            "Saved (demo)",
            f"Title recorded:\n\n{title}\n\nDatabase write goes here.",
        )

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()