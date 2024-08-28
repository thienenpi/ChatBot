from autogen import AssistantAgent
from dotenv import load_dotenv

from utils.prompts import financial_analyzer_prompt
from agents import llm_config

load_dotenv()

def get_analytics_from_result(result: str) -> str:
    analytics = result.split('TERMINATE')[1].strip()
    return analytics

financial_analyzer = AssistantAgent(
    name="Financial_analyzer",
    system_message=financial_analyzer_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=2,
)