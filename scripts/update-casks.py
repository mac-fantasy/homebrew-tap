#!/usr/bin/env python3
"""Update casks from verified stable GitHub Releases listed in apps.json."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
STABLE_TAG = r"v?(?P<version>(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))"


def download(url, *, api=False):
    headers = {"User-Agent": "lljxww-Homebrew-Tap"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if token := os.environ.get("GH_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=60) as response:
        return response.read()


def prepare_update(token, settings, root):
    if not re.fullmatch(r"[a-z0-9][a-z0-9@+._-]*", token):
        raise ValueError(f"Invalid cask token: {token!r}")
    repository = settings["repository"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError(f"Invalid GitHub repository: {repository!r}")
    release = json.loads(
        download(f"https://api.github.com/repos/{repository}/releases/latest", api=True)
    )
    tag = release["tag_name"]
    match = re.fullmatch(settings.get("tag_pattern", STABLE_TAG), tag)
    if release["draft"] or release["prerelease"] or not match:
        raise ValueError(f"{token}: expected a stable version tag, got {tag!r}")
    version = match.group("version")
    if not re.fullmatch(r"[0-9][0-9A-Za-z.+_-]*", version):
        raise ValueError(f"{token}: invalid version: {version!r}")

    filename = settings["asset"].format(version=version, tag=tag)
    assets = {asset["name"]: asset for asset in release["assets"]}
    archive = assets[filename]
    base_url = f"https://github.com/{repository}/releases/download/{tag}/"
    checksum_name = settings.get("checksums")
    for name in (filename, checksum_name):
        if name is not None and assets[name]["browser_download_url"] != base_url + name:
            raise ValueError(f"{token}: unexpected download URL for {name}")

    expected_checksums = []
    if digest := archive.get("digest"):
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
            raise ValueError(f"{token}: unexpected GitHub asset digest")
        expected_checksums.append(digest.removeprefix("sha256:"))
    if checksum_name:
        lines = download(assets[checksum_name]["browser_download_url"]).decode().splitlines()
        matches = [
            match.group(1)
            for line in lines
            if (match := re.fullmatch(r"([0-9a-f]{64}) [ *]" + re.escape(filename), line))
        ]
        if len(matches) != 1:
            raise ValueError(f"{token}: expected exactly one checksum for {filename}")
        expected_checksums.extend(matches)
    if not expected_checksums:
        raise ValueError(f"{token}: release needs a GitHub SHA-256 digest or checksum manifest")

    sha256 = hashlib.sha256(download(archive["browser_download_url"])).hexdigest()
    if any(checksum != sha256 for checksum in expected_checksums):
        raise ValueError(f"{token}: archive and published checksums do not match")

    cask = root / "Casks" / f"{token}.rb"
    content = cask.read_text()
    for field, value in (("version", version), ("sha256", sha256)):
        content, count = re.subn(
            rf'^  {field} "[^"]+"$', lambda _: f'  {field} "{value}"', content, flags=re.MULTILINE
        )
        if count != 1:
            raise ValueError(f"{token}: expected exactly one top-level {field} stanza")
    return cask, content, version, sha256


def update_casks(apps, tokens, root):
    unknown = set(tokens) - set(apps)
    if unknown:
        raise ValueError(f"Unknown casks: {', '.join(sorted(unknown))}")
    # Validate every selected release before writing any cask.
    updates = [prepare_update(token, apps[token], root) for token in tokens]
    for cask, content, version, sha256 in updates:
        if cask.read_text() != content:
            cask.write_text(content)
        print(f"Verified {cask.stem} {version}: {sha256}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("casks", nargs="*", help="Cask tokens; omit to update all apps")
    args = parser.parse_args()
    apps = json.loads((ROOT / "apps.json").read_text())
    update_casks(apps, args.casks or list(apps), ROOT)


if __name__ == "__main__":
    main()
