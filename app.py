import streamlit as st
from ui import render_ui, display_sidebar, display_chat
#from sessions import initialize_session
from config import first_run

st.set_page_config(page_title="MY Assist", layout="wide")


def main():
    first_run()
    render_ui()
    #initialize_session()
    display_sidebar()
    display_chat()


if __name__ == "__main__":
    main()
