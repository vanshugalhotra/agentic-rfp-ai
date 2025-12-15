# agents/pricing_agent/src/load_pricing_tables.py

import csv

def load_product_prices(path="data/product_pricing.csv"):
    prices = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            prices[row["SKU"]] = float(row["Unit_Price"])
    return prices


def load_test_prices(path="data/test_pricing.csv"):
    prices = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            prices[row["Test_Name"]] = float(row["Price"])
    return prices
