"""User interface components for Cursor Updater."""

import os
import platform
import sys
import termios
import tty

from cursor_updater.config import (
    BOLD_BLUE,
    GREEN,
    ESC_KEY,
    MENU_OPTIONS,
    MSG_WAIT_KEY,
    MSG_EXITING,
    CURSOR_DIR,
    DOWNLOADS_DIR,
    ACTIVE_SYMLINK,
    CACHE_FILE,
)
from cursor_updater.version import (
    VersionInfo,
    get_version_status,
    get_latest_remote_version,
    get_latest_local_version,
    get_platform,
)
from cursor_updater.download import download_version, select_version
from cursor_updater.output import format_message, print_error


def getch() -> str:
    """Read a single character from stdin without requiring Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def getch_timeout(timeout: float = 0.1) -> str:
    """Read a single character with timeout. Returns empty string if timeout."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        # Set non-blocking mode with timeout
        new_settings = termios.tcgetattr(fd)
        new_settings[6][termios.VMIN] = 0  # Non-blocking
        new_settings[6][termios.VTIME] = int(
            timeout * 10
        )  # Timeout in tenths of seconds
        termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
        char = sys.stdin.read(1)
        return char if char else ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name != "nt" else "cls")


def print_header() -> None:
    """Print the application header."""
    header_art = [
        "   ▄▖▖▖▄▖▄▖▄▖▄▖  ▖▖▄▖▄ ▄▖▄▖▄▖▄▖",
        "   ▌ ▌▌▙▘▚ ▌▌▙▘  ▌▌▙▌▌▌▌▌▐ ▙▖▙▘",
        "   ▙▖▙▌▌▌▄▌▙▌▌▌  ▙▌▌ ▙▘▛▌▐ ▙▖▌▌",
    ]
    for line in header_art:
        print(format_message(line, BOLD_BLUE))
    print()


def print_menu() -> None:
    """Print the main menu."""
    print()
    for key, description in MENU_OPTIONS.items():
        print(format_message(f"  {key}. {description}"))
    print()


def wait_for_key(message: str = MSG_WAIT_KEY) -> None:
    """Wait for user to press any key."""
    print(format_message(message), end="", flush=True)
    getch()


def exit_app(message: str = MSG_EXITING) -> None:
    """Exit the application with a message."""
    print(f"\n{format_message(message)}")
    sys.exit(0)


def print_version_info(info: VersionInfo) -> None:
    """Print version information."""
    print()
    print(format_message("Cursor App Information:"))

    if not info.latest_remote:
        print(format_message(f"{'  - 📡 Latest remote version:':<33} (unavailable)"))
        return

    prefix_width = 33
    print(
        format_message(
            f"{'  - 📡 Latest remote version:':<{prefix_width}} {info.latest_remote}"
        )
    )
    print(
        format_message(
            f"{'  - 📂 Latest locally available:':<{prefix_width}} {info.latest_local or 'None'}"
        )
    )
    print(
        format_message(
            f"{'  - ⚡ Currently active:':<{prefix_width}} {info.local or 'None'}"
        )
    )


def get_update_status_message(info: VersionInfo) -> str:
    """Determine update status and return formatted message."""
    if not info.local:
        return format_message(
            "💡 No active version. You can install the latest version by pressing 2"
        )

    if info.latest_remote != info.latest_local:
        message = format_message(
            f"🔍 There is a newer Cursor version available for download: {info.latest_remote}"
        )
        if info.latest_local:
            message += f"\n{format_message(f'   (You have {info.latest_local} locally, you can update to the latest version by pressing 2)')}"
        return message

    if info.latest_remote != info.local:
        return format_message(
            f"🔄 There is a newer version available locally: {info.latest_local}, "
            f"you can update to the latest version by pressing 2"
        )

    return format_message("✅ You are running the latest Cursor version!", GREEN)


def check_versions() -> None:
    """Check local vs remote versions."""
    info = get_version_status()
    print_version_info(info)

    if info.latest_remote:
        print(get_update_status_message(info))


def update_cursor() -> bool:
    """Update Cursor to latest version."""
    latest_remote = get_latest_remote_version()

    if not latest_remote:
        print_error("Could not determine latest version")
        return False

    latest_local = get_latest_local_version()
    if latest_remote != latest_local:
        if not download_version(latest_remote):
            return False

    return select_version(latest_remote)


def show_help() -> None:
    """Display help information."""
    print()
    print(format_message("📖 Help & Information", BOLD_BLUE))
    print()

    print(format_message("How it works:"))
    print("  • This tool manages Cursor AppImage versions on your system")
    print(f"  • AppImages are stored in: {DOWNLOADS_DIR}")
    print(f"  • The active version is set via symlink: {ACTIVE_SYMLINK}")
    print(f"  • Version information is cached for 15 minutes at: {CACHE_FILE}")
    print()

    print(format_message("Directory Structure:"))
    print(f"  {CURSOR_DIR}/")
    print("    ├── app-images/     (Downloaded AppImage files)")
    print("    └── active          (Symlink to active version)")
    print()

    print(format_message("Platform Detection:"))
    platform_name = get_platform()
    arch = platform.machine()
    print(f"  • Detected architecture: {arch}")
    print(f"  • Platform: {platform_name}")
    print()

    print(format_message("Menu Options:"))
    print("  1. Check Current Setup Information")
    print("     - Shows your current version, latest local, and latest remote")
    print("     - Displays update status")
    print()
    print("  2. Update Cursor to latest version")
    print("     - Downloads the latest version if not already present")
    print("     - Activates the latest version via symlink")
    print()
    print("  3. Help")
    print("     - Shows this help information")
    print()
    print("  4. Exit")
    print("     - Exits the application")
    print()

    print(format_message("Tips:"))
    print("  • Press ESC key at any time to exit")
    print("  • Old AppImage versions are kept in app-images/ for rollback")
    print("  • The cache speeds up version checks (auto-refreshes every 15 min)")
    print("  • If network issues occur, the tool will use stale cache if available")
    print()


def handle_menu_choice(choice: str) -> None:
    """Handle user menu choice."""
    if choice == "1":
        print()
        check_versions()
        print()
        wait_for_key()
    elif choice == "2":
        print()
        update_cursor()
        print()
        wait_for_key()
    elif choice == "3":
        print()
        show_help()
        print()
        wait_for_key()
    elif choice in ("q", "4"):
        exit_app()


def get_user_choice() -> str:
    """Get user menu choice."""
    while True:
        print(format_message("  Press [1-4] to select: "), end="", flush=True)
        choice = getch()

        # Check if it's an ESC character
        if ord(choice) == ESC_KEY:
            # Check if it's an escape sequence (arrow keys, etc.) or standalone ESC
            # Use a longer timeout to ensure we catch escape sequences
            next_char = getch_timeout(0.15)
            if not next_char:
                # No character followed ESC - it's a standalone ESC, exit
                exit_app()
            # ESC followed by characters - it's an escape sequence, consume and ignore
            while True:
                char = getch_timeout(0.05)
                if not char:
                    break
            # Clear the prompt line
            print("\r" + " " * 60 + "\r", end="", flush=True)
            continue

        # Check if it's a valid menu choice
        choice = choice.strip().lower()
        if choice in ("1", "2", "3", "4", "q"):
            print(choice)
            return choice

        # Invalid character - clear and continue
        print("\r" + " " * 60 + "\r", end="", flush=True)
