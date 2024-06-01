import streamlit as st
import requests

from functions import reset_home as reset
from functions import load_data_entry_summaries as load
from functions import update_worldcup as update
from functions import choose_update_worldcup as choose_update


def select_worldcup_page(BASE_URL):

    summaries = load.load_data_entry_summaries(BASE_URL)
    if summaries:
        st.write("후보를 수정할 월드컵을 선택하세요:")
        for summary in summaries:
            if st.button(f"{summary['description']} (생성일: {summary['created_at']})", key=f"summary_{summary['id']}"):
                st.session_state.prompt = summary['description']
                choose_update.choose_update_worldcup(summary['id'], BASE_URL)

        if st.button("홈으로 돌아가기", key="back_to_home"):
            reset.reset_home()

    else:
        st.write("수정 가능한 월드컵 데이터가 없습니다.")
        if st.button("홈으로 돌아가기", key="back_to_home"):
            reset.reset_home()

def edit_worldcup_page(BASE_URL):

    st.write("후보를 수정하세요:")
    updated_candidates = []
    for i, candidate in enumerate(st.session_state.candidates):
        updated_candidate = st.text_input(f"후보:", value=candidate, key=f"candidate_{i}")
        updated_candidates.append(updated_candidate)

    if st.button("후보 수정하기", key="update_candidates"):
        updated_worldcup = update.update_worldcup(st.session_state.new_worldcup_id, prompt,
                                                                     updated_candidates)
        if updated_worldcup:
            st.success("후보가 성공적으로 수정되었습니다.")
            st.session_state.new_worldcup_id = None
            st.session_state.candidates = []
            if st.button("홈으로 돌아가기", key="home_after_update"):
                reset.reset_home()
