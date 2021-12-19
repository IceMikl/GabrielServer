
FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
#RUN pip3 install psycor

COPY src src
COPY src/main/data_obtainer/resources resources

CMD ["python3", "src/main/app.py"]