import requests
import os
from dotenv import load_dotenv

load_dotenv()

# load env
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')

def get_access_token() -> str:
    # scope for Power BI service
    scope = 'https://analysis.windows.net/powerbi/api/.default'

    # Define the URL and the payload
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'client_id': client_id,
        'grant_type': 'client_credentials',
        'scope': scope,
        'client_secret': client_secret,
    }

    # Define the headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make the POST request
    response = requests.post(url, data=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response (access token and other details)
        return response.json()['access_token']
    else:
        # Print the error
        print(f"Failed to retrieve token: {response.status_code}")
        print(response.text)
        return None
