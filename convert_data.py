import pandas as pd
from requests.models import Response

from query import execute_query

def convert_column_name(column_name: str) -> str:
  return column_name[1:-1]

def convert_data(res: Response) -> pd.DataFrame:
    if res.status_code != 200:
        print(res.text)
        raise ValueError(f"Request failed with status code {res.status_code}")

    data = res.json()['results'][0]['tables'][0]
    df = pd.DataFrame(data=data['rows'])
    df.columns = [convert_column_name(col) for col in df.columns]
    return df.to_markdown(index=False)

