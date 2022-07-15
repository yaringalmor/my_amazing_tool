# my_amazing_tool
CLI tool for setting up web application with alongside databse to serve a certain message based on k8s cluster

#### Setup
1. Running Minikube cluster <br />
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
`minikube service --url web-nodeport-svc`

