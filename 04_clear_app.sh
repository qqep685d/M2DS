cd m2ds/
docker run --rm -v "$PWD":/home -w /home m2ds rm -rf db.sqlite3
docker run --rm -v "$PWD":/home -w /home m2ds rm -rf mm/migrations/*
docker run --rm -v "$PWD":/home -w /home m2ds rm -rf mm/static/download_files/*
docker run --rm -v "$PWD":/home -w /home m2ds rm -rf mm/static/upload_files/*
