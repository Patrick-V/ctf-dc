#TODO Write the health score information into a comma-separated text file with the timestamp of the request included. Each entry in that .csv file should include
#   The timestamp
#   The total health score
#   The maximum severity
import requests
from env import config
from utils.auth import IntersightAuth, get_authenticated_aci_session
from pprint import pprint

aci_session = get_authenticated_aci_session(config['ACI_USER'], config['ACI_PASSWORD'], config['ACI_BASE_URL'])

def get_health_score():

    response = aci_session.get(f"{config['ACI_BASE_URL']}/api/class/fabricHealthTotal.json")
    response.raise_for_status()

    return response.json()['imdata'][0]['fabricHealthTotal']['attributes']['cur'], response.json()['imdata'][0]['fabricHealthTotal']['attributes']['maxSev']

if __name__ == '__main__':
    fabric_health_score, fabric_maximum_severity = get_health_score()
    

        
