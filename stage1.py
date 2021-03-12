# Extract from Intersight API:

# TODO Overivew of deployments running in the kubernetes cluster. Count the number of deployments.

import requests
import json
from pprint import pprint

from utils.auth import IntersightAuth
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def get_descriptions_alarms():
    """
    Returns description of alarms in Intersight
    """
    response = requests.get(f"{BASE_URL}/cond/Alarms?$select=Description", auth=auth)
    response.raise_for_status()

    return response.json()['Results']


def get_summary_phys_infra():
    """
    Returns Management mode, Management IP, Name, CPUs, Cores, PowerState,
    Firmware, Model, Serial and License Tier of the physical infra
    """
    response = requests.get(f"{BASE_URL}/compute/PhysicalSummaries?$select=ManagementMode,MgmtIpAddress,Name,NumCpus,NumCpuCores,OperPowerState,Firmware,Model,Serial,SharedScope", auth=auth)
    response.raise_for_status()

    return response.json()['Results']

def get_compliance_hcl():
    """
    Returns OS Vendor and OS Version from HCL compatibility status 
    """
    # For some reason, the $select=HclOsVersion does not work and gives me bad request 400
    response = requests.get(f"{BASE_URL}/cond/HclStatuses", auth=auth)
    response.raise_for_status()

    return response.json()['Results']

def get_overview_running_kubernetes():
    """
    Returns names of all Kubernetes clusters running
    """
    response = requests.get(f"{BASE_URL}/kubernetes/Clusters?$select=Name", auth=auth)
    response.raise_for_status()

    return response.json()['Results']

def get_count_running_deployments_kubernetes():
    """
    Returns amount of deployments running Kubernetes cluster
    """
    response = requests.get(f"{BASE_URL}/kubernetes/Deployments?$count=true", auth=auth)
    response.raise_for_status()
    
    return response.json()['Count']

if __name__ == '__main__':
    descriptions_alarms = get_descriptions_alarms()
    print('The alarms in Intersight are described in the following way: \n')
    print('---')
    for alarm in descriptions_alarms:
        print(f"{alarm['Description']}\n---")

    print('---\nHere is a summary of the physical infrastructure:\n---')
    pprint(get_summary_phys_infra(), indent=4)

    hcl_statuses = get_compliance_hcl()
    print('---\nThe following are OS Vendors and OS Versions from HCL compatibility statuses:\n---')
    for status in hcl_statuses:
        if status['HclOsVendor'] == '':
            pass
        else:
            print(f"{status['HclOsVendor']}, {status['HclOsVersion']}")

    print('---\nHere is an overview of the names of the running Kubernetes clusters\n---')
    pprint(get_overview_running_kubernetes(), indent=4)

    print(f"There are {get_count_running_deployments_kubernetes()} deployments running in the Kubernetes cluster.")




    


    
    