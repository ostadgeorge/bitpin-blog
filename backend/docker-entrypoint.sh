#!/usr/bin/env bash

cd /app/src/ || exit
echo "Working directory is: $PWD"

echo "Waiting for database..."
while ! nc -z "${DB_HOST}" "${DB_PORT}"; do sleep 0.2; done
echo "Connected to database."

if ! python manage.py migrate --noinput; then
    echo "Migration failed." >&2
    exit 1
fi

if [[ $# -gt 0 ]]; then
    cd /app/ || exit
    INPUT=$*
    sh -c "$INPUT"
else
    mkdir -p /var/log/app
    touch /var/log/app/gunicorn.log
    touch /var/log/app/access.log

    tail -n 0 -f /var/log/app/*.log &

    python manage.py collectstatic --noinput

    echo "Starting Server..."
    python manage.py runserver 0.0.0.0:8000
fi
