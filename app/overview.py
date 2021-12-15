import streamlit as st


def app():
    st.title('Project Overview')

    st.markdown("## The Goal")
    st.image("app/media/wildfire.jpg")
    st.markdown("The aim of the project is to predict the probability of wildfire occurrence in Turkey for each month in 2020. As a result of these predictions, it is aimed to carry out more intensive monitoring studies in possible fire areas and to respond to fires very soon after they start. It is also aimed to derive generalizable relations by interpreting the model outputs and the importance attributed to the each variable used by the model.\n\nThe model trained with the data between 2013-2018, validated with the data from 2019. The results you will see are extracted from 2020, which is the test split for this project. The model didn't see any data from this split during the training.")
    st.markdown("## The Motivation")
    st.image("app/media/wildfire_bodrum.png")
    st.markdown("[The wildfires at Turkey](https://en.wikipedia.org/wiki/2021_Turkey_wildfires) started in August 2021, spread over very large areas and resulted in the destruction of large areas and living things due to lack of intervention, have created a big agenda throughout the country. The public and politicians often complained about this technical inadequacy and suggested that improvements should be made in this regard. Within the scope of the project, it was desired to see whether an estimation could be made on this subject throughout the country, and if so, how successful the results would be.")
    st.markdown('## The Goal')
    st.image("app/media/sample_prediction.png")
    st.markdown('The goal of the project is to estimate the probability of a wildfire occurrence for each month of 2020 for each grid segment by dividing the area of Turkey in latitude and longitude with 1 degree precision.\
It is defined in the H2O Competition Overview as *"Predicting the behavior of wildfires"*.\n\
## Potential Audience\n\
Since the probability of wildfire occurence in certain areas in the future is being calculated, the following groups and individuals can benefit from this project:\n\
- **Firefighters:** Fire departments can keep firefighter density higher in risky areas, this way faster response can be provided in case of a wildfire.\n\
- **Municipal Administrative Staff:** The municipality administration can take protective and prohibitive precautions for various areas. Thus, the loss of life and property is minimized.\n\
- **Civil Society Organizations (CSOs):** Civil society organizations can find the opportunity to strengthen their networks in advance to collect aid in possible disaster situations in risky areas.\n\
## Methodology\n\
LightGBM (an advanced decision tree algorithm) was used in the project. The following factors were effective in choosing this algorithm:\n\
- Decision tree algorithms generally give better results than other statistical algorithms for tabular data. They are among the first algorithms to be tried.\n\
- LightGBM is often faster to train than similar decision-tree-based algorithms.\n\
- It has a library that makes it easy to use. Translation and transfer to different programming languages can be done.\n\
- It contains various evaluation and analysis methods. Thus, when the user wants to measure model performance, s/he does not have to write code from scratch or search for it.\
')
    st.markdown("## The Flow of the Project")
    st.markdown(
        "You can navigate within the application with the menu on the left. You can access the variables used in the estimation phase, the technical details of the trained machine learning model, and the monthly wildfire probability prediction page via the menu.")
