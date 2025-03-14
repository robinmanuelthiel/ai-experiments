import streamlit as st
import numpy as np
import pandas as pd

# Sidebar
with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Title
st.write("Hello world")

# Slider
number = st.slider("Pick a number", 0, 100)

# Table
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# Chart
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)


# Colums
left_column, right_column = st.columns(2)
left_column.button('Press me!') # You can use a column just like st.sidebar:

with right_column: # Or even better, call Streamlit functions inside a "with" block:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

# Chat
st.chat_message("user").write("hello")
st.chat_message("assistant").write("world")

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.chat_message("user").write(prompt)
