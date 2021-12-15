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
    st.markdown("LightGBM, an advanced decision tree algorithm, was used in the project. The machine learning model is trained using the past fire and temperature data and the synthesized data generated from these data.")

    with st.spinner('Extracting model details...'):
        ### Plot Tree
        st.subheader('Structure of the Decision Tree')
        st.markdown("You may need to zoom the figure by clicking the logo on top-right of it.")
        fig, ax = plt.subplots(figsize=(24, 18))
        lgb.plot_tree(lgb_model, ax=ax)

        st.pyplot(fig,
                  clear_figure=True,
                  bbox_inches='tight',
                  transparent=True,
                  pad_inches=0
                  )

        ### FeatImp - Usage

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
        st.pyplot(fig,
                  clear_figure=True,
                  bbox_inches='tight',
                  transparent=True,
                  pad_inches=0
                  )

        ### FeatImp - Gain

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

        st.pyplot(fig,
                  clear_figure=True,
                  bbox_inches='tight',
                  transparent=True,
                  pad_inches=0
                  )
