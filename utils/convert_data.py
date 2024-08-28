import pandas as pd
import streamlit as st
from requests.models import Response

def convert_column_name(column_name: str) -> str:
    if column_name[0] == '[' and column_name[-1] == ']':
        return column_name[1:-1]
    return column_name

def handleNaNValues(df: pd.DataFrame) -> pd.DataFrame:
    na_rows = df[df.isna().any(axis=1)]
    df = df.dropna()

    # convert all columns to int if dtype is float
    for column in df.columns:
        if df[column].dtype == 'float':
            df[column] = df[column].astype(int)

    # do the same with na_rows
    for column in na_rows.columns:
        if na_rows[column].dtype == 'float':
            na_rows[column].fillna(0, inplace=True)
            na_rows[column] = na_rows[column].astype(int)
            na_rows[column] = na_rows[column].replace(0, 'NaN')

    df = pd.concat([df, na_rows])
    df = df.sort_index()

    return df


def get_data_from_response(res: Response) -> pd.DataFrame:
    if res.status_code != 200:
        print(res.text)
        raise ValueError(f"Request failed with status code {res.status_code}")
    data = res.json()['results'][0]['tables'][0]
    df = pd.DataFrame(data=data['rows'])
    df = handleNaNValues(df=df)
    return df

def convert_data(res: Response) -> pd.DataFrame:
    df = get_data_from_response(res=res)
    df.columns = [convert_column_name(col) for col in df.columns]
    return df