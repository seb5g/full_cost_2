#!/bin/sh
echo "Setting up CEMES activities..."

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Populate databases..."
python /usr/src/fullcost/src/fullcoster/constants/manage_fullcost.py populate all

echo "start server"
python /usr/src/fullcost/src/fullcoster/manage.py runserver 0.0.0.0:8000



