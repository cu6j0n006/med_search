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
                     
                    
    

@classmethod
def get_title(doc):
        meta_data = doc.metadata.get("title", "").strip()
        if meta_data:
            return meta_data
        page = doc[0]  # this a Page object
        blocks = page.get_text("dict")["blocks"]  #  May include text and images.
        max_size = 0
        title = ""
        for block in blocks:
            if block["type"] == 0 or "line" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > max_size or span["size"] == max_size:
                        # print(f"found new max_size {max_size} ")
                            max_size = span["size"]
                            title += span["text"]
        return title.strip()
    

    # TODO: add functions to extract sections and text
    @classmethod
    def get_sections(doc): 
        ...
        
    
    # TODO: add parsing pipeline
    
    # TODO: add grade detection using regex
    
    # TODO: extract publications dates