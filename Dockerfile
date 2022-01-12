
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get upgrade
RUN pip install -r requirements.txt
COPY . /code/
