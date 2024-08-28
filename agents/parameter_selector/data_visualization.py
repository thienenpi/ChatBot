import re

from autogen import AssistantAgent
from dotenv import load_dotenv

from agents import llm_config
from utils.prompts import data_visualizer_prompt

load_dotenv()

def escape_brackets(s: str):
    return s.replace("[", "\[").replace("]", "\]")

def get_column_name(str: str):
    match = re.search(r"\[(.*?)\\]", str)
    if match:
        return match.group(1)
    return None

def get_visualization_from_result(result: str) -> dict:
    visualization = eval(result.split("TERMINATE")[1])
    visualization['x_axis'] = escape_brackets(visualization['x_axis'])

    return visualization

data_visualizer = AssistantAgent(
    name="Data_visualizer",
    system_message=data_visualizer_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=100,
)


