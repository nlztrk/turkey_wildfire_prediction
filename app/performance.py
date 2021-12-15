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
from app.global_vars import features_w_descs


def app():
    test = pd.read_csv("data/train_val_test_data/test.csv")
    lgb_model = lgb.Booster(model_file='data/model_ckpt/model.txt')

    # Downloaded from https://gadm.org/download_country.html
    fname = 'data/country_shape/gadm36_TUR_0.shp'
    adm1_shapes = list(shpreader.Reader(fname).geometries())

    features = features_w_descs.keys()

    st.title('Evaluation on Test Data')
    st.markdown(
        "")

    months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December',
              'All Year']

    selected_month = st.select_slider(
        'Prediction period:',
        value="September",
        options=months)

    decision_threshold = st.slider('Decision threshold:', 0., 1., value=0.1, step=0.05)

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
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Precision", value=np.round(precision_score(gt_values, test_binary_predictions), 3))
            with col2:
                st.metric(label="Recall", value=np.round(recall_score(gt_values, test_binary_predictions), 3))
            with col3:
                st.metric(label="F1-Score", value=np.round(f1_score(gt_values, test_binary_predictions), 3))

            ############
            st.subheader('Confusion Matrix')
            fig, ax = plt.subplots()
            cm = confusion_matrix(gt_values, test_binary_predictions)
            sns.heatmap(cm, annot=True, ax=ax, cmap=cmap)
            st.pyplot(fig,
                      clear_figure=True,
                      bbox_inches='tight',
                      transparent=True,
                      pad_inches=0
                      )

            ############

            st.subheader('ROC-AUC Curve')
            fpr, tpr, thr = metrics.roc_curve(gt_values, test_predictions)
            fig = px.line(
                pd.DataFrame({"False Positive Ratio": fpr, "True Positive Ratio": tpr}),
                x='False Positive Ratio',
                y='True Positive Ratio',
                color_discrete_sequence=["red"])
            st.plotly_chart(fig, use_container_width=True)

            ############

            inverse_multipoly = [Polygon([(-50, -50), (-50, 50), (50, 50), (50, -50)],
                                         holes=[list(poly.exterior.coords)[::-1] for poly in adm1_shapes[0]]
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

            st.subheader('Predictions + Ground Truths for ' + selected_month)
            st.markdown(
                "You are seeing a heatmap for the probabilities of wildfire occurences in Turkey, for " + selected_month + " 2020. You can change the target year with editing the split definitions in data generation notebooks in the repository.")

            st.pyplot(fig,
                      clear_figure=True,
                      bbox_inches='tight',
                      transparent=True,
                      pad_inches=0
                      )

            ############

            st.subheader('Detailed Prediction Scatterplot')
            df = pd.DataFrame(
                plot_data[["latitude", "longitude"]][plot_data.pred_value >= decision_threshold].values,
                columns=['lat', 'lon'])
            st.map(df)

            ############

            st.subheader('Detailed Ground Truth Scatterplot')
            df = pd.DataFrame(
                plot_data[["latitude", "longitude"]][plot_data.fire == 1].values,
                columns=['lat', 'lon'])
            st.map(df)
