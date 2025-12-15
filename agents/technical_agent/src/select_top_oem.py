# agents/technical_agent/src/select_top_oem.py

from agents.technical_agent.src.match_specs import match_specs
from agents.technical_agent.src.score import calculate_score


def select_top_oem_products(rfp_product: dict, oem_products: list, top_n: int = 3):
    results = []

    rfp_specs = rfp_product["normalized_specs"]

    for oem in oem_products:
        match_result = match_specs(rfp_specs, oem)
        score = calculate_score(match_result["matched"], match_result["total"])

        results.append({
            "sku": oem.get("SKU"),
            "product_name": oem.get("Product_Name"),
            "score": round(score, 2),
            "match_details": match_result["details"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
