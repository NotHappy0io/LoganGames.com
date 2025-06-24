import streamlit as st
import time # For simulation of time passing

# --- Configuration ---
MAX_BATTERY = 100
INITIAL_BATTERY = 50
CHARGE_PER_CLICK = 5 # How much battery a single click adds
DISCHARGE_RATE = 1   # How many percentage points per "tick"
DISCHARGE_INTERVAL = 0.5 # How often (in seconds) the battery discharges

if not st.session_state['authentication_status']:
    # show a message if the user is not logged in
    st.error("You need to log in to play the game. Please log in first.")
    st.stop()  # Stop further execution if not logged in
    
# --- Session State Initialization ---
# This ensures variables persist across reruns
if 'battery_level' not in st.session_state:
    st.session_state.battery_level = INITIAL_BATTERY
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- CSS for Phone Frame (Graphical Window) ---
st.markdown(
    """
    <style>
    .phone-frame {
        border: 10px solid #333;
        border-radius: 20px;
        padding: 20px;
        background-color: #f0f0f0;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        width: 300px; /* Adjust width as needed */
        margin: 50px auto; /* Center the frame */
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative; /* For the progress bar placement */
    }

    /* Style for the battery progress bar inside the frame */
    .stProgress > div > div {
        border-radius: 5px;
        height: 30px; /* Make the progress bar taller */
        transition: width 0.1s linear; /* Smooth transition for discharge */
    }

    /* Color of the progress bar based on level */
    .stProgress > div > div > div {
        background-color: green; /* Default to green */
    }
    .stProgress.low-battery > div > div > div {
        background-color: orange; /* Change to orange if low */
    }
    .stProgress.critical-battery > div > div > div {
        background-color: red; /* Change to red if critical */
    }

    /* Text on top of progress bar */
    .battery-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: black; /* Or white, depending on contrast */
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
        z-index: 10; /* Ensure text is above bar */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Game Functions ---

def charge_battery():
    if not st.session_state.game_over:
        st.session_state.battery_level += CHARGE_PER_CLICK
        if st.session_state.battery_level > MAX_BATTERY:
            st.session_state.battery_level = MAX_BATTERY # Cap at max
        # Rerun to update the display immediately after click
        # st.experimental_rerun() # Not strictly needed if loop handles updates

def reset_game():
    st.session_state.battery_level = INITIAL_BATTERY
    st.session_state.game_over = False
    st.experimental_rerun() # Rerun to reset the entire display

# --- Game UI Layout ---
st.title("Phone Charging Game 🔋")
st.write("Click the 'Charge Phone' button to keep your phone from dying!")

# Create a placeholder for the entire game display within the phone frame
game_container = st.empty()

# --- Game Loop (Simulating continuous discharge) ---
# We use an infinite loop that breaks if the game is over.
# Streamlit's rerun mechanism will handle the loop effectively.
while True:
    with game_container.container():
        # Apply CSS class based on battery level for color
        progress_class = ""
        if st.session_state.battery_level <= 20:
            progress_class = "critical-battery"
        elif st.session_state.battery_level <= 40:
            progress_class = "low-battery"

        # --- Phone Frame and Battery Display ---
        st.markdown('<div class="phone-frame">', unsafe_allow_html=True)

        # Use an empty slot for the battery text to overlay it
        battery_text_placeholder = st.empty()

        # Display the progress bar
        # We need to render the progress bar with a custom class via markdown as `st.progress` doesn't support custom classes directly.
        # This is a bit of a workaround to get the custom colors based on battery level.
        st.markdown(f'<div class="stProgress {progress_class}"><div><div style="width:{st.session_state.battery_level}%;background-color:{ "red" if st.session_state.battery_level <= 20 else ("orange" if st.session_state.battery_level <= 40 else "green")};"></div></div></div>', unsafe_allow_html=True)
        # Update the text on top
        battery_text_placeholder.markdown(f'<div class="battery-text">{st.session_state.battery_level}%</div>', unsafe_allow_html=True)


        st.markdown('</div>', unsafe_allow_html=True) # Close phone-frame div


        # --- Game Controls ---
        if not st.session_state.game_over:
            st.button("Charge Phone!", on_click=charge_battery, use_container_width=True)
            if st.session_state.battery_level <= 0:
                st.session_state.game_over = True
                st.error("💀 Game Over! Your phone ran out of battery! 💀")
                st.button("Play Again", on_click=reset_game)
        else:
            st.error("💀 Game Over! Your phone ran out of battery! 💀")
            st.button("Play Again", on_click=reset_game)

    # --- Discharge Logic ---
    if not st.session_state.game_over:
        st.session_state.battery_level -= DISCHARGE_RATE
        if st.session_state.battery_level < 0:
            st.session_state.battery_level = 0 # Ensure it doesn't go negative
        time.sleep(DISCHARGE_INTERVAL)
        # Force a rerun to update the display and continue the loop
        st.rerun() # This is crucial for the continuous discharge
    else:
        # If game is over, break the loop to stop reruns from within the loop
        # The 'Play Again' button will trigger a rerun when clicked.
        break