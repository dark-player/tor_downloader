#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

DOWNLOAD_DIR = os.path.expanduser("~/Desktop/tor_downloads")

def check_program(program):
    return shutil.which(program) is not None

def install_requirements():
    print("\nChecking requirements...\n")

    required = ["yt-dlp", "torsocks", "ffmpeg"]

    missing = [p for p in required if not check_program(p)]

    if not missing:
        print("All requirements already installed.\n")
        return

    print("Missing packages:", ", ".join(missing))
    print("\nInstalling automatically...\n")

    try:
        subprocess.run(
            ["sudo", "apt", "update"],
            check=True
        )

        subprocess.run(
            ["sudo", "apt", "install", "-y"] + missing + ["tor"],
            check=True
        )

        print("\nRequirements installed successfully.\n")

    except subprocess.CalledProcessError:
        print("\nFailed to install requirements.")
        sys.exit(1)

def start_tor():
    print("Starting Tor service...\n")

    try:
        subprocess.run(
            ["sudo", "systemctl", "start", "tor"],
            check=True
        )
        print("Tor service started.\n")

    except subprocess.CalledProcessError:
        print("Could not start Tor service.")
        sys.exit(1)

def download_video():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    while True:

        print("=" * 50)
        print(" TOR VIDEO DOWNLOADER ")
        print("=" * 50)

        url = input("Enter TOR/onion video URL: ").strip()

        if not url:
            print("No URL entered.")
            return

        output_template = os.path.join(
            DOWNLOAD_DIR,
            "%(title)s.%(ext)s"
        )

        cmd = [
            "torsocks",
            "yt-dlp",
            "-f", "best",
            "-o", output_template,
            url
        ]

        print("\nDownloading video...\n")

        try:
            subprocess.run(cmd, check=True)

            print("\nDownload completed.")
            print(f"Saved in: {DOWNLOAD_DIR}")

        except subprocess.CalledProcessError:
            print("\nDownload failed.")
            
        choice = input("\nDo you want to download another video? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting.")
        break

if __name__ == "__main__":
    install_requirements()
    start_tor()
    download_video()
