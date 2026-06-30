"""Tests for the backup_db management command and its Celery wrapper.

Covers the parts that don't need a real pg_dump binary or a live database:
engine dispatch, pruning, and the DB_BACKUP_ENABLED toggle on the task.
The actual pg_dump/sqlite3 calls are exercised manually against the
running container (see backup_db.py docstring) rather than here.
"""

import shutil
import tempfile
import time
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from app.tasks import backup_database

POSTGRES_DB_CONFIG = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "db",
        "PORT": "5432",
        "USER": "yamtrack",
        "PASSWORD": "secret",
        "NAME": "yamtrack",
        "OPTIONS": {},
    },
}


def _fake_pg_dump_success(cmd, **_kwargs):
    """Mimic pg_dump actually writing a file to the --file path."""
    file_path = Path(cmd[cmd.index("--file") + 1])
    file_path.write_bytes(b"fake-dump-bytes")
    return MagicMock(returncode=0, stderr="")


class BackupDbDispatchTests(TestCase):
    """Engine dispatch should reject anything that isn't pg/sqlite."""

    @override_settings(DATABASES={"default": {"ENGINE": "django.db.backends.mysql"}})
    def test_unsupported_engine_raises(self):
        with self.assertRaises(CommandError):
            call_command("backup_db", stdout=StringIO())


class BackupDbPostgresTests(TestCase):
    """Postgres path: pg_dump is invoked, failures surface as CommandError."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp_dir, ignore_errors=True)

    def test_pg_dump_failure_raises_and_cleans_up(self):
        with (
            override_settings(DATABASES=POSTGRES_DB_CONFIG, DB_BACKUP_DIR=self.tmp_dir),
            patch("app.management.commands.backup_db.subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(
                returncode=1,
                stderr="connection refused",
            )
            with self.assertRaises(CommandError):
                call_command("backup_db", stdout=StringIO())

        # the failed dump should not be left behind
        self.assertEqual(list(self.tmp_dir.glob("yamtrack_*")), [])

    def test_pg_dump_success_passes_expected_args(self):
        db_config = {
            "default": {**POSTGRES_DB_CONFIG["default"], "OPTIONS": {"sslmode": "require"}},
        }
        with (
            override_settings(DATABASES=db_config, DB_BACKUP_DIR=self.tmp_dir),
            patch("app.management.commands.backup_db.subprocess.run") as mock_run,
        ):
            mock_run.side_effect = _fake_pg_dump_success
            call_command("backup_db", stdout=StringIO())

        cmd = mock_run.call_args.args[0]
        kwargs = mock_run.call_args.kwargs
        self.assertEqual(cmd[0], "pg_dump")
        self.assertIn("yamtrack", cmd)
        self.assertEqual(kwargs["env"]["PGSSLMODE"], "require")
        self.assertEqual(kwargs["env"]["PGPASSWORD"], "secret")
        self.assertEqual(len(list(self.tmp_dir.glob("yamtrack_*.dump"))), 1)


class PruneOldBackupsTests(TestCase):
    """Pruning keeps the newest DB_BACKUP_RETENTION files, deletes the rest."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp_dir, ignore_errors=True)

    @override_settings(DB_BACKUP_RETENTION=2)
    def test_keeps_only_the_newest_n_backups(self):
        existing = []
        for i in range(4):
            path = self.tmp_dir / f"yamtrack_existing_{i}.dump"
            path.write_bytes(b"x")
            existing.append(path)
            time.sleep(0.01)  # ensure distinct mtimes, oldest first

        with (
            override_settings(DATABASES=POSTGRES_DB_CONFIG, DB_BACKUP_DIR=self.tmp_dir),
            patch("app.management.commands.backup_db.subprocess.run") as mock_run,
        ):
            mock_run.side_effect = _fake_pg_dump_success
            call_command("backup_db", stdout=StringIO())

        remaining = {p.name for p in self.tmp_dir.glob("yamtrack_*")}

        # retention=2, plus the fresh dump just created by this run = 3 total
        self.assertEqual(len(remaining), 3)
        self.assertNotIn(existing[0].name, remaining)  # oldest, pruned
        self.assertNotIn(existing[1].name, remaining)  # 2nd oldest, pruned
        self.assertIn(existing[2].name, remaining)  # kept
        self.assertIn(existing[3].name, remaining)  # kept


class BackupDatabaseTaskTests(TestCase):
    """The Celery wrapper should no-op when the feature is disabled."""

    @override_settings(DB_BACKUP_ENABLED=False)
    def test_noop_when_disabled(self):
        with patch("django.core.management.call_command") as mock_call_command:
            backup_database()
        mock_call_command.assert_not_called()

    @override_settings(DB_BACKUP_ENABLED=True)
    def test_calls_command_when_enabled(self):
        with patch("django.core.management.call_command") as mock_call_command:
            backup_database()
        mock_call_command.assert_called_once_with("backup_db")
