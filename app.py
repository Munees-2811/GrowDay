"""
TaskFlow — Main Application
============================
Entry point matching the reference dark mobile productivity app.
Run with: streamlit run app.py
"""

import streamlit as st
from datetime import date, datetime

# ── Streamlit page config (MUST be the first command) ───────────────────
st.set_page_config(
    page_title="TaskFlow",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Imports ─────────────────────────────────────────────────────────────
from database.db import (
    initialize_database,
    add_task,
    get_all_habits,
    get_today_tasks,
    log_habit,
    unlog_habit,
    is_habit_done,
    mark_task_completed,
)
from components.sidebar import render_navbar
from pages.tasks import render_tasks_page
from pages.habits import render_habits_page
from pages.categories import render_categories_page
from pages.timer import render_timer_page
from pages.statistics import render_statistics_page
from utils.helpers import get_week_dates, habit_circle_svg, priority_icon

# ── Initialise database ────────────────────────────────────────────────
initialize_database()


# =========================================================================
#  Custom CSS — Dark theme with #E91E63 Pink Accent
# =========================================================================
def inject_css():
    """Inject global custom CSS matching the reference mobile app."""
    st.markdown(
        """
        <style>
        /* ── Root Variables & Pure Dark Theme ────────── */
        :root {
            --bg: #0D0D12;
            --card-bg: #1C1C28;
            --accent: #E91E63;
            --text: #F0F0F0;
            --subtle: #888899;
            --border: #2A2A3A;
        }

        /* Hide Streamlit top header & footer */
        header[data-testid="stHeader"] { visibility: hidden; height: 0; }
        footer { visibility: hidden; height: 0; }
        #MainMenu { visibility: hidden; }

        .stApp {
            background-color: #0D0D12 !important;
            color: #F0F0F0 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Hide sidebar completely */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Container padding adjustment */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 500px !important;
        }

        /* ── Buttons (Navbar & App wide) ─────────────── */
        .stButton > button {
            border-radius: 16px !important;
            font-weight: 600 !important;
            font-size: 0.73rem !important;
            padding: 0.55rem 0.1rem !important;
            background: #181726 !important;
            color: #8E8EAA !important;
            border: 1px solid #252438 !important;
            transition: all 0.2s ease !important;
            line-height: 1.25 !important;
            white-space: pre !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            height: auto !important;
            min-height: 52px !important;
        }
        .stButton > button:hover {
            border-color: #E91E63 !important;
            color: #FFFFFF !important;
            background: #201F33 !important;
        }
        .stButton > button[kind="primary"] {
            background: #E91E63 !important;
            border: 1px solid #FF2A6D !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 18px rgba(233, 30, 99, 0.45) !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: #D81B60 !important;
            box-shadow: 0 6px 22px rgba(233, 30, 99, 0.6) !important;
        }

        /* ── Form Inputs ─────────────────────────────── */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #1C1C28 !important;
            color: #F0F0F0 !important;
            border: 1px solid #2A2A3A !important;
            border-radius: 10px !important;
        }
        .stForm {
            background: #161622 !important;
            border: 1px solid #2A2A3A !important;
            border-radius: 16px !important;
        }

        /* ── Metrics ─────────────────────────────────── */
        [data-testid="stMetric"] {
            background: #1C1C28 !important;
            border: 1px solid #2A2A3A !important;
            border-radius: 12px !important;
            padding: 0.7rem !important;
        }
        [data-testid="stMetricLabel"] {
            color: #888899 !important;
            font-size: 0.75rem !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }

        /* ── Tabs ────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            color: #888899 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.4rem 0.8rem !important;
            border-bottom: 2px solid transparent !important;
        }
        .stTabs [aria-selected="true"] {
            color: #E91E63 !important;
            border-bottom-color: #E91E63 !important;
        }

        /* ── Expander ────────────────────────────────── */
        .streamlit-expanderHeader {
            background: #1C1C28 !important;
            color: #E91E63 !important;
            border-radius: 12px !important;
            border: 1px solid #2A2A3A !important;
        }

        /* ── Floating Action Button (FAB) Style ──────── */
        .fab-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 56px;
            height: 56px;
            border-radius: 28px;
            background: #E91E63;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            box-shadow: 0 4px 20px rgba(233, 30, 99, 0.5);
            z-index: 9999;
            cursor: pointer;
        }

        /* ── Mobile-first layout overrides ───────────── */
        @media (max-width: 768px) {
            .block-container { padding-left: 0.8rem; padding-right: 0.8rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================================
#  Today Page (Screenshot 1 matching)
# =========================================================================
def render_today_page():
    """Render Today page matching Screenshot 1."""
    # Top bar with Today title + Action icons (Search, Filter, Calendar, Settings)
    cols_hdr = st.columns([5, 1, 1, 1, 1], vertical_alignment="center")
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Today</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        st.button("🔍", key="hdr_today_search")
    with cols_hdr[2]:
        st.button("⚡", key="hdr_today_quick")
    with cols_hdr[3]:
        st.button("📅", key="hdr_today_cal")
    with cols_hdr[4]:
        if st.button("⚙️", key="settings_icon_btn"):
            st.session_state.current_page = "Settings"
            st.rerun()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # Selected Date state
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = date.today()

    sel_date = st.session_state.selected_date

    # Week Date Strip (Screenshot 1 matching: Fri 24, Sat 25, Sun 26, Mon 27, Tue 28, Wed 29, Thu 30...)
    week_dates = get_week_dates(sel_date)

    cols_week = st.columns(7)
    for idx, d_info in enumerate(week_dates):
        d = d_info["date"]
        is_selected = d == sel_date
        bg_color = "#E91E63" if is_selected else "#1A1A26"
        text_color = "#FFFFFF" if is_selected else "#888899"
        border_style = "border:none;" if is_selected else "border:1px solid #252535;"

        with cols_week[idx]:
            if st.button(
                f"{d_info['day_name']}\n{d_info['day_num']}",
                key=f"strip_date_{d.isoformat()}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
            ):
                st.session_state.selected_date = d
                st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Fetch Data ────────────────────────────────────────────────────
    habits = get_all_habits()
    tasks = get_today_tasks() if sel_date == date.today() else []

    # ── Habits List for Today ──────────────────────────────────────────
    if habits:
        for h in habits:
            hid = h["id"]
            done = is_habit_done(hid, sel_date.isoformat())

            col_h1, col_h2, col_h3 = st.columns([1, 6, 1])
            with col_h1:
                st.markdown(
                    f"""
                    <div style="
                        width:40px;height:40px;border-radius:12px;
                        background:{h.get('color','#E91E63')};
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.1rem;margin-top:2px;
                    ">⬛</div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_h2:
                st.markdown(
                    f"""
                    <div style="padding-left:4px;">
                        <div style="font-weight:700;font-size:0.95rem;color:#FFF;">{h['name']}</div>
                        <span style="background:#E91E6333;color:#E91E63;padding:1px 8px;border-radius:10px;font-size:0.7rem;">Habit</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_h3:
                if done:
                    if st.button("✓", key=f"today_unlog_{hid}", use_container_width=True, type="primary"):
                        unlog_habit(hid, sel_date.isoformat())
                        st.rerun()
                else:
                    if st.button("○", key=f"today_log_{hid}", use_container_width=True):
                        log_habit(hid, sel_date.isoformat())
                        st.rerun()

            st.markdown("<hr style='border-color:#1E1E2E;margin:0.5rem 0;'>", unsafe_allow_html=True)

    # ── Tasks for Selected Date ────────────────────────────────────────
    if tasks:
        st.markdown("<h4 style='color:#FFF;margin:1rem 0 0.5rem;'>Tasks</h4>", unsafe_allow_html=True)
        for t in tasks:
            tid = t["id"]
            t_done = bool(t["completed"])
            col_t1, col_t2 = st.columns([7, 1])
            with col_t1:
                strike = "text-decoration:line-through;opacity:0.5;" if t_done else ""
                st.markdown(
                    f"""
                    <div style="{strike}">
                        <span style="font-weight:600;color:#FFF;font-size:0.9rem;">{t['title']}</span>
                        <span style="font-size:0.75rem;color:#888;">({t.get('priority','')})</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_t2:
                if t_done:
                    if st.button("✓", key=f"today_tundo_{tid}", use_container_width=True, type="primary"):
                        mark_task_completed(tid, False)
                        st.rerun()
                else:
                    if st.button("○", key=f"today_tdone_{tid}", use_container_width=True):
                        mark_task_completed(tid, True)
                        st.rerun()

    # ── Clean Empty State ──────────────────────────────────────────────
    if not habits and not tasks:
        st.markdown(
            """
            <div style="text-align:center;padding:3rem 1rem;">
                <div style="
                    width:70px;height:70px;border-radius:50%;
                    background:#1E1E2E;margin:0 auto 1rem;
                    display:flex;align-items:center;justify-content:center;
                    font-size:2rem;color:#E91E63;
                ">🌱</div>
                <h3 style="margin:0;font-weight:700;color:#FFF;">No habits or tasks yet</h3>
                <p style="margin:0.4rem 0 0;color:#666;font-size:0.85rem;">Use the Habits or Tasks tabs to add your first entries</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Premium banner matching screenshot 1
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background:#1A121A;border:1px solid #E91E6344;
            border-radius:14px;padding:0.7rem 1rem;
            display:flex;align-items:center;gap:0.6rem;
        ">
            <span style="color:#E91E63;">🏵️</span>
            <span style="font-weight:700;color:#E91E63;font-size:0.85rem;">Premium</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================================
#  Settings Page
# =========================================================================
def render_settings():
    """Settings page."""
    cols_hdr = st.columns([6, 1], vertical_alignment="center")
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Settings</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        if st.button("✖️", key="close_settings"):
            st.session_state.current_page = "Today"
            st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    name = st.text_input("User Display Name", value=st.session_state.get("user_name", "Munees"))
    if name != st.session_state.get("user_name", "Munees"):
        st.session_state.user_name = name

    st.toggle("Notifications", value=st.session_state.get("notif_on", True), key="notif_toggle")

    if st.button("📊 View Full Statistics", use_container_width=True):
        st.session_state.current_page = "Statistics"
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center;color:#666;font-size:0.8rem;">
            TaskFlow v1.0 • Dark Theme Mobile UI<br>
            Python • Streamlit • SQLite
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================================
#  Page Router
# =========================================================================
PAGE_MAP = {
    "Today":      render_today_page,
    "Habits":     render_habits_page,
    "Tasks":      render_tasks_page,
    "Categories": render_categories_page,
    "Timer":      render_timer_page,
    "Statistics": render_statistics_page,
    "Settings":   render_settings,
}


def main():
    """Application main entry point."""
    st.session_state.setdefault("current_page", "Today")
    st.session_state.setdefault("user_name", "Munees")

    inject_css()

    current_page = st.session_state.current_page

    # Render selected page
    renderer = PAGE_MAP.get(current_page, render_today_page)
    renderer()

    # Bottom Navigation Bar
    render_navbar()


if __name__ == "__main__":
    main()
