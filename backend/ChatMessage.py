import pandas as pd
import streamlit as st

from typing import Optional

from components.chat_message import (
    render_chart, 
    render_analytics, 
    get_avatar, 
    render_view_citation_button
)
from utils.loader import load_html, load_css

class MessageContent:
    data: Optional[pd.DataFrame] = None
    visualization: Optional[dict] = None
    analytics: Optional[str] = None
    results: Optional[list[dict]] = None
    summary: Optional[str] = None
    prompt: Optional[str] = None

    def __init__(self,
                 data: Optional[pd.DataFrame] = None, 
                 visualization: Optional[dict] = None, 
                 analytics: Optional[str] = None, 
                 results: Optional[list[dict]] = None, 
                 summary: Optional[str] = None, 
                 prompt: Optional[str] = None) -> None:
        self.data = data
        self.visualization = visualization
        self.analytics = analytics
        self.results = results
        self.summary = summary
        self.prompt = prompt
    
    def render(self, re_render: bool):
        if self.data is not None and self.visualization is not None and self.analytics is not None:
            return self._render_visualization_analytics(re_render=re_render)
        elif self.results is not None and self.summary is not None:
            return self._render_results_summary(re_render=re_render)
        elif self.prompt is not None:
            return self._render_prompt()
        else:
            raise ValueError("Invalid state for rendering")

    def _render_visualization_analytics(self, re_render: bool):
        # Implement rendering logic for data, visualization, and analytics
        render_chart(visualization=self.visualization, data=self.data)
        st.markdown(self.analytics) if re_render else render_analytics(analytics=self.analytics)

    def _render_results_summary(self, re_render: bool):
        # Implement rendering logic for results and summary
        st.markdown(self.summary) if re_render else render_analytics(analytics=self.summary)
        if len(self.results) > 0:
            st.markdown("**Citation:**\n")
        else:
            st.markdown("**No citation found.**\n")
        for index, result in enumerate(self.results):
            render_view_citation_button(index=index, citation=str(result['sourcefile']).split("/")[-1] + "#" + str(result['sourcepage'])) 

    def _render_prompt(self):
        # Implement rendering logic for prompt
        st.markdown(self.prompt)

class ChatMessage:
    sender: str
    message: MessageContent
    mode: str

    def __init__(self, sender: str, message: MessageContent, mode: str) -> None:
        self.sender = sender
        self.message = message
        self.mode = mode

        if mode == 'Chatbot':
            self = ChatBotMessage(sender, message, mode)
        else:
            self = AISearchMessage(sender, message, mode)

    def render(self, re_render: bool = False):
        with st.chat_message(name=self.sender, avatar=get_avatar(self.sender)):
            self.message.render(re_render=re_render)

class ChatBotMessage(ChatMessage):
    def __init__(self, sender: str, message: MessageContent, mode: str) -> None:
        self.sender = sender
        self.message = message
        self.mode = mode

    def render(self, re_render: bool = False):
        with st.chat_message(name=self.sender, avatar=get_avatar(self.sender)):
            self.message.render(re_render=re_render)

class AISearchMessage(ChatMessage):
    def __init__(self, sender: str, message: MessageContent, mode: str) -> None:
        self.sender = sender
        self.message = message
        self.mode = mode

    def render(self, re_render: bool = False):
        with st.chat_message(name=self.sender, avatar=get_avatar(self.sender)):
            self.message.render(re_render=re_render)