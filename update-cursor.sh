#!/bin/bash

DOWNLOAD_DIR="$HOME/Downloads"
DEST="$HOME/.local/bin/cursor.AppImage"

# --- Step 0: Help option ---
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0"
    echo
    echo "Updates the Cursor Linux AppImage."
    echo "1. Finds the newest downloaded Cursor AppImage in ~/Downloads."
    echo "2. Kills any running Cursor instances."
    echo "3. Updates ~/.local/bin/cursor.AppImage."
    echo "4. Cleans old Cursor AppImages in Downloads."
    echo
    echo "Make sure you downloaded the Linux AppImage (x64) from: https://cursor.com/download"
    exit 0
fi

# --- Step 1: Check if AppImage exists ---
NEW=$(ls -t "$DOWNLOAD_DIR"/Cursor-*.AppImage 2>/dev/null | head -n 1)
if [[ -z "$NEW" ]]; then
    echo "❌ No Cursor AppImage found in $DOWNLOAD_DIR."
    echo "➡️ Please download the Linux AppImage (x64) from: https://cursor.com/download"
    exit 1
fi
echo "📦 Found: $NEW"

# --- Step 2: Kill all running Cursor processes ---
echo "🛑 Killing running Cursor instances..."

# Function to check if any Cursor processes are running
cursor_running() {
    # Check for processes using the AppImage or mount directory
    pgrep -f "/tmp/.mount_Cursor" > /dev/null 2>&1 && return 0
    pgrep -f "cursor.AppImage" > /dev/null 2>&1 && return 0
    pgrep -f "Cursor.AppImage" > /dev/null 2>&1 && return 0
    # Check if destination file is in use
    if [[ -f "$DEST" ]]; then
        lsof "$DEST" > /dev/null 2>&1 && return 0
    fi
    # Check for cursor processes by name (more specific)
    pgrep -x "cursor" > /dev/null 2>&1 && return 0
    pgrep -x "Cursor" > /dev/null 2>&1 && return 0
    return 1
}

# Kill processes if any are running
if cursor_running; then
    # Try multiple methods to kill Cursor
    pkill -9 -f "/tmp/.mount_Cursor" 2>/dev/null || true
    pkill -9 -f "cursor.AppImage" 2>/dev/null || true
    pkill -9 -f "Cursor.AppImage" 2>/dev/null || true
    pkill -9 -x cursor 2>/dev/null || true
    pkill -9 -x Cursor 2>/dev/null || true
    
    # --- Step 2b: Wait until all Cursor processes are gone ---
    echo "⏳ Waiting for Cursor to quit..."
    MAX_WAIT=30
    WAITED=0
    while cursor_running && [ $WAITED -lt $MAX_WAIT ]; do
        sleep 1
        WAITED=$((WAITED + 1))
    done
    
    if cursor_running; then
        echo "❌ Error: Cursor processes are still running after ${MAX_WAIT}s timeout"
        echo "   Please manually close all Cursor windows and try again."
        exit 1
    fi
fi

# --- Step 3: Update AppImage safely ---
echo "📁 Updating $DEST..."
TMP_DEST="$DEST.tmp"
cp "$NEW" "$TMP_DEST"
chmod +x "$TMP_DEST"
mv "$TMP_DEST" "$DEST"

# --- Step 4: Extract and show version ---
VERSION=$(basename "$NEW" | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+')
echo "✨ Updated Cursor to version: $VERSION"

# --- Step 5: Clean old AppImages ---
echo "🧹 Cleaning old AppImages..."
# Delete old AppImages, but keep the one we just used (and any newer ones)
find "$DOWNLOAD_DIR" -type f -name "Cursor-*.AppImage" ! -newer "$NEW" ! -samefile "$NEW" -delete
echo "✔ Done."
