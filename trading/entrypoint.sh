#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#    echo $SQL_HOST $SQL_PORT
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi

# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear
#export DOCKER_KAFKA_HOST=$(ipconfig getifaddr en0)
export DOCKER_KAFKA_HOST=10.1.0.111

exec "$@"
