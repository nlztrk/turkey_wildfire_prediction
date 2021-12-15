import streamlit as st


def app():
    with open('app/markdown/model_variables.md', 'r') as f:
        model_details = f.read()
        st.markdown(model_details)
