import streamlit as st
import pandas as pd
import altair as alt

# Page setup
st.set_page_config(
    page_title="Lab 2 - Altair Visualizations",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Lab 2 - Altair Visualizations")
st.sidebar.markdown("Use the menu below to explore each section.")

page = st.sidebar.selectbox(
    "Choose a section",
    [
        "1. Exploratory Graphics",
        "2. Presentation Graphics",
        "3. Linked Highlighting",
        "4. Multivariate Context"
    ]
)

# Sample dataset
data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [120, 180, 150, 220, 300, 250],
    "Profit": [30, 45, 35, 60, 90, 70],
    "Category": ["A", "B", "A", "B", "A", "B"]
})

st.title("Lab 2 - Altair Visualizations")

# Page 1
if page == "1. Exploratory Graphics":
    st.header("1. Exploratory Graphics")
    st.write("This section shows a basic exploratory bar chart.")

    chart = alt.Chart(data).mark_bar().encode(
        x="Month",
        y="Sales",
        tooltip=["Month", "Sales", "Profit"]
    )

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(data)

# Page 2
elif page == "2. Presentation Graphics":
    st.header("2. Presentation Graphics")
    st.write("This section shows a cleaner chart with title and tooltips.")

    chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("Month", title="Month"),
        y=alt.Y("Sales", title="Total Sales"),
        tooltip=["Month", "Sales", "Profit"]
    ).properties(
        title="Monthly Sales Trend"
    )

    st.altair_chart(chart, use_container_width=True)

# Page 3
elif page == "3. Linked Highlighting":
    st.header("3. Linked Highlighting")
    st.write("Click a category in the legend to highlight the data.")

    selection = alt.selection_point(fields=["Category"], bind="legend")

    chart = alt.Chart(data).mark_circle(size=200).encode(
        x="Sales",
        y="Profit",
        color="Category",
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=["Month", "Sales", "Profit", "Category"]
    ).add_params(
        selection
    )

    st.altair_chart(chart, use_container_width=True)

# Page 4
elif page == "4. Multivariate Context":
    st.header("4. Multivariate Context")
    st.write("This section compares multiple variables together.")

    chart = alt.Chart(data).mark_bar().encode(
        x="Month",
        y="Sales",
        color="Category",
        tooltip=["Month", "Sales", "Profit", "Category"]
    ).properties(
        title="Sales by Month and Category"
    )

    st.altair_chart(chart, use_container_width=True)