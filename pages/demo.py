import streamlit as st
import time
import random
import copy # For deep copying piece shapes

# --- Configuration ---
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE_PX = 25 # Size of each block for display

# Game tick interval (how fast the piece falls)
FALL_INTERVAL_INITIAL = 0.5 # seconds

# --- Tetromino Shapes (using 4x4 bounding box) ---
# Each shape is a list of coordinates (row, col) relative to its top-left corner
TETROMINOES = {
    'I': [[0,0], [0,1], [0,2], [0,3]], # Flat I
    'I_rot': [[0,0], [1,0], [2,0], [3,0]], # Vertical I
    'O': [[0,0], [0,1], [1,0], [1,1]],
    'T': [[0,1], [1,0], [1,1], [1,2]],
    'S': [[0,1], [0,2], [1,0], [1,1]],
    'Z': [[0,0], [0,1], [1,1], [1,2]],
    'J': [[0,0], [1,0], [1,1], [1,2]],
    'L': [[0,2], [1,0], [1,1], [1,2]],
}

TETROMINO_COLORS = {
    'I': '#00FFFF', # Cyan
    'O': '#FFFF00', # Yellow
    'T': '#800080', # Purple
    'S': '#00FF00', # Green
    'Z': '#FF0000', # Red
    'J': '#0000FF', # Blue
    'L': '#FFA500', # Orange
    'empty': '#333333', # Dark background for empty cells
    'locked': '#666666' # A bit lighter for locked blocks
}

# Mapping for rotations (simple for basic shapes, more complex for proper Tetris)
ROTATIONS = {
    'I': 'I_rot',
    'I_rot': 'I',
    'O': 'O', # O doesn't rotate visually
    'T': 'T_rot1', # Placeholder, actual rotation logic below
    # ... define more complex rotations for T, S, Z, J, L
    # For simplicity, we'll implement basic rotation for now
}

# --- Session State Initialization ---
if 'board' not in st.session_state:
    st.session_state.board = [['empty' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
if 'current_piece' not in st.session_state:
    st.session_state.current_piece = None
if 'piece_pos' not in st.session_state: # [row, col] of top-left corner
    st.session_state.piece_pos = [0, 0]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'fall_interval' not in st.session_state:
    st.session_state.fall_interval = FALL_INTERVAL_INITIAL
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- CSS for Board and Blocks ---
st.markdown(f"""
    <style>
    .tetris-board-container {{
        background-color: black;
        border: 5px solid #555;
        display: flex;
        flex-direction: column;
        width: {BOARD_WIDTH * BLOCK_SIZE_PX}px; /* Adjust based on block size */
        margin: 20px auto;
        box-shadow: 0px 0px 15px rgba(0,255,255,0.7);
        padding: 5px;
    }}
    .tetris-row {{
        display: flex;
    }}
    .tetris-block {{
        width: {BLOCK_SIZE_PX}px;
        height: {BLOCK_SIZE_PX}px;
        border: 1px solid #444; /* Grid lines */
        box-sizing: border-box; /* Include padding and border in the element's total width and height */
    }}
    /* Block colors */
    .block-I {{ background-color: {TETROMINO_COLORS['I']}; }}
    .block-I_rot {{ background-color: {TETROMINO_COLORS['I']}; }}
    .block-O {{ background-color: {TETROMINO_COLORS['O']}; }}
    .block-T {{ background-color: {TETROMINO_COLORS['T']}; }}
    .block-S {{ background-color: {TETROMINO_COLORS['S']}; }}
    .block-Z {{ background-color: {TETROMINO_COLORS['Z']}; }}
    .block-J {{ background-color: {TETROMINO_COLORS['J']}; }}
    .block-L {{ background-color: {TETROMINO_COLORS['L']}; }}
    .block-empty {{ background-color: {TETROMINO_COLORS['empty']}; }}
    .block-locked {{ background-color: {TETROMINO_COLORS['locked']}; }}
    </style>
""", unsafe_allow_html=True)

# --- Game Logic Functions ---

def create_new_piece():
    if st.session_state.game_over:
        return
    piece_type = random.choice(list(TETROMINOES.keys()))
    if piece_type.endswith('_rot'): # Ensure we start with a base shape
        piece_type = piece_type.split('_')[0]
    st.session_state.current_piece = {'type': piece_type, 'shape': TETROMINOES[piece_type]}
    st.session_state.piece_pos = [0, (BOARD_WIDTH // 2) - 2] # Start near top-middle

    # Check for immediate game over
    if check_collision(st.session_state.current_piece['shape'], st.session_state.piece_pos[0], st.session_state.piece_pos[1]):
        st.session_state.game_over = True

def check_collision(shape, row_offset, col_offset):
    for r, c in shape:
        board_r, board_c = row_offset + r, col_offset + c

        # Check bounds
        if not (0 <= board_c < BOARD_WIDTH and 0 <= board_r < BOARD_HEIGHT):
            return True # Collision with wall or floor

        # Check existing blocks
        if st.session_state.board[board_r][board_c] != 'empty':
            return True # Collision with a locked block
    return False

def lock_piece():
    piece_type = st.session_state.current_piece['type']
    for r, c in st.session_state.current_piece['shape']:
        board_r, board_c = st.session_state.piece_pos[0] + r, st.session_state.piece_pos[1] + c
        st.session_state.board[board_r][board_c] = piece_type # Mark with piece type for coloring

    # Clear lines (simplified for now)
    clear_lines()

    st.session_state.current_piece = None # No current piece
    create_new_piece() # Create next piece

def clear_lines():
    rows_to_clear = []
    for r_idx, row in enumerate(st.session_state.board):
        if all(cell != 'empty' for cell in row):
            rows_to_clear.append(r_idx)

    if rows_to_clear:
        # Move rows down
        for r_idx in sorted(rows_to_clear, reverse=True):
            del st.session_state.board[r_idx]
            # Add a new empty row at the top
            st.session_state.board.insert(0, ['empty' for _ in range(BOARD_WIDTH)])
        st.session_state.score += len(rows_to_clear) * 100 # Basic scoring

def move_piece(dr, dc):
    if st.session_state.game_over or not st.session_state.current_piece:
        return

    new_row, new_col = st.session_state.piece_pos[0] + dr, st.session_state.piece_pos[1] + dc
    if not check_collision(st.session_state.current_piece['shape'], new_row, new_col):
        st.session_state.piece_pos = [new_row, new_col]
        return True # Move successful
    return False # Move failed (collision)

def rotate_piece():
    if st.session_state.game_over or not st.session_state.current_piece:
        return

    current_type = st.session_state.current_piece['type']
    # Simplified rotation: just flip I piece or do nothing for others for now
    if current_type == 'I':
        new_type = 'I_rot'
    elif current_type == 'I_rot':
        new_type = 'I'
    else:
        # For other pieces, a proper rotation involves matrix math
        # This is a placeholder that does not implement full rotation
        # A common way is to rotate relative to a pivot point [px, py]
        # new_r = -(c - py) + px
        # new_c = (r - px) + py
        # For simplicity, we'll keep other pieces fixed in this example
        st.warning("Rotation for non-I pieces is not fully implemented in this demo.")
        return

    # Create a new shape based on the potential rotation
    temp_shape = TETROMINOES.get(new_type)
    if not temp_shape: # If the rotated type isn't defined, don't rotate
        return

    # Check for collision with new rotated shape
    if not check_collision(temp_shape, st.session_state.piece_pos[0], st.session_state.piece_pos[1]):
        st.session_state.current_piece['type'] = new_type
        st.session_state.current_piece['shape'] = temp_shape

def game_tick():
    if st.session_state.game_over:
        return

    if not st.session_state.current_piece:
        create_new_piece()
        if st.session_state.game_over: # Check if new piece immediately causes game over
            return

    # Try to move piece down
    if not move_piece(1, 0): # Try to move down by 1 row
        # If cannot move down, lock the piece
        lock_piece()

def reset_game():
    st.session_state.board = [['empty' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    st.session_state.current_piece = None
    st.session_state.piece_pos = [0, 0]
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.fall_interval = FALL_INTERVAL_INITIAL
    st.session_state.game_started = False
    st.rerun()

# --- Streamlit UI ---
st.title("Streamlit Tetris 👾")

# Game board placeholder (allows us to update the board dynamically)
board_placeholder = st.empty()

# Control Panel
st.sidebar.header("Controls")
if not st.session_state.game_started:
    if st.sidebar.button("Start Game", use_container_width=True):
        st.session_state.game_started = True
        create_new_piece()
        st.rerun()
elif st.session_state.game_over:
    st.sidebar.error("Game Over!")
    st.sidebar.button("Play Again", on_click=reset_game, use_container_width=True)
else:
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.button("⬅️ Left", on_click=move_piece, args=(0, -1), use_container_width=True)
    with col2:
        st.button("⬇️ Down", on_click=move_piece, args=(1, 0), use_container_width=True)
    with col3:
        st.button("➡️ Right", on_click=move_piece, args=(0, 1), use_container_width=True)
    st.sidebar.button("🔃 Rotate", on_click=rotate_piece, use_container_width=True)
    st.sidebar.button("Restart Game", on_click=reset_game, use_container_width=True)

st.sidebar.markdown(f"**Score: {st.session_state.score}**")

# --- Game Loop (Reruns to simulate real-time) ---
if st.session_state.game_started and not st.session_state.game_over:
    # This block will re-render the board and advance the game state

    # Create a temporary board for display, including the falling piece
    display_board = copy.deepcopy(st.session_state.board)
    if st.session_state.current_piece:
        piece_shape = st.session_state.current_piece['shape']
        piece_color_type = st.session_state.current_piece['type']
        for r, c in piece_shape:
            board_r, board_c = st.session_state.piece_pos[0] + r, st.session_state.piece_pos[1] + c
            # Ensure drawing only if within bounds and not overlapping existing locked blocks (shouldn't happen due to collision check)
            if 0 <= board_r < BOARD_HEIGHT and 0 <= board_c < BOARD_WIDTH and display_board[board_r][board_c] == 'empty':
                 display_board[board_r][board_c] = piece_color_type

    with board_placeholder.container():
        st.markdown('<div class="tetris-board-container">', unsafe_allow_html=True)
        for r_idx, row in enumerate(display_board):
            st.markdown('<div class="tetris-row">', unsafe_allow_html=True)
            for c_idx, cell_value in enumerate(row):
                # Use the piece type as the CSS class for coloring
                st.markdown(f'<div class="tetris-block block-{cell_value}"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True) # Close tetris-row
        st.markdown('</div>', unsafe_allow_html=True) # Close tetris-board-container

    # Advance game state and schedule next rerun
    time.sleep(st.session_state.fall_interval)
    game_tick() # Move piece down or lock it
    st.rerun() # Force Streamlit to rerun the script immediately

elif st.session_state.game_over:
    # Display final board and game over message
    with board_placeholder.container():
        st.markdown('<div class="tetris-board-container">', unsafe_allow_html=True)
        for r_idx, row in enumerate(st.session_state.board):
            st.markdown('<div class="tetris-row">', unsafe_allow_html=True)
            for c_idx, cell_value in enumerate(row):
                st.markdown(f'<div class="tetris-block block-{cell_value}"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.error("GAME OVER! Your final score: " + str(st.session_state.score))
    st.button("Play Again", on_click=reset_game)

else: # Before game starts
    with board_placeholder.container():
        st.markdown('<div class="tetris-board-container">', unsafe_allow_html=True)
        for r_idx in range(BOARD_HEIGHT):
            st.markdown('<div class="tetris-row">', unsafe_allow_html=True)
            for c_idx in range(BOARD_WIDTH):
                st.markdown(f'<div class="tetris-block block-empty"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.info("Press 'Start Game' to begin!")