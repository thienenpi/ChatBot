import streamlit as st

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (QueryType, QueryCaptionType, QueryAnswerType, VectorizedQuery)
from azure.search.documents import SearchItemPaged
from openai import AzureOpenAI
from typing import TypedDict

from config import *
from agents.financial_analyzer.document_summarizer import document_summarizer, get_summarization_from_result
from agents.user_proxy import user_proxy

class AzureAISearch():
    endpoint: str
    index_name: str
    key: str
    number_results_to_return: int
    number_near_neighbors: int
    azure_deployment: str
    embedding_dimensions: int
    credentials: AzureKeyCredential = None
    search_client: SearchClient = None
    openai_client: AzureOpenAI = None

    def __init__(
            self,
            azure_endpoint: str = AZURE_OPENAI_ENDPOINT,
            azure_deployment: str = AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
            api_key: str = AZURE_OPENAI_API_KEY,
            api_version: str = AZURE_OPENAI_API_VERSION,
            endpoint: str = AZURE_SEARCH_SERVICE_ENDPOINT,
            index_name: str = AZURE_SEARCH_INDEX_NAME,
            key: str = AZURE_SEARCH_API_KEY,
            number_results_to_return: int = 2,
            number_near_neighbors: int = 50,
            embedding_dimensions: int = AZURE_OPENAI_EMB_DIMENSIONS,
    ) -> None:
        self.endpoint = endpoint
        self.index_name = index_name
        self.key = key
        self.number_results_to_return = number_results_to_return
        self.number_near_neighbors = number_near_neighbors
        self.azure_deployment = azure_deployment
        self.embedding_dimensions = embedding_dimensions
        self.credentials = AzureKeyCredential(self.key)
        self.search_client = SearchClient(endpoint=self.endpoint, index_name=self.index_name, credential=self.credentials)
        self.openai_client = AzureOpenAI(azure_endpoint=azure_endpoint, azure_deployment=azure_deployment, api_key=api_key, api_version=api_version)

    def get_summary(self, query: str, results: list[dict]) -> str:
        analytics = ""

        for index, result in enumerate(results):
            analytic = f"{index + 1}: {result['content']}"
            analytics += analytic + "\n\n"
        
        if analytics == "":
            analytics = "No information found."

        message = """\
Document:
{analytics}\
Question:
{query}""".format(analytics=analytics, query=query)

        chat_result = user_proxy.initiate_chat(
            recipient=document_summarizer,
            message=message
        )

        result = chat_result.chat_history[-1]['content']
        return get_summarization_from_result(result=result)

    def compute_text_embedding(self, query: str):
        SUPPORTED_DIMENSIONS_MODEL = {
            "text-embedding-ada-002": False,
            "text-embedding-3-small": True,
            "text-embedding-3-large": True,
        }

        class ExtraArgs(TypedDict, total=False):
            dimensions: int

        dimensions_args: ExtraArgs = (
            {"dimensions": self.embedding_dimensions} if SUPPORTED_DIMENSIONS_MODEL[self.azure_deployment] else {}
        )
        embedding = self.openai_client.embeddings.create(
            # Azure OpenAI takes the deployment name as the model name
            model=self.azure_deployment,
            input=query,
            **dimensions_args,
        )
        query_vector = embedding.data[0].embedding
        return VectorizedQuery(vector=query_vector, k_nearest_neighbors=self.number_near_neighbors, fields="embedding")
    
    def get_results_semantic_search(self, query: str) -> list[dict]:
        vector_query = self.compute_text_embedding(query)

        results = self.search_client.search(
            search_text=query,
            search_fields=['content'],
            semantic_configuration_name='default',
            query_type=QueryType.FULL,
            # vector_queries=[vector_query],
            top=self.number_results_to_return,
            # query_caption=QueryCaptionType.EXTRACTIVE, 
            # query_answer=QueryAnswerType.EXTRACTIVE,
        )

        return self.__get_results_to_return(results=results)
    
    def __get_results_to_return(self, results: SearchItemPaged[dict]):
        results_to_return = []

        for result in results:
            # if result['@search.score'] < 8:
            #     continue

            results_to_return.append({
                "content": result['content'],
                "sourcepage": result['sourcepage'],
                "sourcefile": result['sourcefile'],
            })

        return results_to_return