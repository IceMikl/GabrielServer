
FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
COPY src ./request_handler/src
COPY resources ./request_handler/resources

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "request_handler/src/main/app.py"]