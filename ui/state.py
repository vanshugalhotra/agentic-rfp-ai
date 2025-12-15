def init_state(st):
    if "urls" not in st.session_state:
        st.session_state.urls = []

    if "url_status" not in st.session_state:
        st.session_state.url_status = {}

    if "sales_outputs" not in st.session_state:
        st.session_state.sales_outputs = {}

    if "main_summary" not in st.session_state:
        st.session_state.main_summary = {}

    if "tech_results" not in st.session_state:
        st.session_state.tech_results = {}

    if "pricing_results" not in st.session_state:
        st.session_state.pricing_results = {}
