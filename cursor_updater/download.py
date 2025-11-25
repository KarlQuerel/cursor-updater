"""Download and file management for Cursor Updater."""

import os
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from cursor_updater.config import (
    DOWNLOADS_DIR,
    CURSOR_APPIMAGE,
    CHUNK_SIZE,
    DOWNLOAD_TIMEOUT,
    USER_AGENT,
)
from cursor_updater.version import get_download_url
from cursor_updater.output import print_error, print_success, print_info


def get_appimage_path(version: str) -> Path:
    """Get the path to an AppImage file for a given version."""
    return DOWNLOADS_DIR / f"cursor-{version}.AppImage"


def bytes_to_mb(bytes_size: int) -> int:
    """Convert bytes to MB."""
    return bytes_size // 1024 // 1024


def _show_download_progress(downloaded: int, total_size: int) -> None:
    """Display download progress."""
    percent = (downloaded / total_size) * 100
    mb_downloaded = bytes_to_mb(downloaded)
    mb_total = bytes_to_mb(total_size)
    print(f"\r   {percent:.1f}% ({mb_downloaded}MB/{mb_total}MB)", end="", flush=True)


def download_file(url: str, filepath: Path) -> bool:
    """Download a file with progress indication."""
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=DOWNLOAD_TIMEOUT) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            with open(filepath, "wb") as f:
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        _show_download_progress(downloaded, total_size)

            print()
            os.chmod(filepath, 0o755)
            return True
    except (URLError, HTTPError, TimeoutError, OSError) as e:
        print_error(f"Download failed: {e}")
        if filepath.exists():
            filepath.unlink()
        return False


def download_version(version: str) -> bool:
    """Download a specific version."""
    url = get_download_url(version)
    if not url:
        print_error(f"Could not get download URL for {version}")
        return False

    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = get_appimage_path(version)

    if filepath.exists():
        print_success("Already downloaded")
        return True

    print_info(f"⬇️  Downloading {version}...")
    if download_file(url, filepath):
        print_success("Download complete")
        return True
    return False


def create_symlink(target: Path, link: Path) -> bool:
    """Create a symlink, removing existing one if present."""
    link.parent.mkdir(parents=True, exist_ok=True)

    if link.exists() or link.is_symlink():
        if link.is_symlink():
            link.unlink()
        else:
            # If it's a regular file, backup it first
            backup_path = link.with_suffix(".AppImage.backup")
            if backup_path.exists():
                backup_path.unlink()
            link.rename(backup_path)
            print_info("Backed up existing Cursor AppImage")

    try:
        link.symlink_to(target)
        return True
    except OSError:
        return False


def select_version(version: str) -> bool:
    """Select a version by creating symlink."""
    appimage_path = get_appimage_path(version)

    if not appimage_path.exists():
        print_error(f"Version {version} not found locally")
        return False

    if create_symlink(appimage_path, CURSOR_APPIMAGE):
        print_success(
            f"{version} is now the active Cursor version. Please restart Cursor to use it."
        )
        return True

    print_error(f"Failed to activate {version}")
    return False
