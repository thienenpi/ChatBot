from autogen import UserProxyAgent
from utils.prompts import generate_prompt_from_res

user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    code_execution_config={
        "use_docker": False,
    },
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)