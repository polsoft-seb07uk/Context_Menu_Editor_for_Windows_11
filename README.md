<p align="center">
  <img src="screenshot.png" alt="Context Menu Editor screenshot" width="720">
</p>

<h1 align="center">Context Menu Editor</h1>

<p align="center">
  A lightweight, portable Windows 11 tool to manage right-click context menu entries.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows%2011-0078D4" alt="Platform">
  <img src="https://img.shields.io/badge/version-1.1.5-success" alt="Version">
  <img src="https://img.shields.io/badge/build-portable%20.exe-informational" alt="Build">
  <img src="https://img.shields.io/badge/license-Proprietary-lightgrey" alt="License">
</p>

---

## Overview

**Context Menu Editor** shows exactly the entries that appear when you right-click in Windows 11 — the same items visible under "Show more options" — with no extra clutter. From a single window you can **enable**, **disable**, or **permanently delete** any entry.

## Features

- 🖱️ View real right-click context menu entries: files, folders, folder background, drives, and all objects
- ✅ Enable / ❌ disable entries without deleting them
- 🗑️ Permanently delete unwanted entries (with confirmation)
- 🌗 Light and dark theme
- 🌍 English / Polish interface, switchable at runtime
- 🔐 Optional "Run as administrator" mode for full `HKLM` / `HKCR` access
- 📦 Portable — single `.exe` file, no installation required

## Download

Grab the latest portable build from the [Releases](../../releases) page:

```
ContextMenuEditor.exe
```

No installation, no dependencies, no admin rights required to launch (admin mode can be enabled from within the app when needed).

## Usage

1. Download `ContextMenuEditor.exe`.
2. Run it — double-click, no setup needed.
3. Click **Refresh** to scan current context menu entries.
4. Select one or more entries, then **Enable**, **Disable**, or **Delete**.
5. For system-level (`HKLM`) entries, click **Run as administrator** if prompted.

> Settings (theme, language) are stored locally in `%userprofile%\.polsoft\settings\WebViewer.json`.

## Building from source

This repository includes everything needed to build the portable `.exe` yourself with [PyInstaller](https://pyinstaller.org/):

| File | Purpose |
|---|---|
| `context_menu_editor.py` | Application source |
| `ico.ico` | Application icon |
| `ContextMenuEditor.spec` | PyInstaller build spec (one-file, windowed, icon, version info) |
| `version_info.txt` | Windows version resource (file properties) |
| `extract_icon_hook.py` | Runtime hook to keep the icon working in one-file mode |
| `build.bat` | One-click build script |

```bat
build.bat
```

The compiled executable is created at `dist\ContextMenuEditor.exe`.

**Requirements:** Windows, Python 3, `pip install pyinstaller` (installed automatically by `build.bat` if missing).

## Requirements

- Windows 11 (or Windows 10)
- Administrator privileges recommended for editing system-wide (`HKLM`) entries

## License

Proprietary. All rights reserved.

---

<p align="center">Made for a cleaner right-click menu.</p>
