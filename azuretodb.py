import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# load .env
load_dotenv()

TENANTID = os.getenv ("AZURE_TENANTID")
CLIENTID = os.getenv("AZURE_CLIENTID")
CLIENTSECRET = os.getenv("AZURE_CLIENTSECRET")

#grabbing access token 
def getAccessToken():
    app = ConfidentialClientApplication(
        client_id=CLIENTID,
        authority=f"https://login.microsoftonline.com/{TENANTID}",
        client_credential=CLIENTSECRET
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    return result.get("access_token")

def getAADUsers():
    token = getAccessToken()
    if not token:
        raise Exception("Access token not available.")

    # Filter out the data using, UPN, Job Ttle, Department, Company name and City
    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName,jobTitle,department,companyName,city,accountEnabled,createdDateTime,lastSignInDateTime"
    headers = {"Authorization": f"Bearer {token}"}

    users = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Graph API error: {response.status_code} - {response.text}")

        data = response.json()
        users.extend(data.get("value", []))
        url = data.get("@odata.nextLink")  # Get the next page URL if it exists

    # Filter disabled and no company users 
    filtered_users = [u for u in users if u.get("companyName") != 'None' and u.get("accountEnabled") == True]

    return filtered_users

if __name__ == "__main__":
    users = getAADUsers()

    for user in users:
        print(f"{user.get('id', '')} | {user.get('displayName', '')} | {user.get('userPrincipalName', '')} | {user.get('jobTitle', '')} | {user.get('department', '')} | "
              f"{user.get('companyName', '')} | {user.get('city', '')} | {user.get('accountEnabled', '')} | {user.get('createdDateTime', '')} | {user.get('signInActivity', {}).get('lastSignInDateTime', '')}")
