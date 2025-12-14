from agents.main_agent.src.resolve.prompt import (
    TECHNICAL_SUMMARY_PROMPT,
    PRICING_SUMMARY_PROMPT
)


def resolve_rfp_summaries(llm_client, product_table, testing_text):
    """
    Generates role-specific summaries using LLM:
    - Technical summary for Technical Agent
    - Pricing summary for Pricing Agent
    """

    # -------------------------------
    # Build input for Technical Summary
    # -------------------------------
    if product_table:
        technical_input_blocks = []
        for product in product_table:
            block = [
                f"Product {product.get('rfp_item_id')}:"
            ]
            block.extend(product.get("raw_block", []))
            technical_input_blocks.append("\n".join(block))

        technical_input = "\n\n".join(technical_input_blocks)
    else:
        technical_input = "No technical product details were extracted."

    technical_prompt = f"""
{TECHNICAL_SUMMARY_PROMPT}

INPUT:
{technical_input}
"""

    technical_summary = llm_client.generate(technical_prompt)

    # -------------------------------
    # Build input for Pricing Summary
    # -------------------------------
    if testing_text:
        pricing_input = "\n".join(testing_text)
    else:
        pricing_input = "No testing or acceptance requirements were extracted."

    pricing_prompt = f"""
{PRICING_SUMMARY_PROMPT}

INPUT:
{pricing_input}
"""

    pricing_summary = llm_client.generate(pricing_prompt)

    return {
        "technical_summary": technical_summary.strip(),
        "pricing_summary": pricing_summary.strip()
    }
