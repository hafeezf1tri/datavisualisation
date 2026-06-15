import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Lab 3 - Titanic High-Dimensional Visualizations",
    page_icon="🚢",
    layout="wide",
)


@st.cache_data
def load_titanic_data() -> pd.DataFrame:
    """Load and lightly clean the Titanic dataset from Seaborn."""
    df = sns.load_dataset("titanic")

    # Make a safe working copy and create cleaner labels for visualisation.
    df = df.copy()
    df["age"] = df["age"].fillna(df["age"].median())
    df["fare"] = df["fare"].fillna(df["fare"].median())
    df["embark_town"] = df["embark_town"].astype("object").fillna("Unknown")
    df["deck"] = df["deck"].astype("object").fillna("Unknown").astype(str)

    df["passenger_class"] = df["class"].astype(str)
    df["survived_label"] = df["survived"].map({0: "Did not survive", 1: "Survived"})
    df["alone_label"] = df["alone"].map({True: "Alone", False: "With family"})
    df["adult_male_label"] = df["adult_male"].map({True: "Adult male", False: "Not adult male"})
    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["pclass_num"] = df["pclass"].astype(int)

    return df


try:
    df = load_titanic_data()
except Exception as e:
    st.error(
        "Could not load sns.load_dataset('titanic'). "
        "Seaborn may need internet access the first time it downloads the dataset."
    )
    st.exception(e)
    st.stop()

class_order = ["First", "Second", "Third"]

st.title("Lab 3: High-Dimensional Data Visualization with the Titanic Dataset")
st.write(
    "Dataset input: `sns.load_dataset(\"titanic\")`. "
    "This app re-runs the six Lab 3 visualisations using Titanic passenger data, "
    "then adds one extra Seaborn visualisation for the assignment."
)

st.sidebar.title("Navigation")
section = st.sidebar.selectbox(
    "Choose a visualization",
    [
        "Dataset Overview",
        "2.1 Mosaic Plot",
        "2.2 Trellis Display",
        "2.3 Heatmap",
        "2.4 Multivariate Scatter Plot",
        "2.5 Parallel Coordinate Plot",
        "2.6 Grand Tour (3D Scatter)",
        "3. New Visualization - Seaborn Violin Plot",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Main variables used**")
st.sidebar.markdown(
    "- `survived` / `survived_label`\n"
    "- `passenger_class` / `pclass`\n"
    "- `sex`\n"
    "- `age`\n"
    "- `fare`\n"
    "- `family_size`\n"
    "- `embark_town`"
)

if section == "Dataset Overview":
    st.header("Dataset Overview")
    st.write("The Titanic dataset contains passenger-level records such as survival, class, sex, age, fare, embarkation town, and family relationships.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", f"{df.shape[1]:,}")
    col3.metric("Overall Survival Rate", f"{df['survived'].mean() * 100:.1f}%")
    col4.metric("Median Fare", f"${df['fare'].median():.2f}")

    st.subheader("Preview")
    st.dataframe(df.head(15), use_container_width=True)

    st.subheader("Cleaned Columns Used in This App")
    st.write(
        "Missing age and fare values are filled using their median values. "
        "Missing embarkation town and deck values are labelled as `Unknown`."
    )
    st.dataframe(
        df[[
            "survived_label", "passenger_class", "sex", "age", "fare",
            "family_size", "embark_town", "alone_label", "deck"
        ]].head(15),
        use_container_width=True,
    )

elif section == "2.1 Mosaic Plot":
    st.header("2.1 Mosaic Plot (Marimekko-style Normalised Bar Chart)")
    st.write("Purpose: show how survival outcome proportions differ across passenger classes.")

    mosaic_data = (
        df.groupby(["passenger_class", "survived_label"], observed=True)
        .size()
        .reset_index(name="passengers")
    )

    chart = (
        alt.Chart(mosaic_data)
        .mark_bar(size=70, opacity=0.9)
        .encode(
            x=alt.X(
                "passenger_class:N",
                title="Passenger Class",
                sort=class_order,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "passengers:Q",
                stack="normalize",
                title="Proportion of Passengers",
            ),
            color=alt.Color(
                "survived_label:N",
                title="Survival Outcome",
                scale=alt.Scale(scheme="tableau10"),
            ),
            tooltip=[
                alt.Tooltip("passenger_class:N", title="Class"),
                alt.Tooltip("survived_label:N", title="Outcome"),
                alt.Tooltip("passengers:Q", title="Passenger Count"),
            ],
        )
        .properties(
            width=700,
            height=420,
            title="Mosaic-style Plot: Survival Proportion by Passenger Class",
        )
    )

    st.altair_chart(chart, use_container_width=True)
    st.info(
        "Insight: survival is not evenly distributed across classes. "
        "First class has a larger survived segment, while third class has a larger non-survived segment."
    )
    st.markdown(
        "**Customisations made:** x-axis changed to passenger class, y-axis changed to passenger count, "
        "colour changed to survival outcome, and title/tooltips were updated."
    )

elif section == "2.2 Trellis Display":
    st.header("2.2 Trellis Display")
    st.write("Purpose: compare the relationship between age and fare across passenger classes using small multiples.")

    trellis_chart = (
        alt.Chart(df)
        .mark_circle(size=65, opacity=0.55)
        .encode(
            x=alt.X("age:Q", title="Age"),
            y=alt.Y("fare:Q", title="Fare Paid"),
            color=alt.Color(
                "survived_label:N",
                title="Survival Outcome",
                scale=alt.Scale(scheme="redblue"),
            ),
            shape=alt.Shape("sex:N", title="Sex"),
            tooltip=[
                alt.Tooltip("passenger_class:N", title="Class"),
                alt.Tooltip("sex:N", title="Sex"),
                alt.Tooltip("age:Q", title="Age", format=".1f"),
                alt.Tooltip("fare:Q", title="Fare", format=".2f"),
                alt.Tooltip("survived_label:N", title="Outcome"),
                alt.Tooltip("embark_town:N", title="Embarked From"),
            ],
        )
        .facet(
            facet=alt.Facet("passenger_class:N", title="Passenger Class", sort=class_order),
            columns=3,
        )
        .properties(title="Trellis Display: Age vs Fare by Passenger Class")
        .interactive()
    )

    st.altair_chart(trellis_chart, use_container_width=True)
    st.info(
        "Insight: the class panels separate fare ranges clearly. First-class passengers generally paid higher fares, "
        "while third-class passengers are concentrated at lower fares."
    )
    st.markdown(
        "**Customisations made:** scatter variables changed to age and fare, facets changed to passenger class, "
        "colour changed to survival outcome, shape added for sex, and opacity/tooltips were modified."
    )

elif section == "2.3 Heatmap":
    st.header("2.3 Heatmap")
    st.write("Purpose: represent survival-rate intensity across passenger class and sex.")

    heat_data = (
        df.groupby(["passenger_class", "sex"], observed=True)
        .agg(
            survival_rate=("survived", "mean"),
            passengers=("survived", "size"),
        )
        .reset_index()
    )

    heatmap = (
        alt.Chart(heat_data)
        .mark_rect(stroke="white", strokeWidth=2)
        .encode(
            x=alt.X(
                "passenger_class:N",
                title="Passenger Class",
                sort=class_order,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y("sex:N", title="Sex"),
            color=alt.Color(
                "survival_rate:Q",
                title="Survival Rate",
                scale=alt.Scale(scheme="blues", domain=[0, 1]),
            ),
            tooltip=[
                alt.Tooltip("passenger_class:N", title="Class"),
                alt.Tooltip("sex:N", title="Sex"),
                alt.Tooltip("survival_rate:Q", title="Survival Rate", format=".1%"),
                alt.Tooltip("passengers:Q", title="Passenger Count"),
            ],
        )
        .properties(
            width=600,
            height=260,
            title="Heatmap: Survival Rate by Class and Sex",
        )
    )

    st.altair_chart(heatmap, use_container_width=True)
    st.info(
        "Insight: darker cells indicate higher survival rates. Female passengers, especially in higher classes, "
        "usually show stronger survival rates than male passengers."
    )
    st.markdown(
        "**Customisations made:** categories changed to passenger class and sex, value changed to survival rate, "
        "colour scheme changed to blues, and formatted percentage tooltips were added."
    )

elif section == "2.4 Multivariate Scatter Plot":
    st.header("2.4 Multivariate Scatter Plot")
    st.write("Purpose: visualise multiple Titanic variables at once using position, colour, shape, and point size.")

    multi_scatter = (
        alt.Chart(df)
        .mark_point(filled=True, size=90, opacity=0.65)
        .encode(
            x=alt.X("age:Q", title="Age"),
            y=alt.Y("fare:Q", title="Fare Paid"),
            color=alt.Color(
                "survived_label:N",
                title="Survival Outcome",
                scale=alt.Scale(scheme="set1"),
            ),
            shape=alt.Shape("alone_label:N", title="Travel Status"),
            size=alt.Size(
                "family_size:Q",
                title="Family Size",
                scale=alt.Scale(range=[40, 450]),
            ),
            tooltip=[
                alt.Tooltip("passenger_class:N", title="Class"),
                alt.Tooltip("sex:N", title="Sex"),
                alt.Tooltip("age:Q", title="Age", format=".1f"),
                alt.Tooltip("fare:Q", title="Fare", format=".2f"),
                alt.Tooltip("family_size:Q", title="Family Size"),
                alt.Tooltip("alone_label:N", title="Travel Status"),
                alt.Tooltip("survived_label:N", title="Outcome"),
            ],
        )
        .properties(
            width=750,
            height=450,
            title="Multivariate Scatter: Age vs Fare (Colour=Survival, Shape=Alone, Size=Family Size)",
        )
        .interactive()
    )

    st.altair_chart(multi_scatter, use_container_width=True)
    st.info(
        "Insight: fare separates passenger class strongly, and some very high-fare passengers appear as outliers. "
        "Survival patterns can be explored by comparing colour with fare, age, and family size."
    )
    st.markdown(
        "**Customisations made:** x/y changed to age and fare, colour changed to survival outcome, "
        "shape changed to alone/with-family status, point size changed to family size, and interactivity was added."
    )

elif section == "2.5 Parallel Coordinate Plot":
    st.header("2.5 Parallel Coordinate Plot")
    st.write("Purpose: trace each passenger record across several numeric axes to reveal clusters and outliers.")

    fig = px.parallel_coordinates(
        df,
        dimensions=["age", "fare", "family_size", "pclass_num"],
        color="survived",
        color_continuous_scale=px.colors.diverging.Tealrose,
        range_color=[0, 1],
        labels={
            "age": "Age",
            "fare": "Fare Paid",
            "family_size": "Family Size",
            "pclass_num": "Passenger Class (1=First, 3=Third)",
            "survived": "Survived",
        },
        title="Parallel Coordinates: Age, Fare, Family Size, and Passenger Class",
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Survived",
            tickvals=[0, 1],
            ticktext=["No", "Yes"],
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info(
        "Insight: the parallel plot makes it easier to brush high-fare or large-family passengers and see how those "
        "records connect to class and survival."
    )
    st.markdown(
        "**Customisations made:** dimensions changed to Titanic numeric columns, colour changed to survival, "
        "labels/title were modified, and the Plotly brushing interaction remains available."
    )

elif section == "2.6 Grand Tour (3D Scatter)":
    st.header("2.6 Grand Tour: 3D Scatter Plot")
    st.write("Purpose: explore passenger age, fare, and family size in a rotatable 3D space.")

    fig_3d = px.scatter_3d(
        df,
        x="age",
        y="fare",
        z="family_size",
        color="passenger_class",
        symbol="sex",
        size="family_size",
        size_max=14,
        opacity=0.75,
        hover_data=["survived_label", "embark_town", "alone_label", "deck"],
        category_orders={"passenger_class": class_order},
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="3D Scatter: Age vs Fare vs Family Size",
    )
    fig_3d.update_layout(
        scene=dict(
            xaxis_title="Age",
            yaxis_title="Fare Paid",
            zaxis_title="Family Size",
        ),
        legend_title="Passenger Class",
    )

    st.plotly_chart(fig_3d, use_container_width=True)
    st.info(
        "Insight: the 3D view highlights high-fare outliers and helps separate classes by fare. "
        "Rotating the plot can reveal whether large-family passengers cluster in certain fare or class ranges."
    )
    st.markdown(
        "**Customisations made:** axes changed to age/fare/family size, colour changed to passenger class, "
        "symbol changed to sex, point size changed to family size, and hover details were expanded."
    )

elif section == "3. New Visualization - Seaborn Violin Plot":
    st.header("3. New Visualization: Seaborn Violin Plot")
    st.write("Purpose: compare the full distribution of fare values by passenger class and survival outcome.")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(
        data=df,
        x="passenger_class",
        y="fare",
        hue="survived_label",
        order=class_order,
        split=True,
        inner="quartile",
        cut=0,
        ax=ax,
    )
    ax.set_title("Seaborn Violin Plot: Fare Distribution by Class and Survival Outcome")
    ax.set_xlabel("Passenger Class")
    ax.set_ylabel("Fare Paid")
    ax.legend(title="Survival Outcome", loc="upper right")
    st.pyplot(fig)

    st.info(
        "Insight: the violin plot shows distribution shape, not just averages. "
        "First-class fares are spread across a much wider range, while third-class fares are concentrated lower."
    )
    st.markdown(
        "**Why this satisfies the new chart requirement:** it adds a violin plot, which is not one of the six original chart types."
    )