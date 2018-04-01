cd m2ds/
docker run --rm -v "$PWD":/home -w /home -p 8000:8000 m2ds_app \
rm -f db.sqlite3 \
&& rm -f mm/static/downloaded_files/* \
&& rm -f mm/static/uploaded_files/*
