# H2O.ai Wildfire & Bushfire Challenge
### Wildire Forecast for Turkey on a Monthly Basis
#### Team "Too Hot Encoder"

## Getting Started

### Dependencies
Latest version of your favourite conda package manager (>= 4.6) needs to be installed. Please refer to [conda docs](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) for conda installation.

### Setup
To be able to work in the project without any issues, create and activate your virtual working environment with the following commands:
```bash
conda env create -f environment.yml
conda activate wildfire
```
**Warning:** The next steps are explained assuming your virtual environment is active.
### Running the Application
By running the command below, you can run the application where you can access detailed information about the project, generate predictions on test data, view model details, and evaluate model performance:
```bash
streamlit run server.py
```
When the command is run, the application will automatically open a new tab in your default browser.

### Custom Data Generation and Model Training (Optional)
The repository comes with a pre-trained model and a pre-generated test set. But if you want to make your own changes, start a jupyter server with the following command:
```
jupyter notebook
```
A new tab for the jupyter server will open in your default browser, go to the `notebook` folder. You can run all the necessary phases for the project by running the notebooks in their numbered order.

**Warning:** To run the data generation notebooks (numbered 1 and 2) you need to download raw data!

### Downloading Raw Data (Optional)
The project repository includes different datasets. You should download them before training a model. Before downloading, you should configure your AWS-Client, by [AWS-Client Document](docs/aws_guide.md) (only Installation section).

You will need raw data to generate new training data.
- You can download the global fire data pre-uploaded by H2O from [here](https://s3.us-west-1.amazonaws.com/ai.h2o.challenge.datasets/wildfire-challenge/firms_fires_2013_2021.zip)
- You can download the temperature fire data from these links:
  - [Average Temperature (2010-2019)](http://berkeleyearth.lbl.gov/auto/Global/Gridded/Complete_TAVG_Daily_LatLong1_2010.nc)
  - [Average Temperature (2020-)](http://berkeleyearth.lbl.gov/auto/Global/Gridded/Complete_TAVG_Daily_LatLong1_2020.nc)
  - [Maximum Temperature (2010-2019)](http://berkeleyearth.lbl.gov/auto/Global/Gridded/Complete_TMAX_Daily_LatLong1_2010.nc)
  - [Maximum Temperature (2020-)](http://berkeleyearth.lbl.gov/auto/Global/Gridded/Complete_TMAX_Daily_LatLong1_2020.nc)
  - [Minimum Temperature (2010-2019)](http://berkeleyearth.lbl.gov/auto/Global/Gridded/Complete_TMIN_Daily_LatLong1_2010.nc)
  - [Minimum Temperature (2020-)](http://berkeleyearth.lbl.gov/auto/Global/Gridded/Complete_TMIN_Daily_LatLong1_2020.nc)

After the necessary data is downloaded, it should be extracted to the `data/raw_data/` directory. After extraction, the contents of the `data/raw_data/` folder should be as follows:
```
- DL_FIRE_J1V-C2_216004/
- DL_FIRE_M-C61_216003/
- DL_FIRE_M-C61_216006/
...
- Complete_TAVG_Daily_LatLong1_2010.nc
- Complete_TAVG_Daily_LatLong1_2010.nc
- Complete_TMAX_Daily_LatLong1_2020.nc
...
```

### Adding Dependencies (Optional)
If you want to add a dependency, add it to `req.in` and then regenerate the `req.txt` using
```
pip-compile req.in
```
and install the regenerated dependencies using
```
pip install -r req.txt
```

## Author
* [Anil Ozturk](anilozturk96@gmail.com)