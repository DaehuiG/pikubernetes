import streamlit as st


def reset_home():
    st.session_state.home = True
    st.session_state.session_id = None
    st.session_state.current_round = 0
    st.session_state.current_round_sub = 0
    st.session_state.current_matchup = None
    st.session_state.new_worldcup_id = None
    st.session_state.prompt = None
    st.session_state.num_candidates = 0
    st.session_state.candidates = []
    st.session_state.create_worldcup = False
    st.session_state.play_worldcup = False
    st.session_state.edit_worldcup = False
    st.session_state.edit_worldcup_loaded = False
    st.session_state.page_number = None
    st.session_state.used_set = set([])
    st.session_state.similar_exist = False
    st.session_state.similar_candidates = None
    st.rerun()
