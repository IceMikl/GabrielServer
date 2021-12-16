#!/bin/bash
sudo docker build -t twilio_server_image .
sudo docker container stop twilio_server_container
sudo docker rm twilio_server_container
sudo docker create --name twilio_server_container --publish 8888:5000 twilio_server_image
sudo docker start twilio_server_container -a