import os
import uuid
import requests
from urllib.parse import urljoin, urlparse
from config import DOWNLOADS_DIR 


def download_pdf(pdf_url: str, source_url: str) -> str:
    """
    Downloads RFP PDF and saves it at project_root/data/downloads
    Returns absolute path of saved PDF.
    """

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    full_pdf_url = urljoin(source_url, pdf_url)

    parsed = urlparse(full_pdf_url)
    base_name = os.path.basename(parsed.path) or "rfp.pdf"
    unique_id = uuid.uuid4().hex[:8]

    filename = f"rfp_{unique_id}_{base_name}"
    file_path = os.path.join(DOWNLOADS_DIR, filename)

    response = requests.get(full_pdf_url, timeout=20)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path
