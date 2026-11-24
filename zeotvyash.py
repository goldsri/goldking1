#!/usrusr/bin/env python3
"""Fetch and validate the public M3U source, then save it as zeotvyash.m3u."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import time

SOURCE_URL = "https://zeotvyash.streamxlivenow.workers.dev/"
OUTPUT_FILE = Path("zeotvyash.m3u")


def download():
    last_error = None
    for attempt in range(1, 4):
        req = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0 (compatible; PlaylistUpdater/1.0)", "Accept": "*/*"})
        try:
            with urlopen(req, timeout=60) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "unknown")
                final_url = response.geturl()
            text = data.decode("utf-8-sig", errors="replace").strip()
            # Validate the body itself; Content-Type can be inaccurate for M3U endpoints.
            first_nonempty = next((line.strip() for line in text.splitlines() if line.strip()), "")
            if first_nonempty.startswith("#EXTM3U"):
                return text, content_type, final_url
            last_error = f"Body is not M3U. Content-Type={content_type}; final URL={final_url}; preview={text[:180]!r}"
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = str(exc)
        if attempt < 3:
            time.sleep(5 * attempt)
    raise SystemExit(f"Download/validation failed after 3 attempts: {last_error}")


def main():
    text, content_type, final_url = download()
    OUTPUT_FILE.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"Saved {OUTPUT_FILE}: {len(text.splitlines())} lines; Content-Type={content_type}; URL={final_url}")


if __name__ == "__main__":
    main()
