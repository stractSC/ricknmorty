### Features

- Python script to server as webapp, to fetch json file, from rickandmortyapi.com , parse it and save it as .csv file.
- Included a Flask webapp, sevrers on all interfaces on port 500, to fetch the .csv results as json response.
- Helm chart, including deployment.yaml, service.yaml, ingress.yaml
- Instructions to deploy on a local Minikube cluster.

# Rick and Morty REST API
![](https://medias.timeout.co.il/www/uploads/2017/08/rick-and-mortyT-1140x641.jpg)

**Table of Contents**

# Python App
Python webapp to parse a json respinse from rickandmortyapi.com and parse it to a csv file.
Here I used pandas to parse from json to csv and from csv to json.
## RIck and Morty API
API DOC can be found here:
https://rickandmortyapi.com/documentation/#introduction
## Main functions
### main()
Main function of the app. Runs before staring the webapp server.
Its role is to fetch a response from ```url = "https://rickandmortyapi.com/api/character/?Species=Human&status=alive&origin=earth"``` , validate its a valid json , and save it to local storage as a csv. In case any of the functions fails or gets an exception, the app with exit with ```sys.exit(1)``` exit code 1.
```
def main():
    try:
        response = download_json(url)
        validate_json(response)
        convert_json_to_csv(response)
    except ValueError as e:
        print("Couldn't fetch a valid json response and convert is to CSV. Exiting...")
        sys.exit(1)
```
### app.run()
Main loop of the wepapp server. It serves on port 5000, for all network interfaces.
## API Calls
### /healthcheck
Returns ```200``` http response with the body `Healthy!`
### /get_results
Returns a valid json response, after it parses the local .csv file to json using pandas.
# Dockerizig Python App
## Build
Includes a `build.sh` bash script. Please run `chmod u+x build.sh` for later use.
### Prerequisite
Create a dockerhub.conf file in the same directory. build.sh script is using it to have proper credentials to login to your dockerhub account. Structure of this file:
```
#----------------dockerhub.conf template-----------#
export DOCKERHUB_USERNAME=<username>
export DOCKERHUB_PASSWORD=<password>
#--------------------------------------------------#
```
In addition, the relevant repo should exist in your https://hub.docker.com/ account.
### Building
After configurating dockerhub.conf file,  you can run `./build.sh`. This script will:
- Docker build the python app, to create a new docker image using the `Dockerfile` in the repo.
- Install all pip packages.
- Expose port 5000.
- Login to the configured dockerhub account.
- Tag the created image.
- Push the image to dockerhub repo.
- Logout from dockerhub.

# Kubernetes (Minikube)
![](https://kubernetes.io/images/favicon.png)

## Content
This repo includes:
- Helm chart in order to deploy the image into a k8s cluster.
- For more info about helm or kubernetes please visit: https://helm.sh/, https://kubernetes.io/.

## Prerequisite (Minikube)
### Install Minikube cluster on local station
Follow: https://github.com/kubernetes/minikube
### Helm3
Follow: https://helm.sh/docs/intro/install/
### kubectl
Follow: https://kubernetes.io/docs/tasks/tools/install-kubectl/
## How to deploy
Follow instructions in :
```
#Start and setup minikube env
minikube start
minikube addons enable ingress
cd helm/
##### -> Please edit values.yaml file as necessary.
# Install helm chart - deployment, service and ingress reosurces.
helm upgrade --install ricknmorty helm/ -f helm/values.yaml
# View deployed service , ip-address and port
minikube service list
minikube service ricknmorty --url
# Navigate to service to validate app is alive
curl $(minikube service ricknmorty --url)/healthcheck
# Navigate to service to get json results
curl $(minikube service ricknmorty --url)/get_results
```

### End
