from agents.sales_agent import run_sales_agent
from agents.main_agent import run_main_agent


print("\n================ MAIN AGENT TEST START ================\n")

# ------------------------------------------------------
# Step 1: Run Sales Agent
# ------------------------------------------------------

rfp = run_sales_agent()
# rfp = run_sales_agent("2026-09-09")  # optional test case

if not rfp:
    raise ValueError("Sales Agent did not return an RFP")

# ------------------------------------------------------
# Step 2: Run Main Agent (single entrypoint)
# ------------------------------------------------------

result = run_main_agent(rfp)

# ------------------------------------------------------
# Step 3: Display Outputs (test-only responsibility)
# ------------------------------------------------------

print("RFP Reference    :", result["rfp_metadata"].get("tender_reference"))
print("PDF Path         :", result["pdf_info"]["path"])
print("Pages Extracted  :", result["pdf_info"]["num_pages"])

print("\n--- Product Table (Structured Output) ---")
if result["product_table"]:
    for product in result["product_table"]:
        print(product)
else:
    print("No products extracted.")

print("\n--- Technical Summary (for Technical Agent) ---")
print(result["technical_summary"])

print("\n--- Pricing Summary (for Pricing Agent) ---")
print(result["pricing_summary"])

print("\n================ MAIN AGENT TEST END =================\n")
