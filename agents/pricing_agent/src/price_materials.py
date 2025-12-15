# agents/pricing_agent/src/price_materials.py

def price_materials(technical_recos, product_prices):
    priced_items = []

    for item in technical_recos:
        best_oem = item["top_oem_recommendations"][0]

        sku = best_oem["sku"]
        unit_price = product_prices.get(sku, 0)

        priced_items.append({
            "rfp_item_id": item["rfp_item_id"],
            "category": item["category"],
            "sku": sku,
            "product_name": best_oem["product_name"],
            "unit_price": unit_price
        })

    return priced_items
