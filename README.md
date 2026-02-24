# Reindeer Photo Downloader

Automated script to download photos from reindeer-02.topschool.tw (班級114 class albums).

## ✅ Successfully Tested

The script has been tested and successfully downloads **all albums** with **all photos** from 班級114 across multiple pages!

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your credentials (required):

   **Option A: Using .env file (Recommended)**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your credentials
   nano .env  # or use any text editor
   ```

   Edit the `.env` file to add your actual credentials:
   ```
   REINDEER_USERNAME=your_actual_username
   REINDEER_PASSWORD=your_actual_password
   REINDEER_CLASS_NAME=班級114
   MAX_ALBUMS=all
   ```

   **Option B: Export environment variables**
   ```bash
   export REINDEER_USERNAME=your_username
   export REINDEER_PASSWORD=your_password
   export REINDEER_CLASS_NAME=班級114
   export MAX_ALBUMS=all
   ```

   **Note:** The first three environment variables (USERNAME, PASSWORD, CLASS_NAME) are required. The script will exit with an error if any are missing.

## Usage

Run the download script:
```bash
python download_photos_all_pages.py
```

The script will:
1. Navigate to https://reindeer-02.topschool.tw
2. Click `校園花絮` → `班級相簿`
3. Login with your credentials (from environment variables)
4. Select your class (e.g., `班級114`)
5. Scan all album list pages to find all albums (or up to MAX_ALBUMS limit)
6. Download all photos from all pages in each album
7. Save photos to `photo/` folder with album subfolders

### Limiting Album Downloads

By default, the script downloads **all albums**. You can limit the number of albums to download using the `MAX_ALBUMS` environment variable:

**Download all albums (default):**
```bash
MAX_ALBUMS=all
```

**Download only the first 5 albums:**
```bash
MAX_ALBUMS=5
```

**Download only the first 10 albums:**
```bash
MAX_ALBUMS=10
```

The script will stop fetching more album list pages once the limit is reached, making it faster for testing or partial downloads.

## Project Structure

```
reindeer-photo/
├── download_photos_all_pages.py  # Main download script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
└── photo/                         # Downloaded photos (organized by album)
```

## Output Structure

```
photo/
├── 班級1140209-13/
│   ├── image_as0_sid1386_uid553741_a3d843b6-d424-4e08-ac77-64602df45e20.jpg
│   ├── image_as0_sid1386_uid553741_edb37449-c627-4f17-9d7c-17751ac6dd06.jpg
│   └── ... (18 photos)
├── 班級115.02.02~114.02.06/
│   ├── image_as0_sid1386_uid553745_370ac32a-132a-4414-8129-aa5e311a093b.jpeg
│   └── ... (18 photos)
├── 班級1150126-30/
│   └── ... (18 photos)
├── 班級1140119-23/
│   └── ... (18 photos)
├── 班級115.01.12~115.01.16/
│   └── ... (18 photos)
├── 班級115.01.05~115.01.09/
│   └── ... (18 photos)
├── 班級1141229-12/
│   └── ... (18 photos)
├── 班級114.12.22~12.26/
│   └── ... (18 photos)
├── 班級1141215-19/
│   └── ... (18 photos)
└── 班級114.12.08~114.12.12/
    └── ... (18 photos)
```

## Features

- ✅ Automatic navigation and login
- ✅ **Full pagination support** - Downloads from ALL album list pages
- ✅ **Downloads ALL photos** - Goes through all pages within each album
- ✅ **Configurable class name** - Download from any class (班級114, 班級113, etc.)
- ✅ **Configurable album limit** - Download all albums or limit to first N albums
- ✅ Preserves original filenames
- ✅ Skips already downloaded photos (resume capability)
- ✅ Organized folder structure by album name
- ✅ Progress tracking with detailed output
- ✅ Browser visible by default (set `headless=True` to hide)
- ✅ **Secure credential management** - Uses environment variables

## Requirements

- Python 3.8+
- Google Chrome installed at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Internet connection

## Notes

- The script uses Selenium with Chrome WebDriver
- The script automatically loads credentials from `.env` file using `python-dotenv`
- Albums can have multiple pages (typically 18 photos per page)
- Total download time varies based on number of albums and photos
- Photos are saved in their original quality
- Credentials are never stored in code - use environment variables for security

## Security

**Important:** Never commit your `.env` file with actual credentials to version control. The `.gitignore` file is configured to exclude it automatically.

## Quick Start

See [QUICK_START.md](QUICK_START.md) for a step-by-step guide on how to set up and run the script.

