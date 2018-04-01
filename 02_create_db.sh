cd m2ds/
docker run --rm -v "$PWD":/home -w /home m2ds python manage.py makemigrations
docker run --rm -v "$PWD":/home -w /home m2ds python manage.py migrate
