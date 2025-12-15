def consolidate_rfp_response(
    main_result: dict,
    technical_result: dict,
    pricing_result: dict
) -> dict:
    products = []

    for item in pricing_result["materials"]:
        products.append({
            "rfp_item_id": item["rfp_item_id"],
            "sku": item["sku"],
            "product_name": item["product_name"],
            "unit_price": item["unit_price"]
        })

    tests = pricing_result["tests"]

    return {
        "rfp_reference": main_result["rfp_metadata"]["tender_reference"],
        "products": products,
        "tests": tests,
        "totals": {
            "material_cost": pricing_result["total_material_cost"],
            "test_cost": pricing_result["total_test_cost"],
            "grand_total": pricing_result["grand_total"]
        }
    }
