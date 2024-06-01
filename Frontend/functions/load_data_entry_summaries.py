import requests
import streamlit as st


def load_data_entry_summaries(BASE_URL):
    try:
        response = requests.get(f"{BASE_URL}/data_entry_summaries/")
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()['summaries']
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []
