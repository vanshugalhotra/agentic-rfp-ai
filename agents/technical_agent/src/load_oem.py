import csv
import os
from typing import List, Dict


DEFAULT_OEM_CSV_PATH = "data/oem_products.csv"

OEM_REQUIRED_COLUMNS = [
    "SKU",
    "Product_Name",
    "Category",
    "Cable_Type",
    "Armored",
    "Conductor_Material",
    "Conductor_Size",
    "Voltage_Rating_V",
    "Standards"
]


def load_oem_products(csv_path: str = DEFAULT_OEM_CSV_PATH) -> List[Dict]:
    """
    Loads OEM product repository from CSV.
    Enforces required columns for spec matching.
    """

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"OEM repository not found: {csv_path}")

    products = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        missing = set(OEM_REQUIRED_COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"OEM CSV missing columns: {missing}")

        for row in reader:
            # Normalize values
            clean_row = {
                key.strip(): (value.strip() if value else "")
                for key, value in row.items()
            }
            products.append(clean_row)

    if not products:
        print("⚠️ OEM repository loaded but contains no rows")

    print(f"✔ Loaded {len(products)} OEM products")

    return products
