import requests
import streamlit as st


def choose_update_worldcup(entry_id, BASE_URL):
    try:
        response = requests.get(f"{BASE_URL}/data_entries/{entry_id}")
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        data = response.json()
        st.session_state.new_worldcup_id = data['id']
        st.session_state.candidates = data['queries']
        st.session_state.prompt = data['description']
        st.session_state.edit_worldcup_loaded = True
        st.session_state.home = False
        st.rerun()  # 상태 변경 후 재실행
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")