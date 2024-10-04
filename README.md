# Data Analysis Project: Air Quality Dataset

- **Name:** Salsabila Azzahra
- **Email:** salsabilaazzhr@gmail.com / m001b4kx4036@bangkit.academy
- **Dicoding ID:** salsa-zzhra

## Project Overview

This project analyzes an air quality dataset from various stations in China. The data includes key air quality parameters like PM2.5, PM10, SO2, NO2, CO, O3, along with meteorological data like temperature, pressure, and wind speed.

## Streamlit Dashboard
[https://salsa-az-proyek-belajar-analisis-data-dashboarddashboard-3dikow.streamlit.app/](https://salsa-az-proyek-dashboard-3dikow.streamlit.app/)

### Business Questions:

1. What is the correlation between temperature and ozone levels across all stations?
2. How do air quality parameters (PM2.5, PM10) differ between weekdays and weekends in Dongsi?
3. Which station has the highest and lowest air quality parameters (PM2.5, PM10, SO2, NO2, CO, O3) on average?

---

## Dataset

The dataset contains air quality data from multiple monitoring stations across Beijing, including:

- **Features:**
  - PM2.5, PM10, SO2, NO2, CO, O3 (air quality indicators)
  - TEMP (temperature), PRES (pressure), DEWP (dew point), RAIN, wd (wind direction), WSPM (wind speed)
- **Stations:** Aotizhngxin, Changping, Dingling, Dongsi, Guanyuan, Gucheng, Huairou, Nonzhanguan, Shunyi, Tiantan, Wanliu, Wanshouxigong

---

## Data Wrangling

- **Gathering Data:** The dataset consists of multiple CSV files, each representing a different station.
- **Asessing Data**
- **Cleaning Data:** The data is cleaned by handling missing values, converting data types, and removing duplicates.

---

## Exploratory Data Analysis (EDA)

### Question 1: What is the correlation between temperature and ozone levels across all stations?
### Question 2: How do air quality parameters (PM2.5, PM10) differ between weekdays and weekends in Dongsi?
### Question 3: Which station has the highest and lowest air quality parameters (PM2.5, PM10, SO2, NO2, CO, O3) on average?
---

## Visualizations

- Correlation between temperature and ozone levels by station is represented in bar plots.
- PM2.5 and PM10 levels during weekdays and weekends in Dongsi are compared using line plots and scatter plots.
- Heatmaps and bar plots highlight stations with the highest and lowest air quality parameters.

---

## Conclusion

- All stations consistently show a positive correlation between temperature and ozone levels.
- The PM2.5 and PM10 levels are higher on weekdays than on weekends in Dongsi.
- The highest and lowest average air quality parameters vary by station.

---

## How to Run the Project

1. Clone this repository.
2. Navigate to the project directory.

    `cd proyek-belajar-analisis-data`
    `pipenv install`
    `pipenv shell`

2. Ensure you have the required Python libraries installed by running 

    `pip install -r requirements.txt`.

3. Load the dataset by running the code in the notebook.

## Run steamlit app
1. Navigate to dashboard directory
   
     `cd dashboard`
3. Run streamlit app

     `streamlit run dashboard.py`

---
