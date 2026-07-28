"""
TaskFlow — Timer Page
=====================
Timer page matching screenshot 5:
- Top header (< Timer / info, vibrate, volume icons)
- Large circular timer display with pink accent ring
- 00:00 time display inside ring
- Pink pill START / STOP button
- Mode selector: Stopwatch / Countdown / Intervals
- No recent records / No activity selected placeholders
"""

import streamlit as st
import time
from utils.helpers import timer_ring_svg, format_timer
from database.db import add_timer_record, get_recent_timer_records


def render_timer_page():
    """Render Timer page matching screenshot 5."""
    # Top header
    cols_hdr = st.columns([6, 1, 1, 1])
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Timer</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        st.markdown("<div style='text-align:right;font-size:1.1rem;color:#888;'>ℹ️</div>", unsafe_allow_html=True)
    with cols_hdr[2]:
        st.markdown("<div style='text-align:right;font-size:1.1rem;color:#888;'>📳</div>", unsafe_allow_html=True)
    with cols_hdr[3]:
        st.markdown("<div style='text-align:right;font-size:1.1rem;color:#888;'>🔊</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # Session state for timer
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_seconds" not in st.session_state:
        st.session_state.timer_seconds = 0
    if "timer_mode" not in st.session_state:
        st.session_state.timer_mode = "Stopwatch"

    # Timer Circle Display
    seconds = st.session_state.timer_seconds
    time_str = format_timer(seconds)
    pct = min(seconds / 3600.0, 1.0) if seconds > 0 else 0.0

    st.markdown(
        f"""
        <div style="position:relative;width:220px;height:220px;margin:0 auto;">
            {timer_ring_svg(pct, size=220)}
            <div style="
                position:absolute;top:0;left:0;width:100%;height:100%;
                display:flex;align-items:center;justify-content:center;
                font-size:2.8rem;font-weight:800;color:#FFF;
                letter-spacing:1px;
            ">{time_str}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # START / STOP Button (Pink pill)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.session_state.timer_running:
            if st.button("⏹️ STOP", key="btn_stop_timer", use_container_width=True, type="primary"):
                st.session_state.timer_running = False
                add_timer_record("Session", st.session_state.timer_seconds, st.session_state.timer_mode)
                st.rerun()
        else:
            if st.button("▶️ START", key="btn_start_timer", use_container_width=True, type="primary"):
                st.session_state.timer_running = True
                st.rerun()

    # Reset button if timer > 0 and not running
    if not st.session_state.timer_running and st.session_state.timer_seconds > 0:
        with col_btn2:
            if st.button("↺ Reset", key="btn_reset_timer", use_container_width=True):
                st.session_state.timer_seconds = 0
                st.rerun()

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # Mode Selector Tabs: Stopwatch / Countdown / Intervals
    modes = ["Stopwatch", "Countdown", "Intervals"]
    cols_m = st.columns(3)
    for i, mode in enumerate(modes):
        with cols_m[i]:
            is_active = st.session_state.timer_mode == mode
            icon = "⏱️" if mode == "Stopwatch" else "⏳" if mode == "Countdown" else "🕐"
            if st.button(
                f"{icon}\n{mode}",
                key=f"mode_{mode}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.timer_mode = mode
                st.rerun()

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # Recent records / Activity card
    records = get_recent_timer_records(limit=3)

    st.markdown(
        f"""
        <div style="
            background:#1A1A26;border-radius:14px;padding:1.2rem;
            border:1px solid #252535;text-align:center;
        ">
            <div style="padding:0.6rem 0;color:#666;font-size:0.85rem;border-bottom:1px solid #252535;">
                {'Recent session: ' + format_timer(records[0]['duration_seconds']) if records else 'No recent records'}
            </div>
            <div style="padding:0.6rem 0;color:#666;font-size:0.85rem;">
                No activity selected
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Auto increment timer when running
    if st.session_state.timer_running:
        time.sleep(1)
        st.session_state.timer_seconds += 1
        st.rerun()
