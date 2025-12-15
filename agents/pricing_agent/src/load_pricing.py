import csv


def load_product_prices(csv_path: str) -> dict:
    """
    Loads material pricing based on SKU
    Returns: { SKU: Unit_Price }
    """
    prices = {}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            prices[row["SKU"]] = float(row["Unit_Price"])

    return prices


def load_test_prices(csv_path: str) -> list:
    """
    Loads test pricing with applicability rules
    Returns: list of dicts (row-wise)
    Keys preserved to match compute_pricing()
    """
    tests = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            tests.append({
                "Test_Name": row["Test_Name"],
                "Applicable_To": row["Applicable_To"],
                "Test_Cost_Rs": float(row["Test_Cost_Rs"])
            })

    return tests
