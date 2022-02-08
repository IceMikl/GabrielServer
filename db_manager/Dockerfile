
FROM python:3.8-slim-buster

COPY ./db_manager/requirements.txt requirements.txt
COPY ./db_manager/src src
COPY ./db_manager/resources resources

RUN pip3 install -r requirements.txt

EXPOSE 9091

CMD ["python3", "-u", "db_manager/src/main/app.py"]