import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import base64

def getTicketsWithFilter(domain, params, headers):
    url = f"https://{domain}/api/v2/tickets/filter"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise error for bad requests
    return response.json()

def getFreshServiceData():
    '''Get the tickets (total, unresolved, resolved) and SLA resolution compliance data for the IT dashboard.
    Returns: A dictionary with the following entries:
    - device_name: the name of the device reported on
    '''
    # Load environment variables
    load_dotenv()
    fresh_service_api_key = os.getenv('FRESH_SERVICE_API_KEY')
    fresh_service_domain = os.getenv('FRESH_SERVICE_DOMAIN')

    if not fresh_service_api_key or not fresh_service_domain:
        print("API key or domain is not set in the .env file.")
        return
    
    # Calculate the date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    today = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Set up query parameters
    total_tickets_params = {
        "query": f"\"created_at:>\'{seven_days_ago}\' AND created_at:<\'{today}\'\"",
    }
    unresolved_tickets_params = {
        "query": f"\"(created_at:>\'{seven_days_ago}\' AND created_at:<\'{today}\') AND (status:2 OR status:3)\"", # open or pending tickets
    }
    resolved_tickets_params = {
        "query": f"\"(created_at:>\'{seven_days_ago}\' AND created_at:<\'{today}\') AND (status:4 OR status:5)\"", # resolved or closed tickets
    }

    # Set up the headers
    auth_token = base64.b64encode(f"{fresh_service_api_key}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }

    total_tickets = getTicketsWithFilter(fresh_service_domain, total_tickets_params, headers)
    print(f"Total tickets created in the last 7 days: {total_tickets.get("total", [])}")
    unresolved_tickets = getTicketsWithFilter(fresh_service_domain, unresolved_tickets_params, headers)
    print(f"Unresolved tickets created in the last 7 days: {unresolved_tickets.get("total", [])}")
    resolved_tickets = getTicketsWithFilter(fresh_service_domain, resolved_tickets_params, headers)
    print(f"Resolved tickets created in the last 7 days: {resolved_tickets.get("total", [])}")
    resolution_percentage = round(resolved_tickets.get("total", []) / total_tickets.get("total", []) * 100, 2)
    print(f"Resolved tickets percentage in the last 7 days: {resolution_percentage}")

    return {
        "total_tickets": total_tickets.get("total", []),
        "unresolved_tickets": unresolved_tickets.get("total", []),
        "resolved_tickets": resolved_tickets.get("total", []),
        "resolution_percentage": resolution_percentage
    }

__all__ = ['getFreshServiceData']

if __name__ == "__main__":
    getFreshServiceData()
