import streamlit as st

def app():
    st.title('Project Overview')

    st.markdown("## The Goal")
    st.image("app/media/wildfire.jpg")
    st.markdown("The aim of the project is to predict the probability of wildfire occurrence in Turkey for each month in 2020. As a result of these predictions, it is aimed to carry out more intensive monitoring studies in possible fire areas and to respond to fires very soon after they start. It is also aimed to derive generalizable relations by interpreting the model outputs and the importance attributed to the each variable used by the model.\n\nThe model trained with the data between 2013-2018, validated with the data from 2019. The results you will see are extracted from 2020, which is the test split for this project. The model didn't see any data from this split during the training.")
    st.markdown("## The Motivation")
    st.image("app/media/wildfire_bodrum.png")
    st.markdown("[The wildfires at Turkey](https://en.wikipedia.org/wiki/2021_Turkey_wildfires) started in August 2021, spread over very large areas and resulted in the destruction of large areas and living things due to lack of intervention, have created a big agenda throughout the country. The public and politicians often complained about this technical inadequacy and suggested that improvements should be made in this regard. Within the scope of the project, it was desired to see whether an estimation could be made on this subject throughout the country, and if so, how successful the results would be.")
    st.markdown("## The Flow of the Project")
    st.markdown("You can navigate within the application with the menu on the left. You can access the variables used in the estimation phase, the technical details of the trained machine learning model, and the monthly wildfire probability prediction page via the menu.")