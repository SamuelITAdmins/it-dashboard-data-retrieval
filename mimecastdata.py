import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
AUTH_URL = 'https://api.services.mimecast.com/oauth/token'
API_URL = 'https://api.services.mimecast.com/api/audit/get-siem-logs'
CLIENT_ID = os.getenv('MIMECAST_API_KEY')
CLIENT_SECRET = os.getenv('MIMECAST_SECRET_KEY')
PAGE_SIZE= 50 # Default page size

def get_bearer_token(auth_url, client_id, client_secret):
    auth_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    auth_response = requests.post(auth_url, data=auth_data)
    auth_response.raise_for_status()

    return auth_response.json()['access_token']