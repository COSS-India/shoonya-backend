FROM python:3.13

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt install libpq-dev

RUN pip install --upgrade pip
COPY ./deploy/requirements.txt /usr/src/backend/requirements.txt
RUN pip install --default-timeout=200 -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt_tab')"
