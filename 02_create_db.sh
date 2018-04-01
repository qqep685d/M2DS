cd m2ds/
docker run --rm -v "$PWD":/home -w /home -p 8000:8000 m2ds_app \
python manage.py makemigrations && python manage.py migrate
