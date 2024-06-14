import requests
import base64

from urllib.parse import quote

from config import AZURE_STORAGE_ACCOUNT_ENDPOINT

def get_citation_file_path(citation: str) -> str:
    return AZURE_STORAGE_ACCOUNT_ENDPOINT + "content/" + citation

def fetch_citation(file_path: str):
  response = requests.get(url=file_path, headers={})
  return response

def get_citation(source_page: str) -> str:
    file_name = source_page.split("#")[0]

    page = source_page.split("#")[1] if "#" in source_page else None
    file_path = get_citation_file_path(file_name)

    pdf = fetch_citation(file_path=file_path)

    base64_pdf = base64.b64encode(pdf.content).decode('utf-8') + "#" + page
    pdf_display = f'<iframe type="application/pdf" src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px"></iframe>'

    return pdf_display