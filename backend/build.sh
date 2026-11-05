#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py shell -c "from django.db import connection; from django.db.migrations.recorder import MigrationRecorder; MigrationRecorder(connection).record_applied('mobility', '0002_websitesection_alter_sitecontent_key')"

python manage.py migrate