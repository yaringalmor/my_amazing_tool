# my_amazing_tool
CLI tool for setting up web application with alongside databse to serve a certain message based on k8s cluster

## Requirements
- Python (Version 3.8 and later) - [Installation](https://www.python.org/downloads)
- Docker - [Installation](https://docs.docker.com/engine/install)
- Minikube - [Installation](https://minikube.sigs.k8s.io/docs/start)

- Python Packages <br />
  `pip install --no-cache-dir --upgrade -r cli/requirements.txt`

## Auto Configure
Currently support Ubuntu distributions only.
For IOS or Windows, please follow setup instructions.

## Setup
1. Initiate Minikube cluster <br />
  You may refer to following link to set it locally - [minikube setup](https://minikube.sigs.k8s.io/docs/start/)
2. Configure minikube to pull image from local Docker registry by executing the following command - <br />
`eval $(minikube docker-env)`
3. Clone this repo to your workstation.
4. Build web app docker image within web-app dir. <br />
`docker build -t my_amazing_tool/web-app .`
5. Setup mongodb pod by apply it to minikube cluster. <br />
`kubectl apply -f mongodb`
6. Setup web application pod by apply it to minikube cluster. <br />
`kubectl apply -f web-app`
7. Browse to web app endpoint and you're all done! <br />
`minikube service --url web-app`

## Usage
`python3 cli/my_amazing_tool.py <content>`

For example: <br />
`python3 cli/my_amazing_tool.py "This tool is amazing!"`

## Documentation
TODO

## Tips
- Setting minikube as a service

## Planned for next releases
 - Installing requirements and configure local env.
 - Set python script as part of user PATH