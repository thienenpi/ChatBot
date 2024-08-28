import os
from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
      {
        "model": os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
        "api_type": "azure",
        "api_key": os.environ['AZURE_OPENAI_API_KEY'],
        "base_url": os.environ['AZURE_OPENAI_ENDPOINT'],
        "api_version": os.environ['AZURE_OPENAI_API_VERSION'],
      }
    ],
    # "cache_seed": None,
}