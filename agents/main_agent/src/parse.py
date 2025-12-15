import csv
import os
import re
from typing import List, Dict


# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------
def sanitize_filename(text: str) -> str:
    """
    Makes a string safe to use as a filename.
    """
    return (
        text.replace("/", "_")
            .replace("\\", "_")
            .replace(" ", "_")
            .replace(":", "_")
    )


# ---------------------------------------------------------
# PRODUCT TABLE BUILDER
# ---------------------------------------------------------
def build_product_table(technical_text: List[str]) -> List[Dict]:
    """
    Builds a structured product table from extracted technical text.

    Supports:
    - Section-based RFPs (4.1, 4.2)
    - Item-based RFPs (Item 1, Item 2)
    - Bullet-based specifications
    - Free-text specification blocks
    """

    products = []
    current_product = {}
    current_block = []
    item_id = 1

    def finalize_product():
        nonlocal item_id, current_product, current_block
        if current_block:
            current_product["rfp_item_id"] = item_id
            current_product["raw_block"] = current_block
            products.append(current_product)
            item_id += 1
        current_product = {}
        current_block = []

    for line in technical_text:
        text = line.strip()
        if not text:
            continue

        # -------------------------------------------------
        # Detect new product block
        # -------------------------------------------------
        if (
            re.match(r"^\d+\.\d+", text) or
            re.match(r"^item\s+\d+", text, re.I)
        ):
            finalize_product()
            current_block.append(text)

            current_product["category"] = text
            continue

        current_block.append(text)
        lower = text.lower()

        # -------------------------------------------------
        # Attribute extraction (heuristics, NOT brittle)
        # -------------------------------------------------
        if "xlpe" in lower:
            current_product["cable_type"] = "XLPE Insulated"
        elif "pvc" in lower:
            current_product["cable_type"] = "PVC Insulated"

        if "armour" in lower or "armored" in lower:
            current_product["armored"] = "Yes"
        elif "unarmoured" in lower or "unarmored" in lower:
            current_product["armored"] = "No"

        if "aluminium" in lower:
            current_product["conductor_material"] = "Aluminium"
        elif "copper" in lower:
            current_product["conductor_material"] = "Copper"

        size_match = re.search(r"(\d+(\.\d+)?)\s*sqmm", lower)
        if size_match:
            current_product["conductor_size"] = f"{size_match.group(1)} sqmm"

        voltage_match = re.search(r"(\d+(\.\d+)?)\s*(k?v)", lower)
        if voltage_match:
            unit = voltage_match.group(3).upper()
            current_product["voltage_rating"] = f"{voltage_match.group(1)} {unit}"

        if "iec" in lower or "is " in lower or "bs " in lower:
            current_product["standards"] = text

    finalize_product()
    return products


# ---------------------------------------------------------
# CSV EXPORTER
# ---------------------------------------------------------
def export_product_table_to_csv(
    product_table: List[Dict],
    tender_reference: str,
    output_dir: str = "data/outputs"
) -> str | None:
    """
    Exports product table to CSV in a filesystem-safe way.
    """

    if not product_table:
        return None

    os.makedirs(output_dir, exist_ok=True)

    safe_ref = sanitize_filename(tender_reference)

    file_path = os.path.join(
        output_dir,
        f"rfp_products_{safe_ref}.csv"
    )

    # Collect all unique keys dynamically
    fieldnames = set()
    for row in product_table:
        fieldnames.update(row.keys())

    fieldnames = sorted(fieldnames)

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in product_table:
            writer.writerow(row)

    return file_path
