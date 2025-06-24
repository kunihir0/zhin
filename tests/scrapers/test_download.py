"""
Tests for the download functionality.
"""
import pytest
from pathlib import Path
from scrapers.nnols_scrapers import download_file

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url",
    [
        "https://www.nnols.org/wp-content/uploads/2022/05/1-5.pdf",
        "https://www.nnols.org/wp-content/uploads/2022/05/5A-12.pdf",
        "https://www.nnols.org/wp-content/uploads/2022/05/13-20.pdf",
        "https://www.nnols.org/wp-content/uploads/2022/05/21-26.pdf",
    ],
)
async def test_download_file(url: str, tmp_path: Path):
    """
    Tests that the download_file function downloads a file.
    """
    file_name = url.split("/")[-1]
    download_path = tmp_path / file_name
    await download_file(url, download_path)
    assert download_path.exists()