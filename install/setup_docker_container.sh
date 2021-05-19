#!/bin/bash

VERSION="1.0"

docker rm fusap_rpa_test_fwk_api
docker rmi fusap_rpa_test_fwk/api:$VERSION


cp fusap_rpa_test_fwk/install/Dockerfile Dockerfile
cp fusap_rpa_test_fwk/install/requirements.txt requirements.txt
docker build -t fusap_rpa_test_fwk/api:$VERSION .

rm Dockerfile
rm requirements.txt

#completo
#docker run --name fusap_rpa_test_fwk_api -d --network host -w /usr/workspace -v $(pwd):/usr/workspace -p 8080:5000 fusap_rpa_test_fwk/api:latest

#sin el -d
docker run --name fusap_rpa_test_fwk_api -w /usr/workspace -v $(pwd):/usr/workspace -p 0.0.0.0:8090:8090 fusap_rpa_test_fwk/api:$VERSION
