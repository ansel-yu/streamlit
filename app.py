import pandas as pd
import geopandas as gpd
import requests
import streamlit as st
import keplergl as kgl
from streamlit_keplergl import keplergl_static

country_gdf = gpd.read_file('temp_country_geom.geojson')  


def country_map(country_name, admin_unit):
    map_1 = kgl.KeplerGl()
 
    # Counter map.
    if admin_unit == 0: 
        country_data = country_gdf.loc[country_gdf['country_name_eng']== country_name]
        map_1.add_data(data= country_data, name='Country')
    
    return keplergl_static(map_1, center_map=True, height= 800, width= 1200)



option = st.selectbox(
    'Select a country',
    list(country_gdf['country_name_eng'][country_gdf['geometry'].isna()== False]))

country_map(option, 0)
