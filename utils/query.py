import requests
import os
from requests.models import Response

from utils.query_generator import QueryGenerator
from auth.access_token import get_access_token

datasetId = os.getenv('datasetId')
groupId = os.getenv('groupId')
token = get_access_token()

def execute_query(query: str) -> Response:
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/executeQueries"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
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