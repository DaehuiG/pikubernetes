import streamlit as st
import requests

# 서버 URL 설정
BASE_URL = "http://34.134.254.211:8000"

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
if 'creating_worldcup' not in st.session_state:
    st.session_state.creating_worldcup = False
if 'num_candidates' not in st.session_state:
    st.session_state.num_candidates = 16

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
        response = requests.post(f"{BASE_URL}/start", json={"id": str(entry_id)})
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

def generate_candidates(prompt, num_candidates):
    try:
        response = requests.post(f"{BASE_URL}/generate_candidates", json={"prompt": prompt, "num_candidates": num_candidates})
        response.raise_for_status()  # HTTPError가 발생하는지 확인
        return response.json()['candidates']
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []

def create_new_worldcup(description, candidates):
    try:
        payload = {"description": description, "candidates": candidates}
        st.write("Request Payload:", payload)  # 요청 페이로드 출력
        response = requests.post(f"{BASE_URL}/data_entries_from_queries/", json=payload)
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
    st.session_state.creating_worldcup = False
    st.experimental_rerun()

# UI 구성
st.title("이상형 월드컵")

if st.session_state.home:
    if st.button("Play World Cup", key="play_worldcup"):
        st.session_state.home = False
        st.experimental_rerun()
    if st.button("Make World Cup", key="make_worldcup"):
        st.session_state.home = False
        st.session_state.creating_worldcup = True
        st.experimental_rerun()
else:
    if st.session_state.creating_worldcup:
        prompt = st.text_input("새로운 월드컵의 주제를 입력하세요 (예: 연예인, 애니메이션 등):", key="worldcup_prompt")
        num_candidates = st.selectbox("후보 개수를 선택하세요:", [4, 8, 16, 32, 64], index=1, key="num_candidates")
        if st.button("후보 생성하기", key="generate_candidates"):
            candidates = generate_candidates(prompt, num_candidates)
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
                if st.button(f"{summary['description']} (생성일: {summary['created_at']})", key=f"summary_{summary['id']}"):
                    prompt = summary['description']
                    start_worldcup(summary['id'])
        else:
            st.write("사용 가능한 월드컵 데이터가 없습니다.")
            if st.button("홈으로 돌아가기", key="back_to_home"):
                reset_home()

    if st.session_state.current_matchup and st.session_state.current_round != 1:
        st.write(f"현재 라운드: {st.session_state.current_round}, 매치 {st.session_state.current_round_sub + 1}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"선택: {st.session_state.current_matchup[0]['name']}", key="choice_0"):
                make_choice(0)
        with col2:
            if st.button(f"선택: {st.session_state.current_matchup[1]['name']}", key="choice_1"):
                make_choice(1)
        
        try:
            col1.image(st.session_state.current_matchup[0]['url'], use_column_width=True)
        except Exception as e:
            col1.error(f"Error loading image: {e}")
        try:
            col2.image(st.session_state.current_matchup[1]['url'], use_column_width=True)
        except Exception as e:
            col2.error(f"Error loading image: {e}")

    if st.session_state.current_round == 1:
        st.balloons()
        st.success(f"최종 선택: {st.session_state.current_matchup[0]['name']}")
        try:
            st.image(st.session_state.current_matchup[0]['url'], use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
        if st.button("후보 수정하기", key="edit_candidates"):
            st.session_state.session_id = None
            st.experimental_rerun()
        if st.button("홈으로 돌아가기", key="home_after_final"):
            reset_home()

    if st.session_state.new_worldcup_id and not st.session_state.session_id:
        st.write("후보를 수정하세요:")
        updated_candidates = []
        for i, candidate in enumerate(st.session_state.candidates):
            updated_candidate = st.text_input(f"후보:", value=candidate, key=f"candidate_{i}")
            updated_candidates.append(updated_candidate)
        
        if st.button("후보 수정하기", key="update_candidates"):
            updated_worldcup = update_worldcup(st.session_state.new_worldcup_id, prompt, updated_candidates)
            if updated_worldcup:
                st.success("후보가 성공적으로 수정되었습니다.")
                st.session_state.new_worldcup_id = None
                st.session_state.candidates = []
                if st.button("홈으로 돌아가기", key="home_after_update"):
                    reset_home()