import streamlit as st
import functions as funcs

from Pages import create_worldcup_page
from Pages import play_worldcup_page
from Pages import edit_worldcup_page


def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)


BASE_URL = "http://34.41.189.95:8000"

# 세션 상태 유지
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'current_round_sub' not in st.session_state:
    st.session_state.current_round_sub = 0
if 'current_matchup' not in st.session_state:
    st.session_state.current_matchup = None
if 'home' not in st.session_state:
    st.session_state.home = True
if 'new_worldcup_id' not in st.session_state:
    st.session_state.new_worldcup_id = None
if 'candidates' not in st.session_state:
    st.session_state.candidates = []
if 'create_worldcup' not in st.session_state:
    st.session_state.create_worldcup = False
if 'play_worldcup' not in st.session_state:
    st.session_state.play_worldcup = False
if 'edit_worldcup' not in st.session_state:
    st.session_state.edit_worldcup = False
if 'num_candidates' not in st.session_state:
    st.session_state.num_candidates = 16

hide_sidebar()

st.title("이상형 월드컵")

if st.session_state.home:
    if st.button("Play World Cup", key="play_worldcup_button"):
        st.session_state.home = False
        st.session_state.play_worldcup = True
        st.rerun()

    if st.button("Make World Cup", key="make_worldcup_button"):
        st.session_state.home = False
        st.session_state.create_worldcup = True
        st.rerun()

    if st.button("Edit World Cups", key="edit_worldcup_button"):
        st.session_state.home = False
        st.session_state.edit_worldcup = True
        st.rerun()

else:
    if st.session_state.create_worldcup:
        create_worldcup_page.worldcup_create_page(BASE_URL)

    elif st.session_state.play_worldcup:
        if st.session_state.current_matchup:
            play_worldcup_page.play_worldcup_page(BASE_URL)
        else:
            play_worldcup_page.select_worldcup_page(BASE_URL)

    elif st.session_state.edit_worldcup:
        if st.session_state.current_matchup:
            edit_worldcup_page.edit_worldcup_page(BASE_URL)
        else:
            edit_worldcup_page.select_worldcup_page(BASE_URL)
