# Photo Fixinator

## Overview
My project for fixing scanned photos by myself
**Photo Fixinator** is a personal project aimed at building a local desktop application for organizing and annotating images with metadata. 

The long-term goal is to create a simple, maintainable tool that allows browsing images, editing metadata, and storing additional information in a local database.

### Background
There are three driving factors for this project:
1. I do analog photography as a hobby and have a problem with all photos having the same data stamp as the day they are scanned. I would like to set this date myself. 
2. My family have a lot of old pictures that could be interesting to scan, but those images are most interesting with context. If we can scan them, update their metadata and maby even tag the content we can add the context. 
3. I want to have fun.
---

## Current Status 🚧

This project is currently in an **experimental phase**.

Right now, the focus is on:
- Learning the required libraries and tools
- Testing individual pieces of functionality
- Building small scripts instead of a full application

Nothing is final yet — structure, architecture, and implementation may change as the project evolves.

---

## What I'm Exploring

The current work consists of small, focused scripts to understand:

- Loading and iterating through image files
- Reading and writing EXIF metadata (`piexif`, `Pillow`)
- Working with a local SQLite database
- Creating basic UI components with `PySide6`

These experiments will later form the foundation of the full application.

---

## Project Goal (Long-Term)

The intended application will:

- Load images from a selected folder
- Display one image at a time
- Allow adding/editing:
  - Date (saved to EXIF + database)
  - Name (database)
  - Description (database)
- Store metadata in a local SQLite database
- Navigate between images

---

## Tech Stack (Planned)

- **Python**
- **PySide6** (GUI)
- **SQLite** (local database)
- **Pillow + piexif** (image + EXIF handling)

---

## Philosophy

This project is intentionally built in small steps:

- Start simple
- Learn each component in isolation
- Keep code modular so it can be reused later
- Avoid premature complexity

---

## Running the Code

At this stage, there is no single application entry point.

Instead:
- Run individual Python scripts to test specific functionality
- Scripts may change, be replaced, or removed over time

---

## Future Ideas

- Full desktop UI for browsing and editing images
- Thumbnail previews / gallery view
- Search and filtering
- Pre-filling metadata from existing EXIF data
- Possible future web-based version for sharing within family

---

## Notes

This is a learning project, so expect:
- Frequent refactoring
- Incomplete features
- Experimental code

---

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

See the [LICENSE](LICENSE) file for details.