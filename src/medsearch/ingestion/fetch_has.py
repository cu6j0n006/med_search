from abc import ABC, abstractmethod
import pandas as pd
import os
import rich 
from download import download
from pathlib import Path
from urllib.parse import urlparse


class HasIngestor(ABC): 
    @abstractmethod
    def ingest(self, file_path: str)-> pd.DataFrame: 
        pass 

class HasJson(HasIngestor): 
    def ingest(self, file_path: str) -> pd.DataFrame:
        if os.path.exists(file_path): 
            return pd.read_json(file_path)
        else : 
            raise FileNotFoundError("File path doesn't exist")
    
class HasCsv(HasIngestor): 
    def ingest(self, file_path: str) -> pd.DataFrame:
        if os.path.exists(file_path): 
            return pd.read_csv(file_path)
        else : 
            raise FileNotFoundError("File path doesn't exist")

class FetchHasFactory: 
    def start_ingest(self, file_path: str, file_type: str): 
        if file_type == "csv": return HasCsv().ingest(file_path)
        if file_type == "json": return HasJson().ingest(file_path)


def download_pdf(pdf_links: list): 
    output_dir = Path("raw/")
    output_dir.mkdir(parents=True, exist_ok=True)   
    for url in pdf_links:
        filename = Path(urlparse(url).path).name
        download(url, output_dir / filename)
     
def retrieve_document_links(df: pd.DataFrame)->list:
    # we retrieve the links corresponding to document download links
    document_retrieved =   [
    [doc["resolvedUrl"] for doc in df["documentLinkSet"][i]]
    for i in range(len(df["documentLinkSet"]))
    ]
    
    # we sanitize the links to only take every link that ends with .pdf 
    pdf_links = [
        url
        for sublist in document_retrieved
        for url in sublist
        if url.lower().split("?")[0].endswith(".pdf")
    ]
    return pdf_links

        
if __name__== "__main__": 
    file_path = "/Users/roch-joelcubahiro/Desktop/Projects/medsearch/data/raw/has-publications-split/json/RecommandationsProfessionnelles.json"
    data_ingestor = FetchHasFactory()
    df = data_ingestor.start_ingest(file_path, "json")
    # only run this once, it will download 1000+ pdf documents
    # download_pdf(retrieve_document_links(df))
    rich.print (retrieve_document_links(df))