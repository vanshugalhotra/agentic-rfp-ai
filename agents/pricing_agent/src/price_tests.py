# agents/pricing_agent/src/price_tests.py

def price_tests(pricing_summary: str, test_prices: dict):
    applied_tests = []

    summary_lower = pricing_summary.lower()

    for test_name, price in test_prices.items():
        if test_name.lower() in summary_lower:
            applied_tests.append({
                "test_name": test_name,
                "price": price
            })

    return applied_tests
