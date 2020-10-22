#!/bin/bash

#This script is used to build and push a smaple docker image.
#The docker images contains a hello-world war file with tocat web-app server.

#Credentials for DockerHub account are on a seperate file.

#----------------dockerhub.conf tenplate-----------#
#export DOCKERHUB_USERNAME=<username>
#export DOCKERHUB_PASSWORD=<password>
#--------------------------------------------------#

source ./dockerhub.conf

readonly APP_NAME="ricknmorty"
readonly APP_VERSION="1.0.0"

docker build -t $APP_NAME:$APP_VERSION .
docker login --username $DOCKERHUB_USERNAME --password $DOCKERHUB_PASSWORD
docker tag $APP_NAME:$APP_VERSION netanelkoli/$APP_NAME:$APP_VERSION
docker push netanelkoli/$APP_NAME:$APP_VERSION
docker logout
