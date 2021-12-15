from app import inference, model_variables, overview, model_details, dataset_introduction, performance
import streamlit as st



PAGES = {
    "Overview": overview,
    "Data": dataset_introduction,
    "Variables": model_variables,
    "Model Details": model_details,
    "Prediction": inference,
    "Evaluation": performance
}
st.sidebar.image("app/media/turkey_wildfire_logo.png", width=180)
#st.sidebar.title('Menu')

selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]
page.app()
