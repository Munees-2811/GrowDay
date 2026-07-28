"""
TaskFlow — Categories Page
==========================
Categories grid matching the reference UI screenshot:
- Custom categories section
- Default categories grid (Art, Task, Meditation, Study, Sports, Entertainment, etc.)
- NEW CATEGORY full-width button
"""

import streamlit as st
from database.db import (
    get_all_categories,
    add_category,
    delete_category,
    get_category_entry_count,
)


def render_categories_page():
    """Render Categories page matching screenshot 4."""
    # Header
    cols_hdr = st.columns([6, 1, 1])
    with cols_hdr[0]:
        st.markdown("<h2 style='margin:0;font-weight:800;color:#FFF;'>Categories</h2>", unsafe_allow_html=True)
    with cols_hdr[1]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>✓</div>", unsafe_allow_html=True)
    with cols_hdr[2]:
        st.markdown("<div style='text-align:right;font-size:1.2rem;color:#888;'>ℹ️</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Custom categories section
    custom_cats = get_all_categories(default_only=False)

    st.markdown("<h4 style='margin:0 0 0.2rem;color:#FFF;font-weight:700;'>Custom categories</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin:0 0 0.8rem;color:#666;font-size:0.8rem;'>{len(custom_cats)} available</p>", unsafe_allow_html=True)

    if custom_cats:
        cols_c = st.columns(min(len(custom_cats), 4))
        for i, cat in enumerate(custom_cats):
            col_idx = i % 4
            entries = get_category_entry_count(cat["id"])
            with cols_c[col_idx if len(custom_cats) >= 4 else i]:
                st.markdown(
                    f"""
                    <div style="text-align:center;margin-bottom:1rem;">
                        <div style="
                            width:56px;height:56px;border-radius:18px;
                            background:{cat.get('color','#E91E63')};
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.5rem;margin:0 auto 0.4rem;
                        ">{cat.get('icon','📁')}</div>
                        <div style="font-weight:700;font-size:0.85rem;color:#FFF;">{cat['name']}</div>
                        <div style="font-size:0.7rem;color:#666;">{entries} entries</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.markdown("<p style='color:#555;font-size:0.85rem;'>No custom categories added yet.</p>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E1E2E;margin:1.2rem 0;'>", unsafe_allow_html=True)

    # Default categories section
    default_cats = get_all_categories(default_only=True)

    st.markdown("<h4 style='margin:0 0 0.2rem;color:#FFF;font-weight:700;'>Default categories</h4>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0 0 1rem;color:#666;font-size:0.8rem;'>Editable for premium users</p>", unsafe_allow_html=True)

    cols_d = st.columns(3)
    for i, cat in enumerate(default_cats):
        col_idx = i % 3
        entries = get_category_entry_count(cat["id"])
        with cols_d[col_idx]:
            st.markdown(
                f"""
                <div style="
                    background:#1A1A26;border-radius:16px;padding:1rem 0.5rem;
                    text-align:center;margin-bottom:0.8rem;border:1px solid #252535;
                ">
                    <div style="
                        width:52px;height:52px;border-radius:16px;
                        background:{cat.get('color','#E91E63')};
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.4rem;margin:0 auto 0.4rem;
                    ">{cat.get('icon','📁')}</div>
                    <div style="font-weight:700;font-size:0.85rem;color:#FFF;">{cat['name']}</div>
                    <div style="font-size:0.75rem;color:#666;margin-top:2px;">{entries} entries</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # Add category expander
    with st.expander("➕ Add Custom Category", expanded=False):
        with st.form("add_cat_form", clear_on_submit=True):
            cat_name = st.text_input("Category Name", placeholder="e.g. Fitness, Reading...")
            col_icon, col_col = st.columns(2)
            with col_icon:
                cat_icon = st.selectbox("Icon", ["📁", "🎯", "📚", "💪", "🚀", "💡", "🎮", "🎵", "💰"])
            with col_col:
                cat_color = st.color_picker("Color", value="#E91E63")

            cat_sub = st.form_submit_button("NEW CATEGORY", use_container_width=True, type="primary")
            if cat_sub and cat_name.strip():
                add_category(cat_name.strip(), cat_icon, cat_color)
                st.success(f"Category '{cat_name}' added!")
                st.rerun()
