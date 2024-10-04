import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import calendar
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

sns.set(style='dark')

# Load the data
all_df = pd.read_csv("all_data.csv")

# Define numerical columns
numerical_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Define station coordinates
station_coords = {
    'Aotizhongxin': (116.397, 39.982),
    'Changping': (116.23, 40.217),
    'Dingling': (116.22, 40.292),
    'Dongsi': (116.417, 39.929),
    'Guanyuan': (116.339, 39.929),
    'Gucheng': (116.184, 39.914),
    'Huairou': (116.628, 40.328),
    'Nongzhanguan': (116.461, 39.937),
    'Shunyi': (116.655, 40.127),
    'Tiantan': (116.407, 39.886),
    'Wanliu': (116.287, 39.987),
    'Wanshouxigong': (116.352, 39.878)
}

# Add latitude and longitude to the DataFrame
all_df['latitude'] = all_df['station'].map(lambda x: station_coords[x][1])
all_df['longitude'] = all_df['station'].map(lambda x: station_coords[x][0])

# Calculate correlation between TEMP and O3
def calculate_correlation(group):
    return group['TEMP'].corr(group['O3'])
correlation_by_station = all_df.groupby('station')[['TEMP', 'O3']].apply(calculate_correlation)

# Calculate summary statistics for Dongsi
all_df['date'] = pd.to_datetime(all_df[['year', 'month', 'day']])
all_df['day_week'] = all_df['date'].apply(lambda x: calendar.day_name[x.weekday()])
summary_stats = all_df[all_df['station'] == 'Dongsi'].groupby(by="day_week").agg({
    'PM2.5': ['max', 'min', 'mean', 'std'],
    'PM10': ['max', 'min', 'mean', 'std'],
}).reset_index()
summary_stats.columns = ['_'.join(col).strip() if col[1] else col[0] for col in summary_stats.columns.values]
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
summary_stats['day_week'] = pd.Categorical(summary_stats['day_week'], categories=day_order, ordered=True)
summary_stats = summary_stats.sort_values('day_week')

# Calculate station averages
station_averages = all_df.groupby('station')[numerical_columns].mean().reset_index()
melted_data = pd.melt(station_averages, id_vars='station', value_vars=numerical_columns)

# Streamlit dashboard
st.title("Proyek Analisis Data: Air Quality Dataset")
st.markdown("""
- **Nama:** Salsabila Azzahra
- **Email:** salsabilaazzhr@gmail.com / m001b4kx4036@bangkit.academy
- **ID Dicoding:** salsa-zzhra
""")

st.header("Business Questions")
st.markdown("""
1. What is the correlation between temperature and ozone levels across all stations?
2. How do air quality parameters (PM2.5, PM10) differ between weekdays and weekends in Dongsi?
3. Which station has the highest and lowest air quality parameters (PM2.5, PM10, SO2, NO2, CO, O3) on average?
""")

st.header("Exploratory Data Analysis (EDA)")
st.subheader("Correlation between Temperature and Ozone Levels by Station")
highest_correlation = correlation_by_station.max()
lowest_correlation = correlation_by_station.min()
colors = ['blue' if (val != highest_correlation and val != lowest_correlation) else 'red' if val == highest_correlation else 'green' for val in correlation_by_station]
plt.figure(figsize=(12, 6))
correlation_by_station.plot(kind='bar', color=colors)
plt.title('Correlation between Temperature and Ozone Levels by Station')
plt.xlabel('Station')
plt.ylabel('Correlation')
st.pyplot(plt)

st.subheader("Air Quality Parameters in Dongsi by Day of the Week")
fig, axes = plt.subplots(1, 2, figsize=(20, 10))
fig.suptitle('PM2.5 & PM10 Parameters Over Time: Weekdays vs Weekends in Dongsi', fontsize=16)
for i, param in enumerate(['PM2.5', 'PM10']):
    ax = axes[i]
    ax.plot(summary_stats['day_week'], summary_stats[f'{param}_mean'], color='black', label='Overall')
    weekday_data = summary_stats[summary_stats['day_week'].isin(day_order[:5])]
    ax.scatter(weekday_data['day_week'], weekday_data[f'{param}_mean'], color='blue', label='Weekday')
    weekend_data = summary_stats[summary_stats['day_week'].isin(day_order[5:])]
    ax.scatter(weekend_data['day_week'], weekend_data[f'{param}_mean'], color='red', label='Weekend')
    ax.set_title(param)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Concentration')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(fig)

st.subheader("Heatmap of Average Air Quality Parameters by Station")
plt.figure(figsize=(12, 8))
heatmap = sns.heatmap(station_averages.set_index('station'), annot=True, cmap='coolwarm', fmt=".1f", linewidths=.5, linecolor='black', cbar_kws={'label': 'Average Value'})
heatmap.set_title('Heatmap of Average Air Quality Parameters by Station', fontsize=16)
heatmap.set_ylabel('Station', fontsize=14)
heatmap.set_xlabel('Air Quality Parameter', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

st.subheader("Average Air Quality Parameters by Station")

# Interactive widgets
selected_params = st.multiselect("Select parameters to plot", numerical_columns, default=numerical_columns[:3])

fig, axes = plt.subplots((len(selected_params) + 1) // 2, 2, figsize=(15, 5 * ((len(selected_params) + 1) // 2)))
fig.subplots_adjust(hspace=0.6, wspace=0.3)

axes = axes.flatten()

for i, param in enumerate(selected_params):
    ax = axes[i]
    data = melted_data[melted_data['variable'] == param].sort_values('value')
    sns.barplot(x='value', y='station', data=data, ax=ax, hue='station', palette='viridis', dodge=False, legend=False)
    highest, lowest = data.iloc[-1], data.iloc[0]
    ax.set_title(f'Average {param} by Station')

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
st.pyplot(fig)

# Add Folium map
st.subheader("Air Quality Index Heatmap")

# Interactive widgets for map
selected_year = st.selectbox("Select year", list(range(2013, 2018)))
selected_param = st.selectbox("Select parameter to show on map", numerical_columns)

# Filter data based on selected year and parameter
filtered_data = all_df[(all_df['year'] == selected_year)][['station', 'latitude', 'longitude', selected_param]]

# Create Folium map
map_center = [39.9042, 116.4074]
m = folium.Map(location=map_center, zoom_start=11, tiles='CartoDB positron')

# Prepare data for heatmap
heat_data = [[row['latitude'], row['longitude'], row[selected_param]] for _, row in filtered_data.iterrows()]

# Add heatmap to the map
HeatMap(heat_data, radius=15, blur=10, max_zoom=1, gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}).add_to(m)

# Add markers with station names
for station, coords in station_coords.items():
    folium.Marker(
        location=[coords[1], coords[0]],
        popup=station,
        tooltip=station
    ).add_to(m)

# Display the map
st_folium(m, width=700, height=500)

st.header("Conclusions")
st.markdown("""
- All stations consistently show a positive correlation between temperature and ozone levels.
- The PM2.5 and PM10 levels are higher on weekdays than on weekends in Dongsi.
- The highest and lowest average air quality parameters vary by station.
""")