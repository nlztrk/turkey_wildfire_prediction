import lightgbm as lgb
import streamlit as st
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib
from shapely.geometry import Polygon
from app.global_vars import features_w_descs, months
import pydeck as pdk


@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def app():
    test = pd.read_csv("data/train_val_test_data/test.csv")
    lgb_model = lgb.Booster(model_file='data/model_ckpt/model.txt')

    # Downloaded from https://gadm.org/download_country.html
    fname = 'data/country_shape/gadm36_TUR_0.shp'
    adm1_shapes = list(shpreader.Reader(fname).geometries())

    features = features_w_descs.keys()

    st.title('Wildfire Risk Map Prediction for Turkey')
    st.markdown(
        "The model will make predictions for 2020. Please select a month and confidence threshold with the slider below to make a prediction.")
    with st.expander("What is confidence threshold?"):
        st.markdown(
            'At which confidence level your model will mark a region as a *"potential wildfire area"*?'
            '\n\n$[0., 1.]$ will be mapped to $[0\%-100\%]$')

    selected_month = st.select_slider(
        'Prediction period:',
        value="September",
        options=months)
    decision_threshold = st.slider('Confidence threshold:', 0., 1., value=0.1, step=0.05)

    monthnum = np.argwhere(np.array(months) == selected_month)[0][0] + 1

    if st.button("Predict"):
        st.markdown("---")
        with st.spinner('Making prediction for ' + selected_month + ' - 2020 ...'):
            test = test[test["month"] == monthnum]
            plot_data = test[["latitude", "longitude", "fire"]].copy().reset_index(drop=True)
            test = test[features]

            test_predictions = lgb_model.predict(test)
            test_binary_predictions = (test_predictions >= decision_threshold).astype(float)
            plot_data["pred_value"] = test_binary_predictions

            inverse_multipoly = [Polygon([(-50, -50), (-50, 50), (50, 50), (50, -50)],
                                         holes=[list(poly.exterior.coords)[::-1] for poly in adm1_shapes[0]]
                                         )]

            unq_lats = sorted(plot_data["latitude"].unique())
            unq_lons = sorted(plot_data["longitude"].unique())

            ####

            fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

            X, Y = np.meshgrid(unq_lons, unq_lats)

            Z = plot_data["pred_value"].copy().values.reshape(X.shape)
            Z *= 10
            Z = gaussian_filter(Z, sigma=5)
            Z[Z >= 1] = 1

            cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", "red"])
            ax.contourf(X, Y, Z, 100,
                        transform=ccrs.PlateCarree(),
                        cmap=cmap,
                        alpha=1,
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

            st.subheader('Predictions for ' + selected_month + " 2020")
            st.markdown(
                "You are seeing a heatmap for the probabilities of wildfire occurences in Turkey, for " + selected_month + " 2020. You can change the target year with editing the split definitions in data generation notebooks in the repository.")
            st.pyplot(fig,
                      clear_figure=False,
                      bbox_inches='tight',
                      transparent=True,
                      pad_inches=0
                      )
            st.markdown("---")

            ############

            st.subheader('Detailed Prediction Scatterplot')
            st.markdown("You can see on the map that the model marks the areas with the potential to have wildfire in black.")
            df = pd.DataFrame(
                plot_data[["latitude", "longitude"]][plot_data.pred_value >= 0.5].values,
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
                        data=df,
                        get_position='[lon, lat]',
                        get_fill_color=[0, 0, 0],
                        get_line_color=[0, 0, 0],
                        opacity=0.35,
                        get_radius=12000,
                    ),
                ],
            ))

            st.markdown("---")

            ############
            # Download Predictions
            st.subheader('Prediction File')
            st.markdown("You can download the predictions in .csv format:")
            downloaded_df = plot_data[["latitude", "longitude", "pred_value"]]
            downloaded_df["month"] = monthnum
            downloaded_df["year"] = 2020
            csv = convert_df(downloaded_df)
            st.download_button(
                "Download Predictions",
                csv,
                "predictions_" + str(monthnum) + "_" + str(2020) + ".csv",
                "text/csv",
                key='download-csv'
            )
