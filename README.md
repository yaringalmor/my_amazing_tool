# my_amazing_tool
CLI tool for setting up web application with alongside databse to serve a certain message based on k8s cluster

## Requirements
- Spec (minimum): 4 cpu, 6 GB RAM 
- Python (Version 3.8 and later) - [Installation](https://www.python.org/downloads)
- Docker - [Installation](https://docs.docker.com/engine/install)
- Minikube - [Installation](https://minikube.sigs.k8s.io/docs/start)

- Python Packages <br />
  `pip install --no-cache-dir --upgrade -r cli/requirements.txt`

## Setup
1. Configure minikube to pull image from local Docker registry by executing the following command - <br />
Linux: <br />
`eval $(minikube docker-env)` <br />
Windows (PowerShell): <br />
`& minikube -p <profile> docker-env --shell powershell | Invoke-Expression`
2. Clone this repo to your workstation.


## Usage
`python3 cli/my_amazing_tool.py <content>`

For example: <br />
`python3 cli/my_amazing_tool.py "This tool is amazing!"`

## Planned for next releases
 - Set flag to install requirements.
 - Set python script as part of user PATH.
 - Configure service deployment based on Helm.
 - Exclude mongodb credentials from cli common.
 library, and use k8s secrets instead.
 - Support deployment for external k8s clusters.