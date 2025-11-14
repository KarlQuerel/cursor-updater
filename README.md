# cursor-appimage-updater

A simple Bash script to update the [Cursor](https://cursor.com/download) AppImage on Linux.

## Usage

1. Download the Linux AppImage (x64) from [Cursor Download](https://cursor.com/download) into your `~/Downloads` folder.
2. Make the script executable:

	```bash
	chmod +x update-cursor.sh
	```
3. Run the script:

	```bash
	./update-cursor.sh
	```
	Or view help:

	```bash
	./update-cursor.sh -h
	```
### What the script does
- Detects the newest Cursor AppImage in your `Downloads`.  
- Quits any running Cursor instances.  
- Replaces the old AppImage with the new one.  
- Cleans old AppImages from `Downloads`.  

## Requirements
- Linux x64  
- Bash  
- Cursor AppImage downloaded  

## Notes
- Make sure no Cursor instance is running if you want the update to apply immediately.  
- The script uses `pkill` to stop running Cursor processes safely before updating.
