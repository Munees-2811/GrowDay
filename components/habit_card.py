"""
TaskFlow Habit Card Component
==============================
Habit card with weekly completion circles, streak, and completion rate.
"""

import streamlit as st
from database.db import (
    get_habit_week_status,
    get_habit_streak,
    get_habit_completion_rate,
    log_habit,
    unlog_habit,
    is_habit_done,
    delete_habit,
)
from utils.helpers import habit_circle_svg


def render_habit_card(habit, key_prefix="habits"):
    """Render a full habit card matching the reference design."""
    hid = habit["id"]
    color = habit.get("color", "#E91E63")
    week = get_habit_week_status(hid)
    streak = get_habit_streak(hid)
    rate = get_habit_completion_rate(hid)

    # Week circles SVG
    circles_html = ""
    day_labels_html = ""
    for day in week:
        circles_html += habit_circle_svg(
            day["day_num"],
            done=day["done"],
            is_today=day["is_today"],
            is_future=day["is_future"],
        )
        day_labels_html += f'<span style="display:inline-block;width:40px;text-align:center;font-size:0.65rem;color:#888;">{day["day_name"]}</span>'

    st.markdown(
        f"""
        <div style="
            background:#1C1C28;
            border-radius:14px;
            padding:1rem 1rem 0.8rem;
            margin-bottom:0.8rem;
            border:1px solid #2A2A3A;
        ">
            <!-- Header -->
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div style="font-weight:700;font-size:1rem;color:#F0F0F0;">{habit['name']}</div>
                    <div style="font-size:0.75rem;color:{color};margin-top:2px;">{habit.get('frequency','Every day')}</div>
                </div>
                <div style="
                    width:30px;height:30px;border-radius:8px;
                    background:{color};
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.85rem;
                ">⬛</div>
            </div>

            <!-- Week day labels -->
            <div style="margin-top:0.8rem;text-align:center;">
                {day_labels_html}
            </div>

            <!-- Week circles -->
            <div style="text-align:center;margin-top:0.2rem;">
                {circles_html}
            </div>

            <!-- Stats row -->
            <div style="
                display:flex;justify-content:space-between;align-items:center;
                margin-top:0.7rem;padding-top:0.6rem;
                border-top:1px solid #2A2A3A;
            ">
                <div style="font-size:0.75rem;color:#888;">
                    🔗 {streak} &nbsp; ✅ {rate}%
                </div>
                <div style="display:flex;gap:0.8rem;font-size:0.85rem;color:#666;">
                    📅 &nbsp; 📊 &nbsp; ⋮
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action buttons row
    key_base = f"{key_prefix}_{hid}"
    cols = st.columns([1, 1, 1])

    with cols[0]:
        today_done = is_habit_done(hid)
        if today_done:
            if st.button("↩️ Undo Today", key=f"unlog_{key_base}", use_container_width=True):
                unlog_habit(hid)
                st.rerun()
        else:
            if st.button("✅ Mark Done", key=f"log_{key_base}", use_container_width=True):
                log_habit(hid)
                st.rerun()

    with cols[1]:
        if st.button("✏️ Edit", key=f"hedit_{key_base}", use_container_width=True):
            st.session_state["editing_habit"] = hid
            st.rerun()

    with cols[2]:
        if st.button("🗑️", key=f"hdel_{key_base}", use_container_width=True):
            delete_habit(hid)
            st.rerun()
