#!/bin/sh

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input


# Create a Django superuser non-interactively
echo "Creating Django superuser..."
python manage.py createsuperuser --noinput --username=$DJANGO_SUPERUSER_USERNAME --email=$DJANGO_SUPERUSER_EMAIL

exec "$@"
