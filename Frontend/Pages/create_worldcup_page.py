import streamlit as st

from functions import create_new_worldcup as create
from functions import start_worldcup as start


def worldcup_create_page(BASE_URL):
    if st.session_state.creating_worldcup:
        prompt = st.text_input("새로운 월드컵의 주제를 입력하세요 (예: 연예인, 애니메이션 등):", key="worldcup_prompt")
        num_candidates = st.selectbox("후보 개수를 선택하세요:", [4, 8, 16, 32, 64], index=1, key="num_candidates")
        if st.button("후보 생성하기", key="generate_candidates"):
            candidates = create.generate_candidates(prompt, num_candidates, BASE_URL)
            if candidates:
                new_worldcup = create.create_new_worldcup(prompt, candidates, BASE_URL)
                if new_worldcup:
                    st.session_state.new_worldcup_id = new_worldcup['id']
                    st.session_state.candidates = candidates
                    start.start_worldcup(new_worldcup['id'], BASE_URL)
                    st.session_state.creating_worldcup = False
                    st.rerun()
