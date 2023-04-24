import pandas as pd
import geopandas as gpd
import requests
import streamlit as st
import keplergl as kgl
from streamlit_keplergl import keplergl_static

country_gdf = gpd.read_file('temp_country_geom.geojson')  


def country_map(country_name, admin_unit):
    map_1 = kgl.KeplerGl(height=600)
 
    # Counter map.
    if admin_unit == 0: 
        country_data = country_gdf.loc[country_gdf['country_name_eng']== country_name]
        map_1.add_data(data= country_data, name='Country')
    

    # Administrative unit map.
    elif admin_unit == 1 or admin_unit == 2:
        code_a3 = country_gdf['code_a3'].loc[country_gdf['country_name_eng']== country_name]
        admin_unit_data = get_json(0, code_a3.values[0], admin_unit)
        map_1.add_data(data= admin_unit_data, name='Admin unit')

    # Capital point map.
    elif admin_unit == 3:
        json_url = 'http://api.worldbank.org/v2/country/'
        json_name = '?format=json'
        iso_a2 = country_gdf['iso_a2'].loc[country_gdf['country_name_eng']== country_name]
        json_file = requests.get(json_url + iso_a2.values[0] + json_name).json()

        city_df = pd.DataFrame(
        {'City': [json_file[1][0]['capitalCity']],
        'Latitude': [json_file[1][0]['latitude']],
        'Longitude': [json_file[1][0]['longitude']]})
        
        city_gdf = gpd.GeoDataFrame(city_df, geometry=gpd.points_from_xy(city_df.Longitude, city_df.Latitude))
        map_1.add_data(data= city_gdf, name='Capital')

    return keplergl_static(map_1, center_map=True)



option = st.selectbox(
    'Select a country',
    list(country_gdf['country_name_eng'][country_gdf['geometry'].isna()== False]))

st.write('You selected:', option)
country_map(option, 0)
