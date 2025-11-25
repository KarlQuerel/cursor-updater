# Cursor Updater for Linux

Menu-driven Python application to manage and update Cursor AppImage versions on Linux.

## Quick Start

```bash
git clone https://github.com/yourusername/cursor-updater.git
cd cursor-updater
chmod +x cursor_updater.py
./cursor_updater.py
```

## Requirements

- **Linux** (AppImages are Linux-specific)
- **Python 3.7+** (`python3 --version`)
- **Internet connection**
- **`strings` command** (usually pre-installed via `binutils`)

All operations run in user space - **no sudo/root required**.

## First-Time Setup

**No Cursor installation needed!** The script works on fresh systems:

- Creates `~/.local/bin/` and `~/.local/share/cursor-updater/` automatically
- Downloads and installs Cursor on first use
- Sets up symlink at `~/.local/bin/cursor.AppImage`

Just run the script and select option **2** to install Cursor.

## Usage

Interactive menu:

- **1** - Check version status
- **2** - Update/Install to latest version
- **3** - Help
- **4** - Exit

Press `ESC` to exit anytime.

## How It Works

Uses **symlinks** to manage versions efficiently:

- Downloads: `~/.local/share/cursor-updater/app-images/cursor-{version}.AppImage`
- Active: `~/.local/bin/cursor.AppImage` → symlink to selected version
- Cache: `/tmp/cursor_versions.json` (15-min TTL)

Allows easy version switching without duplicating large files.

## Troubleshooting

**Python not found**: Use `python3 cursor_updater.py` instead

**Permission denied**: Run `chmod +x cursor_updater.py`

**Missing dependencies**:

```bash
# Python
sudo apt install python3        # Ubuntu/Debian
sudo dnf install python3        # Fedora
sudo pacman -S python           # Arch

# strings command (rarely needed)
sudo apt install binutils        # Ubuntu/Debian
sudo dnf install binutils        # Fedora
sudo pacman -S binutils          # Arch
```

**Cursor not launching**:

1. Ensure `~/.local/bin/` is in PATH:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
   ```
2. Restart Cursor after updating (running instance won't auto-update)
3. Desktop launchers automatically use the symlink
