
FROM python:3.8-slim-buster

WORKDIR /request_handler

COPY requirements.txt request_handler/requirements.txt
COPY src/ request_handler/src/
COPY resources/ request_handler/resources/

RUN pip3 install -r request_handler/requirements.txt

CMD ["python3", "-u", "request_handler/src/main/app.py"]