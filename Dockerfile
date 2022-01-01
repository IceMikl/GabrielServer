
FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY src ./src
COPY resources ./resources

CMD ["python3", "src/main/app.py"]