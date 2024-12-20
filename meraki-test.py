import meraki
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

def get_switch_names(api_key, output_log, temp_dir):
    """
    Fetches and prints the names of all switches in the organization.
    
    :param api_key: Your Meraki API key
    :param output_log: Whether or not the api log should be created
    :param temp_dir: the temp directory to store the api log
    """
    dashboard = meraki.DashboardAPI(
        api_key, 
        output_log=output_log,
        log_file_prefix=temp_dir + "/meraki_api"
    )
    organizations = dashboard.organizations.getOrganizations()
    print(organizations)
    switches = []

    # organization_id = organizations[0]['id']
    # networks = dashboard.organizations.getOrganizationNetworks(organization_id)
    
    switch_names = []
    # for network in networks:
    #     devices = dashboard.networks.getNetworkDevices(network['id'])
    #     for device in devices:
    #         if device['model'].startswith("MS"):  # MS is the prefix for Meraki switches
    #             switch_names.append(device['name'])
    #             print(device)
    
    return switch_names

def getSwitchDowntime(dashboard, switch):
    # Calculate the start time for the past week
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)

    # Format the timestamps
    start_time_str = start_time.isoformat() + "Z"
    end_time_str = end_time.isoformat() + "Z"

    raise NotImplementedError

if __name__ == "__main__":
    # get the meraki API key from .env
    load_dotenv()
    meraki_api_key = os.getenv('MERAKI_API_KEY')

    # set if you want output API logs
    output_log = False

    # setup a temporary directory for the API logs
    if output_log:
        project_temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(project_temp_dir, exist_ok=True)
    else:
        project_temp_dir = ''

    # create the dashboard opbject for the meraki API
    dashboard = meraki.DashboardAPI(
        meraki_api_key, 
        output_log=output_log,
        log_file_prefix=project_temp_dir + "/meraki_api"
    )

    try:
        # get the organization
        se_organization = dashboard.organizations.getOrganizations()[0]
        if se_organization['name'] != 'Samuel Engineering': raise Exception('Did not get SE as the organizaiton')

        # get the switches
        # switches = dashboard.organizations.getOrganizationDevices(se_organization['id'])
        # if not switches: raise Exception('No switches found')

        # get the networks
        networks = dashboard.organizations.getOrganizationNetworks(se_organization['id'])

        # Calculate the start time for the past week
        start_time = datetime.now() - timedelta(days=7)

        # Format the timestamps
        start_time_str = start_time.isoformat() + "Z"

        events = dashboard.networks.getNetworkEvents(
            networks[0]['id'], 
            productType='switch',
            includedEventTypes=['uplink_connectivity'],
            startingAfter=start_time_str,
            perPage=1000
        )
        print(events)

        # calculate uptime of each switch
        #uptimes = []
        #for switch in switches:
        #    uptimes.append(100 - getSwitchDowntime(dashboard, switch))
    except Exception as e:
        print(f"An error occurred: {e}")
