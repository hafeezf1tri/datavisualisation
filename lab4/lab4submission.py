import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import folium_static


MAP_STATE_NAMES = {
    "Penang": "Pulau Pinang",
}


def get_states():
    states = [
        "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
        "Pahang", "Penang", "Perak", "Perlis", "Sabah", "Sarawak",
        "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"
    ]

    return states


def generate_population_data():
    states = get_states()

    population_samples = np.random.randint(100000, 1000000, size=(len(states), 5))

    data = pd.DataFrame({
        "State": states,
        "Population": population_samples.sum(axis=1),
        "Average Population": population_samples.mean(axis=1)
    })

    return data


def generate_gdp_data():
    states = get_states()

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


def plot_map(malaysia_map, data, value_column, color_scheme, tooltip_columns=None):
    m = folium.Map(location=[4.2105, 101.9758], zoom_start=6)

    tooltip_columns = tooltip_columns or [value_column]
    map_data = data.copy()
    map_data["MapState"] = map_data["State"].replace(MAP_STATE_NAMES)

    folium.Choropleth(
        geo_data=malaysia_map,
        name=f"{value_column} Distribution",
        data=map_data,
        columns=["MapState", value_column],
        key_on="feature.properties.name",
        fill_color=color_scheme,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{value_column} Distribution",
    ).add_to(m)

    tooltip_map = malaysia_map.merge(
        map_data[["MapState"] + tooltip_columns],
        left_on="name",
        right_on="MapState",
        how="left",
    )
    tooltip_fields = ["name"]
    tooltip_aliases = ["State:"]
    for column in tooltip_columns:
        tooltip_column = f"{column} Tooltip"
        tooltip_map[tooltip_column] = tooltip_map[column].apply(
            lambda value: f"{value:,.0f}" if pd.notna(value) else "No data"
        )
        tooltip_fields.append(tooltip_column)
        tooltip_aliases.append(f"{column}:")

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
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True,
            sticky=False,
        ),
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

    if dataset_choice == "Population":
        data = generate_population_data()
        value_column = "Population"
        tooltip_columns = ["Population", "Average Population"]
    else:
        data = generate_gdp_data()
        value_column = "GDP"
        tooltip_columns = ["GDP"]

    state_options = data["State"].tolist()
    selected_states = st.sidebar.multiselect(
        "Filter by State",
        state_options,
        default=state_options,
    )
    data = data[data["State"].isin(selected_states)]

    if data.empty:
        st.warning("Select at least one state to display the map.")
        return

    st.write(f"Sample {dataset_choice} Data:")
    st.dataframe(data)

    malaysia_map = load_map()
    selected_map_states = data["State"].replace(MAP_STATE_NAMES)
    malaysia_map = malaysia_map[malaysia_map["name"].isin(selected_map_states)].copy()
    folium_map = plot_map(malaysia_map, data, value_column, color_scheme, tooltip_columns)

    folium_static(folium_map)


if __name__ == "__main__":
    main()
