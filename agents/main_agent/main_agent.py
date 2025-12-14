from agents.main_agent.pipeline import run_main_pipeline


def run_main_agent(rfp: dict) -> dict:
    """
    Public interface for Main Agent.
    Accepts selected RFP from Sales Agent and returns
    consolidated outputs for Technical & Pricing Agents.
    """
    return run_main_pipeline(rfp)
