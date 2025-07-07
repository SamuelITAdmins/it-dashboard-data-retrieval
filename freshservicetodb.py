import os
import json
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import base64

def getReqVars():
  load_dotenv()
  fresh_service_api_key = os.getenv('FRESH_SERVICE_API_KEY')
  fresh_service_domain = os.getenv('FRESH_SERVICE_DOMAIN')

  if not fresh_service_api_key or not fresh_service_domain:
    print("API key or domain is not set in the .env file.")
    return
  
  auth_token = base64.b64encode(f"{fresh_service_api_key}:".encode()).decode()
  headers = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json",
  }
  
  return headers, fresh_service_domain

def getFreshServiceTickets():
  headers, domain = getReqVars()
  
  seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

  all_tickets = []
  page = 1
  per_page = 100

  while True:
    url = f"https://{domain}/api/v2/tickets?per_page={per_page}&page={page}&include=requester,stats&updated_since={seven_days_ago}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise error for bad requests

    data = response.json()
    tickets = data.get("tickets", [])

    if not tickets:
      break

    all_tickets.extend(tickets)
    page += 1
  
  # print(f'Tickets: {json.dumps(all_tickets, indent=2)}')
  print(f'First ticket: {json.dumps(all_tickets[0:4], indent=2)}')
  print(f'Count: {len(all_tickets)}')

  return all_tickets

def getFreshServiceUsers():
  headers, domain = getReqVars()

  all_users = []
  page = 1
  per_page = 100

  while True:
    url = f"https://{domain}/api/v2/agents?per_page={per_page}&page={page}&active=true"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    users = data.get("agents", [])

    if not users:
      break

    all_users.extend(users)
    page += 1

  print(f'First user: {json.dumps(all_users[0], indent=2)}')
  print(f'Count: {len(all_users)}')

  return all_users


if __name__ == "__main__":
  getFreshServiceTickets()
  getFreshServiceUsers()
