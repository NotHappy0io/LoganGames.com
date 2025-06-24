import random
import streamlit as st

if not st.session_state['authentication_status']:
    # show a message if the user is not logged in
    st.error("You need to log in to play the game. Please log in first.")
    st.stop()  # Stop further execution if not logged in

st.image("pics\847809488_preview_vault2.png")
# make it ask you a random riddle from a list of riddles
#         position: absolute;
#         top: 10px; 
#         left: 50%;
#         transform: translateX(-50%);
st.title("Riddler Game")
st.write("Answer the riddles to score points!")
# List of riddles and their answers
riddles = [
    {"question": "What has keys but can't open locks?", "answer": "A piano"},
    {"question": "What has a heart that doesn't beat?", "answer": "An artichoke"},
    {"question": "What can travel around the world while staying in a corner?", "answer": "A stamp"},
    {"question": "What has words but never speaks?", "answer": "A book"},
    {"question": "What can you catch but not throw?", "answer": "A cold"}
]