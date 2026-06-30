"""Management command: create a compressed database backup and prune old ones.

Postgres: shells out to `pg_dump` in custom format (-Fc), which is already
compressed and lets you restore selectively with `pg_restore` later.
SQLite: uses the stdlib sqlite3 backup API (safe against a live db, unlike
a plain file copy), then gzips the result.

Old backups beyond settings.DB_BACKUP_RETENTION are deleted, oldest first.

Usage:
    docker compose exec yamtrack python manage.py backup_db
"""

import gzip
import logging
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Create a backup of the configured database and prune old backups."""

    help = "Create a compressed backup of the database and prune old backups."

    def handle(self, *args, **options):  # noqa: ARG002
        db = settings.DATABASES["default"]
        backup_dir = Path(settings.DB_BACKUP_DIR)
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(tz=settings.TZ).strftime("%Y%m%d_%H%M%S")

        if db["ENGINE"] == "django.db.backends.postgresql":
            backup_path = backup_dir / f"yamtrack_{timestamp}.dump"
            self._backup_postgres(db, backup_path)
        elif db["ENGINE"] == "django.db.backends.sqlite3":
            backup_path = backup_dir / f"yamtrack_{timestamp}.sqlite3.gz"
            self._backup_sqlite(db, backup_path)
        else:
            msg = f"Unsupported database engine: {db['ENGINE']}"
            raise CommandError(msg)

        self.stdout.write(self.style.SUCCESS(f"Backup written: {backup_path}"))
        logger.info("Database backup written: %s", backup_path)

        self._prune_old_backups(backup_dir)

    def _backup_postgres(self, db, backup_path):
        env = os.environ.copy()
        if db.get("PASSWORD"):
            env["PGPASSWORD"] = db["PASSWORD"]

        sslmode = db.get("OPTIONS", {}).get("sslmode")
        if sslmode:
            env["PGSSLMODE"] = sslmode

        cmd = [
            "pg_dump",
            "--host", db["HOST"],
            "--port", str(db["PORT"]),
            "--username", db["USER"],
            "--format", "custom",
            "--file", str(backup_path),
            db["NAME"],
        ]

        result = subprocess.run(  # noqa: S603, S607
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            backup_path.unlink(missing_ok=True)
            msg = f"pg_dump failed: {result.stderr.strip()}"
            raise CommandError(msg)

    def _backup_sqlite(self, db, backup_path):
        tmp_path = backup_path.with_suffix("")  # strip the .gz suffix

        source_conn = sqlite3.connect(db["NAME"])
        dest_conn = sqlite3.connect(tmp_path)
        try:
            source_conn.backup(dest_conn)
        finally:
            dest_conn.close()
            source_conn.close()

        with Path(tmp_path).open("rb") as f_in, gzip.open(backup_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        Path(tmp_path).unlink()

    def _prune_old_backups(self, backup_dir):
        backups = sorted(
            backup_dir.glob("yamtrack_*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for old_backup in backups[settings.DB_BACKUP_RETENTION :]:
            old_backup.unlink()
            logger.info("Pruned old backup: %s", old_backup)
            self.stdout.write(f"Pruned old backup: {old_backup.name}")
