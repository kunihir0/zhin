"""
Tests for the text extraction functionality.
"""
import pytest
from pathlib import Path
import fitz  # PyMuPDF
from src.processing.text_extraction import extract_text

def test_extract_text_from_pdf(tmp_path: Path):
    """
    Tests that text is correctly extracted from a PDF file.
    """
    pdf_path = tmp_path / "test.pdf"
    expected_text = "This is a test PDF document."

    # Create a dummy PDF for testing
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), expected_text)
    doc.save(pdf_path)
    doc.close()

    # Extract text and verify
    extracted_text = extract_text(str(pdf_path))
    assert expected_text in extracted_text

def test_extract_text_from_markdown(tmp_path: Path):
    """
    Tests that text is correctly extracted from a Markdown file.
    """
    md_path = tmp_path / "test.md"
    expected_text = "# Test Markdown\n\nThis is a test."
    md_path.write_text(expected_text, encoding="utf-8")

    # Extract text and verify
    extracted_text = extract_text(str(md_path))
    assert extracted_text == expected_text

def test_extract_unsupported_file_type(tmp_path: Path):
    """
    Tests that an unsupported file type returns an empty string.
    """
    unsupported_path = tmp_path / "test.txt"
    unsupported_path.write_text("This is a test.", encoding="utf-8")

    extracted_text = extract_text(str(unsupported_path))
    assert extracted_text == ""

def test_extract_nonexistent_file():
    """
    Tests that a non-existent file returns an empty string.
    """
    non_existent_path = "non_existent_file.xyz"
    extracted_text = extract_text(non_existent_path)
    assert extracted_text == ""