import streamlit as st
import time
import inspect
import os

from agents.sales_agent.pipeline import get_rfp

URLS_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "agents",
    "sales_agent",
    "urls.txt"
)
URLS_FILE = os.path.abspath(URLS_FILE)


def start_sales_agent(url: str):
    # ---- INIT STATUS ----
    st.session_state.url_status[url]["stage"] = "Processing"
    st.session_state.url_status[url]["history"].append(
        ("Started", time.time())
    )

    # ---- BACKUP ORIGINAL urls.txt ----
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, "r") as f:
            original_urls = f.read()
    else:
        original_urls = ""

    try:
        # ---- WRITE ONLY SELECTED URL ----
        with open(URLS_FILE, "w") as f:
            f.write(url.strip() + "\n")

        # ---- CALL BACKEND (SAFE SIGNATURE HANDLING) ----
        sig = inspect.signature(get_rfp)
        if len(sig.parameters) == 0:
            result = get_rfp()
        else:
            result = get_rfp(None)

        # ======================================================
        # CASE 1: RFP SKIPPED (NO ERROR, VALID BUSINESS LOGIC)
        # ======================================================
        if not result:
            st.session_state.url_status[url]["stage"] = "Skipped (Not Eligible)"
            st.session_state.url_status[url]["history"].append(
                ("Skipped (due date beyond 3 months)", time.time())
            )
            return

        # ======================================================
        # CASE 2: RESULT PRESENT BUT PDF MISSING / BROKEN LINK
        # ======================================================
        pdf_path = result.get("rfp_pdf_path") if isinstance(result, dict) else None

        if not pdf_path or not os.path.exists(pdf_path):
            st.session_state.url_status[url]["stage"] = "Failed (PDF not found)"
            st.session_state.url_status[url]["history"].append(
                ("PDF download failed", time.time())
            )
            return

        # ======================================================
        # CASE 3: SUCCESS
        # ======================================================
        st.session_state.sales_outputs[url] = result
        st.session_state.url_status[url]["stage"] = "Delivered to Main Agent"
        st.session_state.url_status[url]["history"].append(
            ("Completed", time.time())
        )

    except Exception as e:
        # ---- TRUE ERROR ----
        st.session_state.url_status[url]["stage"] = "Error"
        st.session_state.url_status[url]["error"] = str(e)
        st.session_state.url_status[url]["history"].append(
            ("Error", time.time())
        )

    finally:
        # ---- RESTORE ORIGINAL urls.txt ----
        with open(URLS_FILE, "w") as f:
            f.write(original_urls)


def retry_url(url: str):
    st.session_state.url_status[url] = {
        "stage": "Queued",
        "history": []
    }
