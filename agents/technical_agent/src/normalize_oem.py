# agents/technical_agent/src/normalize_oem.py

def normalize_oem_product(oem: dict) -> dict:
    return {
        # ✅ PRESERVE IDENTITY
        "SKU": oem.get("SKU"),
        "Product_Name": oem.get("Product_Name"),

        # ✅ NORMALIZED COMPARISON FIELDS
        "category": oem.get("Category"),
        "cable_type": oem.get("Cable_Type"),
        "armored": oem.get("Armored") == "Y",
        "conductor_material": oem.get("Conductor_Material"),
        "conductor_size": oem.get("Conductor_Size"),
        "voltage_rating": oem.get("Voltage_Rating_V"),
        "standards": oem.get("Standards")
    }
