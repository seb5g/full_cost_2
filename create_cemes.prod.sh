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
python /home/fullcost/src/fullcoster/manage.py makemigrations lab

echo "Running migrate on lab..."
python /home/fullcost/src/fullcoster/manage.py migrate lab

echo "populate..."
python /home/fullcost/src/fullcoster/lab/management/manage_fullcost.py populate all_but_experiments

echo "Make migrations..."
python /home/fullcost/src/fullcoster/manage.py makemigrations

echo "migrate..."
python /home/fullcost/src/fullcoster/manage.py migrate

echo "populate..."
python /home/fullcost/src/fullcoster/lab/management/manage_fullcost.py populate experiments

echo "creating superuser..."
python /home/fullcost/src/fullcoster/manage.py createsuperuser_if_none_exists --user weber --password changeme

echo "collecting static files..."
python /home/fullcost/src/fullcoster/manage.py collectstatic --no-input --clear