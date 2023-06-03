import streamlit as st
import pandas as pd
import numpy as np

st.title('Mass Shootings in the US')

# Coordinates of shootings in the US
# Reference: https://docs.streamlit.io/library/api-reference/charts/st.map

sheet_url = "https://docs.google.com/spreadsheets/d/1b9o6uDO18sLxBqPwl_Gh9bnhW-ev_dABH83M5Vb5L8o/edit#gid=0"

# Modify the URL to export the sheet as CSV format
url_modified = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

# Read data
df_mj = pd.read_csv(url_modified)

# Select coordinate columns 
df_coordinates = df_mj[['latitude', 'longitude']]

# Remove rows containing '-' in any column
df_coordinates = df_coordinates[(df_coordinates != '-').all(axis=1)]

# Convert the selected columns to numeric data type
df_coordinates = df_coordinates.apply(pd.to_numeric)


st.map(df_coordinates)