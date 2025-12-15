# agents/technical_agent/src/match_specs.py

def match_specs(rfp_specs: dict, oem_product: dict) -> dict:
    """
    Compares normalized RFP specs with OEM product specs.
    Returns match details and score components.
    """

    total = 0
    matched = 0
    details = {}

    for key, rfp_value in rfp_specs.items():
        if rfp_value in (None, [], ""):
            continue  # ignore missing RFP specs

        total += 1
        oem_value = oem_product.get(key) or oem_product.get(key.upper())

        is_match = False

        if oem_value is None:
            is_match = False
        elif isinstance(rfp_value, list):
            is_match = any(str(v).lower() in str(oem_value).lower() for v in rfp_value)
        else:
            is_match = str(rfp_value).lower() in str(oem_value).lower()

        if is_match:
            matched += 1

        details[key] = {
            "rfp": rfp_value,
            "oem": oem_value,
            "match": is_match
        }

    return {
        "matched": matched,
        "total": total,
        "details": details
    }
