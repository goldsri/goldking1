#!/usr/bin/env python3
"""Fetch an authorized public M3U source and save a refreshed playlist."""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from pathlib import Path


SOURCE_URL = "https://zeotvyash.streamxlivenow.workers.dev/"
OUTPUT_FILE = Path("zeotvyash.m3u")



def main() -> None:
    req = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0 (compatible; PlaylistUpdater/1.0)"})
    try:
        with urlopen(req, timeout=45) as response:
            content = response.read()
            content_type = response.headers.get("Content-Type", "")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise SystemExit(f"Source download failed: {exc}")

    text = content.decode("utf-8-sig", errors="replace").strip()
    if not text or "#EXTM3U" not in text[:500]:
        raise SystemExit(
            f"Response is not a recognizable M3U (Content-Type: {content_type}). "
            "The source may redirect, require authorization, or return a web page."
        )
    OUTPUT_FILE.write_text(text + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_FILE} ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
