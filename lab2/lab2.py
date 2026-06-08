import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# Page setup
st.set_page_config(
    page_title="Lab 2 - SDG Dashboard",
    layout="wide"
)

DATA_DIR = Path(__file__).parent
INDEX_FILE = DATA_DIR / "sdg_index_2000-2022.csv"
REPORT_FILE = DATA_DIR / "sustainable_development_report_2023.csv"

@st.cache_data
def load_sdg_data():
    index_df = pd.read_csv(INDEX_FILE, dtype={"country_code": str})
    report_df = pd.read_csv(REPORT_FILE, dtype={"country_code": str})[
        ["country_code", "region"]
    ]

    merged = pd.merge(index_df, report_df, on="country_code", how="left")
    merged["region"] = merged["region"].fillna("Unknown")

    numeric_cols = [
        "year",
        "sdg_index_score",
        "goal_1_score",
        "goal_2_score",
        "goal_3_score",
        "goal_4_score",
        "goal_5_score",
        "goal_6_score",
        "goal_7_score",
        "goal_8_score",
        "goal_9_score",
        "goal_10_score",
        "goal_11_score",
        "goal_12_score",
        "goal_13_score",
        "goal_14_score",
        "goal_15_score",
        "goal_16_score",
        "goal_17_score",
    ]
    merged[numeric_cols] = merged[numeric_cols].apply(
        pd.to_numeric, errors="coerce"
    )
    return merged.dropna(subset=["year", "sdg_index_score"])

sdg_data = load_sdg_data()
selected_year = 2022
current_year = sdg_data[sdg_data["year"] == selected_year]

st.sidebar.title("SDG Dashboard")
st.sidebar.markdown("Use the menu to explore each part of the assignment.")
page = st.sidebar.selectbox(
    "Choose a section",
    [
        "1. Exploratory Graphics",
        "2. Presentation Graphics",
        "3. Linked Highlighting",
        "4. SDG Reflection",
    ]
)

st.title("UN SDG Dashboard: 2022 Country and Regional Progress")
st.markdown(
    "This dashboard uses the SDG index dataset to compare country progress, highlight regional patterns, and show how clean energy outcomes have evolved over time."
)

if current_year.empty:
    st.error("No data available for 2022. Please check the CSV files.")
else:
    region_averages = (
        current_year.groupby("region", as_index=False)["sdg_index_score"]
        .mean()
        .sort_values("sdg_index_score", ascending=False)
    )

    if page == "1. Exploratory Graphics":
        st.header("1. Exploratory Graphics")
        st.write(
            "Scatter plot showing the relationship between overall SDG Index Score and SDG 7 (Affordable and Clean Energy) score for 2022."
        )

        scatter = alt.Chart(current_year).mark_circle(size=100).encode(
            x=alt.X("goal_7_score", title="SDG 7 Score (Affordable & Clean Energy)"),
            y=alt.Y("sdg_index_score", title="Overall SDG Index Score"),
            color=alt.Color("region:N", title="Region"),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("sdg_index_score:Q", title="SDG Index Score", format=".1f"),
                alt.Tooltip("goal_7_score:Q", title="SDG 7 Score", format=".1f"),
            ],
        ).properties(
            width=900,
            height=520,
            title="SDG Index Score vs SDG 7 Score (2022)"
        )

        st.altair_chart(scatter, use_container_width=True)
        st.markdown(
            "The scatter plot shows that countries with stronger SDG 7 performance tend to have higher overall SDG Index scores, but the relationship is not perfectly linear. Some countries perform well on clean energy while still lagging on the overall index, showing that progress on one goal can outpace broader development. Regional clustering is visible, with OECD and Europe-based countries generally appearing toward the top-right, while lower-income regions cluster lower in both scores."
        )

    elif page == "2. Presentation Graphics":
        st.header("2. Presentation Graphics")
        st.write(
            "Average SDG Index Score by region for 2022, shown as a static bar chart."
        )

        bar = alt.Chart(region_averages).mark_bar().encode(
            x=alt.X("sdg_index_score:Q", title="Average SDG Index Score"),
            y=alt.Y(
                "region:N",
                sort=alt.EncodingSortField(
                    field="sdg_index_score", order="descending",
                ),
                title="Region",
            ),
            tooltip=[
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("sdg_index_score:Q", title="Average Score", format=".1f"),
            ],
            color=alt.value("#4c78a8"),
        ).properties(
            width=900,
            height=520,
            title="Average SDG Index Score by Region (2022)"
        )

        st.altair_chart(bar, use_container_width=True)
        st.markdown(
            "The bar chart makes it clear that OECD and Europe lead in average SDG Index scores for 2022. Regions such as Sub-Saharan Africa and South Asia are lower-ranked, highlighting uneven global progress. This static visualization clearly communicates which regions are performing best and where policymakers should focus attention."
        )

    elif page == "3. Linked Highlighting":
        st.header("3. Linked Highlighting")
        st.write(
            "Hover over a region in the bar chart to highlight the corresponding countries in the scatter plot."
        )

        hover = alt.selection_single(
            fields=["region"],
            on="mouseover",
            empty="none",
            clear="mouseout",
        )

        bar_link = alt.Chart(region_averages).mark_bar().encode(
            x=alt.X("sdg_index_score:Q", title="Average SDG Index Score"),
            y=alt.Y(
                "region:N",
                sort=alt.EncodingSortField(
                    field="sdg_index_score", order="descending",
                ),
                title="Region",
            ),
            color=alt.Color("region:N", legend=None),
            opacity=alt.condition(hover, alt.value(1), alt.value(0.6)),
            tooltip=[
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("sdg_index_score:Q", title="Average Score", format=".1f"),
            ],
        ).add_selection(hover).properties(
            width=400,
            height=520,
            title="Average SDG Index by Region"
        )

        scatter_link = alt.Chart(current_year).mark_circle(size=100).encode(
            x=alt.X("goal_7_score", title="SDG 7 Score"),
            y=alt.Y("sdg_index_score", title="SDG Index Score"),
            color=alt.Color("region:N", title="Region"),
            opacity=alt.condition(hover, alt.value(1), alt.value(0.12)),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("sdg_index_score:Q", title="SDG Index Score", format=".1f"),
                alt.Tooltip("goal_7_score:Q", title="SDG 7 Score", format=".1f"),
            ],
        ).properties(
            width=700,
            height=520,
            title="Country SDG 7 vs Overall SDG Index (highlighted by region)"
        )

        st.altair_chart(alt.hconcat(bar_link, scatter_link), use_container_width=True)
        st.markdown(
            "Linking the bar chart and scatter plot reveals how region-level averages map to individual country outcomes. The bar chart alone shows which regions score highest, while the scatter plot alone reveals country variation. Hovering a region highlights the countries that contribute to that region’s average, making it easier to see whether regional performance is broad-based or driven by a few outliers."
        )

    elif page == "4. SDG Reflection":
        st.header("4. SDG Reflection")
        st.write(
            "Regional progress on SDG 7 (Affordable and Clean Energy) from 2000 to 2022."
        )

        trend = (
            sdg_data.groupby(["year", "region"], as_index=False)["goal_7_score"]
            .mean()
            .query("region != 'Unknown'")
        )

        line = alt.Chart(trend).mark_line(point=True).encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("goal_7_score:Q", title="Average SDG 7 Score"),
            color=alt.Color("region:N", title="Region"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("goal_7_score:Q", title="Average SDG 7 Score", format=".1f"),
            ],
        ).properties(
            width=1000,
            height=520,
            title="Regional Progress on SDG 7: Affordable and Clean Energy (2000–2022)"
        )

        st.altair_chart(line, use_container_width=True)
        st.markdown(
            "Progress on SDG 7 is essential for sustainable development because affordable, clean energy supports health, education, and economic opportunity. The chart shows that wealthier regions started at higher SDG 7 levels and have maintained stronger performance, while developing regions have improved more slowly. This pattern reflects real-world energy access gaps, where countries with larger investments in clean infrastructure are better able to reach higher scores. Improving SDG 7 in lagging regions is critical for reducing poverty, powering schools and clinics, and limiting greenhouse gas emissions. The timeline underscores that long-term investment and global cooperation are needed to close the clean energy divide and ensure that sustainable energy advances benefit communities everywhere."
        )
