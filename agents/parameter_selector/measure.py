from autogen import AssistantAgent
from dotenv import load_dotenv
from typing import List

import pandas as pd

from utils.prompts import measure_prompt
from agents import llm_config

load_dotenv()

def get_measures_from_response(response: str) -> List[str]:
    measures = response.split('TERMINATE')[1].strip()
    measures = eval(measures)

    # load all measures
    all_measures = pd.read_csv('data/measures.csv')

    for measure in measures:
        if measure not in all_measures['Measure Name'].values:
            measures[measures.index(measure)] = ''

    return [measure for measure in measures if measure != '']

measures_selector = AssistantAgent(
    name="Measures selector",
    system_message=measure_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=2,
)