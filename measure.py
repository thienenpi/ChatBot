from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
from typing import List
import os

from prompts import measure_prompt

load_dotenv()

def get_measures_from_response(response: str) -> List[str]:
    measures = []

    measures_selected = response.split('TERMINATE')[1].strip()

    # conevert the measures to a list
    measures = eval(measures_selected)

    return measures

llm_config = {
    "config_list": [
      {
        "model": os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
        "api_type": "azure",
        "api_key": os.environ['AZURE_OPENAI_API_KEY'],
        "base_url": os.environ['AZURE_OPENAI_ENDPOINT'],
        "api_version": os.environ['AZURE_OPENAI_API_VERSION']
      }
    ],
}

assistant = AssistantAgent(
    name="Measures selector",
    system_message=measure_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=2,
)

user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    code_execution_config={
        "use_docker": False,
    },
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)
