cd m2ds/
# delete db.sqlite3
# delete files in mm/migrations/
# delete files in mm/static/download_files/
# delete files in mm/static/upload_files/
docker run --rm -v "$PWD":/home -w /home m2ds \
    rm -rf db.sqlite3 \
        mm/__pycache__ \
        mm/migrations/* \
        mm/static/download_files/* \
        mm/static/upload_files/*
# copy mm/__init__.py to mm/migrations/
docker run --rm -v "$PWD":/home -w /home m2ds cp mm/__init__.py mm/migrations/
