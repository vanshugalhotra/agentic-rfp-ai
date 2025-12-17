import streamlit as st

def app_sidebar():
    st.markdown("""
    <style>
    /* Hide Streamlit default nav */
    [data-testid="stSidebarNav"] { display: none; }

    /* Sidebar container */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Header */
    .sidebar-header {
        padding: 1.4rem 1rem 1rem;
    }

    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        letter-spacing: -0.01em;
    }

    /* Section label */
    .sidebar-section {
        padding: 0.7rem 1rem 0.35rem;
        font-size: 0.7rem;
        font-weight: 600;
        color: #6366f1; /* indigo */
        letter-spacing: 0.08em;
    }

    /* Nav wrapper */
    .nav-btn {
        position: relative;
        margin: 0.2rem 0.6rem;
        border-radius: 14px;
    }

    /* Buttons */
    .nav-btn button {
        padding: 0.65rem 0.75rem;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #334155;
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        width: 100%;
        text-align: left;
        transition: all 0.15s ease;
    }

    .nav-btn button:hover {
        background-color: #eef2ff;
        color: #3730a3;
        border-color: #c7d2fe;
    }

    /* Active state */
    .nav-btn.active {
        background-color: #4f46e5;
    }

    .nav-btn.active button {
        background-color: #4f46e5;
        border-color: #4f46e5;
        color: #ffffff;
        font-weight: 600;
    }

    /* Active indicator dot */
    .nav-btn.active::before {
        content: "";
        position: absolute;
        left: -8px;
        top: 50%;
        transform: translateY(-50%);
        width: 6px;
        height: 6px;
        background-color: #6366f1;
        border-radius: 999px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Header
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">Agentic RFP AI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">PIPELINE</div>', unsafe_allow_html=True)

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

            st.markdown(f'<div class="nav-btn {active_class}">', unsafe_allow_html=True)
            clicked = st.button(
                label,
                key=f"nav-{key}",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

            if clicked:
                st.session_state.current_page = key
                st.switch_page(page)
