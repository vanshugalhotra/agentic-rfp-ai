from agents.pricing_agent.src.validate_input import validate_pricing_input
from agents.pricing_agent.src.load_pricing import (
    load_product_prices,
    load_test_prices
)
from agents.pricing_agent.src.compute_pricing import compute_pricing

PRODUCT_PRICE_CSV = "data/product_pricing.csv"
TEST_PRICE_CSV = "data/test_pricing.csv"


def run_pricing_pipeline(main_result: dict) -> dict:
    """
    Pricing Agent Pipeline

    Flow:
    Main Agent
        ↓
    Technical recommendations + testing requirements
        ↓
    Pricing Agent
        ↓
    Consolidated pricing table
    """

    # --------------------------------------------------
    # Step 1: Validate input from Main Agent
    # --------------------------------------------------
    validated = validate_pricing_input(main_result)

    technical_recommendations = validated["technical_recommendations"]
    pricing_summary = validated["pricing_summary"]

    # --------------------------------------------------
    # Step 2: Load pricing repositories (CSV)
    # --------------------------------------------------
    product_prices = load_product_prices(PRODUCT_PRICE_CSV)
    test_prices = load_test_prices(TEST_PRICE_CSV)

    # --------------------------------------------------
    # Step 3: Compute pricing
    # --------------------------------------------------
    pricing_result = compute_pricing(
    technical_recommendations=technical_recommendations,
    pricing_summary=pricing_summary,   # ✅ CORRECT NAME
    product_prices=product_prices,
    test_prices=test_prices
    )


    # --------------------------------------------------
    # Final output (to Main Agent)
    # --------------------------------------------------
    return {
    "status": "Pricing Agent completed",
    "materials": pricing_result["materials"],
    "tests": pricing_result["tests"],
    "total_material_cost": pricing_result["total_material_cost"],
    "total_test_cost": pricing_result["total_test_cost"],
    "grand_total": pricing_result["grand_total"]
    }
