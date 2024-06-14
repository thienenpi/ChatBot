from autogen import AssistantAgent
from dotenv import load_dotenv
from typing import List

import pandas as pd

from utils.prompts import columns_prompt
from agents import llm_config

load_dotenv()

def get_columns_from_response(response: str) -> List[str]:
    columns = response.split('TERMINATE')[1].strip()
    columns = eval(columns)

    # load all columns
    tables = pd.read_csv('data/tables.csv')

    for column in columns:
        if '[' not in column or ']' not in column:
            columns[columns.index(column)] = ''
            continue
        table, column_name = column.split('[')
        column_name = column_name.rstrip(']')

        # check if table and column_name exist in tables
        if tables[(tables['Name'] == table) & (tables['Columns'].str.contains(column_name))].shape[0] > 0:
            print('Found')
        else:
            # remove the column from the list
            columns[columns.index(column)] = ''

    return [column for column in columns if column != '']

columns_selector = AssistantAgent(
    name="Columns selector",
    system_message=columns_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=2,
)