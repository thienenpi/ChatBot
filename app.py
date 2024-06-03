import streamlit as st
import streamlit_authenticator as stauth
import yaml

from streamlit_authenticator.utilities.exceptions import LoginError
from agents.parameter_selector.measure import user_proxy, assistant, get_measures_from_response
from utils.query import execute_query, QueryGenerator
from utils.convert_data import convert_data
from utils.loader import load_css, load_html
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Chatbot", 
    page_icon="https://tcdata.vn/wp-content/themes/tcdata/assets/images/favicon.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def login():
    html = load_css('templates/css/login.css') + load_html('templates/html/login.html')
    st.markdown(html, unsafe_allow_html=True)
    return authenticator.login()

def get_avatar(name: str):
    if name == "assistant":
        return "https://tcdata.vn/wp-content/themes/tcdata/assets/images/logo_green.svg"
    else:
        return "https://storagetcdata.blob.core.windows.net/images/avatar.png"

try:
    login()
except LoginError as e:
    st.error(e)

def main():
    html = load_css('templates/css/app.css') + load_html('templates/html/app.html')
    st.markdown(html, unsafe_allow_html=True)

    with st.sidebar:
        # openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
        # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "TCData Chatbot - Version 0.0.2:"
        "- UI customed."

        "TCData Chatbot - Version 0.0.1:"
        "- Turn on tcfabric before asking questions."
        "- Only MEASURES related question are supported for now."
        "- Conversation memory is not supported."
        "- [Log stream](https://portal.azure.com/#@tcdata.vn/resource/subscriptions/72fe64ba-7b7a-4803-a4a1-1f8449ab657d/resourceGroups/TC_PAYG/providers/Microsoft.Web/sites/TCDataAI/logStream-quickstart)"
        authenticator.logout()

    st.title("TCData Chatbot")
    st.caption("🚀 A Power BI chatbot powered by TCData")

    query_generator = QueryGenerator()

    # Initialize chat history
    if "messages" not in st.session_state:
        # print("Creating session state")
        st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm your Power BI assistant.\nHow can I help you?"}]

    if "user_prompt" not in st.session_state:
        st.session_state.user_prompt = ""

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(name=message["role"], avatar=get_avatar(message["role"])):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(placeholder="Enter your question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user", avatar=get_avatar("user")):
            st.markdown(prompt)

        st.session_state.user_prompt += st.session_state.messages[-1]["content"] + "\n"
        print(st.session_state.user_prompt)

        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            with st.chat_message("assistant", avatar=get_avatar("assistant")):
                chat_result = user_proxy.initiate_chat(
                    recipient=assistant,
                    message=prompt,
                )
                response = chat_result.chat_history[-1]['content']
                measures = get_measures_from_response(response=response)
                query = query_generator.generate_query(measure=measures)
                result = execute_query(query=query)
                data = convert_data(res=result)

                st.markdown(data)
        st.session_state.messages.append({"role": "assistant", "content": data})
        print(st.session_state.messages)

if __name__ == "__main__":
    if st.session_state["authentication_status"] is True:
        main()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
