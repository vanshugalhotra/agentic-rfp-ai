from .pipeline import run_technical_pipeline


def run_technical_agent(main_agent_output: dict) -> dict:
    """
    Public interface for Technical Agent.

    Accepts consolidated output from Main Agent and returns
    technical recommendations for OEM SKU matching.

    Input:
    - main_agent_output: dict containing product_table and technical_summary

    Output:
    - Technical Agent result (SKU recommendations, comparison tables, etc.)
    """
    return run_technical_pipeline(main_agent_output)
