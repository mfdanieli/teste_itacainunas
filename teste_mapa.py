import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import folium_static        

st.write("Obs: Perda do solo, % APP e HI variam de 0 a 1 em cada minibacia e vem de um shapefile; IQM = soma dos 3 / 3")

# Slider to allow the user to input a factor
factor1 = st.slider("Selecione fator de multiplicação de perda de solo", 1.0, 10.0, 1.0)
factor2 = st.slider("Selecione fator de multiplicação de % APP", 1.0, 10.0, 1.0)
factor3 = st.slider("Selecione fator de multiplicação do health index", 1.0, 10.0, 1.0)

def mapa(factor1,factor2,factor3):
    
    minibacias = gpd.read_file('minibacias.geojson')
    minibacias_df = minibacias[['FID_catchm','ID','GRIDCODE','perda_solo','Perc_APP','Healt_ index']]

    # cores = ['green','darkcyan','coral','grey','firebrick','deepskyblue']
        
    # Adjust the dataframe directly
    minibacias_df['perda_solo'] *= factor1
    minibacias_df['Perc_APP'] *= factor2
    minibacias_df['Healt_ index'] *= factor3

    # Calculate IQM and update dataframe e o geojson
    minibacias_df['IQM'] = (minibacias_df['perda_solo'] + minibacias_df['Perc_APP'] + minibacias_df['Healt_ index']) / 3
    minibacias['IQM'] = minibacias_df['IQM']
    minibacias_df['IQM'] = minibacias_df['IQM']

    # map
    m = folium.Map(location=[-6, -50], zoom_start=9)
    
    
    c = folium.Choropleth(
        geo_data=minibacias,                     # the GeoJSON data containing the geometry of the regions (polygons) to be visualized on the map
        name="IQM",                       # assigns a name to the layer
        data=minibacias_df,               # data to bind to the GeoJSON
        columns=['FID_catchm','IQM'],     # if the data is dataframe, the columns of data to be bound. Must pass column 1 as the key, and column 2 the values!
        key_on='feature.properties.FID_catchm',  # variable in the geo_data GeoJSON file to bind the data to. Must start with ‘feature’ and be in JavaScript objection notation. Ex: ‘feature.id’ or ‘feature.properties.statename’.
        fill_color="BuPu",
        legend_name='IQM',
        fill_opacity=0.8,
        line_opacity=1,
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        overlay=True,
        nan_fill_color = "black"
    ).add_to(m)

    # Create a GeoJson layer for popups # AGORA POPUS ESTAO SENDO ATUALIZADOS!!!!

    folium.GeoJson(
        minibacias,
        name="IQM",
        style_function=lambda feature: {
            'fillColor': 'white',
            'color': 'black',
            'weight': 0.5,
            # 'dashArray': '5, 5',
            'fillOpacity': 0
        },
        highlight_function=lambda x: {'weight': 3},
        popup=folium.features.GeoJsonPopup(fields=['IQM'], aliases=['IQM']),
        tooltip=folium.features.GeoJsonTooltip(fields=['IQM'], aliases=['IQM'])
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    folium_static(m,width=800,height=800)   
    
    # st.write(minibacias_df['IQM'])
    # st.write(minibacias_updated)

    
mapa(factor1, factor2, factor3)




# popup=folium. Popup(max_width=450). add_child(
# folium. Veralison. load(open ('vis3.]son')), width=450, height=250)) ). add_to (buoy_map)