import shlex
import subprocess
from argparse import ArgumentParser
from emoji import emojize
from shutil import which

emojies = {
    'stressed': ':magnifying_glass_tilted_right:',    
    'relifed': ':check_mark_button:',
    'panic': ':man_gesturing_NO_medium-light_skin_tone:'    
}

installation_links = {
    'docker': 'https://docs.docker.com/engine/install',
    'minikube': 'https://minikube.sigs.k8s.io/docs/start',
    'python': 'https://www.python.org/downloads'
}

DOCUMENT_QUERY = {'input': 'user'}

MONGODB_DETAILS = {
                    'db': 'my_amazing_tool',
                    'collection': 'data',
                    'creds': {
                        'username': 'adminuser',
                        'password': 'password123'
                    }
                  }

MONGODB_SERVICE_NAME = 'mongo-nodeport-svc'

WEB_APP_IMAGE_TAG = 'my_amazing_tool/web-app'

WEB_APP_SERVICE_NAME = 'web-app'

def create_parser():
    parser = ArgumentParser(description='Set website with preffered content')
    parser.add_argument('content', type=str, help='Content to be displayed on website.')
    return parser

def exec_cmd(cmd, shell=False, return_output=False):
    subprocess_command = cmd if shell else shlex.split(cmd)
    if return_output:
        cmd_exec = subprocess.run(subprocess_command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_exec.check_returncode()
        return cmd_exec.stdout, cmd_exec.stdout
    else:
        subprocess.run(subprocess_command, shell=shell).check_returncode()

def get_service_url(service_name):
    service_url, _ = exec_cmd(f'minikube service {service_name} --url',return_output=True)
    return service_url.decode('utf-8')

def greetings():
    print('\n\n*** Done! Thanks for choosing My Amazing Tool. ***')

def is_tool_exists(name):
    return which(name) is not None

def print_verify_tool(name):
    print(emojize(f'{emojies["stressed"]}  Verify {name} is installed'))

def print_tool_installed(name):
    print(emojize(f'{emojies["relifed"]}  {name} is installed and well configured'))

def print_tool_not_installed(name, installation_link):
    print(emojize(f"""{emojies["panic"]}  {name} is not installed or could not be found.
Please refer {name} installation guide:
{installation_link[name]}"""))

def print_phase_start(name):
    print(f'\n=== Starting phase: {name} ===')

def verify_tool(name):
    print_verify_tool(name)
    if not is_tool_exists(name):
        print_tool_not_installed(name)
        raise EnvironmentError("Please refer README installation guide.")
    print_tool_installed(name)