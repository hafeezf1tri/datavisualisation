import streamlit as st
import pandas as pd
import altair as alt

# Page setup
st.set_page_config(
    page_title="Begin Lab 2 - Data Visualization",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Begin Lab 2 - Data Visualization")
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
raw_data = {
    'Age': [23, 35, 44, 55, 31, 45, 36, 22, 32, 27, 33, 44],
    'Income': [35000, 88000, 60000, 80000, 37000, 75000, 54000, 29000, 82000, 36000, 61000, 63000],
    'Education': [
        'High School', 'Bachelors', 'Masters', 'PhD', 'High School', 'Masters',
        'Bachelors', 'High School', 'Bachelors', 'High School', 'Bachelors', 'Masters'
    ],
    'Occupation': [
        'Salesman', 'Doctor', 'Artist', 'Scientist', 'Teacher', 'Engineer',
        'Artist', 'Clerk', 'Doctor', 'Teacher', 'Engineer', 'Scientist'
    ]
}

data = pd.DataFrame(raw_data)

st.title("Begin Lab 2 - Data Visualization")

# Page 1
if page == "1. Exploratory Graphics":
    st.title("Exploratory Graphics vs Presentation Graphics")
    st.header("Exploratory Graphics: Interactive Scatter Plot")
    scatter_chart = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('Age:Q', title='Age'),
        y=alt.Y('Income:Q', title='Income'),
        color=alt.Color('Education:N', title='Education'),
        tooltip=['Age', 'Income', 'Education', 'Occupation']
    ).interactive().properties(
        title='Age vs Income by Education Level'
    )

    st.altair_chart(scatter_chart, use_container_width=True)
    st.write(
        "This scatter plot is an example of exploratory graphics, where you can hover over data points to explore details interactively."
    )

# Page 2
elif page == "2. Presentation Graphics":
    st.title("Exploratory Graphics vs Presentation Graphics")
    st.header("Presentation Graphics: Static Bar")
    bar_chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Education:N', title='Education'),
        y=alt.Y('sum(Income):Q', title='Total Income'),
        color=alt.Color('Education:N', legend=None),
    ).properties(
        title='Total Income by Education Level'
    )

    st.altair_chart(bar_chart, use_container_width=True)
    st.write(
        "This static bar chart is an example of presentation graphics, conveying a simple message without interactivity."
    )



# Page 3
elif page == "3. Linked Highlighting":
    st.title("Interactive Linked Highlighting for High-Dimensional Data")
    st.write("Hover over any education level in either chart to highlight the related points in the other chart.")

    highlight = alt.selection(type='single', on='mouseover', fields=['Education'], nearest=True, empty='none')

    scatter_chart_linked = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('Age:Q', title='Age'),
        y=alt.Y('Income:Q', title='Income'),
        color=alt.condition(highlight, alt.Color('Education:N', title='Education'), alt.value('lightgray')),
        tooltip=['Age', 'Income', 'Education', 'Occupation']
    ).add_selection(highlight).properties(
        title='Age vs Income by Education'
    )

    bar_chart_linked = alt.Chart(data).mark_bar().encode(
        x=alt.X('Education:N', title='Education'),
        y=alt.Y('sum(Income):Q', title='Total Income'),
        color=alt.condition(highlight, alt.Color('Education:N', title='Education'), alt.value('lightgray'))
    ).properties(
        title='Total Income by Education Level'
    )

    linked_charts = scatter_chart_linked | bar_chart_linked
    st.altair_chart(linked_charts, use_container_width=True)
    st.write(
        "Here, hovering over any education level in either chart will highlight relevant data points in the other chart, showing relationships between variables interactively."
    )

# Page 4
elif page == "4. Multivariate Context":
    st.header("Finding Appropriate Graphics and Linking Multivariate Context")
    st.write(
        "This bar chart shows how to find the most appropriate graphic (a count bar chart for occupation) while preserving the context of education level as a linked variable."
    )

    occupation_bar = alt.Chart(data).mark_bar().encode(
        x=alt.X('Occupation:N', title='Occupation'),
        y=alt.Y('count():Q', title='Count'),
        color=alt.Color('Education:N', title='Education'),
        tooltip=['Occupation', 'Education', alt.Tooltip('count():Q', title='Count')]
    ).interactive()

    st.altair_chart(occupation_bar, use_container_width=True)
