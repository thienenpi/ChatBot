from autogen import AssistantAgent
from dotenv import load_dotenv

from utils.prompts import document_summarizer_prompt
from agents import llm_config

load_dotenv()

def get_summarization_from_result(result: str) -> str:
    summarization = result.split('TERMINATE')[1].strip()
    return summarization

document_summarizer = AssistantAgent(
    name="Document_summarizer",
    system_message=document_summarizer_prompt,
    llm_config=llm_config,
    max_consecutive_auto_reply=2,
)