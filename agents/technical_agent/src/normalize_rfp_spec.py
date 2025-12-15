import re
from typing import List, Dict


def normalize_rfp_specs(
    product_table: List[Dict],
    technical_summary: str
) -> List[Dict]:
    """
    Normalize RFP product requirements into a strict,
    comparable schema aligned with OEM datasheets.

    Returns one normalized spec dict per RFP item.
    """

    normalized_items = []

    for item in product_table:
        spec = {
            "rfp_item_id": item.get("rfp_item_id"),
            "category": normalize_text(item.get("category")),
            "cable_type": normalize_text(item.get("cable_type")),
            "armored": extract_armored(item),
            "conductor_material": normalize_text(item.get("conductor_material")),
            "conductor_size": normalize_conductor_size(
                item.get("conductor_size")
            ),
            "voltage_rating_v": extract_voltage(item),
            "standards": normalize_standards(item),
            "raw_block": item.get("raw_block", [])
        }

        normalized_items.append(spec)

    return normalized_items


# --------------------------------------------------
# Helpers (deterministic, no AI)
# --------------------------------------------------

def normalize_text(value):
    if not value:
        return None
    return value.strip().lower()


def extract_armored(item: Dict):
    raw = " ".join(item.get("raw_block", [])).lower()
    if "armored yes" in raw or "armoured yes" in raw:
        return "Y"
    if "armored no" in raw or "armoured no" in raw:
        return "N"
    return None


def extract_voltage(item: Dict):
    if "voltage_rating" in item:
        return normalize_voltage(item["voltage_rating"])

    raw = " ".join(item.get("raw_block", []))
    match = re.search(r"(\d+)\s*k?v", raw, re.IGNORECASE)
    if match:
        return normalize_voltage(match.group(1))
    return None


def normalize_voltage(value):
    value = str(value).lower()
    if "kv" in value:
        return int(float(value.replace("kv", "").strip()) * 1000)
    return int(re.sub(r"\D", "", value))


def normalize_conductor_size(value):
    if not value:
        return None
    value = value.lower().replace("sqmm", "").replace("mm²", "").strip()
    return value


def normalize_standards(item: Dict):
    raw = " ".join(item.get("raw_block", []))
    standards = []

    if "iec" in raw.lower():
        standards.append("IEC")
    if "is " in raw.lower():
        standards.append("IS")

    return list(set(standards)) if standards else None
