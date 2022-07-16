import docker
import kubernetes
import os
from argparse import ArgumentParser
from pymongo import MongoClient
from shutil import which

from common import (exec_cmd,
                    greetings,
                    print_phase_start,
                    print_tool_installed,
                    print_tool_not_installed,
                    print_verify_tool,
                    WEB_APP_IMAGE_TAG,
                    WEB_APP_SERVICE_NAME,
                    DOCUMENT_QUERY)

def create_parser():
    parser = ArgumentParser(description='Set website with preffered content')
    parser.add_argument('content', type=str, help='Content to be displayed on website.')

    return parser

def is_tool_exists(name):
    return which(name) is not None

def verify_tool(name):
    print_verify_tool(name)
    if not is_tool_exists(name):
        print_tool_not_installed(name)
        raise EnvironmentError("Please refer README installation guide.")
    print_tool_installed(name)

def initialize_kubernetes_cluster():
    print_phase_start("Kubernetes cluster initialize")
    exec_cmd("minikube start --driver=docker")


def eval_docker_env():
    exec_cmd("eval $(minikube -p minikube docker-env)", shell=True)

def verify_cluster_exists():
    try: 
        contexts, _ = kubernetes.config.list_kube_config_contexts()
    except kubernetes.config.config_exception.ConfigException:
        initialize_kubernetes_cluster()
        
    eval_docker_env()

def verify_minukube():
    print_phase_start("Verify minikube setup")
    verify_tool('docker')
    verify_tool('minikube')
    verify_cluster_exists()

def build_web_app():
    print_phase_start("Building web-app image")
    docker_client = docker.from_env()
    current_dir = os.getcwd()
    os.chdir('web-app')
    docker_client.images.build(path='.',
                               tag=WEB_APP_IMAGE_TAG)
    os.chdir(current_dir)

def deploy_mongodb():
    print_phase_start("Deploy mongodb to cluster")
    exec_cmd("kubectl apply -f mongodb")

def delpoy_web_app():
    print_phase_start("Deploy web-app to cluster")
    exec_cmd("kubectl apply -f web-app")

def initialize_setup():
    verify_minukube()
    build_web_app()
    deploy_mongodb()
    delpoy_web_app()

def initialize_db_client():
    mongo_client = MongoClient(host=os.environ.get('MONGODB_HOST'),
                     port=int(os.environ.get('MONGODB_PORT')),
                     username=os.environ.get('MONGODB_USERNAME'),
                     password=os.environ.get('MONGODB_PASSWORD'))
    return mongo_client

def update_document_content(content):
    cursor = initialize_db_client()
    db_name = os.environ.get('MONGODB_DATABASE')
    collection_name = os.environ.get('MONGODB_COLLECTION')
    collection = cursor[db_name][collection_name]

    if collection.find_one(DOCUMENT_QUERY):
        document = collection.find_one(DOCUMENT_QUERY)
        document.update({'message': f'{content}'})
        collection.update_one(DOCUMENT_QUERY, {'$set': document})
    else:
        cursor[db_name][collection_name].insert_one({'input': 'user',
                                                     'message': content})

def display_web_app_url():
    service_url, _ = exec_cmd(f'minikube service {WEB_APP_SERVICE_NAME} --url',return_output=True)
    print(f'Browse the following link to access web-app - CLICK HERE -> {service_url.decode("utf-8")}')

def update_web_content(content):
    print_phase_start("Set web content")
    update_document_content(content)
    display_web_app_url()   


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    initialize_setup()
    update_web_content(args.content)
    greetings()