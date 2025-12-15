def compute_pricing(
    technical_recommendations,
    pricing_summary,
    product_prices,
    test_prices
):
    # -------------------------------
    # MATERIAL PRICING
    # -------------------------------
    material_rows = []
    total_material_cost = 0

    for item in technical_recommendations:
        top_oem = item["top_oem_recommendations"][0]  # Top-1 OEM
        sku = top_oem["sku"]

        unit_price = product_prices.get(sku, 0)
        total_material_cost += unit_price

        material_rows.append({
            "rfp_item_id": item["rfp_item_id"],
            "sku": sku,
            "product_name": top_oem["product_name"],
            "unit_price": unit_price
        })

    # -------------------------------
    # TEST / SERVICE PRICING
    # -------------------------------
    test_rows = []
    total_test_cost = 0
    pricing_summary_text = pricing_summary.lower()

    for test in test_prices:
        test_name = test["Test_Name"]
        applicable_to = test["Applicable_To"].lower()
        price = float(test["Test_Cost_Rs"])

        # Simple applicability logic (demo-correct)
        if applicable_to == "all cables" or applicable_to in pricing_summary_text:
            total_test_cost += price
            test_rows.append({
                "test_name": test_name,
                "applicable_to": test["Applicable_To"],
                "price": price
            })

    # -------------------------------
    # FINAL OUTPUT
    # -------------------------------
    return {
        "materials": material_rows,
        "tests": test_rows,
        "total_material_cost": total_material_cost,
        "total_test_cost": total_test_cost,
        "grand_total": total_material_cost + total_test_cost
    }
