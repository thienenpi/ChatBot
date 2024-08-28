import requests
import base64

from urllib.parse import quote

from config import AZURE_STORAGE_ACCOUNT_ENDPOINT

def get_citation_file_path(citation: str) -> str:
    return AZURE_STORAGE_ACCOUNT_ENDPOINT + "document/" + citation

def fetch_citation(file_path: str):
  response = requests.get(url=file_path, headers={})
  return response

def get_citation(source_page: str) -> str:
    file_name = source_page.split("#")[0]

    page = source_page.split("#")[1] if "#" in source_page else None
    file_path = get_citation_file_path(file_name)

    src = file_path + "#page=" + page

    pdf_display = f'<iframe style="position: fixed; top: 20px; width: 47%; height: 95%" src="{src}"></iframe>'

    return pdf_display