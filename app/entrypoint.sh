#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate admin
python manage.py migrate
python manage.py collectstatic -c --no-input

# python manage.py import_file incipit -f input_files/incipits.xls
# python manage.py import_file explicit -f input_files/reverse_explicits.xls
# python manage.py import_file title -f input_files/titles_rubrics_and_colophons.xls
# python manage.py import_file subject -f input_files/general_index.xls

exec "$@"
