#!/bin/bash

VERSION="1.0"

docker rm rpa_robot_api
docker rmi rpa_robot/api:$VERSION


cp rpa_robot/install/Dockerfile Dockerfile
cp rpa_robot/install/requirements.txt requirements.txt
docker build -t rpa_robot/api:$VERSION .

rm Dockerfile
rm requirements.txt

#completo
#docker run --name rpa_robot_api -d --network host -w /usr/workspace -v $(pwd):/usr/workspace -p 8080:5000 rpa_robot/api:latest

#sin el -d
docker run --name rpa_robot_api -w /usr/workspace -v $(pwd):/usr/workspace -p 0.0.0.0:8090:8090 rpa_robot/api:$VERSION
