
FROM python:3.8-slim-buster

COPY ./request_handler/requirements.txt requirements.txt
COPY ./request_handler/src src
COPY ./request_handler/resources resources

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "request_handler/src/main/app.py"]