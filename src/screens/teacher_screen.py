import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

def teacher_screen():
    st.header("Teacher Screen")

    style_background_dashboard()
    style_base_layout()
