"""
TaskFlow — Statistics Page
==========================
Statistics & Analytics styled to match dark mobile theme.
"""

import streamlit as st
from database.db import get_task_stats


def render_statistics_page():
    """Render Statistics page."""
    cols_hdr = st.columns([6, 1], vertical_alignment="center")
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Statistics</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        st.button("📊", key="hdr_stats_chart")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    stats = get_task_stats()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", stats["total"])
    c2.metric("Completed", stats["completed"])
    c3.metric("Pending", stats["pending"])
    c4.metric("Overdue", stats["overdue"])

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Progress bar
    rate = stats["completion_rate"]
    st.markdown(
        f"""
        <div style="
            background:#1C1C28;border-radius:14px;padding:1.4rem;
            border:1px solid #2A2A3A;margin-bottom:1.2rem;
        ">
            <div style="font-weight:700;color:#FFF;margin-bottom:0.8rem;">Completion Rate</div>
            <div style="background:#2A2A3A;border-radius:10px;height:18px;overflow:hidden;">
                <div style="
                    width:{rate}%;height:100%;background:#E91E63;
                    border-radius:10px;transition:width 0.5s ease;
                "></div>
            </div>
            <div style="text-align:right;margin-top:0.4rem;font-weight:700;color:#E91E63;">{rate}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h4 style='color:#FFF;margin:1rem 0 0.6rem;'>📌 Today's Overview</h4>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    t1.metric("Today Total", stats["today_total"])
    t2.metric("Done Today", stats["today_completed"])
    t3.metric("Today Rate", f"{stats['today_completion_rate']}%")
