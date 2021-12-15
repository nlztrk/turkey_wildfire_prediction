import streamlit as st


def app():
    st.title('Used Datasets')

    with st.expander("1. Active Fire Data"):
        with open('app/markdown/data_active_fire.md', 'r') as f:
            model_details = f.read()
            st.markdown(model_details)
    with st.expander("2. Temperature Data"):
        with open('app/markdown/data_temperatures.md', 'r') as f:
            model_details = f.read()
            st.markdown(model_details)
    with st.expander("References"):
        with open('app/markdown/data_references.md', 'r') as f:
            model_details = f.read()
            st.markdown(model_details)
