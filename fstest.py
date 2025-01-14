import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta


# Load environment variables
load_dotenv()
fresh_service_api_key = os.getenv('FRESH_SERVICE_API_KEY')
fresh_service_domain = os.getenv('FRESH_SERVICE_DOMAIN')
    
if not fresh_service_api_key or not fresh_service_domain:
    print("API key or domain is not set in the .env file.")

# Base URL for the Freshservice API
BASE_URL = f"https://{fresh_service_domain}/api/v2"
HEADERS = {
    "Authorization": f"Basic {fresh_service_api_key.encode('utf-8').decode()}",
    "Content-Type": "application/json"
}

# Helper function to get tickets using the filter endpoint
def get_tickets_with_filter(query):
    url = f"{BASE_URL}/ticketsaa"
    params = {"query": query}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()  # Raise error for bad requests
    return response.json()["tickets"]

# Calculate date range for the past week in 'YYYY-MM-DD' format
def get_past_week_date_range():
    today = datetime.utcnow()
    last_week = today - timedelta(days=7)
    return last_week.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

# Main API Requests
def fetch_ticket_data():
    last_week_start, today = get_past_week_date_range()
    date_filter = ""

    # All tickets created in the past week
    all_tickets = get_tickets_with_filter(date_filter)
    total_tickets = len(all_tickets)

    # Filter for unresolved and resolved tickets
    unresolved_filter = f'{date_filter} AND "status:<\'4\'"'
    unresolved_tickets = get_tickets_with_filter(unresolved_filter)
    total_unresolved = len(unresolved_tickets)

    resolved_filter = f'{date_filter} AND "status:\'4\'"'
    resolved_tickets = get_tickets_with_filter(resolved_filter)
    total_resolved = len(resolved_tickets)

    # For SLA compliance, adjust as needed based on your API's capabilities
    # Placeholder for SLA Resolution Compliance
    sla_compliance = 0  # You might need a separate API call for this.

    return {
        "total_tickets": total_tickets,
        "total_unresolved": total_unresolved,
        "total_resolved": total_resolved,
        "sla_resolution_compliance_percentage": sla_compliance
    }

# Execution
if __name__ == "__main__":
    try:
        data = fetch_ticket_data()
        print("Ticket Data Summary:")
        print(f"Total Tickets: {data['total_tickets']}")
        print(f"Unresolved Tickets: {data['total_unresolved']}")
        print(f"Resolved Tickets: {data['total_resolved']}")
        print(f"SLA Resolution Compliance: {data['sla_resolution_compliance_percentage']}%")
    except Exception as e:
        print(f"Error: {e}")
