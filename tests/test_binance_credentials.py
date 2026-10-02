import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.server import binance_credentials


class BinanceCredentialsTests(unittest.TestCase):
    def make_repo(self, env_contents):
        temporary_directory = TemporaryDirectory()
        repo_root = Path(temporary_directory.name)
        (repo_root / ".gitignore").write_text(".env\n", encoding="utf-8")
        (repo_root / ".env").write_text(env_contents, encoding="utf-8")
        return temporary_directory, repo_root

    def test_complete_process_environment_pair_takes_precedence(self):
        temporary_directory, repo_root = self.make_repo(
            "BINANCE_WEB3_API_KEY=file-key\nBINANCE_WEB3_SECRET_KEY=file-secret\n"
        )
        self.addCleanup(temporary_directory.cleanup)

        with patch.dict(
            os.environ,
            {
                "BINANCE_WEB3_API_KEY": "env-key",
                "BINANCE_WEB3_SECRET_KEY": "env-secret",
            },
            clear=True,
        ):
            self.assertEqual(binance_credentials(repo_root), ("env-key", "env-secret"))

    def test_complete_ignored_file_pair_is_used_as_fallback(self):
        temporary_directory, repo_root = self.make_repo(
            "BINANCE_WEB3_API_KEY=file-key\nBINANCE_WEB3_SECRET_KEY='file-secret'\n"
        )
        self.addCleanup(temporary_directory.cleanup)

        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(binance_credentials(repo_root), ("file-key", "file-secret"))

    def test_incomplete_sources_are_not_combined(self):
        temporary_directory, repo_root = self.make_repo(
            "BINANCE_WEB3_SECRET_KEY=file-secret\n"
        )
        self.addCleanup(temporary_directory.cleanup)

        with patch.dict(
            os.environ,
            {"BINANCE_WEB3_API_KEY": "env-key"},
            clear=True,
        ):
            self.assertIsNone(binance_credentials(repo_root))


if __name__ == "__main__":
    unittest.main()
