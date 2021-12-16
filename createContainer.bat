
CALL docker build -t server_image .
CALL docker container stop server_container
CALL docker rm server_container
CALL docker create --name server_container --publish 8080:8080 server_image
CALL docker start server_container -a