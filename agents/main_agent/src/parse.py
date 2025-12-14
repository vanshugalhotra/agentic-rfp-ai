import re
import csv
import os
from typing import List, Dict


def build_product_table(technical_text: List[str]) -> List[Dict]:
    products = []
    current_product = None
    current_block = []
    item_id = 1

    def finalize():
        nonlocal current_product, current_block, item_id
        if current_product:
            current_product["rfp_item_id"] = item_id
            current_product["raw_block"] = current_block
            products.append(current_product)
            item_id += 1
        current_product = None
        current_block = []

    for line in technical_text:
        line = line.strip()
        if not line:
            continue

        # --- Section header detection ---
        header_match = re.match(r"^\d+\.\d+\s+(.*)", line)
        if header_match:
            finalize()
            current_product = {
                "category": header_match.group(1)
            }
            current_block.append(line)
            continue

        if not current_product:
            continue

        current_block.append(line)
        text = line.lower()

        # --- Attribute extraction ---
        if "xlpe" in text:
            current_product["cable_type"] = "XLPE Insulated"
        elif "pvc" in text:
            current_product["cable_type"] = "PVC Insulated"

        if "armour" in text:
            current_product["armored"] = "Yes" if "unarm" not in text else "No"

        if "aluminium" in text:
            current_product["conductor_material"] = "Aluminium"
        elif "copper" in text:
            current_product["conductor_material"] = "Copper"

        size_match = re.search(r"(\d+(\.\d+)?)\s*sqmm", text)
        if size_match:
            current_product["conductor_size"] = f"{size_match.group(1)} sqmm"

        voltage_match = re.search(r"(\d+\.?\d*)\s*kV", text, re.I)
        if voltage_match:
            current_product["voltage_rating"] = f"{voltage_match.group(1)} kV"

        if "standard" in text or "iec" in text or "is " in text:
            current_product["standards"] = line.split(":")[-1].strip()

    finalize()
    return products


def export_product_table_to_csv(products: List[Dict], tender_ref: str):
    if not products:
        return None

    os.makedirs("data/outputs", exist_ok=True)
    path = f"data/outputs/rfp_products_{tender_ref}.csv"

    keys = sorted({k for p in products for k in p.keys()})

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for p in products:
            writer.writerow(p)

    return path
