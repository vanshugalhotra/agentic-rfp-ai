from agents.main_agent.pipeline import run_main_pipeline
from agents.technical_agent import run_technical_agent
from agents.pricing_agent import run_pricing_agent

from agents.main_agent.src.consolidate_response import consolidate_rfp_response
from agents.main_agent.src.generate_pdf import generate_rfp_response_pdf


def run_main_agent(rfp: dict) -> dict:
    """
    Orchestrates Main → Technical → Pricing
    and generates final consolidated RFP response PDF
    """

    # -------------------------------------------------
    # Step 1: Run Main Agent pipeline
    # -------------------------------------------------
    main_result = run_main_pipeline(rfp)

    # -------------------------------------------------
    # Step 2: Run Technical Agent
    # -------------------------------------------------
    technical_result = run_technical_agent(main_result)

    # -------------------------------------------------
    # Step 3: Run Pricing Agent
    # NOTE: Pricing Agent receives data VIA Main Agent
    # -------------------------------------------------
    pricing_result = run_pricing_agent({
        **main_result,
        "technical_recommendations": technical_result["rfp_items"]
    })

    # -------------------------------------------------
    # Step 4: Consolidate final RFP response
    # -------------------------------------------------
    final_rfp_response = consolidate_rfp_response(
        main_result=main_result,
        technical_result=technical_result,
        pricing_result=pricing_result
    )

    # -------------------------------------------------
    # Step 5: Generate PDF
    # -------------------------------------------------
    pdf_path = (
        f"data/outputs/RFP_RESPONSE_"
        f"{main_result['rfp_metadata']['tender_reference']}.pdf"
    )

    generate_rfp_response_pdf(final_rfp_response, pdf_path)

    # -------------------------------------------------
    # Step 6: Return EVERYTHING (single source of truth)
    # -------------------------------------------------
    return {
        **main_result,
        "technical_recommendations": technical_result["rfp_items"],
        "pricing": pricing_result,
        "final_rfp_response": final_rfp_response,
        "final_pdf_path": pdf_path
    }
