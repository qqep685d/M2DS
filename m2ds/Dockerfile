FROM python:3.6.5-slim

LABEL maintainer "A. Ohta"

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends sqlite3 \
    && apt-get clean

WORKDIR /home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
