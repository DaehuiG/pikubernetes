import requests
import streamlit as st


def create_new_worldcup(description, candidates, BASE_URL):
    try:
        payload = {"description": description, "candidates": candidates}
        st.write("Request Payload:", payload)  # 요청 페이로드 출력
        response = requests.post(f"{BASE_URL}/data_entries_from_queries/", json=payload)
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None


def generate_candidates(prompt, num_candidates, BASE_URL):
    try:
        response = requests.post(f"{BASE_URL}/generate_candidates",
                                 json={"prompt": prompt, "num_candidates": num_candidates})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()['candidates']
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []

