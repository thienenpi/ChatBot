from dotenv import load_dotenv
import os

load_dotenv()

AZURE_SEARCH_SERVICE_ENDPOINT=os.environ['AZURE_SEARCH_SERVICE_ENDPOINT']
AZURE_SEARCH_INDEX_NAME=os.environ['AZURE_SEARCH_INDEX_NAME']
AZURE_SEARCH_API_KEY=os.environ['AZURE_SEARCH_API_KEY']

AZURE_OPENAI_API_KEY=os.environ['AZURE_OPENAI_API_KEY']
AZURE_OPENAI_ENDPOINT=os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_API_VERSION=os.environ['AZURE_OPENAI_API_VERSION']
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME']
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME']
AZURE_OPENAI_EMB_DIMENSIONS=int(os.environ['AZURE_OPENAI_EMB_DIMENSIONS'])

AZURE_STORAGE_ACCOUNT_ENDPOINT=os.environ['AZURE_STORAGE_ACCOUNT_ENDPOINT']

datasetId=os.environ['datasetId']
groupId=os.environ['groupId']