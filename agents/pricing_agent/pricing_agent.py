from agents.pricing_agent.pipeline import run_pricing_pipeline


def run_pricing_agent(main_result: dict) -> dict:
    return run_pricing_pipeline(main_result)
