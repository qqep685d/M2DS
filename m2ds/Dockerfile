FROM python:3.4

LABEL maintainer "A. Ohta"

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends sqlite3

WORKDIR /home

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
