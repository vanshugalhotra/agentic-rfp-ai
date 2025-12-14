from urllib.parse import urljoin
from dateutil import parser


def normalize_metadata(raw_metadata: dict, source_url: str) -> dict:
    """
    Normalize LLM-extracted RFP metadata into a stable canonical format.
    """

    # --- Normalize date ---
    raw_date = raw_metadata.get("submission_due_date")
    try:
        submission_due_date = (
            parser.parse(raw_date, dayfirst=True).date().isoformat()
            if raw_date else None
        )
    except Exception:
        submission_due_date = None

    # --- Normalize PDF URL ---
    raw_pdf_url = raw_metadata.get("pdf_url")
    pdf_url = urljoin(source_url, raw_pdf_url) if raw_pdf_url else None

    return {
        "tender_reference": raw_metadata.get("tender_reference"),
        "tender_title": raw_metadata.get("tender_title"),
        "submission_due_date": submission_due_date,
        "pdf_url": pdf_url,
        "source_url": source_url
    }
