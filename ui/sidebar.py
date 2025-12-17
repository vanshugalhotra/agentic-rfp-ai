import streamlit as st

def app_sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #f2f2f2;
        width: 300px !important;
    }

    .sidebar-header {
        padding: 1rem 1.5rem 1.5rem;
        border-bottom: 1px solid #f2f2f2;
    }

    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.03em;
    }

    .sidebar-section-label {
        padding: 0 1.5rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .nav-link {
        display: block;
        padding: 0.6rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        color: #334155;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        transition: all 0.2s ease;
    }

    .nav-link:hover {
        background-color: #f8fafc;
        color: #1e293b;
    }

    .nav-link.active {
        font-weight: 600;
        color: #4f46e5;
        background-color: #f8fbff;
    }

    .nav-link.active::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background-color: #6366f1;
    }

    /* Completely hide the actual buttons */
    .hidden-button button {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><div class="sidebar-title">Agentic RFP AI</div></div>', unsafe_allow_html=True)

        nav_items = [
            ("Dashboard", "app.py", "dashboard"),
            ("Input Layer", "pages/1_Input.py", "input"),
            ("Sales Agent", "pages/2_Sales_Agent.py", "sales"),
            ("Main Agent", "pages/3_Main_Agent.py", "main"),
            ("Technical Agent", "pages/4_Technical_Agent.py", "technical"),
            ("Pricing Agent", "pages/5_Pricing_Agent.py", "pricing"),
            ("Final Report", "pages/6_Final_Report.py", "report"),
        ]

        current = st.session_state.get("current_page", "dashboard")

        for label, page, key in nav_items:
            active_class = "active" if current == key else ""

            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown(f'<div class="nav-link {active_class}">{label}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("→", key=f"nav_{key}", type="primary"):
                    st.session_state.current_page = key
                    st.switch_page(page)
            
