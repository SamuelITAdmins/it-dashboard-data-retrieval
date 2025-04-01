import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# load .env
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

#grabbing access token 
def get_access_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return result.get("access_token")

def get_AAD_Users(company_name):
    token = get_access_token()
    if not token:
        raise Exception("Access token not available.")

    # Filter out the data using, UPN, Job Ttle, Department, Company name and City
    url = url = "https://graph.microsoft.com/v1.0/users?$select=userPrincipalName,jobTitle,department,companyName,city"
    headers = {"Authorization": f"Bearer {token}"}

    users = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Graph API error: {response.status_code} - {response.text}")

        data = response.json()
        users.extend(data.get("value", []))
        url = data.get("@odata.nextLink")  # Get the next page URL if it exists

    # Filter users 
    filtered_users = [u for u in users if u.get("companyName") == company_name]

    return filtered_users
