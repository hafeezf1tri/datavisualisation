# Data Visualisation Coursework
This is for personal coursework use.

This repository contains university coursework for the **TFB3133/TEB3133: Data Visualization - May 2026** class. It includes a collection of Python and Streamlit applications created to explore data-visualisation concepts, progressing from introductory chart selection and linked highlighting to interactive dashboards and high-dimensional visualisations.

This repository will be continuously updated until the end of semester/when the labwork finishes.

The examples use:

- Altair for declarative and interactive charts
- Streamlit for browser-based dashboards
- Pandas for data preparation and aggregation
- Plotly, Seaborn, and Matplotlib for selected Lab 3 visualisations

## Repository Contents

```text
datavisualisation/
|-- inclass-grup-campus/
|   `-- dashboard.py
|-- lab2/
|   |-- beginla2.py
|   |-- lab2.py
|   |-- sdg_index_2000-2022.csv
|   `-- sustainable_development_report_2023.csv
|-- lab3/
|   `-- lab3.py
|-- requirements.txt
`-- README.md
```

### Campus Pulse Dashboard

`inclass-grup-campus/dashboard.py` is a simulated smart-campus operations dashboard. It generates 24 hours of mock data for five campus buildings and displays:

- Electricity and water usage
- Connected WiFi users
- Attendance
- Estimated CO2 emissions
- KPI cards and sparklines
- Building-level energy comparisons
- A linked building filter for the energy and carbon chart
- Dashboard design notes and a proposed real-time data strategy

The data is generated locally and changes when **Refresh now** is selected.

### Lab 2: Introductory Visualisation

`lab2/beginla2.py` introduces core visualisation ideas using a small in-memory demographic dataset. It demonstrates:

- Exploratory scatter plots
- Presentation-oriented bar charts
- Linked highlighting between charts
- Multivariate context through colour, tooltips, and interaction

### Lab 2: UN Sustainable Development Goals

`lab2/lab2.py` uses the included UN Sustainable Development Goal datasets to examine country and regional progress. It includes:

- A country-level SDG Index versus SDG 7 scatter plot
- Regional average SDG Index rankings
- Linked highlighting between regional bars and country points
- Regional SDG 7 trends from 2000 to 2022

The application merges the time-series index data with regional information from the 2023 Sustainable Development Report.

### Lab 3: Titanic High-Dimensional Visualisation

`lab3/lab3.py` uses Seaborn's Titanic dataset to demonstrate several techniques for exploring many variables:

- Mosaic-style normalised bars
- Trellis displays
- Heatmaps
- Multivariate scatter plots
- Parallel coordinate plots
- Interactive 3D scatter plots
- A Seaborn violin plot

The app also performs light data cleaning, derives passenger and family labels, and provides a dataset overview.

## Getting Started

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Install the core dependencies:

```powershell
pip install -r requirements.txt
```

Lab 3 also imports Seaborn, Matplotlib, and Plotly:

```powershell
pip install seaborn matplotlib plotly
```

### 3. Run an application

Run one Streamlit application at a time from the repository root:

```powershell
streamlit run inclass-grup-campus/dashboard.py
streamlit run lab2/beginla2.py
streamlit run lab2/lab2.py
streamlit run lab3/lab3.py
```

Streamlit will print a local URL, usually `http://localhost:8501`, which can be opened in a browser.

## Data Sources

- The Lab 2 SDG CSV files are stored directly in `lab2/`.
- The Campus Pulse dashboard uses generated mock data and does not require an external service.
- Lab 3 loads the Titanic dataset through `seaborn.load_dataset("titanic")`. The first run may require an internet connection so Seaborn can download and cache the dataset.

## Notes

- The applications are independent and do not share a common entry point.
- The repository is intended for learning and coursework rather than production deployment.
- Some Altair APIs used in the earlier exercises may produce deprecation warnings with newer Altair releases, but they document the interaction techniques used in the assignments.
