import streamlit as st
import requests


def get_similar_worldcup(description, BASE_URL):
    try:
        response = requests.post(f"{BASE_URL}/compare_description",
                                 json={"description": description})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")