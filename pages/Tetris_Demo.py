import streamlit as st
import random

# --- Configuration for Board Dimensions and Block Size ---
# You'll use these in your game logic and for CSS.
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE_PX = 25 # Size of each block in pixels (e.g., 25x25px)

if not st.session_state['authentication_status']:
    # show a message if the user is not logged in
    st.error("You need to log in to play the game. Please log in first.")
    st.stop()  # Stop further execution if not logged in

# --- Tetromino Colors (Standard AWT colors) ---
# Use these strings as keys/values in your game board's cell state
TETROMINO_COLORS = {
    'I': '#00FFFF', # Cyan
    'O': '#FFFF00', # Yellow
    'T': '#800080', # Purple (Magenta)
    'S': '#00FF00', # Green
    'Z': '#FF0000', # Red
    'J': '#0000FF', # Blue
    'L': '#FFA500', # Orange
    'empty': '#1a1a1a', # Dark background for empty cells
    'locked': '#444444' # A slightly lighter dark gray for settled blocks
}

# --- CSS for Tetris Board and Blocks ---
# This block should go at the beginning of your Streamlit app script.
st.markdown(f"""
    <style>
    /* Main container for the Tetris board */
    .tetris-board-container {{
        background-color: black;
        border: 5px solid #555; /* A subtle border for the game well */
        display: flex;
        flex-direction: column; /* Stacks rows vertically */
        width: {BOARD_WIDTH * BLOCK_SIZE_PX}px; /* Calculated width based on block size */
        margin: 20px auto; /* Center the board horizontally */
        box-shadow: 0px 0px 15px rgba(0,255,255,0.7); /* A cool glowing effect */
        padding: 2px; /* Small padding inside the border */
        border-radius: 5px; /* Slightly rounded corners */
    }}
    /* Each row within the board */
    .tetris-row {{
        display: flex; /* Arranges blocks horizontally in a row */
    }}
    /* Individual Tetris block */
    .tetris-block {{
        width: {BLOCK_SIZE_PX}px;
        height: {BLOCK_SIZE_PX}px;
        border: 1px solid #222; /* Inner grid lines */
        box-sizing: border-box; /* Ensures padding/border are included in element's total size */
        /* Optional: Add a subtle inner shadow or gradient for 3D effect */
        box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
    }}
    /* Block colors - these classes will be dynamically assigned */
    .block-I {{ background-color: {TETROMINO_COLORS['I']}; }}
    .block-O {{ background-color: {TETROMINO_COLORS['O']}; }}
    .block-T {{ background-color: {TETROMINO_COLORS['T']}; }}
    .block-S {{ background-color: {TETROMINO_COLORS['S']}; }}
    .block-Z {{ background-color: {TETROMINO_COLORS['Z']}; }}
    .block-J {{ background-color: {TETROMINO_COLORS['J']}; }}
    .block-L {{ background-color: {TETROMINO_COLORS['L']}; }}
    .block-empty {{ background-color: {TETROMINO_COLORS['empty']}; }}
    .block-locked {{ background-color: {TETROMINO_COLORS['locked']}; }}

    /* Hide Streamlit's default hamburger menu and footer for a cleaner game feel */

    </style>
""", unsafe_allow_html=True)

import streamlit as st
import time # Just for demonstration, to show a dummy update

# (Include the CSS and Configuration from section 1 above first)

# --- Session State Initialization (Crucial for persistence) ---
if 'board_state' not in st.session_state:
    # Initialize an empty board with 'empty' strings
    st.session_state.board_state = [['empty' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    # You could also set some initial blocks here for testing
    # st.session_state.board_state[BOARD_HEIGHT - 1][0] = 'L'
    # st.session_state.board_state[BOARD_HEIGHT - 2][5] = 'T'


st.title("Tetris Board Visualization Demo")
st.write("This shows how to render the board based on `st.session_state.board_state`.")
st.write("You will write the game logic to update `board_state`.")


# --- Board Rendering Function ---
# This function will draw the board based on the current `st.session_state.board_state`
def draw_board(board_data):
    # Start the main container div
    board_html = '<div class="tetris-board-container">'
    for r_idx, row in enumerate(board_data):
        # Start a row div
        board_html += '<div class="tetris-row">'
        for c_idx, cell_value in enumerate(row):
            # Add an individual block div with its appropriate color class
            # The class will be 'block-empty', 'block-I', 'block-O', etc.
            board_html += f'<div class="tetris-block block-{cell_value}"></div>'
        board_html += '</div>' # Close row div
    board_html += '</div>' # Close main container div
    return board_html

# --- Streamlit App Flow ---

# Create an empty placeholder where the board will be rendered.
# This allows us to re-render the board without the whole app jumping.
board_display_placeholder = st.empty()

# --- Example of Board Update (For testing the visualization) ---
# In your actual game, this `if` block would be part of your game loop
# and would update `st.session_state.board_state` based on piece movement.

if st.button("Simulate Piece Drop & Lock"):
    # Clear a random row for demonstration
    random_row_to_clear = random.randint(0, BOARD_HEIGHT - 1)
    st.session_state.board_state[random_row_to_clear] = ['empty' for _ in range(BOARD_WIDTH)]

    # Add a random block at a random position for demonstration
    random_r = random.randint(0, BOARD_HEIGHT - 1)
    random_c = random.randint(0, BOARD_WIDTH - 1)
    random_piece_type = random.choice(list(TETROMINO_COLORS.keys())[:-2]) # Exclude empty/locked
    st.session_state.board_state[random_r][random_c] = random_piece_type
    
    st.rerun() # Force Streamlit to rerun and update the display

if st.button("Reset Board"):
    st.session_state.board_state = [['empty' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    st.rerun()

# Always render the board using the current state
with board_display_placeholder.container():
    st.markdown(draw_board(st.session_state.board_state), unsafe_allow_html=True)

st.write("Now, go build your game logic to update `st.session_state.board_state`!")