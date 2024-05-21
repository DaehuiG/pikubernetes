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
if 'home' not in st.session_state:
    st.session_state.home = True
if 'new_worldcup_id' not in st.session_state:
    st.session_state.new_worldcup_id = None
if 'candidates' not in st.session_state:
    st.session_state.candidates = []

def load_data_entry_summaries():
    try:
        response = requests.get(f"{BASE_URL}/data_entry_summaries/")
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()['summaries']
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []

def start_worldcup(entry_id):
    try:
        response = requests.post(f"{BASE_URL}/start", json={"id": entry_id})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        data = response.json()
        st.session_state.session_id = data['session_id']
        st.session_state.current_round = data['current_round']
        st.session_state.current_round_sub = data['current_round_sub']
        st.session_state.current_matchup = data['current_matchup']
        st.session_state.home = False
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

def generate_candidates(prompt):
    try:
        response = requests.post(f"{BASE_URL}/generate_candidates", json={"prompt": prompt, "num_candidates": 16})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()['candidates']
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []

def create_new_worldcup(description, candidates):
    try:
        response = requests.post(f"{BASE_URL}/data_entries_from_queries/", json={"description": description, "candidates": candidates})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

def update_worldcup(entry_id, description, candidates):
    try:
        response = requests.put(f"{BASE_URL}/data_entries/{entry_id}/", json={"description": description, "candidates": candidates})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

def reset_home():
    st.session_state.home = True
    st.session_state.session_id = None
    st.session_state.current_round = 0
    st.session_state.current_round_sub = 0
    st.session_state.current_matchup = None
    st.session_state.new_worldcup_id = None
    st.session_state.candidates = []
    st.experimental_rerun()

# UI 구성
st.title("이상형 월드컵")

if st.session_state.home:
    if st.button("play world cup"):
        st.session_state.home = False
        st.experimental_rerun()
    if st.button("make world cup"):
        st.session_state.home = False
        st.session_state.creating_worldcup = True
        st.experimental_rerun()
else:
    if 'creating_worldcup' in st.session_state and st.session_state.creating_worldcup:
        prompt = st.text_input("새로운 월드컵의 주제를 입력하세요 (예: 연예인, 애니메이션 등):")
        if st.button("후보 생성하기"):
            candidates = generate_candidates(prompt)
            if candidates:
                new_worldcup = create_new_worldcup(prompt, candidates)
                if new_worldcup:
                    st.session_state.new_worldcup_id = new_worldcup['id']
                    st.session_state.candidates = candidates
                    start_worldcup(new_worldcup['id'])
                    st.session_state.creating_worldcup = False
                    st.experimental_rerun()
    elif st.session_state.session_id is None:
        summaries = load_data_entry_summaries()
        if summaries:
            st.write("플레이 할 월드컵을 선택하세요:")
            for summary in summaries:
                if st.button(f"{summary['description']} (생성일: {summary['created_at']})"):
                    start_worldcup(summary['id'])
        else:
            st.write("사용 가능한 월드컵 데이터가 없습니다.")
            if st.button("홈으로 돌아가기"):
                reset_home()

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
        if st.button("후보 수정하기"):
            st.session_state.session_id = None
            st.experimental_rerun()
        if st.button("홈으로 돌아가기"):
            reset_home()

    if st.session_state.new_worldcup_id and not st.session_state.session_id:
        st.write("후보를 수정하세요:")
        updated_candidates = []
        for candidate in st.session_state.candidates:
            updated_candidate = st.text_input(f"후보:", value=candidate)
            updated_candidates.append(updated_candidate)
        
        if st.button("후보 수정하기"):
            updated_worldcup = update_worldcup(st.session_state.new_worldcup_id, "동물", updated_candidates)
            if updated_worldcup:
                st.success("후보가 성공적으로 수정되었습니다.")
                st.session_state.new_worldcup_id = None
                st.session_state.candidates = []
                if st.button("홈으로 돌아가기"):
                    reset_home()
