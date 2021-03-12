import requests
import json
from pprint import pprint

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def get_ntp_policies():
    response = requests.get(f"{BASE_URL}/ntp/Policies", auth=auth)
    response.raise_for_status()

    return response.json()

if __name__ == '__main__':
    ntp_policies = get_ntp_policies()
    pprint(ntp_policies, indent=4)