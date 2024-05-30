import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def load_css():
    with open('auth/styles/login.css') as f:
        css = f'<style>{f.read()}</style>'
        st.markdown(css, unsafe_allow_html=True)

def load_html():
    with open('auth/html/login.html') as f:
        html = f.read()
        st.markdown(html, unsafe_allow_html=True)

def login():
    load_css()
    load_html()
    return authenticator.login()