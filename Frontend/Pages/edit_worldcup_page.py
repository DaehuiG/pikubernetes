import streamlit as st
import requests

from functions import reset_home as reset
from functions import load_data_entry_summaries as load
from functions import update_worldcup as update
from functions import choose_update_worldcup as choose_update


def select_worldcup_page(BASE_URL):
    divider_html = """
        <div style="border-top: 1px solid #bbb; margin: 0; padding: 0;"></div>
        """

    if st.session_state.page_number is None:
        st.session_state.page_number = 1

    summaries = load.load_data_entry_summaries(BASE_URL)
    maximum_page = (len(summaries) // 10) + 1

    if summaries:
        st.write("후보를 수정할 월드컵을 선택하세요:")
        if st.session_state.page_number != maximum_page or maximum_page != 1:
            for summary in summaries[(st.session_state.page_number - 1) * 10:st.session_state.page_number * 10]:
                column1, column2 = st.columns([0.8, 0.2])
                with column1:
                    if st.button(f"{summary['description']}", key=f"summary_{summary['id']}"):
                        st.session_state.prompt = summary['description']
                        choose_update.choose_update_worldcup(summary['id'], BASE_URL)
                with column2:
                    date_and_time = summary['created_at'].split('T')
                    st.write(date_and_time[0] + " " + date_and_time[1][:8])
                st.markdown(divider_html, unsafe_allow_html=True)

        else:
            for summary in summaries[(st.session_state.page_number - 1) * 10:]:
                column1, column2 = st.columns([0.8, 0.2])
                with column1:
                    if st.button(f"{summary['description']}", key=f"summary_{summary['id']}"):
                        st.session_state.prompt = summary['description']
                        choose_update.choose_update_worldcup(summary['id'], BASE_URL)
                with column2:
                    date_and_time = summary['created_at'].split('T')
                    st.write(date_and_time[0] + " " + date_and_time[1][:8])
                st.markdown(divider_html, unsafe_allow_html=True)

        page_number = st.session_state.get('page_number', 1)

        # 좌, 우 버튼 및 페이지 번호 입력 필드 배치
        col1, col2, col3 = st.columns([0.1, 0.1, 0.8])

        with col1:
            if st.session_state.page_number != 1:
                if st.button("◀"):
                    page_number -= 1
                    st.session_state.page_number = page_number
                    st.rerun()

        with col2:
            if st.session_state.page_number != maximum_page:
                if st.button("▶"):
                    page_number += 1
                    st.session_state.page_number = page_number
                    st.rerun()

        st.write(f"현재 페이지: {page_number}")

        if st.button("홈으로 돌아가기", key="back_to_home"):
            reset.reset_home()

def edit_worldcup_page(BASE_URL):

    st.write("후보를 수정하세요:")
    updated_candidates = []
    for i, candidate in enumerate(st.session_state.candidates):
        updated_candidate = st.text_input(f"후보:", value=candidate, key=f"candidate_{i}")
        updated_candidates.append(updated_candidate)

    col1,col2,col3 = st.columns([0.05,0.05,0.8])
    with col1 :
        if st.button("＋", key="more_candidates"):
            st.session_state.candidates.append(" ")
            st.rerun()
    with col2 :
        if len(st.session_state.candidates) != 0:
            if st.button("－", key="less_candidates"):
                st.session_state.candidates.pop()
                st.rerun()

    updated_worldcup = None

    if st.button("후보 수정하기", key="update_candidates"):
        if len(st.session_state.candidates) & (len(st.session_state.candidates) - 1) == 0 :
            updated_worldcup = update.update_worldcup(st.session_state.new_worldcup_id, st.session_state.prompt,
                                                                         updated_candidates, BASE_URL)
        else :
            st.warning("후보는 2의 제곱으로 나타내야 합니다.")

        if updated_worldcup:
            st.success("후보가 성공적으로 수정되었습니다.")

    if st.button("홈으로 돌아가기", key="home_update"):
        reset.reset_home()
