#!/usr/bin/env python3
"""
Complete script to download ALL photos from ALL pages in reindeer-02.topschool.tw
Downloads all albums from a specified class with full pagination support
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PhotoDownloader:
    def __init__(self):
        self.base_url = "https://reindeer-02.topschool.tw"
        self.username = os.getenv("REINDEER_USERNAME")
        self.password = os.getenv("REINDEER_PASSWORD")
        self.class_name = os.getenv("REINDEER_CLASS_NAME")

        # Validate required environment variables
        if not self.username:
            raise ValueError("REINDEER_USERNAME environment variable is required")
        if not self.password:
            raise ValueError("REINDEER_PASSWORD environment variable is required")
        if not self.class_name:
            raise ValueError("REINDEER_CLASS_NAME environment variable is required")
        self.photo_dir = Path("photo")
        self.photo_dir.mkdir(exist_ok=True)
        self.driver = None
        self.wait = None
        self.total_photos_downloaded = 0
        self.total_albums_processed = 0
        
    def run(self):
        try:
            # Setup Chrome driver
            print("Setting up Chrome driver...", flush=True)
            options = Options()
            options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            # options.add_argument('--headless')  # Uncomment to run headless
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            print("Launching Chrome...", flush=True)
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome launched successfully!\n", flush=True)
            
            print(f"Navigating to {self.base_url}...", flush=True)
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Step 1: Click 校園花絮
            print("Clicking '校園花絮'...", flush=True)
            self.driver.find_element(By.XPATH, "//*[contains(text(), '校園花絮')]").click()
            time.sleep(1)
            
            # Step 2: Click 班級相簿
            print("Clicking '班級相簿'...", flush=True)
            self.driver.find_element(By.XPATH, "//*[contains(text(), '班級相簿')]").click()
            time.sleep(2)
            
            # Step 3: Handle login
            print("Logging in...", flush=True)
            self.login()
            
            # Step 4: Select class
            print(f"Selecting '{self.class_name}'...", flush=True)
            self.driver.find_element(By.XPATH, f"//*[contains(text(), '{self.class_name}')]").click()
            time.sleep(3)
            
            # Step 5: Get all album URLs from all pages
            print("Finding all albums across all pages...", flush=True)
            all_album_urls = self.get_all_album_urls()
            print(f"Found {len(all_album_urls)} total albums\n", flush=True)
            
            # Step 6: Download photos from each album
            for idx, album_url in enumerate(all_album_urls, 1):
                print(f"[{idx}/{len(all_album_urls)}] Processing album...", flush=True)
                self.download_album(album_url, idx, len(all_album_urls))
            
            print(f"\n✅ All photos downloaded successfully!", flush=True)
            print(f"📊 Summary:", flush=True)
            print(f"   - Total albums: {self.total_albums_processed}", flush=True)
            print(f"   - Total photos: {self.total_photos_downloaded}", flush=True)
            
        except Exception as e:
            print(f"❌ Error: {e}", flush=True)
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("\nClosing browser...", flush=True)
                time.sleep(2)
                self.driver.quit()
    
    def login(self):
        """Handle the login process"""
        try:
            time.sleep(2)
            
            # Find and fill username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "account"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            
            # Find and fill password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Submit login
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            
            time.sleep(3)
            print("  ✓ Login completed", flush=True)
            
        except Exception as e:
            print(f"  Login error: {e}", flush=True)
            raise
    
    def get_all_album_urls(self):
        """Get all album URLs from all pages in the album list"""
        all_urls = []
        page_num = 1
        
        while True:
            print(f"  Scanning album list page {page_num}...", flush=True)
            
            # Get albums on current page
            time.sleep(2)
            albums = self.driver.find_elements(By.CLASS_NAME, "albumbgphoto")
            page_urls = [link.get_attribute("href") for link in albums]
            all_urls.extend(page_urls)
            print(f"    Found {len(page_urls)} albums on page {page_num}", flush=True)
            
            # Check if there's a next page
            pagination = self.driver.find_elements(By.CSS_SELECTOR, "ul.pagination li a")
            next_page_num = page_num + 1
            next_page_link = None
            
            for link in pagination:
                if link.text.strip() == str(next_page_num):
                    next_page_link = link
                    break
            
            if next_page_link:
                print(f"    Navigating to page {next_page_num}...", flush=True)
                next_page_link.click()
                time.sleep(3)
                page_num = next_page_num
            else:
                print(f"    No more pages (reached page {page_num})", flush=True)
                break
        
        return all_urls

    def download_album(self, album_url, current, total):
        """Download all photos from all pages of a specific album"""
        try:
            # Navigate to album (page 1)
            base_album_url = album_url.split('&pageIndex=')[0]
            self.driver.get(f"{base_album_url}&pageIndex=1")
            time.sleep(3)

            # Get album name from H2
            try:
                h2_element = self.driver.find_element(By.TAG_NAME, "h2")
                album_name_full = h2_element.text  # e.g., "相簿名稱: 班級1140209-13"
                # Extract just the album name part
                if ":" in album_name_full:
                    album_name = album_name_full.split(":", 1)[1].strip()
                else:
                    album_name = album_name_full.strip()
            except:
                album_name = f"album_{current}"

            album_name = self.sanitize_filename(album_name)
            album_dir = self.photo_dir / album_name
            album_dir.mkdir(exist_ok=True)

            print(f"  Album: {album_name}", flush=True)

            # Download photos from all pages
            album_photos_count = 0
            page_num = 1

            while True:
                print(f"    Page {page_num}...", flush=True)

                # Get all photo links on current page
                photo_links = self.driver.find_elements(By.CLASS_NAME, "photo-gallery")
                photo_urls = []
                for link in photo_links:
                    href = link.get_attribute("href")
                    if href and any(ext in href.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        photo_urls.append(href)

                print(f"      Found {len(photo_urls)} photos on page {page_num}", flush=True)

                # Download each photo
                for idx, photo_url in enumerate(photo_urls, 1):
                    try:
                        filename = self.get_filename_from_url(photo_url)
                        filepath = album_dir / filename

                        # Skip if already downloaded
                        if filepath.exists():
                            print(f"        [{idx}/{len(photo_urls)}] Skipped (exists): {filename}", flush=True)
                            continue

                        print(f"        [{idx}/{len(photo_urls)}] Downloading: {filename}", flush=True)
                        self.download_file(photo_url, filepath)
                        album_photos_count += 1
                        self.total_photos_downloaded += 1

                    except Exception as e:
                        print(f"        ❌ Failed to download {photo_url}: {e}", flush=True)

                # Check if there's a next page in this album
                pagination = self.driver.find_elements(By.CSS_SELECTOR, "ul.pagination li a")
                next_page_num = page_num + 1
                next_page_link = None

                for link in pagination:
                    if link.text.strip() == str(next_page_num):
                        next_page_link = link
                        break

                if next_page_link:
                    print(f"      Navigating to page {next_page_num}...", flush=True)
                    next_page_link.click()
                    time.sleep(3)
                    page_num = next_page_num
                else:
                    print(f"      No more pages in album (reached page {page_num})", flush=True)
                    break

            self.total_albums_processed += 1
            print(f"  ✓ Album completed - Downloaded {album_photos_count} photos\n", flush=True)

        except Exception as e:
            print(f"  ❌ Album error: {e}", flush=True)
            import traceback
            traceback.print_exc()

    def download_file(self, url, filepath):
        """Download a file using the DownloadImage API"""
        try:
            # Get cookies from Selenium session
            selenium_cookies = self.driver.get_cookies()

            # Convert to requests format
            cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

            # Make POST request to DownloadImage API
            api_url = f"{self.base_url}/Home/DownloadImage"
            headers = {
                'Content-Type': 'application/json',
                'Referer': self.driver.current_url
            }
            payload = {
                'imageUrl': url
            }

            response = requests.post(api_url, json=payload, cookies=cookies, headers=headers, timeout=30)
            response.raise_for_status()

            # Save the downloaded file
            with open(filepath, 'wb') as f:
                f.write(response.content)

        except Exception as e:
            print(f"      Download error: {e}", flush=True)
            raise

    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.strip()
        return filename if filename else "unnamed"

    def get_filename_from_url(self, url):
        """Extract filename from URL"""
        filename = url.split('/')[-1].split('?')[0]
        if '.' not in filename:
            filename += '.jpg'
        return filename


if __name__ == "__main__":
    downloader = PhotoDownloader()
    downloader.run()


