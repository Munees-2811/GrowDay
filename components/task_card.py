"""
TaskFlow Task Card Component
=============================
Dark-themed task card with pink accents and action buttons.
"""

import streamlit as st
from utils.helpers import priority_color, priority_icon, days_remaining, format_date
from database.db import mark_task_completed, delete_task


def render_task_card(task, key_prefix=""):
    """Display a single task as a styled dark card."""
    tid = task["id"]
    is_done = bool(task["completed"])
    pri = task.get("priority", "Medium")
    color = priority_color(pri)
    remaining = days_remaining(task.get("due_date"))

    # Status indicator
    check_color = "#4CAF50" if is_done else "#333"
    check_icon = "✓" if is_done else ""
    strike = "text-decoration:line-through;opacity:0.45;" if is_done else ""

    st.markdown(
        f"""
        <div style="
            background:#1C1C28;
            border-radius:14px;
            padding:0.9rem 1rem;
            margin-bottom:0.6rem;
            border:1px solid #2A2A3A;
        ">
            <div style="display:flex;align-items:center;gap:0.7rem;">
                <div style="
                    width:22px;height:22px;border-radius:6px;
                    border:2px solid {check_color};
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.7rem;color:#fff;flex-shrink:0;
                    {'background:' + check_color + ';' if is_done else ''}
                ">{check_icon}</div>
                <div style="flex:1;min-width:0;">
                    <div style="font-weight:600;font-size:0.95rem;color:#F0F0F0;{strike}">{task['title']}</div>
                    {"<div style='font-size:0.78rem;color:#888;margin-top:2px;'>" + task['description'][:60] + "</div>" if task.get('description') else ""}
                </div>
                <span style="
                    background:{color}22;color:{color};
                    padding:2px 8px;border-radius:8px;
                    font-size:0.68rem;font-weight:600;white-space:nowrap;
                ">{pri}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:0.5rem;padding-left:2.1rem;font-size:0.72rem;color:#666;">
                <span>📅 {format_date(task.get('due_date'), '%b %d') if task.get('due_date') else 'No date'}</span>
                <span style="color:{'#E91E63' if 'Overdue' in remaining else '#666'}">{remaining}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action buttons
    key_base = f"{key_prefix}_{tid}"
    cols = st.columns([1, 1, 1])

    with cols[0]:
        if is_done:
            if st.button("↩️ Undo", key=f"undo_{key_base}", use_container_width=True):
                mark_task_completed(tid, completed=False)
                st.rerun()
        else:
            if st.button("✅ Done", key=f"done_{key_base}", use_container_width=True):
                mark_task_completed(tid, completed=True)
                st.rerun()

    with cols[1]:
        if st.button("✏️ Edit", key=f"edit_{key_base}", use_container_width=True):
            st.session_state["editing_task"] = tid
            st.rerun()

    with cols[2]:
        if st.button("🗑️", key=f"del_{key_base}", use_container_width=True):
            delete_task(tid)
            st.rerun()
