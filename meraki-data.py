import meraki
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

def getSwitchDowntime(dashboard, organization, switch, report_length=7):
    '''Get the downtime and uptime percentage of the given switch.

    Input:
    - dashboard: the meraki DashboardAPI
    - organization: the SE organization
    - switch: a switch device within the organization
    - report_length: the report duration in days (default = 7)
    
    Returns: A dictionary with the following entries:
    - switch_name: the name of the switch reported on
    - downtime: the duration, in seconds, that the switch was down for
    - uptime_percentage: the amount of time the switch was connected for as a percentage
    '''
    # calculate the start time for the past week
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=report_length)

    # format the timestamps
    start_time_str = start_time.isoformat() + "Z"
    end_time_str = end_time.isoformat() + "Z"

    # get the history for the organization
    org_history = dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
            organization['id'],
            t0=start_time_str,
            t1=end_time_str
    )

    # get the history for the switch
    switch_history = [
        record for record in org_history
        if record['device']['productType'] == 'switch' and record['device']['name'] == switch['name']
    ]

    # sort events by timestamp
    switch_history.sort(key=lambda x: x['ts'])
    # print(switch_history)

    # calculate the downtime
    downtime = 0
    last_status = None
    last_time = start_time

    for event in switch_history:
        timestamp = datetime.fromisoformat(event['ts'].replace('Z', ''))
        status = event['details']['new'][0]['value']

        # add the time the device was not connected for
        if last_status == 'offline' or last_status == 'alerting' or last_status == 'dormant':
            downtime += (timestamp - last_time).total_seconds()

        # update last status and time
        last_status = status
        last_time = timestamp

    # add any remaining time since the last event
    if last_status == "offline" or last_status == 'alerting' or last_status == 'dormant':
        downtime += (end_time - last_time).total_seconds()

    # calculate the total time
    total_time = timedelta(days=report_length).total_seconds()
    uptime_percentage = round((1 - (downtime / total_time)) * 100, 2) if total_time > 0 else 0

    return {
        'switch_name': switch['name'],
        'downtime': downtime,
        'uptime_percentage': uptime_percentage
    }

def getMerakiSwitchData():
    # get the meraki API key from .env
    load_dotenv()
    meraki_api_key = os.getenv('MERAKI_API_KEY')

    # set if you want output API logs
    output_log = True

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
        if se_organization['name'] != 'Samuel Engineering': raise Exception('Did not get SE as the organization')

        # get the switches
        switches = dashboard.organizations.getOrganizationDevices(
            se_organization['id'], 
            productTypes=['switch'], 
            # name='DEN-CREATIVE'
        )
        if not switches: raise Exception('No switches found')

        # pair switches with switch downtimes
        switch_downtimes = []
        for switch in switches:
            switch_downtime = getSwitchDowntime(dashboard, se_organization, switch)
            switch_downtimes.append(switch_downtime)
        #for switch_downtime in switch_downtimes:
        #    print(switch_downtime)
        return switch_downtimes


        '''
        # get the networks
        networks = dashboard.organizations.getOrganizationNetworks(se_organization['id'])

        # get events of a network
        #events = dashboard.networks.getNetworkEvents(
        #    networks[0]['id'], 
        #    #includedEventTypes=['boot'],
        #    excludedEventTypes=['stp_port_role_change', 'port_status'],
        #    deviceName='DEN-LISTENING',
        #    startingAfter=start_time_str,
        #    perPage=10
        #)
        #print(events)

        # get device avaiability history
        #availability = dashboard.organizations.getOrganizationDevicesPowerModulesStatusesByDevice(
        #    se_organization['id'],
            #perPage=100,
            #startingAfter=start_time_str
        #)
        #print(availability)
        '''
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    switch_data = getMerakiSwitchData()
    print(len(switch_data))
    # access_point_data = getMerakiAPData()
