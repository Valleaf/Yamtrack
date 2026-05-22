#!/bin/sh
# Run inside the container: docker compose exec yamtrack sh /yamtrack/check_migrations.sh
python manage.py showmigrations app | tail -20
