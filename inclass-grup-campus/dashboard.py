from datetime import datetime, timedelta
import math
import random

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Campus Pulse",
    layout="wide",
)

COLORS = {
    "Electricity Usage": "#F4B942",
    "Water Usage": "#43A5BE",
    "WiFi Users": "#7D6CDF",
    "Attendance": "#39A96B",
    "CO2 Emissions": "#E66B5B",
}

BUILDINGS = ["Engineering", "Library", "Science", "Student Centre", "Administration"]

st.markdown(
    """
    <style>
        .stApp { background: #F4F7F9; color: #17222B; }
        [data-testid="stSidebar"] { background: #132D36; }
        [data-testid="stSidebar"] * { color: #F5FAFB; }
        .block-container { padding-top: 1.7rem; padding-bottom: 2rem; }
        .eyebrow {
            color: #49707B; font-size: .78rem; font-weight: 700;
            letter-spacing: .13em; text-transform: uppercase;
        }
        .dashboard-title {
            color: #132D36; font-size: 2.25rem; font-weight: 760;
            letter-spacing: -.04em; margin: .15rem 0 .15rem;
        }
        .subtitle { color: #63747A; margin-bottom: 1.15rem; }
        .metric-card {
            background: white; border: 1px solid #DFE8EB; border-radius: 14px;
            box-shadow: 0 5px 18px rgba(24, 55, 64, .06);
            min-height: 114px; padding: 1rem 1.05rem .85rem;
        }
        .metric-label {
            color: #61757C; font-size: .76rem; font-weight: 700;
            letter-spacing: .06em; text-transform: uppercase;
        }
        .metric-value {
            color: #152D35; font-size: 1.65rem; font-weight: 760;
            letter-spacing: -.035em; margin-top: .25rem;
        }
        .metric-change { font-size: .78rem; font-weight: 650; margin-top: .2rem; }
        .good { color: #23875B; }
        .bad { color: #CC554A; }
        .neutral { color: #687A80; }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: white; border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def build_dummy_data(refresh_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create stable, plausible hourly campus readings for a mock dashboard."""
    rng = random.Random(2406 + refresh_id)
    start = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(
        hours=23
    )
    building_factor = {
        "Engineering": 1.18,
        "Library": 0.91,
        "Science": 1.28,
        "Student Centre": 1.02,
        "Administration": 0.72,
    }
    rows = []

    for hour_index in range(24):
        timestamp = start + timedelta(hours=hour_index)
        hour = timestamp.hour
        occupied = 1 if 8 <= hour <= 20 else 0
        activity = max(0, math.sin((hour - 7) * math.pi / 14))

        for building in BUILDINGS:
            factor = building_factor[building]
            electricity = (44 + 53 * activity + 18 * occupied) * factor
            electricity += rng.uniform(-4.5, 4.5)
            water = (3.3 + 7.2 * activity + 1.7 * occupied) * factor
            water += rng.uniform(-0.7, 0.7)
            wifi = max(4, int((18 + 215 * activity) * factor + rng.uniform(-10, 10)))
            capacity = int(230 * factor)
            attendance = min(capacity, max(0, int(wifi * 0.78 + rng.uniform(-8, 8))))
            co2 = electricity * 0.39 + rng.uniform(-1.3, 1.3)

            rows.append(
                {
                    "timestamp": timestamp,
                    "building": building,
                    "electricity_kwh": round(max(0, electricity), 1),
                    "water_m3": round(max(0, water), 1),
                    "wifi_users": wifi,
                    "attendance": attendance,
                    "co2_kg": round(max(0, co2), 1),
                }
            )

    hourly = pd.DataFrame(rows)
    latest = hourly[hourly["timestamp"] == hourly["timestamp"].max()].copy()
    return hourly, latest


def sparkline(data: pd.DataFrame, field: str, color: str) -> alt.Chart:
    trend = data.groupby("timestamp", as_index=False)[field].sum()
    return (
        alt.Chart(trend)
        .mark_area(
            line={"color": color, "strokeWidth": 2},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color=color, offset=0),
                    alt.GradientStop(color="#FFFFFF", offset=1),
                ],
                x1=1,
                x2=1,
                y1=0,
                y2=1,
            ),
        )
        .encode(
            x=alt.X("timestamp:T", axis=None),
            y=alt.Y(f"{field}:Q", axis=None, scale=alt.Scale(zero=False)),
        )
        .properties(height=42)
    )


def metric_card(
    label: str,
    value: str,
    change: float,
    inverse: bool = False,
) -> None:
    is_good = change <= 0 if inverse else change >= 0
    change_class = "good" if is_good else "bad"
    arrow = "up" if change >= 0 else "down"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-change {change_class}">
                {arrow} {abs(change):.1f}% vs previous hour
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "refresh_id" not in st.session_state:
    st.session_state.refresh_id = 0

with st.sidebar:
    st.title("Campus Pulse")
    st.caption("Facilities operations centre")
    st.divider()
    view = st.radio("View", ["Overview", "Design notes"], label_visibility="collapsed")
    st.divider()
    st.markdown("**Data status**")
    st.success("All 5 feeds online")
    auto_refresh = st.toggle("Auto-refresh plan", value=True)
    st.caption("Mock data is regenerated when Refresh now is clicked.")

if st.button("Refresh now", type="primary"):
    st.session_state.refresh_id += 1

hourly, latest = build_dummy_data(st.session_state.refresh_id)
generated_at = datetime.now().strftime("%d %b %Y, %H:%M")

st.markdown('<div class="eyebrow">Smart campus operations</div>', unsafe_allow_html=True)
title_col, status_col = st.columns([4, 1])
with title_col:
    st.markdown('<div class="dashboard-title">Campus Pulse</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">A live view of resource demand, occupancy, and environmental impact.</div>',
        unsafe_allow_html=True,
    )
with status_col:
    st.caption(f"Last updated\n\n**{generated_at}**")

if view == "Overview":
    current = hourly[hourly["timestamp"] == hourly["timestamp"].max()]
    previous = hourly[
        hourly["timestamp"]
        == hourly["timestamp"].max() - timedelta(hours=1)
    ]

    metric_specs = [
        ("Electricity", "electricity_kwh", " kWh", True, COLORS["Electricity Usage"]),
        ("Water", "water_m3", " m3", True, COLORS["Water Usage"]),
        ("WiFi users", "wifi_users", "", False, COLORS["WiFi Users"]),
        ("Attendance", "attendance", "", False, COLORS["Attendance"]),
        ("CO2 emissions", "co2_kg", " kg", True, COLORS["CO2 Emissions"]),
    ]
    metric_cols = st.columns(5)
    for col, (label, field, unit, inverse, color) in zip(metric_cols, metric_specs):
        current_value = current[field].sum()
        previous_value = previous[field].sum()
        change = ((current_value - previous_value) / previous_value) * 100
        display_value = (
            f"{current_value:,.1f}{unit}"
            if field in {"water_m3", "co2_kg"}
            else f"{current_value:,.0f}{unit}"
        )
        with col:
            metric_card(label, display_value, change, inverse)
            st.altair_chart(
                sparkline(hourly, field, color),
                width="stretch",
            )

    st.write("")
    main_col, side_col = st.columns([2.35, 1], gap="large")

    with main_col:
        with st.container(border=True):
            st.subheader("Energy demand and carbon impact")
            st.caption(
                "Click a building bar to filter the hourly composite chart. Click empty space to reset."
            )

            building_click = alt.selection_point(
                fields=["building"], on="click", empty=True
            )
            building_summary = (
                hourly.groupby("building", as_index=False)["electricity_kwh"].sum()
            )
            building_bars = (
                alt.Chart(building_summary)
                .mark_bar(cornerRadiusEnd=4)
                .encode(
                    x=alt.X(
                        "electricity_kwh:Q",
                        title="Electricity in last 24 hours (kWh)",
                    ),
                    y=alt.Y("building:N", title=None, sort="-x"),
                    color=alt.condition(
                        building_click,
                        alt.value(COLORS["Electricity Usage"]),
                        alt.value("#D9E2E5"),
                    ),
                    tooltip=[
                        alt.Tooltip("building:N", title="Building"),
                        alt.Tooltip(
                            "electricity_kwh:Q",
                            title="24h electricity",
                            format=",.0f",
                        ),
                    ],
                )
                .add_params(building_click)
                .properties(height=145)
            )

            base = alt.Chart(hourly).transform_filter(building_click)
            electricity_area = base.mark_area(
                color=COLORS["Electricity Usage"], opacity=0.24
            ).encode(
                x=alt.X("timestamp:T", title=None, axis=alt.Axis(format="%H:%M")),
                y=alt.Y(
                    "sum(electricity_kwh):Q",
                    title="Electricity (kWh)",
                    axis=alt.Axis(titleColor=COLORS["Electricity Usage"]),
                ),
                tooltip=[
                    alt.Tooltip("timestamp:T", title="Time", format="%d %b, %H:%M"),
                    alt.Tooltip(
                        "sum(electricity_kwh):Q",
                        title="Electricity",
                        format=",.1f",
                    ),
                ],
            )
            electricity_line = electricity_area.mark_line(
                color=COLORS["Electricity Usage"], strokeWidth=2.5
            )
            co2_line = base.mark_line(
                color=COLORS["CO2 Emissions"], strokeWidth=2.5
            ).encode(
                x="timestamp:T",
                y=alt.Y(
                    "sum(co2_kg):Q",
                    title="CO2 (kg)",
                    axis=alt.Axis(
                        orient="right", titleColor=COLORS["CO2 Emissions"]
                    ),
                ),
                tooltip=[
                    alt.Tooltip("timestamp:T", title="Time", format="%d %b, %H:%M"),
                    alt.Tooltip("sum(co2_kg):Q", title="CO2", format=",.1f"),
                ],
            )

            event_time = hourly["timestamp"].min() + timedelta(hours=13)
            annotations = pd.DataFrame(
                {
                    "timestamp": [event_time],
                    "event": ["Peak lab period"],
                }
            )
            event_rule = (
                alt.Chart(annotations)
                .mark_rule(color="#667A81", strokeDash=[5, 4])
                .encode(x="timestamp:T")
            )
            event_text = (
                alt.Chart(annotations)
                .mark_text(
                    align="left",
                    dx=6,
                    dy=-95,
                    color="#52676E",
                    fontSize=11,
                )
                .encode(x="timestamp:T", text="event:N")
            )
            composite = alt.layer(
                electricity_area,
                electricity_line,
                co2_line,
                event_rule,
                event_text,
            ).resolve_scale(y="independent").properties(height=285)

            st.altair_chart(
                alt.vconcat(building_bars, composite, spacing=18),
                width="stretch",
            )

    with side_col:
        with st.container(border=True):
            st.subheader("Current building load")
            st.caption("WiFi users compared with recorded attendance")
            occupancy_long = latest.melt(
                id_vars=["building"],
                value_vars=["wifi_users", "attendance"],
                var_name="measure",
                value_name="people",
            )
            occupancy_long["measure"] = occupancy_long["measure"].map(
                {"wifi_users": "WiFi users", "attendance": "Attendance"}
            )
            occupancy_chart = (
                alt.Chart(occupancy_long)
                .mark_bar(cornerRadiusEnd=3)
                .encode(
                    x=alt.X("people:Q", title="People"),
                    y=alt.Y("building:N", title=None, sort=BUILDINGS),
                    color=alt.Color(
                        "measure:N",
                        title=None,
                        scale=alt.Scale(
                            domain=["WiFi users", "Attendance"],
                            range=[
                                COLORS["WiFi Users"],
                                COLORS["Attendance"],
                            ],
                        ),
                        legend=alt.Legend(orient="top"),
                    ),
                    yOffset="measure:N",
                    tooltip=["building:N", "measure:N", "people:Q"],
                )
                .properties(height=250)
            )
            st.altair_chart(occupancy_chart, width="stretch")


else:
    st.header("Dashboard design rationale")
    notes = [
        (
            "Suitable chart types",
            "KPI cards give the latest reading; 24-hour sparklines show direction without taking much space. "
            "Horizontal bars make building comparisons easy, while grouped bars compare WiFi users with attendance.",
        ),
        (
            "Sparkline variables",
            "Time is on the x-axis. The y-variable is electricity (kWh), water (m3), connected WiFi users, "
            "attendance count, or CO2 emissions (kg). Each sparkline aggregates all campus buildings hourly.",
        ),
        (
            "Composite chart",
            "The main chart layers an electricity area/line with a CO2 line on an independent right axis. "
            "This shows whether carbon impact rises with demand while preserving each variable's unit.",
        ),
        (
            "Click interaction",
            "Clicking a building in the ranking filters the composite chart to that building. "
            "Clicking outside the bars restores the whole-campus view.",
        ),
        (
            "Annotations",
            "A dashed rule labels the peak laboratory period. In production, annotations should mark timetable events, "
            "maintenance, outages, leaks, holidays, and threshold breaches.",
        ),
        (
            "Real-time update strategy",
            "Meters and access systems would publish readings to a message broker. A stream processor would validate and "
            "aggregate them into one-minute and hourly tables. The dashboard would poll a fast API every 30 seconds, "
            "refresh only changed components, show the last successful update, and retain the previous reading during feed failures.",
        ),
    ]
    for heading, text in notes:
        with st.container(border=True):
            st.subheader(heading)
            st.write(text)

    if auto_refresh:
        st.info(
            "Recommended production cadence: electricity, water, WiFi, and CO2 every 30 seconds; attendance every 1-5 minutes."
        )
