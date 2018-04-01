FROM python:3.6.5-alpine3.7

LABEL maintainer "A. Ohta"

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk --no-cache add cmake gcc g++ gfortran sqlite

WORKDIR /home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python manage.py makemigrations \
    && python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
