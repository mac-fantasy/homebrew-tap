#!/usr/bin/env python3
"""Update the cask from the latest stable upstream release after verifying it."""

import hashlib
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen


REPOSITORY = "lljxww/ClipBar"
CASK = Path(__file__).resolve().parents[1] / "Casks" / "clipbar.rb"


def download(url, *, api=False):
    headers = {"User-Agent": "ClipBar-Homebrew-Tap"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if token := os.environ.get("GH_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=60) as response:
        return response.read()


def main():
    release = json.loads(
        download(f"https://api.github.com/repos/{REPOSITORY}/releases/latest", api=True)
    )
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"] or not re.fullmatch(
        r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", tag
    ):
        raise ValueError(f"Expected a stable version tag, got {tag!r}")

    version = tag[1:]
    filename = f"ClipBar-{version}-macOS-universal.zip"
    assets = {asset["name"]: asset for asset in release["assets"]}
    archive = assets[filename]
    checksums = assets["SHA256SUMS"]
    base_url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/"
    for name in (filename, "SHA256SUMS"):
        if assets[name]["browser_download_url"] != base_url + name:
            raise ValueError(f"Unexpected download URL for {name}")

    checksum_lines = download(checksums["browser_download_url"]).decode().splitlines()
    matches = [
        match.group(1)
        for line in checksum_lines
        if (match := re.fullmatch(r"([0-9a-f]{64})  " + re.escape(filename), line))
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one checksum for {filename}")
    sha256 = hashlib.sha256(download(archive["browser_download_url"])).hexdigest()
    if sha256 != matches[0] or archive.get("digest") != f"sha256:{sha256}":
        raise ValueError("Archive, SHA256SUMS and GitHub asset digest do not match")

    content = CASK.read_text()
    for field, value in (("version", version), ("sha256", sha256)):
        content, count = re.subn(
            rf'^  {field} "[^"]+"$', f'  {field} "{value}"', content, flags=re.MULTILINE
        )
        if count != 1:
            raise ValueError(f"Expected exactly one {field} stanza")
    CASK.write_text(content)
    print(f"Verified ClipBar {version}: {sha256}")


if __name__ == "__main__":
    main()
