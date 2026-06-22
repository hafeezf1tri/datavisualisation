import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import folium_static


def get_states(include_imaginary=False):
    states = [
        "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
        "Pahang", "Penang", "Perak", "Perlis", "Sabah", "Sarawak",
        "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"
    ]

    if include_imaginary:
        states.append("Aurelion")

    return states


def generate_population_data(include_imaginary=False):
    states = get_states(include_imaginary)

    # Changed range: 1 million to 10 million
    population = np.random.randint(1000000, 10000000, size=len(states))

    data = pd.DataFrame({
        "State": states,
        "Population": population
    })

    return data


def generate_gdp_data(include_imaginary=False):
    states = get_states(include_imaginary)

    # Random GDP values
    gdp = np.random.randint(10000, 100000, size=len(states))

    data = pd.DataFrame({
        "State": states,
        "GDP": gdp
    })

    return data


@st.cache_data
def load_map():
    malaysia_map = gpd.read_file("malaysia_states.json")
    return malaysia_map


def plot_map(malaysia_map, data, value_column, color_scheme):
    m = folium.Map(location=[4.2105, 101.9758], zoom_start=6)

    folium.Choropleth(
        geo_data=malaysia_map,
        name=f"{value_column} Distribution",
        data=data,
        columns=["State", value_column],
        key_on="feature.properties.name",
        fill_color=color_scheme,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{value_column} Distribution",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m


def main():
    st.title("Malaysia State Distribution Map")

    dataset_choice = st.sidebar.selectbox(
        "Choose Dataset",
        ["Population", "GDP"]
    )

    color_scheme = st.sidebar.selectbox(
        "Choose Map Color Scheme",
        ["YlOrRd", "BuGn", "Blues", "Greens"]
    )

    include_imaginary = st.sidebar.checkbox("Add imaginary state")

    if dataset_choice == "Population":
        data = generate_population_data(include_imaginary)
        value_column = "Population"
    else:
        data = generate_gdp_data(include_imaginary)
        value_column = "GDP"

    st.write(f"Sample {dataset_choice} Data:")
    st.dataframe(data)

    malaysia_map = load_map()
    folium_map = plot_map(malaysia_map, data, value_column, color_scheme)

    folium_static(folium_map)


if __name__ == "__main__":
    main()