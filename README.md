# Media Automation Tools

A collection of scripts designed to automate video transcoding and media library management using [HandBrakeCLI](https://handbrake.fr/).

## Scripts

### 1. Python Batch Converter (`hb_batchconvertvideos.py`)
A cross-platform (Python 2.7+) script for batch-converting video files into a standard MP4 format.

- **Features**: Automatically crawls a directory and converts common formats (`.avi`, `.mkv`, `.mov`, etc.) to MP4 using the Handbrake "Normal" preset.
- **Dependencies**: Requires `HandBrakeCLI.exe` located at `C:\Program Files\Handbrake\HandBrakeCLI.exe`.
- **> [!CAUTION]**
  > This script **permanently deletes** the original source file upon successful conversion.

### 2. PowerShell Media Manager (`ConvertM4V.ps1`)
A Windows-focused script tailored for home media servers (e.g., Microserver setups).

- **Features**:
  - Handles conversion from network shares.
  - Checks for existing movies in the destination library to avoid duplicates.
  - Moves original files to `Converted` or `Duplicates` folders instead of deleting them.
  - Uses the `AppleTV` preset by default.
- **Dependencies**: Configured for a specific `Microserver` environment; requires paths to be updated in the script header.

## Prerequisites

- [HandBrake Command Line Interface (HandBrakeCLI)](https://handbrake.fr/downloads2.php)
- Python 2.7 (for the Python script)
- PowerShell (for the PS1 script)
