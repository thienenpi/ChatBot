import streamlit as st
import pandas as pd
import time
import altair as alt

from typing import Any

def stream_data(analysis: str):
    for word in analysis.split(" "):
        yield word + " "
        time.sleep(0.05)

def get_avatar(name: str):
    if name == "assistant":
        return "https://tcdata.vn/wp-content/themes/tcdata/assets/images/logo_green.svg"
    else:
        return "https://storagetcdata.blob.core.windows.net/images/avatar.png"

def render_data(data: pd.DataFrame):
    st.dataframe(
        data=data, 
        use_container_width=True,
        hide_index=True
    )

def render_chart(visualization: dict, data: pd.DataFrame):
    if visualization['chart_type'] == 'line chart':
        line_chart = alt.Chart(data).mark_line().encode(
            y=alt.Y(visualization['y_axis']),
            x=alt.X(visualization['x_axis'], sort=None),
        ).properties(
            height=400, width=700,
            title="Sale (fixed)"
        ).configure_title(
            fontSize=16
        )

        st.altair_chart(line_chart, use_container_width=True)    
    elif visualization['chart_type'] == 'bar chart':
        bar_chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(visualization['x_axis']),
            y=alt.Y(visualization['y_axis']),
        ).properties(
            height=400, width=700,
            title="Sale (fixed)"
        ).configure_title(
            fontSize=16
        )

        st.altair_chart(bar_chart, use_container_width=True)
    else:
        raise ValueError(f"Unsupported chart type: {visualization['chart_type']}")

def render_analytics(analytics: str):
    st.write_stream(stream_data(analytics))

def re_render_analytics(analytics: str):
    st.markdown(analytics)

def render_view_citation_button(index: int, citation: str):
    label = f'{index + 1}' + "\. " + citation
    st.button(label=label, on_click=lambda: render_citation(citation=citation))

def render_citation(citation: str):
    if citation == st.session_state.citation or st.session_state.citation == "":
        st.session_state.single_column = not st.session_state.single_column
    st.session_state.citation = citation

def render_chat_message(message: dict[str, Any]):
    with st.chat_message(name=message["role"], avatar=get_avatar(message["role"])):
        if message['role'] == "assistant":
            data = message["content"]["data"]
            analytics = message["content"]["analytics"]

            # if data is not None:
                # render_data(data)
                # render_chart(data)
            render_analytics(analytics)
        else:
            st.markdown(body=message["content"])

def render_chat_history(messages: list[dict[str, Any]]):
    for message in messages:
        render_chat_message(message)