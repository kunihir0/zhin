"""
Handles the chunking of text into smaller, semantically meaningful units.
"""
import re
from typing import List
from logger import get_logger

log = get_logger(__name__)

def chunk_text_by_paragraph(text: str) -> List[str]:
    """
    Splits a block of text into paragraphs.

    A paragraph is considered to be a block of text separated by one or more
    blank lines.
    """
    try:
        # Split by one or more newline characters
        paragraphs = re.split(r'\n\s*\n', text)
        # Filter out any empty strings that may result from the split
        return [p.strip() for p in paragraphs if p.strip()]
    except Exception as e:
        log.error(f"Failed to chunk text into paragraphs: {e}")
        return []