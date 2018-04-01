cd m2ds/
docker run --rm -v "$PWD":/home -w /home m2ds_app python manage.py makemigrations
docker run --rm -v "$PWD":/home -w /home m2ds_app python manage.py migrate
