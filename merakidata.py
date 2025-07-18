import meraki
import json
from dotenv import load_dotenv
import os
import sys
from datetime import datetime, timedelta, timezone

def getDeviceDowntime(dashboard, organization, device, report_length=7):
    '''Get the downtime and uptime percentage of the given device (switch or access point).

    Input:
    - dashboard: the meraki DashboardAPI
    - organization: the SE organization
    - device: a device within the organization
    - report_length: the report duration in days (default = 7)
    
    Returns: A dictionary with the following entries:
    - device_name: the name of the device reported on
    - downtime: the duration, in seconds, that the device was down for
    - uptime_percentage: the amount of time the device was connected for as a percentage
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

    # get the device network to access the location of the device
    device_network = dashboard.networks.getNetwork(device['networkId'])
    device_location = device_network['name']

    # get the history for the device
    device_history = [
        record for record in org_history if record['device']['name'] == device['name']
    ]

    # sort events by timestamp
    device_history.sort(key=lambda x: x['ts'])
    # print(device_history)

    # calculate the downtime
    downtime = 0
    # assume that the switch is online if no updates have been made in the timeframe
    last_status = 'online' # TODO: change so that dormant devices are not considered online by default
    last_time = start_time

    for event in device_history:
        timestamp = datetime.fromisoformat(event['ts'].replace('Z', '+00:00'))
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
        'device_name': device['name'],
        'location': device_location,
        'downtime': downtime,
        'uptime_percentage': uptime_percentage,
        'status': last_status
    }

def getMerakiData():
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

        device_statuses = dashboard.organizations.getOrganizationDevicesStatusesOverview(se_organization['id'])
        print(device_statuses)

        # get the switches
        switches = dashboard.organizations.getOrganizationDevices(
            se_organization['id'], 
            productTypes=['switch'], 
            # name='DEN-1ST-TEMP'
        )
        if not switches: raise Exception('No switches found')
        print(f'Number of switches: {len(switches)}')

        access_points = dashboard.organizations.getOrganizationDevices(
            se_organization['id'],
            productTypes=['wireless'],
            # name='DEN-4TH-AP-04'
        )
        if not access_points: raise Exception('No access points found')
        print(f'Number of access points: {len(access_points)}')

        # pair switches with switch downtimes
        switch_downtimes = []
        for switch in switches:
            switch_downtime = getDeviceDowntime(dashboard, se_organization, switch)
            switch_downtimes.append(switch_downtime)
        #for switch_downtime in switch_downtimes:
        #    print(switch_downtime)

        # pair access points with AP downtimes
        ap_downtimes = []
        for access_point in access_points:
            ap_downtime = getDeviceDowntime(dashboard, se_organization, access_point)
            ap_downtimes.append(ap_downtime)
        #for ap_downtime in ap_downtimes:
        #    print(ap_downtime)

        return switch_downtimes, ap_downtimes
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def getDeviceUsage():
    load_dotenv()
    meraki_api_key = os.getenv("MERAKI_API_KEY")

    # create the dashboard opbject for the meraki API
    dashboard = meraki.DashboardAPI(
        meraki_api_key,
        output_log=False
    )

    try:
        # get the organization
        se_organization = dashboard.organizations.getOrganizations()[0]
        if se_organization['name'] != 'Samuel Engineering': raise Exception('Did not get SE as the organization')

        device_summary = dashboard.organizations.getOrganizationSummaryTopDevicesByUsage(se_organization['id'], quantity=100, timespan=7*24*60*60)
        print(len(device_summary))
        # print(json.dumps(device_summary, indent=2))

        return device_summary
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def getAlerts():
    load_dotenv()
    meraki_api_key = os.getenv("MERAKI_API_KEY")

    # create the dashboard opbject for the meraki API
    dashboard = meraki.DashboardAPI(
        meraki_api_key,
        output_log=False
    )

    try:
        # get the organization
        se_organization = dashboard.organizations.getOrganizations()[0]
        if se_organization['name'] != 'Samuel Engineering': raise Exception('Did not get SE as the organization')

        device_alerts = dashboard.organizations.getOrganizationWebhooksAlertTypes(se_organization['id'], productType='switch')
        print(len(device_alerts))
        print(json.dumps(device_alerts, indent=2))

        return device_alerts
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def getLosses():
    load_dotenv()
    meraki_api_key = os.getenv("MERAKI_API_KEY")

    # create the dashboard opbject for the meraki API
    dashboard = meraki.DashboardAPI(
        meraki_api_key,
        output_log=False
    )

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=60)

    try:
        # get the organization
        se_organization = dashboard.organizations.getOrganizations()[0]
        if se_organization['name'] != 'Samuel Engineering': raise Exception('Did not get SE as the organization')

        latency_losses = dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(se_organization['id'], t0=start_time)
        print(len(latency_losses))
        print(json.dumps(latency_losses, indent=2))

        return latency_losses
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

__all__ = ['getMerakiData']

if __name__ == "__main__":
    # getLosses()
    switch_data, ap_data = getMerakiData()
    print('Switch data:')
    for switch in switch_data:
        print(switch)
    print('Access Point data:')
    for ap in ap_data:
        print(ap)
