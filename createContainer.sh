#!/bin/bash
sudo docker build -t multiple_containers_server_image .
sudo docker container stop icemikl/multiple_containers_server
sudo docker rm icemikl/multiple_containers_server
sudo docker create --name icemikl/multiple_containers_server --publish 8080:8080 multiple_containers_server_image
sudo docker start icemikl/multiple_containers_server -a
