FROM python:3.8

RUN apt-get update && apt-get install -y python3-pip

COPY . /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

CMD python3 main.py