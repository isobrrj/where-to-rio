import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

class AuthUser:
    def __init__(self, config_path='./utils/auth/config.yaml'):
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)

        self.authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )

    def login(self):
        return self.authenticator.login()
    
    def logout(self):
        return self.authenticator.logout()
