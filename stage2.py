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

    return response.json()['imdata']

if __name__ == '__main__':
    health_score = get_health_score()

    with open('output.csv','w') as file:
        for element in health_score:
            fabric_health_score = element['fabricHealthTotal']['attributes']['cur']
            fabric_maximum_severity = element['fabricHealthTotal']['attributes']['maxSev']
            timestamp = element['fabricHealthTotal']['attributes']['modTs']
            file.write(f"{fabric_health_score}, {fabric_maximum_severity}, {timestamp}\n")

        file.close()