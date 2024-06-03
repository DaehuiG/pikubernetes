import streamlit as st

from functions import load_data_entry_summaries as load
from functions import start_worldcup as start
from functions import reset_home as reset
from functions import make_choice as choice
from functions import choose_update_worldcup as update
from functions import find_candidates_num as num


def select_worldcup_page(BASE_URL):

    divider_html = """
    <div style="border-top: 1px solid #bbb; margin: 0; padding: 0;"></div>
    """

    if st.session_state.page_number is None:
        st.session_state.page_number = 1

    summaries = load.load_data_entry_summaries(BASE_URL)
    maximum_page = (len(summaries) // 10) + 1

    if summaries:
        st.write("플레이 할 월드컵을 선택하세요:")
        if st.session_state.page_number != maximum_page or maximum_page != 1:
            for summary in summaries[(st.session_state.page_number-1)*10:st.session_state.page_number*10]:
                column1, column2 = st.columns([0.8, 0.2])
                with column1:
                    if st.button(f"{summary['description']}", key=f"summary_{summary['id']}"):
                        st.session_state.prompt = summary['description']
                        start.start_worldcup(summary['id'], BASE_URL)

                with column2:
                    date_and_time = summary['created_at'].split('T')
                    st.write(date_and_time[0] + " " + date_and_time[1][:8])
                st.markdown(divider_html, unsafe_allow_html=True)

        else:
            for summary in summaries[(st.session_state.page_number-1)*10:]:
                column1, column2 = st.columns([0.8, 0.2])
                with column1:
                    if st.button(f"{summary['description']}", key=f"summary_{summary['id']}"):
                        st.session_state.prompt = summary['description']
                        start.start_worldcup(summary['id'], BASE_URL)

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

    else:
        st.write("사용 가능한 월드컵 데이터가 없습니다.")
        if st.button("홈으로 돌아가기", key="back_to_home"):
            reset.reset_home()


def play_worldcup_page(BASE_URL):

    if st.session_state.current_round != 1:
        if st.session_state.current_round == 2:
            st.info(f"결승전! ({2 * (st.session_state.current_round_sub + 1)}/{st.session_state.current_round})")
        else :
            st.info(f"{st.session_state.current_round}강 매치 ({2 * (st.session_state.current_round_sub + 1)}/{st.session_state.current_round})")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"선택: {st.session_state.current_matchup[0]['name']}", key="choice_0"):
                choice.make_choice(0, BASE_URL)

        with col2:
            if st.button(f"선택: {st.session_state.current_matchup[1]['name']}", key="choice_1"):
                choice.make_choice(1,BASE_URL)

        st.markdown("""
                    <style>
                    img {
                        aspect-ratio : 1/1;
                        object-fit: contain;
                    }
                    img:hover {
                        transform : scale(1.1);
                        transition-duration : 1s;
                        
                    }
                    </style>
                    """, unsafe_allow_html=True)

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
            update.choose_update_worldcup(st.session_state.new_worldcup_id, BASE_URL)
            st.rerun()

    if st.button("홈으로 돌아가기", key="home_after_final"):
        reset.reset_home()
