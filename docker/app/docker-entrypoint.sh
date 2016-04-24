#!/bin/sh

MAX_ATTEMPTS=10
ATTEMPT=1
until /srv/configs/manage.py migrate || [ $ATTEMPT -eq $MAX_ATTEMPTS ]
do
    ATTEMPT=$((ATTEMPT + 1))
    sleep 1
done

/srv/configs/manage.py collectstatic --noinput

exec /usr/bin/uwsgi \
    --chdir /srv/configs \
    --die-on-term \
    --need-app \
    --env DJANGO_SETTINGS_MODULE=configs.settings \
    --enable-threads \
    --master \
    --processes 2 \
    --socket :8000 \
    --wsgi-file configs/wsgi.py \
    "$@"
