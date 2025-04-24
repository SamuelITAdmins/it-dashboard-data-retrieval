import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('NASUNI_API_KEY')
DOMAIN = os.getenv('NASUNI_DOMAIN')
IP = os.getenv('NASUNI_IP')

GET_FILERS_URL = f"https://nmc-dn-01/api/v1.1/filers/"
# GET_FILER_URL = f'https://{IP}/api/v1.1/filers/{filer_serial}/'
# status => platform => cache_status of the filer: size, used, dirty, free, percent_used

def getNasuniData():
  query = {
    "limit": "50",
    "offset": "0"
  }

  print(GET_FILERS_URL)

  headers = {"Authorization": 'NNJLp+GPSWBrEL79'}

  response = requests.get(GET_FILERS_URL, headers=headers)

  data = response.json()
  print(data)

if __name__ == "__main__":
  getNasuniData()