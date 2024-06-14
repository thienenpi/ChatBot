from autogen import AssistantAgent
from dotenv import load_dotenv

import os
import pandas as pd
import altair as alt

from agents import llm_config
from utils.prompts import data_visualizer_prompt

load_dotenv()

def escape_brackets(s):
    return s.replace("[", "\[").replace("]", "\]")

def get_visualization_from_result(result: str) -> dict:
    visualization = eval(result.split("TERMINATE")[1])
    visualization['x_axis'] = escape_brackets(visualization['x_axis'])

    return visualization

data_visualizer = AssistantAgent(
    name="Data visualizer",
    system_message=data_visualizer_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=100,
)


