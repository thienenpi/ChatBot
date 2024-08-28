import streamlit as st

from autogen import initiate_chats

from agents.parameter_selector.measure import measures_selector, get_measures_from_response
from agents.parameter_selector.groupby_column import columns_selector, get_columns_from_response
from agents.parameter_selector.data_visualization import data_visualizer, get_visualization_from_result
from agents.financial_analyzer.financial_analyzer import financial_analyzer, get_analytics_from_result
from agents.user_proxy import user_proxy, generate_prompt_from_res

from backend.ChatMessage import ChatMessage, MessageContent

from utils.query import execute_query, QueryGenerator
from utils.convert_data import convert_data
from utils.loader import load_css, load_html
from utils.citation import get_citation

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

def render_heading():
    html = load_css('templates/css/dataChatbot.css') + load_html('templates/html/app.html')
    st.markdown(html, unsafe_allow_html=True)

def render_chat_history(messages: list[ChatMessage]):
    for message in messages:
        message.render(re_render=True)

def render_chat_view(messages: list[ChatMessage]):
    render_heading()
    render_chat_history(messages=messages)

def render_chat_input(mode: str):
    query_generator: QueryGenerator = QueryGenerator()
    # Accept user input
    if prompt := st.chat_input(placeholder="Enter your question..."):
        # Add user message to chat history
        user_message = ChatMessage(sender="user", message=MessageContent(prompt=prompt), mode=mode)
        user_message.render()
        st.session_state.messages.append(user_message)

        # Display assistant response in chat message container
        with st.spinner("Generating response..."):
            chat_results = initiate_chats([
                {
                    "sender": user_proxy,
                    "recipient": measures_selector,
                    "message": prompt,
                },
                {
                    "sender": user_proxy,
                    "recipient": columns_selector,
                    "message": prompt,
                }
            ])
            responses = [chat_result.chat_history[-1]['content'] for chat_result in chat_results]
            
            # select parameters
            measures = get_measures_from_response(response=responses[0])
            columns = get_columns_from_response(response=responses[1])
            print(columns)
            query = query_generator.generate_query(measure=measures, groupby_columns=columns)
            print(query)
            
            # execute query
            response = execute_query(query=query)
            data = convert_data(res=response)

            # prompt to visualize the data
            chat_result = user_proxy.initiate_chat(
                recipient=data_visualizer,
                message=str(data.columns.values)
            )
            result = chat_result.chat_history[-1]['content']
            visualization = get_visualization_from_result(result=result)
            
            # prompt to analyze the data
            prompt_to_analyze = generate_prompt_from_res(res=response, question=prompt)
            chat_result = user_proxy.initiate_chat(
                recipient=financial_analyzer,
                message=prompt_to_analyze
            )
            result = chat_result.chat_history[-1]['content']
            analytics = get_analytics_from_result(result=result)

            assistant_message = ChatMessage(
                sender='assistant',
                message=MessageContent(
                    data=data,
                    visualization=visualization,
                    analytics=analytics
                ),
                mode=mode
            )
            st.session_state.messages.append(assistant_message)            
        assistant_message.render()

def main():
    # st.session_state.clear()  
    mode = 'Chatbot'
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            ChatMessage(
                sender="assistant",
                message=MessageContent(
                    prompt="Welcome to TCData Chatbot! How can I help you today?"
                ),
                mode=mode
            )
        ]

    if "citation" not in st.session_state:
        st.session_state.citation = ""

    if 'single_column' not in st.session_state:
        st.session_state.single_column = True

    if st.session_state.single_column:
        # Display chat messages from history on app rerun
        render_chat_view(messages=st.session_state.messages)
        render_chat_input(mode=mode)
    else:
        col1, col2 = st.columns(2)
        with col1:
            render_chat_view(messages=st.session_state.messages)
            render_chat_input(mode=mode)
        with col2:
            pdf_display = get_citation(source_page=st.session_state.citation)
            st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
