from app import inference, model_variables, overview, model_details, dataset_introduction, performance, wildfire_data_insights, temperature_data_insights, training_data_insights
import streamlit as st


PAGES = {
    "Project Overview": overview,
    "Used Datasets": dataset_introduction,
    "Wildfire Data Insights": wildfire_data_insights,
    "Temperature Data Insights": temperature_data_insights,
    "Training Data Insights": training_data_insights,
    "Used Variables": model_variables,
    "Model Details": model_details,
    "Prediction": inference,
    "Evaluation": performance
}

CATEGORIES = ["Overview", "Data Analysis", "Pipeline Details", "Runtime"]

st.sidebar.image("app/media/turkey_wildfire_logo.png", width=285)
#st.sidebar.title('Menu')
#selection = st.sidebar.radio("", list(PAGES.keys()))

st.sidebar.markdown("First select a category and then the page you want to view that belongs to the selected category.")

st.sidebar.markdown("## Select a category:")
#cat_selection = st.sidebar.selectbox("", CATEGORIES)
cat_selection = st.sidebar.radio("", CATEGORIES)

st.sidebar.markdown("## Select a page:")

if cat_selection == "Overview":
    #selection = st.sidebar.selectbox("", list(PAGES.keys())[:2])
    selection = st.sidebar.radio("", list(PAGES.keys())[:2])
elif cat_selection == "Data Analysis":
    #selection = st.sidebar.selectbox("", list(PAGES.keys())[2:4])
    selection = st.sidebar.radio("", list(PAGES.keys())[2:5])
if cat_selection == "Pipeline Details":
    #selection = st.sidebar.selectbox("", list(PAGES.keys())[4:6])
    selection = st.sidebar.radio("", list(PAGES.keys())[5:7])
if cat_selection == "Runtime":
    #selection = st.sidebar.selectbox("", list(PAGES.keys())[6:])
    selection = st.sidebar.radio("", list(PAGES.keys())[7:])


print(selection)
page = PAGES[selection]
page.app()
