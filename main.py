# To Run Program, In Terminal, Type: streamlit run main.py

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt

csv_path = r'./museum_data.csv'

dtype_options = {
    'Latitude': float,
    'Longitude': float,
}

df = pd.read_csv(csv_path, dtype=dtype_options, low_memory=False)

# Drop Unnecessary Columns
unnecessary_columns = ['Museum ID', 'Legal Name', 'Alternate Name', 'Street Address (Administrative Location)', 'City (Administrative Location)', 'State (Administrative Location)', 'Zip Code (Administrative Location)']
df_cleaned = df.drop(columns=unnecessary_columns)

# Drop rows with NaN values in Latitude and Longitude columns
df_cleaned = df_cleaned.dropna(subset=['Latitude', 'Longitude'])

# Task 1: Display DataFrame
st.subheader('Data Table')
st.write(df_cleaned)

# Task 2: Data Summarization and Statistics
total_museums = df_cleaned.shape[0]
average_income_per_type = df_cleaned.groupby('Museum Type')['Income'].mean()

st.subheader('Data Summarization and Statistics')
st.write(f'Total number of museums: {total_museums}')
st.write('Average income per museum type:')
st.write(average_income_per_type)

# Task 3: Data Visualization
st.subheader('Data Visualization')

# Pie chart for distribution of museums by type
st.subheader('Distribution of Museums by Type')
fig, ax = plt.subplots()
df_cleaned['Museum Type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax)
ax.set_ylabel('')  # Remove y-axis label
st.pyplot(fig)

# Visualization for relationship between income and revenue (scatter plot)
st.subheader('Relationship between Income and Revenue')
fig, ax = plt.subplots()
ax.scatter(df_cleaned['Income'], df_cleaned['Revenue'], alpha=0.5)
ax.set_xlabel('Income')
ax.set_ylabel('Revenue')
st.pyplot(fig)

# Map visualization
st.subheader('Map Visualization')
m = folium.Map(location=[df_cleaned['Latitude'].mean(), df_cleaned['Longitude'].mean()], zoom_start=5, height=500)

marker_cluster = MarkerCluster().add_to(m)

for idx, row in df_cleaned.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Museum Name']).add_to(marker_cluster)

# Convert Folium map object to HTML
map_html = m._repr_html_()

# Embed the HTML in the Streamlit app
st.components.v1.html(map_html, width=700, height=500)
