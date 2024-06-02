import streamlit as st
import requests

def find_candidates_num(entry_id, BASE_URL):
    try:
        response = requests.get(f"{BASE_URL}/data_entries/{entry_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")
