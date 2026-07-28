"""
TaskFlow — Habits Page
======================
Habits page matching the reference mobile UI design.
Features:
- "All" / "New list" filter chips
- Full habit list with weekly completion status circles, streaks & rate
- Habit creation form inside expander
"""

import streamlit as st
from database.db import (
    get_all_habits,
    add_habit,
    get_habit_by_id,
    update_habit,
)
from components.habit_card import render_habit_card


def _habit_form(defaults=None, key_suffix="new"):
    """Form to create or edit a habit."""
    defaults = defaults or {}
    with st.form(f"habit_form_{key_suffix}", clear_on_submit=True):
        name = st.text_input("Habit Name *", value=defaults.get("name", ""), placeholder="e.g. 3_min_english, Daily 10 words...")
        description = st.text_input("Description", value=defaults.get("description", ""), placeholder="Optional note...")

        col1, col2 = st.columns(2)
        with col1:
            frequency = st.selectbox(
                "Frequency",
                ["Every day", "Weekdays", "Weekends", "3 times a week"],
                index=0,
            )
        with col2:
            color = st.color_picker("Color Accent", value=defaults.get("color", "#E91E63"))

        submitted = st.form_submit_button(
            "💾 Save Habit" if defaults else "➕ Create Habit",
            use_container_width=True,
            type="primary",
        )

    if submitted and not name.strip():
        st.warning("Habit name is required.")
        return False, {}

    return submitted, {
        "name": name.strip(),
        "description": description.strip(),
        "frequency": frequency,
        "color": color,
    }


def render_habits_page():
    """Main entry point for Habits page."""
    # Top header
    cols_hdr = st.columns([6, 1, 1])
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Habits</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>🔍</div>", unsafe_allow_html=True)
    with cols_hdr[2]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>📥</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Filter chips (All / + New list)
    st.markdown(
        """
        <div style="display:flex;gap:0.5rem;margin-bottom:1rem;">
            <span style="background:#E91E63;color:#FFF;padding:4px 16px;border-radius:20px;font-size:0.8rem;font-weight:600;">All</span>
            <span style="background:#1C1C28;color:#888;padding:4px 14px;border-radius:20px;font-size:0.8rem;border:1px solid #2A2A3A;">+ New list</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Edit habit state check
    editing_id = st.session_state.get("editing_habit")
    if editing_id:
        habit = get_habit_by_id(editing_id)
        if habit:
            st.markdown("### ✏️ Edit Habit")
            submitted, data = _habit_form(defaults=habit, key_suffix="edit")
            if submitted:
                update_habit(editing_id, data["name"], data["description"], data["frequency"], data["color"])
                st.session_state.pop("editing_habit", None)
                st.success("Habit updated!")
                st.rerun()
            if st.button("Cancel", key="cancel_habit_edit"):
                st.session_state.pop("editing_habit", None)
                st.rerun()
            return

    # Add Habit expander
    with st.expander("➕ Add New Habit", expanded=False):
        submitted, data = _habit_form()
        if submitted:
            add_habit(data["name"], data["description"], data["frequency"], data["color"])
            st.success(f"✅ Habit '{data['name']}' created!")
            st.rerun()

    # List habits
    habits = get_all_habits()
    if not habits:
        st.markdown(
            """
            <div style="text-align:center;padding:3rem 1rem;">
                <div style="
                    width:70px;height:70px;border-radius:50%;
                    background:#1E1E2E;margin:0 auto 1rem;
                    display:flex;align-items:center;justify-content:center;
                    font-size:2rem;color:#E91E63;
                ">🎯</div>
                <h3 style="margin:0;font-weight:700;color:#FFF;">No habits yet</h3>
                <p style="margin:0.4rem 0 0;color:#666;font-size:0.85rem;">Create a habit to start tracking consistency</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for h in habits:
            render_habit_card(h, key_prefix="habits_page")
