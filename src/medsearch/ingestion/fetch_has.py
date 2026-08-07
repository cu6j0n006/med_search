from abc import ABC, abstractmethod
import pandas as pd

class HasIngestor(ABC): 
    @abstractmethod
    def ingest(self, file_path: str)-> pd.DataFrame: 
        pass 


class fetchHas(HasIngestor): 
    def ingest(file_path: str) -> pd.DataFrame: 
        if not file_path.endswith(""): 
            ...