import pandas as pd
import streamlit as st
from requests.models import Response

def convert_column_name(column_name: str) -> str:
    if column_name[0] == '[' and column_name[-1] == ']':
        return column_name[1:-1]
    return column_name

def convert_column(col):
    if col.dtype == 'float':
        return pd.to_numeric(col, downcast='integer', errors='ignore')
    return col


def get_data_from_response(res: Response) -> pd.DataFrame:
    if res.status_code != 200:
        print(res.text)
        raise ValueError(f"Request failed with status code {res.status_code}")
    data = res.json()['results'][0]['tables'][0]
    df = pd.DataFrame(data=data['rows'])
    df = df.apply(lambda col: convert_column(col))
    return df

def convert_data(res: Response) -> pd.DataFrame:
    df = get_data_from_response(res=res)
    df.columns = [convert_column_name(col) for col in df.columns]
    return df