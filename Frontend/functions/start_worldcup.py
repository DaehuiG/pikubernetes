import requests
import streamlit as st


def start_worldcup(entry_id, BASE_URL):
    try:
        response = requests.post(f"{BASE_URL}/start", json={"id": str(entry_id)})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        data = response.json()
        st.session_state.session_id = data['session_id']
        st.session_state.current_round = data['current_round']
        st.session_state.current_round_sub = data['current_round_sub']
        st.session_state.current_matchup = data['current_matchup']
        st.session_state.home = False
        st.rerun()  # 상태 변경 후 재실행
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")