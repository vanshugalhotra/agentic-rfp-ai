# agents/technical_agent/src/validate_input.py

def validate_technical_input(main_result: dict) -> list:
    """
    Validates input received from Main Agent.
    Returns product_table if valid.
    """

    if not main_result:
        raise ValueError("Technical Agent received empty input")

    if "product_table" not in main_result:
        raise KeyError("Main Agent output missing 'product_table'")

    product_table = main_result["product_table"]

    if not isinstance(product_table, list):
        raise TypeError("product_table must be a list")

    if len(product_table) == 0:
        print("⚠️ No products found in Scope of Supply")
        return []

    filtered_products = []

    for product in product_table:
        if any([
            product.get("voltage_rating"),
            product.get("conductor_size"),
            product.get("conductor_material"),
            product.get("cable_type")
        ]):
            filtered_products.append(product)

    if not filtered_products:
        print("⚠️ No valid technical products found")

    return filtered_products

