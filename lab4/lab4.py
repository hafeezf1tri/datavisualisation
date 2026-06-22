import numpy as np
import pandas as pd
def generate_population_data():

    states = [ "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Pulau Pinang", "Perak",
    "Perlis", "Sabah", "Sarawak", "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya" ]

    population_samples = np.random.randint(500000, 5000000, size=(len(states), 5))

    data = pd.DataFrame({
        "State": states,
        "Total": population_samples.sum(axis=1),
        "Average": population_samples.mean(axis=1)
    })

    return data

import geopandas as gpd
import streamlit as st

@st.cache_data

def load_map():
    malaysia_map = gpd.read_file("malaysia_states.json")
    return malaysia_map

import folium

def plot_map(malaysia_map, data):
    m = folium.Map(location=[4.2105, 101.9758], zoom_start=6)
    folium.Choropleth(
    geo_data=malaysia_map,
    name="Average Population Distribution",
    data=data, columns=["State", "Average"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Average Population Distribution",
    ).add_to(m)

    tooltip_map = malaysia_map.merge(
        data[["State", "Total", "Average"]],
        left_on="name",
        right_on="State",
        how="left",
    )
    tooltip_map["TotalTooltip"] = tooltip_map["Total"].apply(
        lambda value: f"{value:,.0f}" if pd.notna(value) else "No data"
    )
    tooltip_map["AverageTooltip"] = tooltip_map["Average"].apply(
        lambda value: f"{value:,.0f}" if pd.notna(value) else "No data"
    )

    folium.GeoJson(
        tooltip_map,
        name="State Details",
        style_function=lambda feature: {
            "fillColor": "transparent",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0,
            "opacity": 0.4,
        },
        highlight_function=lambda feature: {
            "fillColor": "white",
            "fillOpacity": 0.2,
            "color": "black",
            "weight": 2,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["name", "TotalTooltip", "AverageTooltip"],
            aliases=["State:", "Total:", "Average:"],
            localize=True,
            sticky=False,
        ),
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m

from streamlit_folium import folium_static

def main():
    st.title("Malaysia Average Population Distribution Map")
    population_data = generate_population_data()
    st.write("Total and Average Population Data for States:")
    st.dataframe(population_data)
    malaysia_map = load_map()
    folium_map = plot_map(malaysia_map, population_data)
    folium_static(folium_map)

if __name__ == "__main__":
    main()
