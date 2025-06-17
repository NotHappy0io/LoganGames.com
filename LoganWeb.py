import streamlit as st

st.set_page_config(
    page_title="My Awesome App",
    page_icon="🎮",
    layout="centered"
)

st.title("Welcome to the App! 🎮")
st.write("Navigate to the Phone Charging Game using the sidebar.")

st.markdown("---")

st.header("App Features:")
st.write("""
- **Phone Charging Game**: Test your clicking speed to keep your phone alive!
- More features coming soon...
""")

# --- Sidebar Content ---
# Everything inside this 'with' block will be in the sidebar
with st.sidebar:
    st.header("Sidebar Controls and Info")
    st.write("Use the elements below to interact with the app or find information.")

    # A selectbox widget
    option = st.selectbox(
        "Choose a theme!", # Corrected "an theme" to "a theme"
        ("2D", "3D", "IDLE")
    )
    # You could use the 'option' variable later to conditionally display content
    # or change game aspects based on the selected theme.

    # A checkbox
    agree = st.checkbox("I agree to the terms and conditions")
    # You might want to add logic here, e.g., if not agree, disable certain features

    # A text input
    user_name = st.text_input("Enter your name", "Guest")
    st.write(f"Hello, {user_name}!")

    # A button
    if st.button("Don't know what to play? Click me!"): # Corrected "Dont" to "Don't"
        st.success("Placeholder for a game or action!")
        # Here, you could potentially use st.switch_page("pages/game_page.py")
        # to navigate the user directly to a game, but it might feel abrupt.
        # Often, this button would trigger a random game suggestion or similar.

    # An image in the sidebar
    st.image("https://via.placeholder.com/150?text=Sidebar+Image", caption="A little image")

    # Some static text
    st.write("Developed with ❤️ using Streamlit.")
    # You can update the time dynamically using Python's datetime module:
    current_time = st.session_state.get('current_time', '') # Initialize if not exists
    st.write(f"Current time: {current_time}")

    # To update the time dynamically, you'd typically need to trigger a rerun.
    # For a simple display, this is fine. For live updates, you'd need a loop
    # with st.rerun() like in your game page, but that's usually overkill for static info.

# Ensure your 'pages' folder and 'game_page.py' are set up correctly as before.