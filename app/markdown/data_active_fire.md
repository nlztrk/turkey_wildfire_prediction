## Active Fire Data

We used [active fire dataset given by H2O](https://github.com/h2oai/challenge-wildfires/blob/main/notebook/data/Data.md). Thanks to NASA's full and open sharing [Data Policy](https://science.nasa.gov/earth-science/earth-science-data/data-information-policy/) we acknowledge the use of data and/or imagery from NASA's FIRMS (https://earthdata.nasa.gov/firms), part of NASA's Earth Observing System Data and Information System (EOSDIS).

### MODIS Collection 6
MODIS Collection 6 Hotspot / Active Fire Detections [MCD14ML](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/mcd14ml) distributed from NASA FIRMS. It has a temporal coverage from 11 Nov 2000 – 30 Nov 2020.

### MODIS Collection 61
MODIS Collection 61 NRT Hotspot / Active Fire Detections [MCD14DL](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/mcd14ml) distributed from NASA FIRMS. It has a temporal coverage from 01 Nov 2020 - present.

### VIIRS 375m NRT (Suomi NPP)
NRT VIIRS 375 m Active Fire product [VNP14IMGT](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/v1-vnp14imgt) distributed from NASA FIRMS. It has a temporal coverage from 1 January 2020 - present.

#### Variables
Following variables are accessible in these datasets:
- **Latitude:** The angular distance of a place north or south of the earth's equator, or of the equator of a celestial object, expressed in degrees.
- **Longitude:** The angular distance of a place east or west of the Greenwich meridian, or west of the standard meridian of a celestial object, expressed in degrees.
- **Brightness:** The brightness temperature of a fire pixel is measured (in Kelvin) using the MODIS channels 21/22 and channel 31. Brightness temperature is actually a measure of the photons at a particular wavelength received by the spacecraft, but presented in units of temperature.
- **Scan & Track:** The scan value represents the spatial-resolution in the East-West direction of the scan and the track value represents the North-South spatial resolution of the scan. It should be noted that the pixel size is not always 1 km across the scan track. The pixels at the “Eastern” and the “Western” edges of the scan are bigger than 1 km. It is 1 km only along the nadir (exact vertical from the satellite). Thus, the values shown for scan and track represent the actual spatial resolution of the scanned pixel.
- **Acquire Date:** The day, month and year of the acquired data.
- **Satellite:** The satellite ID.
- **Instrument:** The indicator of the instrument that makes the measurement. (eg: VIIRS, MODIS etc.)
- **Day&Night:** Whether it was day or night in the area where the data was taken.