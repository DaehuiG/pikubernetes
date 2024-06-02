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


BASE_URL = "http://YOUR_ADDRESS_HERE:port"

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
if 'edit_worldcup_loaded' not in st.session_state:
    st.session_state.edit_worldcup_loaded = False
if 'page_number' not in st.session_state:
    st.session_state.page_number = None
if 'num_candidates' not in st.session_state:
    st.session_state.num_candidates = 16
if 'prompt' not in st.session_state:
    st.session_state.prompt = None
if 'similar_exist' not in st.session_state:
    st.session_state.similar_exist = False
if 'similar_candidates' not in st.session_state:
    st.session_state.similar_candidates = None

hide_sidebar()

st.title("Pikubernetes")

st.subheader("AI로 쉽게 만드는 나만의 이상형 월드컵", divider="blue")

if st.session_state.home:
    col1, col2, col3, empty= st.columns([0.2,0.2,0.2,0.3])
    with col1:
        if st.button("Play World Cup", key="play_worldcup_button"):
            st.session_state.home = False
            st.session_state.play_worldcup = True
            st.rerun()
    with col2:
        if st.button("Make World Cup", key="make_worldcup_button"):
            st.session_state.home = False
            st.session_state.create_worldcup = True
            st.rerun()
    with col3:
        if st.button("Edit World Cups", key="edit_worldcup_button"):
            st.session_state.home = False
            st.session_state.edit_worldcup = True
            st.rerun()

else:
    if st.session_state.create_worldcup:
        if st.session_state.similar_exist:
            create_worldcup_page.worldcup_similar_check(BASE_URL)
        else:
            create_worldcup_page.worldcup_create_page(BASE_URL)

    elif st.session_state.play_worldcup:
        if st.session_state.current_matchup:
            play_worldcup_page.play_worldcup_page(BASE_URL)
        else:
            play_worldcup_page.select_worldcup_page(BASE_URL)

    elif st.session_state.edit_worldcup:
        if st.session_state.edit_worldcup_loaded :
            edit_worldcup_page.edit_worldcup_page(BASE_URL)
        else:
            edit_worldcup_page.select_worldcup_page(BASE_URL)
