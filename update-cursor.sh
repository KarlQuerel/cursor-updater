#!/bin/bash

DOWNLOAD_DIR="$HOME/Downloads"
DEST="$HOME/.local/bin/cursor.AppImage"

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
pkill -9 -f "/tmp/.mount_Cursor" || true

# --- Step 2b: Wait until all Cursor processes are gone ---
echo "⏳ Waiting for Cursor to quit..."
while pgrep -f "/tmp/.mount_Cursor" > /dev/null; do
    sleep 1
done

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
find "$DOWNLOAD_DIR" -type f -name "Cursor-*.AppImage" ! -newer "$NEW" -delete
echo "✔ Done."
