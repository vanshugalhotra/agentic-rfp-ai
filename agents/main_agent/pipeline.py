import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from agents.main_agent.src.load_pdf import load_rfp_pdf
from agents.main_agent.src.summary import extract_role_relevant_text
from agents.main_agent.src.parse import (
    build_product_table,
    export_product_table_to_csv
)
from agents.main_agent.src.resolve.resolver import resolve_rfp_summaries
from agents.technical_agent import run_technical_agent
from core.llm.ollama_client import OllamaLLM


def run_main_pipeline(rfp: dict) -> dict:
    """
    Core pipeline for Main Agent.
    - Orchestrates Sales → Technical → (Pricing later)
    - Acts as the single source of truth
    """

    if not rfp or "rfp_pdf_path" not in rfp:
        raise ValueError("Invalid RFP input to Main Agent")

    # -------------------------------
    # Step 1: Load RFP PDF
    # -------------------------------
    pdf_data = load_rfp_pdf(rfp["rfp_pdf_path"])

    # -------------------------------
    # Step 2: Extract role-relevant text
    # -------------------------------
    relevant_text = extract_role_relevant_text(pdf_data["full_text"])

    # -------------------------------
    # Step 3: Build structured product table
    # -------------------------------
    product_table = build_product_table(
        relevant_text["technical_text"]
    )

    # -------------------------------
    # Step 4: Export product table CSV
    # -------------------------------
    csv_path = export_product_table_to_csv(
        product_table,
        rfp.get("tender_reference", "unknown_rfp")
    )

    # -------------------------------
    # Step 5: Generate summaries (AI)
    # -------------------------------
    llm = OllamaLLM(model="llama3.2")

    summaries = resolve_rfp_summaries(
        llm_client=llm,
        product_table=product_table,
        testing_text=relevant_text["testing_text"]
    )
    # -------------------------------
    # Final consolidated output
    # -------------------------------
    return {
        "rfp_metadata": rfp,
        "pdf_info": {
            "path": pdf_data["rfp_pdf_path"],
            "num_pages": pdf_data["num_pages"]
        },
        "product_table": product_table,
        "product_csv": csv_path,
        "technical_summary": summaries["technical_summary"],
        "pricing_summary": summaries["pricing_summary"],
    }
