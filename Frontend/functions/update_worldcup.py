import requests
import streamlit as st


def update_worldcup(entry_id, description, candidates, BASE_URL):
    try:
        response = requests.put(f"{BASE_URL}/data_entries/{entry_id}/",
                                json={"description": description, "candidates": candidates})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None
