import streamlit as st
import pandas as pd

from parameters.measure import user_proxy, assistant, get_measures_from_response
from utils.query import execute_query, QueryGenerator
from utils.convert_data import convert_data

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

with st.sidebar:
#     openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
    # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "TCData Chatbot - Version 0.0.1:"
    "- Turn on tcfabric before asking questions"
    "- Only MEASURES are supported for now"
    "- Conversation memory is not finished yet"

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
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(placeholder="Enter your question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.user_prompt += st.session_state.messages[-1]["content"] + "\n"
    print(st.session_state.user_prompt)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            chat_result = user_proxy.initiate_chat(
                recipient=assistant,
                message=st.session_state.user_prompt,
            )
            response = chat_result.chat_history[-1]['content']
            measures = get_measures_from_response(response=response)
            query = query_generator.generate_query(measure=measures)
            result = execute_query(query=query)
            data = convert_data(res=result)

            st.markdown(data)
    st.session_state.messages.append({"role": "assistant", "content": data})
    print(st.session_state.messages)