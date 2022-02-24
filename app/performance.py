import streamlit as st
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import lightgbm as lgb
import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib
from shapely.geometry import Polygon
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
import plotly.express as px
from app.global_vars import features_w_descs, months
import pydeck as pdk


def app():
    test = pd.read_csv("data/train_val_test_data/test.csv")
    lgb_model = lgb.Booster(model_file='data/model_ckpt/model.txt')

    # Downloaded from https://gadm.org/download_country.html
    fname = 'data/country_shape/gadm36_TUR_0.shp'
    adm1_shapes = list(shpreader.Reader(fname).geometries())

    features = features_w_descs.keys()

    st.title('Evaluation on Test Data')
    st.markdown(
        "The model will make predictions for 2020. Please select a month and confidence threshold with the slider below to execute the evaluation.")
    with st.expander("What is confidence threshold?"):
        st.markdown(
            'At which confidence level your model will mark a region as a *"potential wildfire area"*?'
            '\n\n$[0., 1.]$ will be mapped to $[0\%-100\%]$')

    selected_month = st.select_slider(
        'Prediction period:',
        value="September",
        options=months)

    decision_threshold = st.slider('Confidence threshold:', 0., 1., value=0.1, step=0.05)

    if selected_month == "All Year":
        monthnum = 13
    else:
        monthnum = np.argwhere(np.array(months) == selected_month)[0][0] + 1

    if st.button("Evaluate"):
        st.markdown("---")
        with st.spinner('Making prediction for ' + selected_month + ' - 2020 ...'):

            cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", "red"])

            if monthnum < 13:
                test = test[test["month"] == monthnum]

            plot_data = test[["latitude", "longitude", "fire"]].copy().reset_index(drop=True)
            gt_values = test.fire
            test = test[features]
            test_predictions = lgb_model.predict(test)

            test_binary_predictions = (test_predictions >= decision_threshold).astype(float)
            plot_data["pred_value"] = test_binary_predictions

            unq_lats = sorted(plot_data["latitude"].unique())
            unq_lons = sorted(plot_data["longitude"].unique())

            if monthnum == 13:
                plot_data = plot_data.groupby(["latitude", "longitude"])["fire", "pred_value"].max().reset_index()

            ############
            st.subheader('Metrics')
            with st.expander("What these metrics mean?"):
                st.markdown("**Precision:** The ratio of positive identifications was being actually correct. A model that produces no false positives has a precision of $1.0$.")
                st.markdown(
                    "**Recall:** The proportion of actual positives was being identified correctly. A model that produces no false negatives has a recall of $1.0$.")
                st.markdown(
                    "**F1-Score:** The harmonic mean of the precision and recall.")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Precision", value=np.round(precision_score(gt_values, test_binary_predictions), 3))
            with col2:
                st.metric(label="Recall", value=np.round(recall_score(gt_values, test_binary_predictions), 3))
            with col3:
                st.metric(label="F1-Score", value=np.round(f1_score(gt_values, test_binary_predictions), 3))
            st.markdown("---")
            ############
            st.subheader('Confusion Matrix')
            with st.expander("What is confusion matrix?"):
                st.markdown('It is a specific table layout that allows visualization of the performance of an algorithm, typically a supervised learning model. Each row of the matrix represents the instances in an actual class while each column represents the instances in a predicted class. The name stems from the fact that it makes it easy to see whether the system is confusing two classes (i.e. commonly mislabeling one as another).It is a special kind of contingency table, with two dimensions ("actual" and "predicted"), and identical sets of "classes" in both dimensions (each combination of dimension and class is a variable in the contingency table). [(source)](https://en.wikipedia.org/wiki/Confusion_matrix)')

            fig, ax = plt.subplots()
            cm = confusion_matrix(gt_values, test_binary_predictions)
            confmat_plot = sns.heatmap(cm, annot=True, ax=ax, cmap=cmap)
            confmat_plot.set_xlabel('Prediction', fontweight="bold")
            confmat_plot.set_ylabel('Truth', fontweight="bold")
            confmat_plot.set_xticklabels(['There is not a wildfire', 'There is a wildfire'])
            confmat_plot.set_yticklabels(['There is not a wildfire', 'There is a wildfire'])
            st.pyplot(fig,
                      clear_figure=True,
                      bbox_inches='tight',
                      transparent=True,
                      pad_inches=0
                      )
            st.markdown("---")
            ############

            st.subheader('ROC-AUC Curve')
            with st.expander("What is ROC-AUC?"):
                st.markdown('A receiver operating characteristic curve, or ROC curve, is a graphical plot that illustrates the diagnostic ability of a binary classifier system as its discrimination threshold is varied. The ROC curve is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. To summarize: If used correctly, ROC curves are a very powerful tool as a statistical performance measure in detection/classification theory and hypothesis testing, since they allow having all relevant quantities in one plot. [(source)](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)')

            fpr, tpr, thr = metrics.roc_curve(gt_values, test_predictions)
            fig = px.line(
                pd.DataFrame({"False Positive Ratio": fpr, "True Positive Ratio": tpr}),
                x='False Positive Ratio',
                y='True Positive Ratio',
                color_discrete_sequence=["red"])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")
            ############

            st.subheader('Precision-Recall Curve')
            with st.expander("What is Precision-Recall Curve?"):
                st.markdown(
                    'A PR curve is simply a graph with Precision values on the y-axis and Recall values on the x-axis. In other words, the PR curve contains TP/(TP+FN) on the y-axis and TP/(TP+FP) on the x-axis. It is important to note that Precision is also called the Positive Predictive Value (PPV). [(source)](https://www.geeksforgeeks.org/precision-recall-curve-ml/#:~:text=A%20PR%20curve%20is%20simply,Positive%20Predictive%20Value%20(PPV).)'
                )
            fpr, tpr, thr = metrics.precision_recall_curve(gt_values, test_predictions)
            fig = px.line(
                pd.DataFrame({"Recall": fpr, "Precision": tpr}),
                x='Recall',
                y='Precision',
                color_discrete_sequence=["red"])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")
            ############

            inverse_multipoly = [Polygon([(-50, -50), (-50, 50), (50, 50), (50, -50)],
                                         holes=[list(poly.exterior.coords) for poly in adm1_shapes[0]]
                                         )]

            ####

            fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

            X, Y = np.meshgrid(unq_lons, unq_lats)

            Z_gt = plot_data["fire"].values.reshape(X.shape)
            Z = plot_data["pred_value"].values.reshape(X.shape)
            Z *= 10
            Z = gaussian_filter(Z, sigma=5)
            Z[Z >= 1] = 1

            ax.contourf(X, Y, Z, 100,
                        transform=ccrs.PlateCarree(),
                        cmap=cmap,
                        alpha=1,
                        vmin=0, vmax=1,
                        extend="min"
                        )

            ax.contourf(X, Y, Z_gt, 100,
                        transform=ccrs.PlateCarree(),
                        cmap="Reds",
                        alpha=0.5,
                        vmin=0, vmax=1,
                        extend="min"
                        )

            ax.add_geometries(adm1_shapes,
                              ccrs.PlateCarree(),
                              facecolor='black',
                              alpha=0.2)
            ax.add_geometries(inverse_multipoly,
                              ccrs.PlateCarree(),
                              facecolor='white',
                              alpha=1)

            ax.set_extent([26, 45, 36, 42], ccrs.PlateCarree())
            ax.axis("off")

            st.subheader('Predictions + Ground Truths for ' + selected_month + " 2020")
            st.markdown(
                "You are seeing: \n\n - A heatmap for the probabilities of wildfire occurences in faint red"
                "\n- Ground truth (actual) wildfire occurences in dark red"
                "\n\nThe predictions and ground-truths are for " + selected_month + " 2020.")

            st.pyplot(fig,
                      clear_figure=True,
                      bbox_inches='tight',
                      transparent=True,
                      pad_inches=0
                      )
            st.markdown("---")
            ############

            st.subheader('Detailed Prediction Scatterplot')
            st.markdown("On the map, areas that are said by the model to have a potential for having wildfire are shown in black, and places that have actually have wildfire are shown in red.")
            pred_map_df = pd.DataFrame(
                plot_data[["latitude", "longitude"]][plot_data.pred_value >= decision_threshold].values,
                columns=['lat', 'lon'])
            gt_map_df = pd.DataFrame(
                plot_data[["latitude", "longitude"]][plot_data.fire == 1].values,
                columns=['lat', 'lon'])

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=38.76,
                    longitude=34.4,
                    zoom=4.5,
                    pitch=0
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=pred_map_df,
                        get_position='[lon, lat]',
                        get_fill_color=[0, 0, 0],
                        get_line_color=[0, 0, 0],
                        opacity=0.2,
                        get_radius=12000,
                    ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=gt_map_df,
                        get_position='[lon, lat]',
                        get_fill_color=[255, 0, 0],
                        get_line_color=[0, 0, 0],
                        opacity=0.2,
                        get_radius=12000,
                    ),
                ],
            ))
