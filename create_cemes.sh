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


echo "Make migration on lab..."
python /usr/src/fullcost/src/fullcoster/manage.py makemigrations lab

echo "Running migrate on lab..."
python /usr/src/fullcost/src/fullcoster/manage.py migrate lab

echo "populate..."
python /usr/src/fullcost/src/fullcoster/lab/management/manage_fullcost.py populate all_but_experiments

echo "Make migrations..."
python /usr/src/fullcost/src/fullcoster/manage.py makemigrations

echo "migrate..."
python /usr/src/fullcost/src/fullcoster/manage.py migrate

echo "populate..."
python /usr/src/fullcost/src/fullcoster/lab/management/manage_fullcost.py populate experiments

echo "creating superuser..."
python /usr/src/fullcost/src/fullcoster/manage.py createsuperuser_if_none_exists --user weber --password changeme
