// button_events.js

// 버튼 1 클릭 이벤트 처리
document.getElementById('button1').addEventListener('click', function() {
    Streamlit.setComponentValue('session_state.home', false);
    Streamlit.setComponentValue('session_state.play_worldcup', true);
    Streamlit.rerun();
});

// 버튼 2 클릭 이벤트 처리
document.getElementById('button2').addEventListener('click', function() {
    Streamlit.setComponentValue('session_state.home', false);
    Streamlit.setComponentValue('session_state.create_worldcup', true);
    Streamlit.rerun();
});

// 버튼 3 클릭 이벤트 처리
document.getElementById('button3').addEventListener('click', function() {
    Streamlit.setComponentValue('session_state.home', false);
    Streamlit.setComponentValue('session_state.edit_worldcup', true);
    Streamlit.rerun();
});
