import lightgbm as lgb
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from app.global_vars import features_w_descs
import copy


def app():
    lgb_model = lgb.Booster(model_file='data/model_ckpt/model.txt')

    features = copy.deepcopy(features_w_descs)

    st.title('Model Details')
    st.markdown(
        "LightGBM, an advanced decision tree algorithm, was used in the project. The machine learning model is trained using the past fire and temperature data and the synthesized data generated from these data.")
    st.markdown("---")
    with st.spinner('Extracting model details...'):
        # Plot Tree
        st.subheader('Structure of the Decision Tree')
        with st.expander("What does it mean?"):
            st.markdown("In the figure, you see the model summarized as a decision tree. The model asks questions from left to right and decides what the next question should be based on the answer it receives. Outputs are in *logit* format, we can say that negative results will turn into positive results and positive ones will turn into positive results when converted to probabilities.")
        st.markdown("\n\nYou may need to zoom the figure by clicking the logo on top-right of it.")
        fig, ax = plt.subplots(figsize=(24, 18))
        lgb.plot_tree(lgb_model, ax=ax)

        st.pyplot(fig,
                  clear_figure=True,
                  bbox_inches='tight',
                  transparent=True,
                  pad_inches=0
                  )

        st.markdown("---")
        # FeatImp - Usage
        feature_imp = pd.DataFrame(sorted(zip(lgb_model.feature_importance(),
                                              features.values())), columns=['Usage Count',
                                                                            ''])

        fig = plt.figure(figsize=(4, 3))
        pd.Series(lgb_model.feature_importance(), index=features).nlargest(4).plot(kind='barh')

        sns.barplot(x="Usage Count",
                    y="",
                    data=feature_imp.sort_values(by="Usage Count", ascending=False),
                    palette="Reds_d")
        st.subheader('Feature Importance (Based on Usage Count)')
        with st.expander("What does it mean?"):
            st.markdown("Graph of feature importance scores calculated according to how many times questions are asked to features in the data during the prediction process in the model.")

        st.pyplot(fig,
                  clear_figure=True,
                  bbox_inches='tight',
                  transparent=True,
                  pad_inches=0
                  )
        st.markdown("---")
        # FeatImp - Gain
        feature_imp = pd.DataFrame(sorted(zip(lgb_model.feature_importance(importance_type="gain"),
                                              features.values())), columns=['Information Gain Ratio',
                                                                            ''])

        fig = plt.figure(figsize=(4, 3))
        pd.Series(lgb_model.feature_importance(), index=features).nlargest(4).plot(kind='barh')

        sns.barplot(x="Information Gain Ratio",
                    y="",
                    data=feature_imp.sort_values(by="Information Gain Ratio", ascending=False),
                    palette="Reds_d")
        st.subheader('Feature Importance (Based on Information Gain Ratio)')
        with st.expander("What does it mean?"):
            st.markdown("Graph of the feature importance scores calculated according to the effect of the features in the data on the model optimization metric.")

        st.pyplot(fig,
                  clear_figure=True,
                  bbox_inches='tight',
                  transparent=True,
                  pad_inches=0
                  )
