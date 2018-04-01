cd m2ds/
docker run --rm -v "$PWD":/home -w /home m2ds rm -f db.sqlite3
docker run --rm -v "$PWD":/home -w /home m2ds rm -f mm/static/downloaded_files/*
docker run --rm -v "$PWD":/home -w /home m2ds rm -f mm/static/uploaded_files/*
