from pydantic import BaseModel, HttpUrl
from datetime import date
import Section
from typing import final, Any 


@final 
class Section (BaseModel) : 
    title: str
    text: str 
    grade: str | None = None 

class Document(BaseModel):
    doc_id: int
    source: str | None 
    title: str | None
    sections: list[Section] = []
    lang: str | None = None 
    pub_date: date | None
    url : HttpUrl
    doc_type: str  
    metadata: dict[str, Any] = {}
    
