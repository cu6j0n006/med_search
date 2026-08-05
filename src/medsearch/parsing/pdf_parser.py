from dataclasses import dataclass


@dataclass
class HasDocument:
    def __init__(self, path):
        self.path = path

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
    
    # TODO: add parsing pipeline
    
    # TODO: add grade detection using regex
    
    # TODO: extract publications dates
