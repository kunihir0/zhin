"""
Handles the extraction of metadata from text content and file paths.
"""
from pathlib import Path
import re
from typing import Dict, Any
from logger import get_logger

log = get_logger(__name__)

def extract_metadata(file_path: Path, text_content: str) -> Dict[str, Any]:
    """
    Extracts metadata from a given file and its content.

    This function will serve as a dispatcher to more specific extraction
    logic based on the file type or source.

    Args:
        file_path: The path to the file.
        text_content: The text content of the file.

    Returns:
        A dictionary containing the extracted metadata.
    """
    metadata = {
        "source": "unknown",
        "title": file_path.stem,
        "original_path": str(file_path),
    }
    log.debug(f"Extracting metadata for {file_path.name}")

    # Determine the source from the path
    parts = file_path.parts
    if "opvp" in parts:
        metadata["source"] = "OPVP"
    elif "navajonationcouncil" in parts:
        metadata["source"] = "Navajo Nation Council"
    elif "courts" in parts:
        metadata["source"] = "Navajo Nation Courts"
    elif "nndoj" in parts:
        metadata["source"] = "Navajo Nation Department of Justice"
    elif "nnols" in parts:
        metadata["source"] = "Navajo Nation Office of Legislative Services"

    # Add more specific metadata extraction logic here based on source...
    # Example: Use regex to find a resolution number if it exists
    resolution_match = re.search(r'([A-Z]{2,3}-\d{2,3}-\d{2})', text_content)
    if resolution_match:
        metadata['resolution_number'] = resolution_match.group(1)

    return metadata