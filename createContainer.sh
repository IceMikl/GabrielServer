#!/bin/bash
sudo docker build -t multiple_containers_image .
sudo docker container stop multiple_containers
sudo docker rm multiple_containers
sudo docker create --name multiple_containers --publish 8080:8080 multiple_containers_image
sudo docker start multiple_containers -a