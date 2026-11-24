#!/usr/bin/env python3
"""Refresh an authorized, non-DRM M3U playlist from a source URL."""
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen



SOURCE_URL = os.environ.get("SOURCE_M3U_URL", "").strip()
OUTPUT_FILE = Path("playlist.m3u")


def main() -> int:
    if not SOURCE_URL:
        print("Set SOURCE_M3U_URL in GitHub Actions secrets before running.")
        return 2

    req = Request(SOURCE_URL, headers={"User-Agent": "M3U-Playlist-Updater/1.0"})
    try:
        with urlopen(req, timeout=30) as response:
            content = response.read()
    except Exception as exc:
        print(f"Download failed: {exc}")
        return 1


    text = content.decode("utf-8-sig", errors="replace")
    if not text.lstrip().startswith("#EXTM3U"):
        print("Downloaded file is not a valid M3U (missing #EXTM3U header).")
        return 1
    if len(text.strip()) < 20:
        print("Playlist appears empty or too short; leaving previous file unchanged.")
        return 1


    OUTPUT_FILE.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_FILE} ({len(text.splitlines())} lines)")
    return 0



if __name__ == "__main__":
    sys.exit(main())
