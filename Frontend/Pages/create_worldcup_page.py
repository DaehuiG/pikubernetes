import streamlit as st

from functions import create_new_worldcup as create
from functions import start_worldcup as start
from functions import reset_home as reset
from functions import get_similar_worldcup as similar


def worldcup_create_page(BASE_URL):
    prompt = st.text_input("새로운 월드컵의 주제를 입력하세요 (예: 연예인, 애니메이션 등):", key="worldcup_prompt")
    num_candidates = st.selectbox("후보 개수를 선택하세요:", [4, 8, 16, 32, 64], index=1, key="num_candidates_choose")
    if st.button("후보 생성하기", key="generate_candidates"):
        similar_worldcup = similar.get_similar_worldcup(prompt, BASE_URL)['similar_descriptions']
        used_set = dict([])
        for worldcup in similar_worldcup:
            if worldcup[0] not in used_set.keys():
                used_set[worldcup[0]] = tuple(worldcup)
        st.session_state.used_set = used_set

        if len(st.session_state.used_set) == 0:
            response = create.generate_candidates(prompt, num_candidates, BASE_URL)
            candidates = response['candidates']
            new_description = response['new_description']
            new_description = prompt # 원상 복구
            if candidates:
                new_worldcup = create.create_new_worldcup(new_description, candidates, BASE_URL)
                if new_worldcup:
                    st.session_state.new_worldcup_id = new_worldcup['id']
                    st.session_state.candidates = candidates
                    start.start_worldcup(new_worldcup['id'], BASE_URL)
                    st.rerun()

        else:
            st.session_state.similar_exist = True
            st.session_state.prompt = prompt
            st.session_state.similar_candidates = num_candidates
            st.rerun()

    if st.button("홈으로 돌아가기", key="return_home_create"):
        reset.reset_home()


def worldcup_similar_check(BASE_URL):
    st.write('비슷한 주제의 월드컵이 존재합니다 : ')

    for cup in st.session_state.used_set.values():
        if st.button(f"{cup[1]} 바로 플레이!"):
            st.session_state.prompt = cup[1]
            start.start_worldcup(cup[0], BASE_URL)
            st.rerun()

    if st.button("그래도 생성하기", key="generate_anyway"):
        response = create.generate_candidates(st.session_state.prompt, st.session_state.similar_candidates, BASE_URL)
        candidates = response['candidates']
        new_description = response['new_description']
        new_description = st.session_state.prompt # 원상복구
        if candidates:
            new_worldcup = create.create_new_worldcup(new_description, candidates, BASE_URL)
            if new_worldcup:
                st.session_state.new_worldcup_id = new_worldcup['id']
                st.session_state.candidates = candidates
                start.start_worldcup(new_worldcup['id'], BASE_URL)
                st.rerun()
    if st.button("홈으로 돌아가기"):
        reset.reset_home()
