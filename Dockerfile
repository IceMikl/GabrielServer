
FROM python:3.8-slim-buster

#WORKDIR /src/main

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY src src

#CMD ["ls", "src/main/"]
CMD ["python3", "src/main/app.py"]