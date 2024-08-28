import streamlit as st

from backend.AzureAISearch import AzureAISearch
from backend.ChatMessage import ChatMessage, MessageContent

from utils.loader import load_css, load_html
from utils.citation import get_citation

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

def render_heading():
    html = load_css('templates/css/documentSearch.css') + load_html('templates/html/app.html')
    st.markdown(html, unsafe_allow_html=True)

def render_chat_history(messages: list[ChatMessage]):
    for message in messages:
        message.render(re_render=True)

def render_chat_view(messages: list[ChatMessage]):
    render_heading()
    render_chat_history(messages=messages)

def render_chat_input(mode: str):
    searcher: AzureAISearch = AzureAISearch()
    # Accept user input
    if prompt := st.chat_input(placeholder="Enter your question..."):
        # Add user message to chat history
        user_message = ChatMessage(sender="user", message=MessageContent(prompt=prompt), mode=mode)
        user_message.render()
        st.session_state.messages.append(user_message)

        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            results = searcher.get_results_semantic_search(query=prompt)
            summary = searcher.get_summary(query=prompt, results=results)
            assistant_message = ChatMessage(
                sender='assistant',
                message=MessageContent(
                    results=results,
                    summary=summary
                ),
                mode=mode
            )
            st.session_state.messages.append(assistant_message)
        assistant_message.render()

def main():
    # st.session_state.clear()
    # print('state cleared')
    mode = 'Document Search'

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            ChatMessage(
                sender="assistant",
                message=MessageContent(
                    prompt="Welcome to TCData Document Search! How can I help you today?"
                ),
                mode=mode
            )
        ]

    if "citation" not in st.session_state:
        st.session_state.citation = ""

    if 'single_column' not in st.session_state:
        st.session_state.single_column = True

    if st.session_state.single_column:
        print(st.session_state.single_column)
        print(st.session_state.messages)
        # Display chat messages from history on app rerun
        render_chat_view(messages=st.session_state.messages)
        render_chat_input(mode=mode)
    else:
        print(st.session_state.single_column)
        col1, col2 = st.columns(2)
        with col1:
            render_chat_view(messages=st.session_state.messages)
            render_chat_input(mode=mode)
            st.container(height=100, border=0)
        with col2:
            pdf_display = get_citation(source_page=st.session_state.citation)
            st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
