"""
TaskFlow Navigation Bar
========================
Horizontal navigation bar matching the user's exact UI design snippet.
Features:
- Active tab: Bright pink pill with soft glow (#E91E63)
- Inactive tabs: Dark rounded pills (#161626 / #1C1C28)
- Icon on top, label on bottom (no line wrapping)
"""

import streamlit as st


NAV_ITEMS = [
    ("📋", "Today"),
    ("🎯", "Habits"),
    ("✅", "Tasks"),
    ("📂", "Categories"),
    ("⏱️", "Timer"),
]


def render_navbar():
    """Draw the horizontal navigation bar matching the reference image snippet."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Today"

    active = st.session_state.current_page

    # Wrapper container for navbar
    st.markdown(
        """
        <style>
        div[data-testid="column"] {
            padding: 0 2px !important;
        }
        .nav-btn-container {
            display: flex;
            gap: 6px;
            justify-content: space-between;
            margin-bottom: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(NAV_ITEMS))
    for i, (icon, label) in enumerate(NAV_ITEMS):
        with cols[i]:
            is_active = active == label
            btn_label = f"{icon}\n{label}"
            if st.button(
                btn_label,
                key=f"nav_btn_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.current_page = label
                st.rerun()

    st.markdown("<hr style='border-color:#1E1E2E;margin:0.2rem 0 1rem 0;'>", unsafe_allow_html=True)
    return st.session_state.current_page
