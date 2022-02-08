
FROM python:3.8-slim-buster

COPY requirements.txt ./db_manager/requirements.txt
COPY src ./db_manager/src
COPY resources ./db_manager/resources

RUN pip3 install -r requirements.txt

EXPOSE 9091

CMD ["python3", "-u", "db_manager/src/main/app.py"]