import streamlit as st
import requests

# 서버 URL 설정
BASE_URL = "http://localhost:8000"

# 세션 상태 유지
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'current_round_sub' not in st.session_state:
    st.session_state.current_round_sub = 0
if 'current_matchup' not in st.session_state:
    st.session_state.current_matchup = None

def start_worldcup():
    try:
        response = requests.post(f"{BASE_URL}/start", json={"id": "7"})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        data = response.json()
        st.session_state.session_id = data['session_id']
        st.session_state.current_round = data['current_round']
        st.session_state.current_round_sub = data['current_round_sub']
        st.session_state.current_matchup = data['current_matchup']
        st.experimental_rerun()  # 상태 변경 후 재실행
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")

def make_choice(choice):
    session_id = st.session_state.session_id
    try:
        response = requests.post(f"{BASE_URL}/choice?session_id={session_id}", json={"choice": choice})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        data = response.json()
        st.session_state.current_round = data['current_round']
        st.session_state.current_round_sub = data['current_round_sub']
        st.session_state.current_matchup = data['current_matchup']
        st.experimental_rerun()  # 상태 변경 후 재실행
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")

def get_current_info():
    session_id = st.session_state.session_id
    try:
        response = requests.get(f"{BASE_URL}/info/{session_id}")
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        data = response.json()
        st.session_state.current_round = data['current_round']
        st.session_state.current_round_sub = data['current_round_sub']
        st.session_state.current_matchup = data['current_matchup']
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")

# UI 구성
st.title("이상형 월드컵")

if st.session_state.session_id is None:
    if st.button("월드컵 시작"):
        start_worldcup()

if st.session_state.current_matchup and st.session_state.current_round != 1:
    st.write(f"현재 라운드: {st.session_state.current_round}, 매치 {st.session_state.current_round_sub + 1}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"선택: {st.session_state.current_matchup[0]['name']}"):
            make_choice(0)
    with col2:
        if st.button(f"선택: {st.session_state.current_matchup[1]['name']}"):
            make_choice(1)

    col1.image(st.session_state.current_matchup[0]['url'], use_column_width=True)
    col2.image(st.session_state.current_matchup[1]['url'], use_column_width=True)

if st.session_state.current_round == 1:
    st.balloons()
    st.success(f"최종 선택: {st.session_state.current_matchup[0]['name']}")
    st.image(st.session_state.current_matchup[0]['url'], use_column_width=True)
