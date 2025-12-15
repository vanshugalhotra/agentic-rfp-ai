import csv
import os


DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "data",
    "product.csv"
)


def load_oem_datasheet() -> list:
    """
    Loads OEM product datasheets from CSV and returns
    a list of structured product dictionaries.

    Returns:
        List[Dict]: Each dict represents one SKU with specs
    """

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"OEM product file not found at {DATA_PATH}")

    datasheets = []

    with open(DATA_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            normalized_row = {
                normalize_key(k): normalize_value(v)
                for k, v in row.items()
            }
            datasheets.append(normalized_row)

    return datasheets


def normalize_key(key: str) -> str:
    """
    Normalize CSV headers into snake_case keys.
    """
    return key.strip().lower().replace(" ", "_")


def normalize_value(value: str):
    """
    Normalize CSV values.
    - Strip whitespace
    - Convert empty strings to None
    """
    if value is None:
        return None

    value = value.strip()
    return value if value else None
