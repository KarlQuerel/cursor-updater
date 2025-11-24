# Cursor Updater

Simple interactive Python script to check and update Cursor AppImage on Linux.

## Features

- 🔍 Check current Cursor version vs latest available
- ⬇️ Download and update to latest version automatically
- 🎯 Clean, interactive menu interface
- 💾 Uses CVM directory structure (`~/.local/share/cvm`)

## Usage

```bash
./cursor_updater.py
```

The script will display an interactive menu:

1. Check Current Setup Information
2. Update Cursor to latest version
3. Exit

## Requirements

- Linux (x64 or ARM64)
- Python 3.6+
- Internet connection

## Installation

```bash
chmod +x cursor_updater.py
./cursor_updater.py
```

## How it works

- Downloads AppImages to `~/.local/share/cvm/app-images/`
- Creates symlink at `~/.local/share/cvm/active` pointing to the active version
- Caches version history for 15 minutes
- Automatically detects your platform architecture
