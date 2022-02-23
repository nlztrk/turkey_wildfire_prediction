import streamlit as st
import plotly.express as px
import pandas as pd
from app.global_vars import months
import numpy as np
import pydeck as pdk


def latitude_wfire_counter(df):
    df["lat_int"] = df["latitude"].astype(int)
    lat_fire_df = df[["lat_int", "confidence"]].groupby(["lat_int"]).count().\
                reset_index().rename(columns={"lat_int": "Latitude", "confidence": "Wildfire Count"})
    lat_fire_df["Latitude"] = lat_fire_df["Latitude"].astype(str) + " - " + (lat_fire_df["Latitude"]+0.99).astype(str)
    return lat_fire_df


def longitude_wfire_counter(df):
    df["long_int"] = df["longitude"].astype(int)
    lon_fire_df = df[["long_int", "confidence"]].groupby(["long_int"]).count().\
                reset_index().rename(columns={"long_int": "Longitude", "confidence": "Wildfire Count"})
    lon_fire_df["Longitude"] = lon_fire_df["Longitude"].astype(str) + " - " + (lon_fire_df["Longitude"]+0.99).astype(str)
    return lon_fire_df


def app():
    st.title('Wildfire Data Insights')
    with st.spinner('Creating wildfire data analysis...'):
        fires = pd.read_csv('data/processed_data/fire_daily.csv.gz', parse_dates=['acq_date'])

        ############

        st.markdown("---")
        st.markdown("### Wildfire detection count of instrument types")
        st.markdown("Most of the data collected with VIIRS.")
        instrument_counts = fires[["instrument", "confidence"]].groupby("instrument")\
            .count().reset_index().rename(columns={"confidence":"count"})
        fig = px.pie(instrument_counts, values='count', names='instrument', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Wildfire detection count of satellite types")
        st.markdown("Most of the data collected by Suomi-NPP.")
        satellite_counts = fires[["satellite", "confidence"]].groupby("satellite")\
            .count().reset_index().rename(columns={"confidence":"count"})
        satellite_counts = satellite_counts.replace("N", "Suomi NPP")
        fig = px.pie(satellite_counts, values='count', names='satellite', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Distribution of wildfire detection confidence")
        st.markdown("Most of the detections have low confidence value. It may be useful if we give more importance to "
                    "the samples with higher confidence when we train our model.")
        fig = px.histogram(fires, x="confidence", nbins=10)
        fig.update_traces(marker_color='#B95A5A')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Total wildfire count by latitude")
        st.markdown("There are more wildfire detections on the south side of the country.")
        lat_fire_df = latitude_wfire_counter(fires)
        fig = px.bar(lat_fire_df, x='Latitude', y='Wildfire Count')
        fig.update_traces(marker_color='#B95A5A')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Total wildfire count by longitude")
        st.markdown("There are more wildfire detections on the east side of the country.")
        long_fire_df = longitude_wfire_counter(fires)
        fig = px.bar(long_fire_df, x='Longitude', y='Wildfire Count')
        fig.update_traces(marker_color='#B95A5A')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("To generate the analyses below, you should specify a temporal mode for them. On what basis do you want to run the analysis?")
        temporal_mode = st.radio(
            "Select your analysis type:",
            ('by Year', 'by Month', 'All time'))


        if temporal_mode == "by Month":
            month_slider = st.select_slider('Month:', value="September", options=months)
            monthnum = np.argwhere(np.array(months) == month_slider)[0][0] + 1
            selected_slider = monthnum
            selected_slider_text = month_slider

        elif temporal_mode == "by Year":
            year_slider = st.slider('Year:', 2013, 2020, value=2013, step=1)
            selected_slider = year_slider
            selected_slider_text = year_slider

        elif temporal_mode == "All time":
            selected_slider_text = "all time"

        temporal_selection = fires["acq_date"].dt.year if temporal_mode == "by Year" else fires["acq_date"].dt.month

        ############

        st.markdown("---")
        st.markdown("### Wildfire detections with high confidence for " + str(selected_slider_text))

        masking_var = (temporal_selection == selected_slider) if not temporal_mode == "All time" else np.array([[True] * len(fires)]).reshape(-1)

        if temporal_mode == "All time":
            st.markdown("The map-plot can't be shown because there is so much data points.")
        else:
            gt_map_df = pd.DataFrame(
                fires[["latitude", "longitude"]][masking_var & fires.confidence>0.95].values,
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
                        data=gt_map_df,
                        get_position='[lon, lat]',
                        get_fill_color=[190, 0, 0],
                        get_line_color=[0, 0, 0],
                        opacity=0.2,
                        get_radius=12000,
                    ),
                ],
            ))

        lat_fire_df = latitude_wfire_counter(fires[masking_var].copy())
        lon_fire_df = longitude_wfire_counter(fires[masking_var].copy())

        ############

        st.markdown("### Wildfire count by latitude for " + str(selected_slider_text))
        fig = px.bar(lat_fire_df, x='Latitude', y='Wildfire Count')
        fig.update_traces(marker_color='#B95A5A')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("### Wildfire count by longitude for " + str(selected_slider_text))
        fig = px.bar(lon_fire_df, x='Longitude', y='Wildfire Count')
        fig.update_traces(marker_color='#B95A5A')
        st.plotly_chart(fig, use_container_width=True)
