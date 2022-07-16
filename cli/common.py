import shlex
import subprocess
from emoji import emojize
from random import choice

emojies = {
    'stressed': [':worried_face:',
                 ':man_shrugging_medium_skin_tone:',
                 ':man_getting_massage_light_skin_tone:',
                 ':man_frowning_dark_skin_tone:',
                 ':mage_light_skin_tone:',
                 ':hushed_face:',
                 ':frowning_face_with_open_mouth:',
                 ':confused_face:',
                 ':check_mark_button:',
                 ':anxious_face_with_sweat:'],
    'relifed': [':nerd_face:',
                ':man_tipping_hand_medium_skin_tone:',
                 ':man_dancing_light_skin_tone:',
                 ':man_cartwheeling_light_skin_tone:',
                 ':kissing_face_with_smiling_eyes:',
                 ':grinning_face_with_sweat:',
                 ':face_without_mouth:',
                 ':face_savoring_food:'
                 ':crown:',
                 ':cowboy_hat_face:',
                 ':beaming_face_with_smiling_eyes:'],                 
    'panic': [':woozy_face:',
              ':nauseated_face:',
              ':man_mechanic_medium-light_skin_tone:',
              ':man_gesturing_NO_medium-light_skin_tone:',
              ':man_facepalming_medium_skin_tone:',
              ':man_bowing_dark_skin_tone:',
              ':lying_face:',
              '	:loudly_crying_face:',
              ':face_with_spiral_eyes:',
              ':face_with_rolling_eyes:',
              ':face_with_steam_from_nose:',
              ':face_with_head-bandage:',
              ':downcast_face_with_sweat:',
              ':disappointed_face:',
              ':crying_face:',
              ':bomb:',
              ':anguished_face:']
}

installation_links = {
    'docker': 'https://docs.docker.com/engine/install',
    'minikube': 'https://minikube.sigs.k8s.io/docs/start',
    'python': 'https://www.python.org/downloads'
}

WEB_APP_IMAGE_TAG = 'web-app'

WEB_APP_SERVICE_NAME = 'web-app'

DOCUMENT_QUERY = {'input': 'user'}

def exec_cmd(cmd, shell=False, return_output=False):
    subprocess_command = cmd if shell else shlex.split(cmd)
    if return_output:
        cmd_exec = subprocess.run(subprocess_command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_exec.check_returncode()
        return cmd_exec.stdout, cmd_exec.stdout
    else:
        subprocess.run(subprocess_command, shell=shell).check_returncode()

def greetings():
    print('\n\n*** Done! Thanks for choosing My Amazing Tool. ***')

def print_verify_tool(name):
    print(emojize(f'{choice(emojies["stressed"])}  Verify {name} is installed'))

def print_tool_installed(name):
    print(emojize(f'{choice(emojies["relifed"])}  {name} is installed and well configured'))

def print_tool_not_installed(name, installation_link):
    print(emojize(f"""{choice(emojies["panic"])}  {name} is not installed or could not be found.
Please refer {name} installation guide:
{installation_link[name]}"""))

def print_phase_start(name):
    print(f'\n=== Starting phase: {name} ===')