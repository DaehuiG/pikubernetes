import streamlit as st


def reset_home():
    st.session_state.home = True
    st.session_state.session_id = None
    st.session_state.current_round = 0
    st.session_state.current_round_sub = 0
    st.session_state.current_matchup = None
    st.session_state.new_worldcup_id = None
    st.session_state.candidates = []
    st.session_state.creating_worldcup = False
    st.rerun()
