# H2O.ai Wildfire & Bushfire Challenge
### Wildfire Forecast for Turkey on a Monthly Basis
#### Team "Too Hot Encoder"

---

## Future Work

### Can-Be-Implemented
Due to time constraints, more effort has been put into *application* part. But the following features can also be considered for further implementations:
- Relative humidity
- Wind speed
- Flora
- Extracting features for time-series analysis on wildfire occurrence. *(eg: autocorrelation, seasonality)*
- Generating features that represent the areal average rather than spot on location-based detections
- Trying different ML models. *(eg. CatBoost, XGBoost, neural networks, ensembles)*

### Any Issues
- Plotly plots make the interface slower when selecting areas with high data amount. *(eg. Brazil)*
- Country shapefiles for plotting the predictions on maps are hardcoded. This can be parametric. For now, the required steps for making predictions for another countries are explained in [README](README.md) file.

## Author
* [Anil Ozturk](anilozturk96@gmail.com)