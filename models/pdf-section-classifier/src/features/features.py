from dataclasses import dataclass
from typing import Protocol
import re

class FeatureExtractor(Protocol): 
    def extract (self, LineContext: "LineContext") -> dict[str, any]:
        ... 
        

@dataclass
class PDFLine : 
    document_id: str
    page_number: int
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    font: str 
    font_size: float
    flags: int
    page_height: float 
    page_width: float
    
@dataclass
class LineContext: 
    previous: PDFLine
    line: PDFLine | None
    next: PDFLine | None


class TypographyExtractor(FeatureExtractor): 
    def extract(self, ctx: LineContext):
        Line = ctx.line
        return {
        "font": Line.font, 
        "font_size": LineContext.font_size
    }

class GeometryExtractor(FeatureExtractor): 
    def extract(self, ctx: LineContext): 
        Line = ctx.line
        return {
            "x_norm": Line.x0 / Line.page_width, 
            "y_norm": Line.y0 / Line.page_height, 
            "height_norm":(Line.y1 - Line.x0) / Line.page_height, 
            "width_norm": (Line.x1 - Line.x0) / Line.page_width
        }

class TextExtractor(FeatureExtractor): 
    def count_word(text: str) : 
        return len(re.findall(r'\b[a-zA-Z]+\b', text)) 

    def uppercase_ratio(text: str): 
        return sum(1 for c in text if c.isalpha() and c.isupper()) / sum(1 for c in text if c.isalpha())
    
    def starts_with_number(text: str) -> bool: 
        return text[0].isdigit()

    def ends_with_number(text: str) -> bool: 
        last_word = text.split()[-1]
        return bool(re.search("\w+\.$", last_word))
    
    def extract (self, ctx: LineContext): 
        Line = ctx.line
        return {
            "word_count":  self.count_word(Line.text), 
            "uppercase_ratio": self.uppercase_ratio(Line.text), 
            "starts_with_number": self.starts_with_number(Line.text),
            "ends_with_number": self.ends_with_number(Line.text)
        }