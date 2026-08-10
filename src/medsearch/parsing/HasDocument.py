from datetime import date
from typing import Any, final

import Section
from pydantic import BaseModel, HttpUrl


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
    
