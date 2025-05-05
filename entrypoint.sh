#!/bin/sh
echo "Running entry point..."

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Running flush..."
python -m fullcoster.manage flush --no-input
echo "Running migrate..."
python -m fullcoster.manage migrate

exec "$@"
