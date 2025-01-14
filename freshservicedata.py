import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import base64

def getFreshServiceData():
    # Load environment variables
    load_dotenv()
    fresh_service_api_key = os.getenv('FRESH_SERVICE_API_KEY')
    fresh_service_domain = os.getenv('FRESH_SERVICE_DOMAIN')
    
    if not fresh_service_api_key or not fresh_service_domain:
        print("API key or domain is not set in the .env file.")
        return

    # Base URL for the Freshservice API
    BASE_URL = f"https://{fresh_service_domain}/api/v2/tickets/filter"

    # Calculate the date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    today = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    print(seven_days_ago)

    # Set up the headers
    auth_token = base64.b64encode(f"{fresh_service_api_key}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }

    # Set up query parameters
    params = {
        "query": f"\"created_at:>\'{seven_days_ago}\' AND created_at:<\'{today}\'\"",
    }

    # Make the API request
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            tickets = response.json()
            total_tickets = len(tickets.get("tickets", []))
            print(f"Total tickets created in the last 7 days: {total_tickets}")
            return tickets
        else:
            print(f"Failed to fetch tickets. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    getFreshServiceData()
