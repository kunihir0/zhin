"""
Handles the extraction of text from various file types.
"""
from pathlib import Path
import fitz  # PyMuPDF
from logger import get_logger

log = get_logger(__name__)

def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extracts text content from a PDF file using PyMuPDF.
    """
    try:
        log.debug(f"Extracting text from PDF: {file_path}")
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        log.error(f"Failed to extract text from PDF {file_path}: {e}")
        return ""

def extract_text_from_markdown(file_path: Path) -> str:
    """
    Extracts text content from a Markdown file.
    """
    try:
        log.debug(f"Extracting text from Markdown: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        log.error(f"Failed to extract text from Markdown {file_path}: {e}")
        return ""

def extract_text(file_path: str) -> str:
    """
    Extracts text from a file based on its extension.
    """
    path = Path(file_path)
    if not path.exists():
        log.error(f"File not found: {file_path}")
        return ""

    if path.suffix == ".pdf":
        return extract_text_from_pdf(path)
    elif path.suffix == ".md":
        return extract_text_from_markdown(path)
    else:
        log.warning(f"Unsupported file type: {path.suffix}")
        return ""