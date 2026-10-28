import hashlib
from http.client import IncompleteRead
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("update_casks", ROOT / "scripts/update-casks.py")
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class DownloadTests(unittest.TestCase):
    def test_partial_download_is_retried_from_the_start(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.side_effect = [IncompleteRead(b"partial", 4), b"complete"]
        with patch.object(updater, "urlopen", return_value=response) as urlopen, patch.object(updater.time, "sleep"):
            self.assertEqual(updater.download("https://example.com/app.zip"), b"complete")
            self.assertEqual(urlopen.call_count, 2)

    def test_partial_download_retries_are_bounded(self):
        with patch.object(updater, "urlopen", side_effect=IncompleteRead(b"partial", 4)) as urlopen, patch.object(updater.time, "sleep"):
            with self.assertRaises(IncompleteRead):
                updater.download("https://example.com/app.zip")
            self.assertEqual(urlopen.call_count, 3)

    def test_missing_asset_is_not_retried(self):
        error = HTTPError("https://example.com/missing.zip", 404, "Not found", None, None)
        with patch.object(updater, "urlopen", side_effect=error) as urlopen, patch.object(updater.time, "sleep") as sleep:
            with self.assertRaises(HTTPError):
                updater.download("https://example.com/missing.zip")
            urlopen.assert_called_once()
            sleep.assert_not_called()


class UpdateCaskTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "Casks").mkdir()
        self.cask = self.root / "Casks/clipbar.rb"
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
        self.checksum_filename = "SHA256SUMS"
        self.settings = {
            "repository": "lljxww/ClipBar",
            "asset": "ClipBar-{version}-macOS-universal.zip",
            "checksums": "SHA256SUMS",
        }
        self.apps = {"clipbar": self.settings}
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
            self.base_url + self.checksum_filename: self.checksums,
        }[url]

    def run_update(self, tokens=None):
        with patch.object(updater, "download", self.download):
            updater.update_casks(self.apps, tokens or list(self.apps), self.root)

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

    def test_manifest_is_optional_when_github_digest_is_present(self):
        self.settings.pop("checksums")
        self.run_update()
        self.assertIn('version "99.0.0"', self.cask.read_text())

    def test_manifest_can_verify_an_asset_without_github_digest(self):
        self.release["assets"][0].pop("digest")
        self.run_update()
        self.assertIn(self.sha256, self.cask.read_text())

    def test_no_published_checksum_is_rejected(self):
        self.settings.pop("checksums")
        self.release["assets"][0].pop("digest")
        self.assert_rejected()

    def test_multiple_casks_are_updated_independently(self):
        second = self.root / "Casks/second-app.rb"
        second.write_text(self.original.replace('cask "clipbar"', 'cask "second-app"'))
        self.apps["second-app"] = self.settings.copy()
        self.run_update()
        self.assertIn('version "99.0.0"', self.cask.read_text())
        self.assertIn('version "99.0.0"', second.read_text())
        self.assertIn('cask "second-app"', second.read_text())

    def test_one_invalid_cask_prevents_all_writes(self):
        second = self.root / "Casks/second-app.rb"
        invalid = 'cask "second-app" do\n  app "Second.app"\nend\n'
        second.write_text(invalid)
        self.apps["second-app"] = self.settings.copy()
        self.assert_rejected()
        self.assertEqual(second.read_text(), invalid)

    def test_selecting_one_cask_leaves_other_casks_unchanged(self):
        second = self.root / "Casks/second-app.rb"
        second.write_text(self.original)
        self.apps["second-app"] = self.settings.copy()
        self.run_update(["clipbar"])
        self.assertEqual(second.read_text(), self.original)

    def test_unknown_cask_is_rejected_before_downloading(self):
        with patch.object(updater, "download") as download:
            with self.assertRaises(ValueError):
                updater.update_casks(self.apps, ["missing"], self.root)
            download.assert_not_called()
        self.assertEqual(self.cask.read_text(), self.original)

    def test_invalid_stable_tags_are_rejected(self):
        for tag in ("v01.2.3", "v1.2.3-beta.1", "v1.2", "../1.2.3"):
            with self.subTest(tag=tag):
                self.release["tag_name"] = tag
                self.assert_rejected()

    def test_checksum_filename_can_include_the_release_tag(self):
        self.settings["checksums"] = "SHA256SUMS-{tag}"
        self.checksum_filename = "SHA256SUMS-v99.0.0"
        self.release["assets"][1]["name"] = self.checksum_filename
        self.release["assets"][1]["browser_download_url"] = self.base_url + self.checksum_filename
        self.run_update()
        self.assertIn(self.sha256, self.cask.read_text())

    def test_two_component_tag_can_use_three_component_bundle_version(self):
        self.settings["tag_pattern"] = r"v(?P<version>[0-9]+\.[0-9]+)"
        self.settings["version_components"] = 3
        self.settings["url_from_asset"] = True
        self.cask.write_text(self.original.replace('  app "ClipBar.app"', '  url "https://example.com/old.zip"\n  app "ClipBar.app"'))
        self.release["tag_name"] = "v99.0"
        self.base_url = "https://github.com/lljxww/ClipBar/releases/download/v99.0/"
        for asset in self.release["assets"]:
            asset["browser_download_url"] = self.base_url + asset["name"]
        self.run_update()
        self.assertIn('version "99.0.0"', self.cask.read_text())
        self.assertIn(f'url "{self.base_url}{self.filename}"', self.cask.read_text())

    def test_invalid_version_component_count_is_rejected_without_writing(self):
        for components in (0, 2, 5, "3", True):
            with self.subTest(components=components):
                self.settings["version_components"] = components
                self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
