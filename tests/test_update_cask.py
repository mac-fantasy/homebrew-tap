import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("update_cask", ROOT / "scripts/update-cask.py")
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class UpdateCaskTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.cask = Path(directory.name) / "clipbar.rb"
        self.original = (
            'cask "clipbar" do\n'
            '  version "1.0.0"\n'
            f'  sha256 "{"0" * 64}"\n'
            '  app "ClipBar.app"\n'
            'end\n'
        )
        self.cask.write_text(self.original)
        self.archive = b"test release archive"
        self.sha256 = hashlib.sha256(self.archive).hexdigest()
        self.filename = "ClipBar-99.0.0-macOS-universal.zip"
        self.base_url = "https://github.com/lljxww/ClipBar/releases/download/v99.0.0/"
        self.checksums = f"{self.sha256}  {self.filename}\n".encode()
        self.release = {
            "tag_name": "v99.0.0",
            "draft": False,
            "prerelease": False,
            "assets": [
                {
                    "name": self.filename,
                    "digest": f"sha256:{self.sha256}",
                    "browser_download_url": self.base_url + self.filename,
                },
                {"name": "SHA256SUMS", "browser_download_url": self.base_url + "SHA256SUMS"},
            ],
        }

    def download(self, url, **kwargs):
        return {
            "https://api.github.com/repos/lljxww/ClipBar/releases/latest": json.dumps(self.release).encode(),
            self.base_url + self.filename: self.archive,
            self.base_url + "SHA256SUMS": self.checksums,
        }[url]

    def run_update(self):
        with patch.object(updater, "CASK", self.cask), patch.object(updater, "download", self.download):
            updater.main()

    def assert_rejected(self):
        with self.assertRaises(ValueError):
            self.run_update()
        self.assertEqual(self.cask.read_text(), self.original)

    def test_verified_release_updates_version_and_checksum_only(self):
        self.run_update()
        expected = self.original.replace('version "1.0.0"', 'version "99.0.0"')
        expected = expected.replace("0" * 64, self.sha256)
        self.assertEqual(self.cask.read_text(), expected)

    def test_archive_checksum_mismatch_leaves_cask_unchanged(self):
        self.archive = b"different archive"
        self.assert_rejected()

    def test_github_digest_mismatch_leaves_cask_unchanged(self):
        self.release["assets"][0]["digest"] = "sha256:" + "0" * 64
        self.assert_rejected()

    def test_missing_or_duplicate_manifest_checksum_leaves_cask_unchanged(self):
        for checksums in (b"", self.checksums * 2):
            with self.subTest(checksums=checksums):
                self.checksums = checksums
                self.assert_rejected()

    def test_prerelease_or_unexpected_download_url_leaves_cask_unchanged(self):
        self.release["prerelease"] = True
        self.assert_rejected()
        self.release["prerelease"] = False
        self.release["assets"][0]["browser_download_url"] = "https://example.com/ClipBar.zip"
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
