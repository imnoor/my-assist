import streamlit as st
from input_handle import handle_user_input
from sessions import create_new_session, rename_session, delete_session, switch_session
from utils import display_chat_history, get_base64_image
from config import get_db_connection
import os
import shutil

def render_ui():
    """Renders the main UI header with an image and title."""
    session_name = st.session_state.get("active_session", "Default")
    image_base64 = get_base64_image("assets/deep-seek.png")

    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <img src="data:image/png;base64,{image_base64}" width="120" style="margin-bottom: 10px;"/>
        <h1 style="color: #333; margin-bottom: 5px;">🤖 MY Assist</h1>
        <h4 style="color: #666; font-weight: normal;">💬 Session: <span style="color: #0078FF;">{session_name}</span></h4>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Displays the chat session management UI in the sidebar."""
    with st.sidebar:
        render_sidebar_header()
        render_session_management()

def render_sidebar_header():
    """Displays the logo and sidebar title."""
    image_base64 = get_base64_image("assets/deep-seek.png")
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src="data:image/png;base64,{image_base64}" width="150"/>
    </div>
    """, unsafe_allow_html=True)
    st.title("💬 Chat Sessions")

def render_session_management():
    """Displays session switching and management options."""
    with st.sidebar:
        # Fetch sessions from database
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sessions;")
            sessions = [row[0] for row in cur.fetchall()]

        for session_name in sessions:
            col1, col2 = st.columns([4, 1])

            with col1:
                if st.button(f"📁 {session_name}", key=f"session_{session_name}", help="Switch session", use_container_width=True):
                    switch_session(session_name)

            with col2:
                action = st.selectbox(
                    "⋮",
                    ["", "✏️ Rename", "🗑 Delete"],
                    key=f"menu_{session_name}",
                    label_visibility="collapsed"
                )

                if action == "✏️ Rename":
                    rename_session(session_name)
                elif action == "🗑 Delete":
                    delete_session(session_name)

        st.markdown("---")
        create_new_session()
        st.markdown("---")
        render_admin()

def render_admin():
    """Admin Settings"""
    with open('chat_history.db', 'rb') as file:
        st.download_button(
            label='Download Chat History',
            data=file,
            file_name='chat_history.db',
            mime='application/octet-stream'
        )

    uploaded_file = st.file_uploader("Restore Chat History", type=["db"])
    if uploaded_file is not None:
        if st.button("Confirm Restore"):
            with open('chat_history.db', 'wb') as file:
                shutil.copyfileobj(uploaded_file, file)
            st.success("Chat history restored successfully!")

    if st.button('Terminate App'):
        os.kill(os.getpid(), 9)

def display_chat():
    """Displays the chat interface for the active session."""
    display_chat_history()
    handle_user_input()
