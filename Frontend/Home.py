import streamlit as st
import functions as funcs
import os

from Pages import create_worldcup_page
from Pages import play_worldcup_page
from Pages import edit_worldcup_page
worldcup_icon_url = 'https://cdn1.iconfinder.com/data/icons/road-to-worldcup-filled-line/128/15_worldcup_fifa_champion_win_soccer_football_sport-1024.png'
st.set_page_config(
    page_title="Pikubernetes",
    page_icon=worldcup_icon_url
)

head_css = """
<style> 
h1 {
    font-size: 50px;
    font-weight: bold;
    font-family: Arial, sans-serif;
    text-align: left;
    padding: 0px;
    animation: changeColor 15s infinite alternate; /* 5초 간격으로 색이 변하며 반복 */
}

@keyframes changeColor {
    0% { color: red; }
    25% { color: blue; }
    50% { color: green; }
    75% { color: orange; }
    100% { color: purple; }
}
</style>
"""

st.markdown("""
<style>
.element-container:has(#button-after1) + div button {
    position: relative;
    width: 200px; /* Adjust button width as needed */
    height: 300px; /* Adjust button height as needed */
    margin: 10 auto; /* Center the button */
}

.element-container:has(#button-after1) + div button::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://previews.123rf.com/images/larryrains/larryrains1606/larryrains160601693/57936373-%EC%9A%B0%EC%8A%B9-%ED%8A%B8%EB%A1%9C%ED%94%BC.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
    background-position: center;
}

.element-container:has(#button-after1) + div button:hover::before {
    opacity: 1;
    z-index: 1;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.element-container:has(#button-after2) + div button {
    position: relative;
    width: 200px; /* Adjust button width as needed */
    height: 300px; /* Adjust button height as needed */
    margin: 10 auto; /* Center the button */
}

.element-container:has(#button-after2) + div button::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://png.pngtree.com/element_our/20190603/ourlarge/pngtree-writing-brush-cartoon-illustration-image_1432501.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
    background-position: center;
}

.element-container:has(#button-after2) + div button:hover::before {
    opacity: 1;
    z-index: 1;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.element-container:has(#button-after3) + div button {
    position: relative;
    width: 200px; /* Adjust button width as needed */
    height: 300px; /* Adjust button height as needed */
    margin: 10 auto; /* Center the button */
}

.element-container:has(#button-after3) + div button::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://www.urbanbrush.net/web/wp-content/uploads/2021/02/urbanbrush-20210218112906679353.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
    background-position: center;
}

.element-container:has(#button-after3) + div button:hover::before {
    opacity: 1;
    z-index: 1;
}
</style>
""", unsafe_allow_html=True)


def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

BASE_URL = os.getenv('backendAddress')

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

st.markdown(head_css, unsafe_allow_html=True)
st.title("Pikubernetes")

st.subheader("AI로 쉽게 만드는 나만의 이상형 월드컵", divider="blue")

if st.session_state.home:
    col1, col2, col3, empty= st.columns([1,1, 1,0.3])
    with col1:
        st.markdown('<span id="button-after1"></span>', unsafe_allow_html=True)
        if st.button("Play World Cup", key="play_worldcup_button"):
            st.session_state.home = False
            st.session_state.play_worldcup = True
            st.rerun()
    with col2:
        st.markdown('<span id="button-after2"></span>', unsafe_allow_html=True)
        if st.button("Make World Cup", key="make_worldcup_button"):
            st.session_state.home = False
            st.session_state.create_worldcup = True
            st.rerun()
    with col3:
        st.markdown('<span id="button-after3"></span>', unsafe_allow_html=True)
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