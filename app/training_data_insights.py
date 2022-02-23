import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px



def app():
    st.title('Training Data Insights')
    with st.spinner('Creating training data analysis...'):
        full_df = pd.read_csv('./data/train_val_test_data/full_data.csv')
        features = [
            'latitude', 'longitude', 'month',
            'fire_cnt_before', 'fire_before',
            'fire_cnt_last_year', 'fire_last_year',
            'fire_cnt_last_year_same_month', 'fire_last_year_same_month',
            'temperature_min', 'temperature_max', 'temperature_avg', 'fire'
        ]
        full_df = full_df[features]

        ############

        st.markdown("---")
        st.markdown("### Feature Correlation Matrix")
        with st.expander("What does correlation mean?"):
            st.markdown("Correlation means association - more precisely it is a measure of the extent to which two variables are related. \n\n**A positive correlation** is a relationship between two variables in which both variables move in the same direction. Therefore, when one variable increases as the other variable increases, or one variable decreases while the other decreases. \n\n**A negative correlation** is a relationship between two variables in which an increase in one variable is associated with a decrease in the other. \n\n**A zero correlation** exists when there is no relationship between two variables.")

        st.markdown("We can see high positive correlation between latitude - latitude rounded and longitude - longitude as expected. Also we see high correlation fire report counts and fire occurence counts which is also normal. We are also see high correlation between temperatures since they are derived from each other. In this heatmap, we can focus more on the negative correlation. We see dark red colors in some places. We can see high correlation between latitude - temperatures, longitude - temperatures, fire report count - latitude and fire occurence count - latitude.")
        feature_corr = full_df.drop("fire",1).corr()
        fig = px.imshow(feature_corr, aspect="auto", color_continuous_scale=px.colors.sequential.RdBu)
        fig.update_layout(
            yaxis=dict(
            tickfont=dict(size=11)),
        xaxis = dict(
            tickfont=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

        ############

        st.markdown("---")
        st.markdown("### Feature-Label Correlation Matrix")
        with st.expander("What does correlation mean?"):
            st.markdown("Correlation means association - more precisely it is a measure of the extent to which two variables are related. \n\n**A positive correlation** is a relationship between two variables in which both variables move in the same direction. Therefore, when one variable increases as the other variable increases, or one variable decreases while the other decreases. \n\n**A negative correlation** is a relationship between two variables in which an increase in one variable is associated with a decrease in the other. \n\n**A zero correlation** exists when there is no relationship between two variables.")

        st.markdown("In this plot we are seeing the correlation between the features used in training and the prediction ground-truth. We see the highest correlation at fire occurence count in the past and fire occurence count in the same month last year.")
        feature_label_corr = full_df.corr()[["fire"]].drop(index='fire')
        fig = px.imshow(feature_label_corr, aspect="auto", color_continuous_scale=px.colors.sequential.RdBu)
        for i, r in enumerate(np.round(feature_label_corr.to_numpy(),3)):
            for k, c in enumerate(r):
                fig.add_annotation(x=k, y=i,
                                   text='{}'.format(c),
                                   showarrow=False,
                                   font=dict(size=17)
                                   )

        fig.update_layout(
            yaxis=dict(
            tickfont=dict(size=15)),
        xaxis = dict(
            tickfont=dict(size=20)))

        fig.update_xaxes(side="top")
        st.plotly_chart(fig, use_container_width=True)
