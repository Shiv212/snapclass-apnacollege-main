import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.database.db import create_teacher, check_teacher_exists, teacher_login, get_teacher_subjet
from src.components.dialog_create_subjects import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog

import time

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

    footer_dashboard()

    
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome back {teacher_data['name']}!", text_alignment="center")
        if st.button("Logout", type="secondary", key="loginbackbtn", shortcut="Control + backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subects":
        teacher_tab_manage_subects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    st.header('Take AI Attendance')

def teacher_tab_manage_subects():
    
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    #List all subjects
    subjects = get_teacher_subjet(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", " Students", sub['total_students']),
                ("🕐", " Classes", sub['total_classes'])
            ]
        def share_btn():
            st.space()
            
            if st.button(f"Share code: {sub['name']}", key=f"share_{sub['suject_code']}", icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['suject_code'])
            

        subject_card(
            name = sub['name'],
            code = sub['suject_code'],
            section = sub['section'],
            stats = stats,
            footer_callback=share_btn
        )
    else:
        st.info("No Subject Found, Create One Above")
        

def teacher_tab_attendance_records():
    st.header('Attendance Records')

def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        st.session_state.user_role = "teacher"
        return True
    return False

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type="secondary", key="loginbackbtn", shortcut="Control + backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using password", text_alignment="center")

    st.space()
    st.space()
    

    username = st.text_input("Enter username", placeholder="@Shivendra", key="teacher_login_username")
    password = st.text_input("Enter password", placeholder="Enter your password", type="password", key="teacher_login_password")

    st.divider()

    login_btn, register_btn = st.columns(2, gap="small", vertical_alignment="top")

    with login_btn:
        if st.button("Login", type="secondary", key="teacher_login_btn", shortcut="Control + enter", icon=':material/passkey:', icon_position='left', width='stretch'):
            if login_teacher(username, password):
                st.toast(f"Welcome back {username}!", icon="👋")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")

    with register_btn:
        if st.button("Register Instead", type="primary", key="teacher_register_btn", icon=':material/passkey:', icon_position='left', width='stretch'):
            st.session_state.teacher_login_type = "register"
            st.rerun()


def register_teacher(username, name, password, confirm_password):
    if not username or not name or not password or not confirm_password:
        return False, "All fields are requird!"
    if check_teacher_exists(username):
        return False, "Username already taken"
    if password != confirm_password:
        return False, "Password doesn't match"

    try:
        create_teacher(username, password, name)
        return True, "Successfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type="secondary", key="registerbackbtn", shortcut="Control + backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your teacher profile", text_alignment="center")

    st.space()
    st.space()
    

    username = st.text_input("Enter username", placeholder="@Shivendra", key="teacher_login_username")
    name = st.text_input("Enter name", placeholder="Shivendra", key="teacher_login_name")
    password = st.text_input("Enter password", placeholder="Enter your password", type="password", key="teacher_login_password")
    confirm_password = st.text_input("Confirm password", placeholder="Confirm your password", type="password", key="teacher_login_confirm_password")

    st.divider()

    register_btn, login_btn = st.columns(2, gap="small", vertical_alignment="top")

    with register_btn:
        if st.button("Register Now", type="primary", key="teacher_register_btn", shortcut="Control + enter", icon=':material/passkey:', icon_position='left', width='stretch'):
            success, message = register_teacher(username, name, password, confirm_password)
            if success:
                st.success(message)
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with login_btn:
        if st.button("Login instead", type="secondary", key="teacher_login_btn", icon=':material/passkey:', icon_position='left', width='stretch'):
            st.session_state.teacher_login_type = "login"
            st.rerun()