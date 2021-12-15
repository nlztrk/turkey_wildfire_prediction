## Temperature Data

We used [Berkeley Earth Global-Warming Dataset](http://berkeleyearth.org/data/). 
The Berkeley Earth averaging process generates a variety of Output data including a set of gridded temperature fields, regional averages, and bias-corrected station data. Source data consists of the raw temperature reports that form the foundation of our averaging system. Source observations are provided as originally reported and will contain many quality control and redundancy issues. Intermediate data is constructed from the source data by merging redundant records, identifying a variety of quality control problems, and creating monthly averages from daily reports when necessary.

The dataset expresses temperatures as anomalies. It determines the average temperature between the years 70-80 as climatology, and the difference to this average temperature in the current date as anomaly.

#### Variables
Following variables are accessible in these datasets:
- **Latitude:** The angular distance of a place north or south of the earth's equator, or of the equator of a celestial object, expressed in degrees.
- **Longitude:** The angular distance of a place east or west of the Greenwich meridian, or west of the standard meridian of a celestial object, expressed in degrees.
- **Date Number:** The brightness temperature of a fire pixel is measured (in Kelvin) using the MODIS channels 21/22 and channel 31. Brightness temperature is actually a measure of the photons at a particular wavelength received by the spacecraft, but presented in units of temperature.
- **Year:** The year of observation.
- **Month:** The month of observation.
- **Day:** The day of the week of observation.
- **Day of Year:** The day of the year of observation.
- **Land Mask:** Global binary mask for the observation area
- **Temperature:** Sign and magnitude of the anomaly
- **Climatology:** The average temperature for the observed area between 1970-1980.