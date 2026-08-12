from dataclasses import dataclass

@dataclass
class RawSpan:
    text: str
    size: float
    bold: bool
    page: int
    bbox: tuple[float, float, float, float]

@dataclass
class ParsedSection: 
    title: str
    text: str
    grade: str | None
    order: int


@dataclass
class parsedDocument : 
    title: str
    sections: list[ParsedSection]
    full_text: str

# TODO: calculate how to now if text is bold or not
def extract_spans(doc) -> list[RawSpan]: 
    spans: list[RawSpan] = []
    meta_data = doc.metadata.get("title", "").strip()
    if meta_data:
        return meta_data
    for page_index, page in enumerate(doc):
        raw_page = page.get_text("dict")
        for block in raw_page.get("blocks", []): 
            if block.get("type") != 0:  # text only (0 = texte, 1 = image)
                continue
            if block["type"] == 0 or "line" in block:
             for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text: 
                        continue 
                    font_flag = span.get ("flags", 0)
                    is_bold = True # for now
                    spans.add(RawSpan(
                        text=text, 
                        size=round(span.get("size", 0.0), 1),
                        bold=is_bold, 
                        page=page_index, 
                        bbox=span.get("bbox", (0, 0, 0, 0))
                    ))

def extract_title(spans: list[RawSpan]):
        first_page_spans = [s for s in spans if s.page == 0]
        if not first_page_spans: 
            return ""
        return max(first_page_spans, key=lambda s: s.size ).text

# TODO: add functions to extract sections and text

def extract_sections(doc): 
        ...
        
    
    # TODO: add parsing pipeline
    
    # TODO: add grade detection using regex
    
    # TODO: extract publications dates