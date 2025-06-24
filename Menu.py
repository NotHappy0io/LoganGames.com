import streamlit as st
import streamlit_authenticator as stauth


st.set_page_config(
    page_title="My Awesome App",
    page_icon="🎮",
    layout="centered"
)

import yaml
from yaml.loader import SafeLoader

# Pre-hashing all plain text passwords once
# Hasher.hash_passwords(config['credentials'])

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


st.title("Welcome to the App! 🎮")
st.write("Navigate to the Phone Charging Game using the sidebar.")

st.markdown("---")

st.header("App Features:")
st.write("""
- **Phone Charging Game**: Test your clicking speed to keep your phone alive!
- More features coming soon...
""")

# Lets create a login menu:


try:
    authenticator.login()
except Exception as e:
    st.error(e)

# try:
#     authenticator.experimental_guest_login('Login with Google',
#                                            provider='google',
#                                            oauth2=config['oauth2'])
#     authenticator.experimental_guest_login('Login with Microsoft',
#                                            provider='microsoft',
#                                            oauth2=config['oauth2'])
# except Exception as e:
#     st.error(e)


if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')


# create a button to show the registration form
if st.button('Register a new user'):
    # Toggle the registration form visibility
    if 'show_registration_form' not in st.session_state:
        st.session_state['show_registration_form'] = True
    else:
        st.session_state['show_registration_form'] = not st.session_state['show_registration_form']

# Conditionally show the registration part
if st.session_state.get('show_registration_form', False):
    try:
        email_of_registered_user, \
        username_of_registered_user, \
        name_of_registered_user = authenticator.register_user(
            pre_authorized=config['pre-authorized']['emails']
        )
        if email_of_registered_user:
            st.success('User registered successfully')
            # Optionally, hide the form after successful registration
            st.session_state['show_registration_form'] = False
            # You might also want to save the updated config here
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.rerun() # Rerun to update the app with the new user in config
    except Exception as e:
        st.error(e)