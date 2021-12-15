# H2O.ai Wildfire & Bushfire Challenge
### Wildfire Forecast for Turkey on a Monthly Basis
#### Team "Too Hot Encoder"

---

## Non-Technical Report
### Challenge Description
Wildfires (a.k.a. bushfires) are a serious problem that threaten lives, communities, wildlife, and forests every year, with global climate change, it is getting worse. They are a global issue and are considered one of the most dangerous disasters we face. While humans cause many fires, other factors, including wind, lightning, drought, and landscape, impact where fires occur and how they spread.

Wildfires present unique and severe forecasting challenges. Compared to storms, such as hurricanes, wildfires are ambiguous and hard to predict, especially when you start looking at large, intense wildfires. Those fires combine complex weather, different landscapes, fuel sources such as housing materials or dry forests, and more.

The H2O.ai Fights Fire Challenge aims to provide first responders, local leaders, businesses, and the public with new AI applications that can be used to help save lives and property. We expect the participants and teams to build for one of these audiences, but we want to make sure you have the creative freedom to decide which one to design for, as that will lead to a greater breadth of new applications being built.

### Motivation
![](app/media/wildfire.jpg)

The aim of the project is to predict the probability of wildfire occurrence in Turkey for each month in 2020. As a result of these predictions, it is aimed to carry out more intensive monitoring studies in possible fire areas and to respond to fires very soon after they start. It is also aimed to derive generalizable relations by interpreting the model outputs and the importance attributed to each variable used by the model.\n\nThe model trained with the data between 2013-2018, validated with the data from 2019. The results you will see are extracted from 2020, which is the test split for this project. The model didn't see any data from this split during the training.

![](app/media/wildfire_bodrum.png)

[The wildfires at Turkey](https://en.wikipedia.org/wiki/2021_Turkey_wildfires) started in August 2021, spread over very large areas and resulted in the destruction of large areas and living things due to lack of intervention, have created a big agenda throughout the country. The public and politicians often complained about this technical inadequacy and suggested that improvements should be made in this regard. Within the scope of the project, it was desired to see whether an estimation could be made on this subject throughout the country, and if so, how successful the results would be.

### The Goal
The goal of the project is to estimate the probability of a wildfire occurrence for each month of 2020 for each grid segment by dividing the area of Turkey in latitude and longitude with 1 degree precision.
It is defined in the H2O Competition Overview as *"Predicting the behavior of wildfires"*.

### Potential Audience
Since the probability of wildfire occurence in certain areas in the future is being calculated, the following groups and individuals can benefit from this project:
- **Firefighters:** Fire departments can keep firefighter density higher in risky areas, this way faster response can be provided in case of a wildfire.
- **Municipal Administrative Staff:** The municipality administration can take protective and prohibitive precautions for various areas. Thus, the loss of life and property is minimized.
- **Civil Society Organizations (CSOs):** Civil society organizations can find the opportunity to strengthen their networks in advance to collect aid in possible disaster situations in risky areas.
### Methodology
LightGBM (an advanced decision tree algorithm) was used in the project. The following factors were effective in choosing this algorithm:
- Decision tree algorithms generally give better results than other statistical algorithms for tabular data. They are among the first algorithms to be tried.
- LightGBM is often faster to train than similar decision-tree-based algorithms.
- It has a library that makes it easy to use. Translation and transfer to different programming languages can be done.
- It contains various evaluation and analysis methods. Thus, when the user wants to measure model performance, s/he does not have to write code from scratch or search for it.
- It was used in the example application 🤷‍♂️

The machine learning model is trained using the past fire and temperature data and the synthesized data generated from these data.

- You can access the details of wildfire dataset from [here](app/markdown/data_active_fire.md).
- You can access the details of temperature dataset from [here](app/markdown/data_temperatures.md).
- You can access the list of used and synthetically produced variables from [here](app/markdown/model_variables.md).

## Author
* [Anil Ozturk](anilozturk96@gmail.com)