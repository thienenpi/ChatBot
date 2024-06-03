import requests
import os
from requests.models import Response
from dotenv import load_dotenv

from utils.query_generator import QueryGenerator
from auth.access_token import get_access_token

load_dotenv()

datasetId = os.environ['datasetId']
groupId = os.environ['groupId']

def execute_query(query: str) -> Response:
    access_token = get_access_token()
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/executeQueries"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    res = requests.post(url, headers=headers, json={
            "queries": [
                {
                    "query": query,
                }
            ]
        }
    )

    return res