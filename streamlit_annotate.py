"""
Streamlit tool to annotate PDF lines as: header / body / header_footer / other.

Usage:
    pip install streamlit pymupdf
    streamlit run annotate_lines.py

Workflow:
    1. Point it at a folder of PDFs (sidebar).
    2. It extracts every line (via PyMuPDF get_text("dict")) from each PDF,
       with font metadata.
    3. You label lines one at a time. Each label is appended immediately to
       the output JSONL file (crash-safe, same convention as rejected.jsonl).
    4. Re-running resumes where you left off (already-labeled line_ids are
       skipped).
"""

import json
from pathlib import Path

import fitz  # PyMuPDF
import streamlit as st

st.set_page_config(page_title="PDF line annotator", layout="centered")

LABELS = ["header", "body", "header_footer", "other"]


# ---------- extraction ----------

def extract_lines(pdf_path: Path):
    """Yield one dict per line of text in the PDF, with font metadata."""
    doc = fitz.open(pdf_path)
    doc_id = pdf_path.stem
    idx = 0
    for page_num, page in enumerate(doc):
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:  # skip images
                continue
            for line in block["lines"]:
                spans = line["spans"]
                text = "".join(s["text"] for s in spans).strip()
                if not text:
                    continue
                first = spans[0]
                yield {
                    "line_id": f"{doc_id}_p{page_num}_l{idx}",
                    "doc_id": doc_id,
                    "page": page_num,
                    "text": text,
                    "font_size": round(first["size"], 1),
                    "font": first["font"],
                    "bold": "bold" in first["font"].lower(),
                    "bbox": [round(c, 1) for c in line["bbox"]],
                }
                idx += 1
    doc.close()


@st.cache_data(show_spinner="Extracting lines from PDFs...")
def build_line_pool(pdf_folder: str):
    pdf_folder = Path(pdf_folder)
    all_lines = []
    for pdf_path in sorted(pdf_folder.glob("*.pdf")):
        all_lines.extend(extract_lines(pdf_path))
    return all_lines


# ---------- output handling ----------

def load_labeled_ids(output_path: Path) -> set:
    if not output_path.exists():
        return set()
    ids = set()
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ids.add(json.loads(line)["line_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return ids


def append_label(output_path: Path, record: dict):
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------- UI ----------

st.title("📄 PDF line annotator")

with st.sidebar:
    pdf_folder = st.text_input("Folder of PDFs", value="pdfs")
    output_path_str = st.text_input("Output JSONL path", value="labels.jsonl")
    load = st.button("Load / reload", type="primary")

if load or "pool" not in st.session_state:
    if not Path(pdf_folder).is_dir():
        st.error(f"Folder not found: {pdf_folder}")
        st.stop()
    pool = build_line_pool(pdf_folder)
    labeled_ids = load_labeled_ids(Path(output_path_str))
    remaining = [l for l in pool if l["line_id"] not in labeled_ids]
    st.session_state.pool = pool
    st.session_state.remaining = remaining
    st.session_state.total = len(pool)
    st.session_state.output_path = Path(output_path_str)

if "remaining" not in st.session_state:
    st.info("Set a folder and click Load / reload to start.")
    st.stop()

remaining = st.session_state.remaining
total = st.session_state.total
done = total - len(remaining)

st.progress(done / total if total else 0, text=f"{done} / {total} labeled")

if not remaining:
    st.success("All lines labeled. 🎉")
    st.stop()

current = remaining[0]

st.caption(f"{current['doc_id']}  ·  page {current['page']}  ·  {current['line_id']}")

st.markdown(
    f"""
    <div style="border:1px solid #ddd; border-radius:8px; padding:16px;
                font-size:{min(max(current['font_size'], 10), 28)}px;
                font-weight:{'bold' if current['bold'] else 'normal'};">
        {current['text']}
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    f"**font_size:** {current['font_size']}  ·  "
    f"**bold:** {current['bold']}  ·  "
    f"**font:** {current['font']}"
)

st.write("")
cols = st.columns(len(LABELS))
for col, label in zip(cols, LABELS):
    if col.button(label, use_container_width=True):
        record = {**current, "label": label}
        append_label(st.session_state.output_path, record)
        st.session_state.remaining = st.session_state.remaining[1:]
        st.rerun()

st.write("")
if st.button("⏭ Skip (label as 'other', revisit later)"):
    record = {**current, "label": "other"}
    append_label(st.session_state.output_path, record)
    st.session_state.remaining = st.session_state.remaining[1:]
    st.rerun()