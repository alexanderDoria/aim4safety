import streamlit as st
import pandas as pd
import numpy as np

st.title('Mass Shootings in the US')

# Coordinates of shootings in the US
# Reference: https://docs.streamlit.io/library/api-reference/charts/st.map

filepath = 'data/violence_project.xlsx'

# Read the excel file into a dataframe
df_data = pd.read_excel(filepath, sheet_name='Full Database')

# Include coordinate columns and drop nulls
df_coordinates = df_data[['Latitude', 'Longitude']].dropna()

# Rename columns to 'lat' and 'lon' 
df_coordinates.columns = ['lat', 'lon']

st.map(df_coordinates)