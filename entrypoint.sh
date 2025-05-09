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

#echo "Make flush..."
#python /usr/src/fullcost/src/fullcoster/manage.py flush --no-input
#
#echo "Running migrate..."
#python /usr/src/fullcost/src/fullcoster/manage.py migrate
#
#echo "Make migrations..."
#python /usr/src/fullcost/src/fullcoster/manage.py makemigrations
#
#echo "migrate..."
#python /usr/src/fullcost/src/fullcoster/manage.py migrate
#
#echo "populate..."
#python /usr/src/fullcost/src/fullcoster/constants/manage_fullcost.py populate all

cd /usr/src/fullcost/src/fullcoster/

exec "$@"
