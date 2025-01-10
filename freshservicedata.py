import os
import sys
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

def getFreshServiceData():
    # get the meraki API key from .env
    load_dotenv()
    fresh_service_api_key = os.getenv('FRESH_SERVICE_API_KEY')
    fresh_service_domain = os.getenv('FRESH_SERVICE_DOMAIN')
    BASE_URL = f"https://{fresh_service_domain}/api/v2/tickets"

    # Calculate the date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Set up headers
    headers = {
      "Authorization": f"Basic {fresh_service_api_key}",
      "Content-Type": "application/json",
    }

    # Parameters to filter tickets created in the last 7 days
    params = {
      "query": f"(created_at:>'{seven_days_ago}')"
    }

    # Make the API request
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
      tickets = response.json()
      total_tickets = len(tickets.get("tickets", []))
      print(f"Total tickets created in the last 7 days: {total_tickets}")
    else:
      print(f"Failed to fetch tickets. Status code: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    getFreshServiceData()
