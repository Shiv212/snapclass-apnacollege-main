import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

def student_screen():
    st.header("Student Screen")
    style_background_dashboard()
    style_base_layout()