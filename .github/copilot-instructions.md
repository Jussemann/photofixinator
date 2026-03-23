# Copilot Instructions for MetaCruncher

## Preliminary Context (Will be removed later)

**Goal:** The ultimate goal is to build **MetaCruncher**, a full-featured local desktop application for managing and annotating images with metadata.  

**Current Phase:** For now, focus on creating small, simple Python scripts to test and experiment with individual functionalities such as:  
- Loading images from a folder.  
- Reading and writing EXIF metadata with `piexif`.  
- Saving and retrieving data from an SQLite database.  
- Displaying images with PySide6 in a basic window.  

**Important:**  
- Keep the future project in mind while experimenting: separate UI, metadata handling, and database logic.  
- Modularize functions and code snippets so they can be easily integrated into the full application later.  
- Avoid building full UI features or complex flows at this stage; focus on validating core functionality and learning how components will interact.  

---

## Project Overview
**MetaCruncher** is a local desktop application for annotating and managing a collection of images.  
Its primary purpose is to allow a user to load images from a folder, view them one at a time, and store associated metadata (date, name, description) locally.

- **Language:** Python
- **GUI Framework:** PySide6
- **Database:** SQLite
- **Image Metadata:** piexif + Pillow

---

## Core Features

### 1. Image Loading & Navigation
- Load images from a user-selected folder.
- Support JPEG images (primary) and optionally other common formats.
- Display images one at a time with next/previous navigation buttons.
- Optional: thumbnail preview or image list in future updates.

### 2. Metadata Management
- Input fields for:
  - **Date** (stored in image EXIF and database)
  - **Name** (database only)
  - **Description** (database only)
- Update EXIF metadata for date fields using **piexif**.
- Save all metadata in a **local SQLite database**.
- Optional: pre-fill fields with existing metadata if available.

### 3. Database
- Single-user, local SQLite database.
- Tables should include at minimum:
  - `images` with `file_path`, `date`, `name`, `description`
- Abstract database operations in a dedicated access layer.

---

## Architectural Guidelines

### 1. Layer Separation
- **UI Layer:** PySide6 widgets and user interactions.
- **Image/Metadata Layer:** Logic for reading/writing EXIF and image files.
- **Database Layer:** SQLite access, CRUD operations, migrations.

### 2. Design Principles
- Single-user local tool (no cloud/multi-user requirements initially).
- Maintainable and extendable structure.
- Avoid hardcoding paths; use dynamic folder selection.
- Prepare for potential future web migration:
  - Keep database access and image handling decoupled from UI.
  - Store data in normalized structures for easy export/migration.

---

## Coding Conventions
- Follow **PEP8** for Python code formatting.
- Use **type hints** where possible.
- Separate UI code from business logic:
  - UI classes only handle layout and signals.
  - Metadata/database operations in separate classes/modules.
- Use exception handling for:
  - File I/O errors
  - Database operations
  - Image metadata read/write errors
- Comment functions and classes with purpose and usage.

---

## Future Considerations
- Search/filter functionality based on metadata.
- Web-based interface for family sharing.
- Thumbnail grid or gallery mode.
- Pre-fill metadata fields automatically using existing EXIF or previous database entries.
- Support for additional image formats (PNG, TIFF).

---

## Copilot Usage Notes
- Prefer **modular functions** over large monolithic blocks.
- Suggest database schema and CRUD methods when detecting image metadata operations.
- Generate PySide6 UI components with signals/slots for next/previous navigation.
- Include EXIF date handling using `piexif`.
- Ensure AI suggestions respect the separation between UI, database, and metadata layers.
- When generating code for future web migration, note decoupling of data handling from UI.