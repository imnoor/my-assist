import streamlit as st
import json
from config import get_session, save_message, get_chat_history
from chat_model import get_chat_model
from utils import process_stream, display_assistant_message, display_message


def handle_user_input():
    """Handles user input and generates the assistant's response."""

    # Get active session (default to "Default")
    active_session = st.session_state.get("active_session", "Default")
    #print("Active Session :" + active_session)
    # Ensure session exists in DB, else create it
    session = get_session(active_session)

    if session:
        session_id, selected_model = session  # Session exists, use stored model
        #print(f"Session ID {session_id}")
    else:
        # If session doesn't exist, force user to create a new one
        st.error("⚠️ This session does not exist. Please create a new session.")
        st.stop()

    chat_history = get_chat_history(session_id)
    
    # 🛠 Ensure messages are properly formatted before sending to chat model
    formatted_chat_history = [
        {"role": msg[0], "content": msg[1]} for msg in chat_history]

    # Display chat history
    for msg in formatted_chat_history:
        display_message(msg)

    # Get user input
    user_input = st.chat_input("💬 Type your message here...")

    if user_input:
        # Save user input
        display_message({"role": "user", "content": user_input})
        save_message(session_id, "user", user_input)

        # Generate response
        with st.chat_message("assistant"):
            chat_model = get_chat_model(model_name=selected_model)

            # 🛠 FIX: Pass correctly formatted history to the chat model
            stream = chat_model(formatted_chat_history +
                                [{"role": "user", "content": user_input}])

            response_content = process_stream(stream, "💡 Responding...")

            # Display & save assistant response
            display_assistant_message(response_content)
            save_message(session_id, "assistant", response_content)
