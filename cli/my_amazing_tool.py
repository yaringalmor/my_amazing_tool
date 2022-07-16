import docker
import kubernetes
import os
import re
import requests
from pymongo import MongoClient

from common import (create_parser,
                    exec_cmd,
                    get_service_url,
                    greetings,
                    is_tool_exists,
                    print_phase_start,
                    print_tool_installed,
                    print_tool_not_installed,
                    print_verify_tool,
                    verify_tool,
                    WEB_APP_IMAGE_TAG,
                    WEB_APP_SERVICE_NAME,
                    MONGODB_SERVICE_NAME,
                    MONGODB_DETAILS,
                    DOCUMENT_QUERY)

def initialize_kubernetes_cluster():
    print_phase_start("Kubernetes cluster initialize")
    exec_cmd("minikube start --driver=docker")

def verify_cluster_exists():
    try: 
        contexts, _ = kubernetes.config.list_kube_config_contexts()
    except kubernetes.config.config_exception.ConfigException:
        initialize_kubernetes_cluster()

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

def get_mongo_service_details():
    k8s_service_url_regex = re.compile('http://(.*):([0-9]{5})')
    service_url = get_service_url(MONGODB_SERVICE_NAME)

    service_url_match = k8s_service_url_regex.match(service_url)
    if service_url_match:
        mongodb_host = service_url_match.group(1)
        mongodb_port = int(service_url_match.group(2))
        return mongodb_host, mongodb_port
    
    raise RuntimeError("Failed to detect MongoDB service details")


def initialize_db_client():
    mongodb_host, mongodb_port = get_mongo_service_details()
    mongo_client = MongoClient(host=mongodb_host,
                               port=int(mongodb_port),
                               username=MONGODB_DETAILS['creds']['username'],
                               password= MONGODB_DETAILS['creds']['password'])
    return mongo_client

def update_document_content(content):
    cursor = initialize_db_client()
    db_name = MONGODB_DETAILS['db']
    collection_name = MONGODB_DETAILS['collection']
    collection = cursor[db_name][collection_name]

    if collection.find_one(DOCUMENT_QUERY):
        document = collection.find_one(DOCUMENT_QUERY)
        document.update({'message': f'{content}'})
        collection.update_one(DOCUMENT_QUERY, {'$set': document})
    else:
        cursor[db_name][collection_name].insert_one({'input': 'user',
                                                     'message': content})
def validate_web_app_content(content):
    service_url = get_service_url(WEB_APP_SERVICE_NAME)
    res = requests.get(service_url)
    web_app_content = res.content.decode('utf-8')
    if content != web_app_content:
        raise RuntimeError("Web app failed to load content from db")

def display_web_app_url():
    service_url = get_service_url(WEB_APP_SERVICE_NAME)
    print(f'Browse the following link to access web-app - CLICK HERE -> {service_url}')

def update_web_content(content):
    print_phase_start("Set web content")
    update_document_content(content)
    validate_web_app_content(content)
    display_web_app_url()   


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    initialize_setup()
    update_web_content(args.content)
    greetings()