"""
TaskFlow — Tasks Page
=====================
Task management page matching the reference mobile UI design.
Features:
- Single tasks vs Recurring tasks tabs
- Filter options & search
- Pink Floating Add Action Button / Expander
- Empty state matching screenshot ("No tasks / There are no upcoming tasks")
"""

import streamlit as st
from datetime import date
from database.db import (
    add_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    get_all_categories,
)
from components.task_card import render_task_card


def _task_form(defaults=None, key_suffix="new"):
    """Reusable task form."""
    defaults = defaults or {}
    categories = get_all_categories()
    cat_options = {c["id"]: f"{c['icon']} {c['name']}" for c in categories}
    cat_ids = list(cat_options.keys())

    with st.form(f"task_form_{key_suffix}", clear_on_submit=True):
        title = st.text_input("Task Title *", value=defaults.get("title", ""), placeholder="Task title...")
        description = st.text_area("Description", value=defaults.get("description", ""), placeholder="Details (optional)...", height=80)

        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
                index=["High", "Medium", "Low"].index(defaults.get("priority", "Medium")),
            )
        with col2:
            default_due = None
            if defaults.get("due_date"):
                try:
                    default_due = date.fromisoformat(defaults["due_date"])
                except ValueError:
                    default_due = None
            due_date = st.date_input("Due Date", value=default_due or date.today())

        col3, col4 = st.columns(2)
        with col3:
            is_recurring = st.checkbox("Recurring Task", value=bool(defaults.get("is_recurring", 0)))
        with col4:
            selected_cat = st.selectbox(
                "Category",
                options=[None] + cat_ids,
                format_func=lambda x: "None" if x is None else cat_options.get(x, "Category"),
                index=0,
            )

        submitted = st.form_submit_button(
            "💾 Save Task" if defaults else "➕ Add Task",
            use_container_width=True,
            type="primary",
        )

    if submitted and not title.strip():
        st.warning("Task title is required.")
        return False, {}

    return submitted, {
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "due_date": due_date.isoformat() if due_date else None,
        "is_recurring": 1 if is_recurring else 0,
        "category_id": selected_cat,
    }


def render_tasks_page():
    """Main entry point for Tasks page."""
    # Top header with icon buttons like in screenshot
    cols_hdr = st.columns([6, 1, 1, 1])
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Tasks</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>🔍</div>", unsafe_allow_html=True)
    with cols_hdr[2]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>⚡</div>", unsafe_allow_html=True)
    with cols_hdr[3]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>📥</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Editing state check
    editing_id = st.session_state.get("editing_task")
    if editing_id:
        task = get_task_by_id(editing_id)
        if task:
            st.markdown("### ✏️ Edit Task")
            submitted, data = _task_form(defaults=task, key_suffix="edit")
            if submitted:
                update_task(
                    editing_id,
                    data["title"],
                    data["description"],
                    data["priority"],
                    data["due_date"],
                    data["is_recurring"],
                    data["category_id"],
                )
                st.session_state.pop("editing_task", None)
                st.success("Task updated!")
                st.rerun()
            if st.button("Cancel", key="cancel_edit"):
                st.session_state.pop("editing_task", None)
                st.rerun()
            return

    # Add task expander / modal toggle
    with st.expander("➕ Add New Task", expanded=False):
        submitted, data = _task_form()
        if submitted:
            add_task(
                data["title"],
                data["description"],
                data["priority"],
                data["due_date"],
                data["is_recurring"],
                data["category_id"],
            )
            st.success(f"✅ Task '{data['title']}' added!")
            st.rerun()

    # Tabs: Single tasks / Recurring tasks
    tabs = st.tabs(["Single tasks", "Recurring tasks"])

    with tabs[0]:
        tasks = get_all_tasks(recurring=False)
        if not tasks:
            st.markdown(
                """
                <div style="text-align:center;padding:4rem 1rem;">
                    <div style="
                        width:80px;height:80px;border-radius:50%;
                        background:#1E1E2E;margin:0 auto 1rem;
                        display:flex;align-items:center;justify-content:center;
                        font-size:2.5rem;color:#E91E63;
                    ">📋</div>
                    <h3 style="margin:0;font-weight:700;color:#FFF;">No tasks</h3>
                    <p style="margin:0.4rem 0 0;color:#666;font-size:0.9rem;">There are no upcoming tasks</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for t in tasks:
                render_task_card(t, key_prefix="single")

    with tabs[1]:
        rec_tasks = get_all_tasks(recurring=True)
        if not rec_tasks:
            st.markdown(
                """
                <div style="text-align:center;padding:4rem 1rem;">
                    <div style="
                        width:80px;height:80px;border-radius:50%;
                        background:#1E1E2E;margin:0 auto 1rem;
                        display:flex;align-items:center;justify-content:center;
                        font-size:2.5rem;color:#E91E63;
                    ">🔄</div>
                    <h3 style="margin:0;font-weight:700;color:#FFF;">No recurring tasks</h3>
                    <p style="margin:0.4rem 0 0;color:#666;font-size:0.9rem;">Create tasks that repeat regularly</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for t in rec_tasks:
                render_task_card(t, key_prefix="rec")
