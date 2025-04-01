import os
from dotenv import load_dotenv
import requests
import uuid
import datetime
import hashlib
import hmac
import base64
import json

# Load environment variables
load_dotenv()
mimecast_api_key = os.getenv('MIMECAST_API_KEY')
mimecast_secret_key = os.getenv('MIMECAST_SECRET_KEY')
mimecast_domain = os.getenv('MIMECAST_DOMAIN')

# API Endpoint
BASE_URL = os.getenv('MIMECAST_DOMAIN')

# Generate headers for Mimecast authentication
def generate_headers():
    request_id = str(uuid.uuid4())
    date_str = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S UTC")
    
    secret_bytes = base64.b64decode(mimecast_secret_key)
    data_to_sign = f"{date_str}:{request_id}".encode('utf-8')
    signature = hmac.new(secret_bytes, data_to_sign, digestmod=hashlib.sha1).digest()
    signature_b64 = base64.b64encode(signature).decode()

    headers = {
        "Authorization": f"MC {mimecast_api_key}:{signature_b64}",
        "x-mc-app-id": mimecast_api_key,
        "x-mc-date": date_str,
        "x-mc-req-id": request_id,
        "Content-Type": "application/json"
    }
    return headers

# Function to fetch email statistics
def get_email_statistics(start_date, end_date):
    url = f"https://{BASE_URL}/api/message/traffic"
    headers = generate_headers()
    
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "metrics": ["totalInbound", "totalOutbound", "totalInternal", "rejectedInbound", "cleanInbound"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Process statistics for each Month-Year
def process_statistics():
    current_date = datetime.datetime.utcnow()
    results = []

    for i in range(12):  # Get data for the past 12 months
        first_day = (current_date - datetime.timedelta(days=i*30)).replace(day=1)
        last_day = (first_day + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

        start_date = first_day.strftime("%Y-%m-%dT00:00:00Z")
        end_date = last_day.strftime("%Y-%m-%dT23:59:59Z")

        data = get_email_statistics(start_date, end_date)
        if data:
            stats = data.get("data", [])[0]  # Extract first item

            total_inbound = stats.get("totalInbound", 0)
            rejected_inbound = stats.get("rejectedInbound", 0)
            clean_inbound = stats.get("cleanInbound", 0)
            total_outbound = stats.get("totalOutbound", 0)
            total_internal = stats.get("totalInternal", 0)

            rejection_percentage = (rejected_inbound / total_inbound * 100) if total_inbound > 0 else 0

            results.append({
                "Month-Year": first_day.strftime("%B-%Y"),
                "Total Inbound Email": total_inbound,
                "Rejections": rejected_inbound,
                "Legit Inbound Email": clean_inbound,
                "% Rejections": round(rejection_percentage, 2),
                "Total Outbound Email": total_outbound,
                "Total Internal Email": total_internal
            })

    return results

# Run the script
if __name__ == "__main__":
    stats = process_statistics()
    for row in stats:
        print(row)
