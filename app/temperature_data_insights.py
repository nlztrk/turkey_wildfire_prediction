import streamlit as st
import plotly.express as px
import pandas as pd
from app.global_vars import months
import numpy as np
import pydeck as pdk


def app():
    st.title('Temperature Data Insights')
    with st.spinner('Creating temperature data analysis...'):
        temp_df = pd.read_csv('data/processed_data/temperatures.csv')
        temp_df["month"] = temp_df["month"].astype(int)
        temp_df["year"] = temp_df["year"].astype(int)

        temp_df = temp_df.rename(columns={"temperature_max": "Maximum Temperature",
                                          "temperature_avg": "Average Temperature",
                                          "temperature_min": "Minimum Temperature",
                                          "latitude": "Latitude",
                                          "longitude": "Longitude",
                                          "month": "Month",
                                          "year": "Year"})

        yearly_means = temp_df.groupby(["Longitude", "Latitude", "Year"]).mean() \
            .drop("Month", axis=1).reset_index()
        monthly_means = temp_df.groupby(["Longitude", "Latitude", "Month"]).mean() \
            .drop("Year", axis=1).reset_index()

        temp_cols = ["Maximum Temperature", "Average Temperature", "Minimum Temperature"]

        ############

        st.markdown("---")
        st.markdown("### Yearly temperature means for Turkey")
        st.markdown("The temperature trend seems oscillating bi-yearly.")
        turkey_yearly_means = yearly_means.groupby("Year").mean().reset_index()
        fig = px.line(turkey_yearly_means, x="Year", y=temp_cols,
                      color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_yaxes(title_text="Temperature (°C)")
        fig['data'][0]['name'] = 'Maximum Temperature'
        fig['data'][1]['name'] = 'Average Temperature'
        fig['data'][2]['name'] = 'Minimum Temperature'
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Monthly temperature means for Turkey")
        st.markdown("The temperature has its peaks in summer. It seems like a typical trend for a year.")
        turkey_monthly_means = monthly_means.groupby("Month").mean().reset_index()
        fig = px.line(turkey_monthly_means, x="Month", y=temp_cols,
                      color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_yaxes(title_text="Temperature (°C)")
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=months
            )
        )
        fig['data'][0]['name'] = 'Maximum Temperature'
        fig['data'][1]['name'] = 'Average Temperature'
        fig['data'][2]['name'] = 'Minimum Temperature'
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Average temperature distributions by year for Turkey")
        st.markdown("All years have similar distribution patterns for temperature. Turkey seems like didn't have any "
                    "anomaly in terms of temperature through these years.")
        fig = px.box(yearly_means, x="Year", y='Average Temperature')
        fig.update_traces(marker_color='#B95A5A')
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Average temperature distributions by month for Turkey")
        st.markdown("The temperature has its peaks in summer, and outlier temperatures occur most in July.")
        fig = px.box(monthly_means, x="Month", y='Average Temperature')
        fig.update_traces(marker_color='#B95A5A')
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=months
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Temperature distribution for latitude")
        st.markdown("Highest temperatures are seen in the south. Also the most uneven distribution is in the north.")
        fig = px.box(temp_df, x="Latitude", y='Average Temperature')
        fig.update_traces(marker_color='#B95A5A')
        fig.update_yaxes(title_text="Average Temperature (°C)")
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Temperature distribution for longitude")
        st.markdown("As we go to the east, lower bounds are becoming lower and higher bounds are becoming higher. "
                    "We can say that the hottest zone is south-east. We can also validate that with the wildfire map!")
        fig = px.box(temp_df, x="Longitude", y='Average Temperature')
        fig.update_traces(marker_color='#B95A5A')
        fig.update_yaxes(title_text="Average Temperature (°C)")
        st.plotly_chart(fig, use_container_width=True)