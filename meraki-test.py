import meraki
from dotenv import load_dotenv
import os

def get_switch_names(api_key, output_log=False, temp_dir=''):
    """
    Fetches and prints the names of all switches in the organization.
    
    :param api_key: Your Meraki API key
    :param output_log: Whether or not the api log should be created
    :param temp_dir: the temp directory to store the api log
    """
    dashboard = meraki.DashboardAPI(
        api_key, 
        output_log=output_log,
        log_file_prefix=temp_dir + "/meraki_api__log__"
    )
    organizations = dashboard.organizations.getOrganizations()
    organization_id = organizations[0]['id']
    networks = dashboard.organizations.getOrganizationNetworks(organization_id)
    
    switch_names = []
    for network in networks:
        devices = dashboard.networks.getNetworkDevices(network['id'])
        for device in devices:
            if device['model'].startswith("MS"):  # MS is the prefix for Meraki switches
                switch_names.append(device['name'])
    
    return switch_names

if __name__ == "__main__":
    # setup a temporary directory for the api logs
    project_temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(project_temp_dir, exist_ok=True)

    # get the api key from .env
    load_dotenv()
    meraki_api_key = os.getenv('MERAKI_API_KEY')

    try:
        # no logs created
        # switches = get_switch_names(meraki_api_key)
        # create api logs
        switches = get_switch_names(meraki_api_key, True, project_temp_dir)
        if switches:
            print("Switch Names:")
            for switch in switches:
                print(switch)
        else:
            print("No switches found.")
    except Exception as e:
        print(f"An error occurred: {e}")
