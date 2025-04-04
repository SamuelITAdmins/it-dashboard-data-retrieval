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
def getaccesstoken():
    app = ConfidentialClientApplication(
        client_id=CLIENTID,
        authority=f"https://login.microsoftonline.com/{TENANTID}",
        client_credential=CLIENTSECRET
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    print("Token result:", result)  

    return result.get("access_token")

def getAADUsers(companyname):
    token = getaccesstoken()
    if not token:
        raise Exception("Access token not available.")

    # Filter out the data using, UPN, Job Ttle, Department, Company name and City
    url = "https://graph.microsoft.com/v1.0/users?$select=userPrincipalName,jobTitle,department,companyName,city"
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
    filtered_users = [u for u in users if u.get("companyName") == companyname]

    

    return filtered_users

if __name__ == "__main__":
    companyname = "Samuel Engineering"
    users = getAADUsers(companyname)

    # Exclude users without job titles
    users = [u for u in users if u.get("jobTitle")]

    for user in users:
        print(f"{user.get('userPrincipalName', '')} | {user.get('jobTitle', '')} | {user.get('department', '')} | {user.get('city', '')}")
