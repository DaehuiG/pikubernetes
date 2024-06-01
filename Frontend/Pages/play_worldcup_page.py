import streamlit as st

from functions import load_data_entry_summaries as load
from functions import start_worldcup as start
from functions import reset_home as reset
from functions import make_choice as choice


def select_worldcup_page(BASE_URL):

    summaries = load.load_data_entry_summaries(BASE_URL)
    if summaries:
        st.write("플레이 할 월드컵을 선택하세요:")
        for summary in summaries:
            if st.button(f"{summary['description']} (생성일: {summary['created_at']})", key=f"summary_{summary['id']}"):
                st.session_state.prompt = summary['description']
                start.start_worldcup(summary['id'], BASE_URL)

        if st.button("홈으로 돌아가기", key="back_to_home"):
            reset.reset_home()

    else:
        st.write("사용 가능한 월드컵 데이터가 없습니다.")
        if st.button("홈으로 돌아가기", key="back_to_home"):
            reset.reset_home()


def play_worldcup_page(BASE_URL):

    if st.session_state.current_round != 1:

        st.write(f"현재 라운드: {st.session_state.current_round}, 매치 {st.session_state.current_round_sub + 1}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"선택: {st.session_state.current_matchup[0]['name']}", key="choice_0"):
                choice.make_choice(0, BASE_URL)
        with col2:
            if st.button(f"선택: {st.session_state.current_matchup[1]['name']}", key="choice_1"):
                choice.make_choice(1,BASE_URL)

        try:
            image_can1 = st.session_state.current_matchup[0]['url']
            col1.image(image_can1, use_column_width=True)
        except Exception as e:
            col1.error(f"Error loading image: {e}")
        try:
            image_can2 = st.session_state.current_matchup[1]['url']

            col2.image(image_can2, use_column_width=True)
        except Exception as e:
            col2.error(f"Error loading image: {e}")

    else:
        st.balloons()
        st.success(f"최종 선택: {st.session_state.current_matchup[0]['name']}")
        try:
            st.image(st.session_state.current_matchup[0]['url'], use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
        if st.button("후보 수정하기", key="edit_candidates"):
            st.session_state.play_worldcup = False
            st.session_state.edit_worldcup = True
            st.rerun()

    if st.button("홈으로 돌아가기", key="home_after_final"):
        reset.reset_home()
