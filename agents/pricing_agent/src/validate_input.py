def validate_pricing_input(main_result: dict) -> dict:
    """
    Validates input received from Main Agent.
    """

    if not main_result:
        raise ValueError("Pricing Agent received empty input")

    if "technical_recommendations" not in main_result:
        raise KeyError("Missing technical_recommendations in Main Agent output")

    if "pricing_summary" not in main_result:
        raise KeyError("Missing pricing_summary in Main Agent output")

    return {
        "technical_recommendations": main_result["technical_recommendations"],
        "pricing_summary": main_result["pricing_summary"]
    }
