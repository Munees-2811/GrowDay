"""
TaskFlow Navigation Bar (Bottom Tab Bar)
=========================================
Horizontal bottom navigation bar matching the user's mobile design.
Features:
- Active tab: Bright pink pill with soft glow (#E91E63)
- Inactive tabs: Dark rounded pills (#161626 / #1C1C28)
- Positioned at the bottom of the page screen
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
    """Draw the horizontal bottom navigation bar."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Today"

    active = st.session_state.current_page

    # Separator above bottom navbar
    st.markdown("<hr style='border-color:#1E1E2E;margin:1.5rem 0 0.8rem 0;'>", unsafe_allow_html=True)

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

    return st.session_state.current_page
