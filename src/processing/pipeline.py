"""
Main pipeline for Phase 2: Data Processing and Storage.
"""
from pathlib import Path
from logger import get_logger
from processing.text_extraction import extract_text
from processing.chunking import chunk_text_by_paragraph
from processing.metadata_extraction import extract_metadata
from progress import ProgressBar

log = get_logger(__name__)

def run_text_extraction_pipeline():
    """
    Runs the text extraction process for all files in the data directory.
    """
    log.info("Starting Phase 2: Text Extraction Pipeline...")
    data_dir = Path("data")
    
    # Find all relevant files
    files_to_process = list(data_dir.glob("**/*.pdf")) + list(data_dir.glob("**/*.md"))
    log.info(f"Found {len(files_to_process)} files to process.")

    if not files_to_process:
        log.warning("No files found to process. Exiting.")
        return

    progress_bar = ProgressBar(len(files_to_process), text="Extracting Text")
    
    for file_path in files_to_process:
        log.debug(f"Processing file: {file_path}")
        text = extract_text(str(file_path))
        if text:
            chunks = chunk_text_by_paragraph(text)
            metadata = extract_metadata(file_path, text)
            
            # For demonstration, log the extracted metadata.
            log.info(f"Extracted metadata for {file_path.name}: {metadata['title']}")

            if not chunks:
                log.warning(f"Could not chunk text from {file_path.name}")
        else:
            log.warning(f"No text extracted from {file_path.name}")
        progress_bar.update()

    progress_bar.finish()
    log.info("Text extraction pipeline complete.")