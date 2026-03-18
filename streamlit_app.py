import streamlit as st
import pandas as pd
import math
from pathlib import Path

# -----------------------------
# Page Config
st.set_page_config(
    page_title="GDP Dashboard - Kalyan",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Load Data
@st.cache_data
def load_data():
    DATA_FILENAME = Path(__file__).parent / "data/gdp_data.csv"
    raw_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    df = raw_df.melt(
        ['Country Name', 'Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP'
    )

    df['Year'] = pd.to_numeric(df['Year'])
    return df

df = load_data()

# -----------------------------
# Title
st.title("🌍 GDP Dashboard - Kalyan")

st.markdown("Analyze GDP trends across countries and years.")

st.divider()

# -----------------------------
# Sidebar Filters
st.sidebar.header("🔍 Filters")

min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

from_year, to_year = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

countries = sorted(df['Country Name'].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=["India", "United States", "China"] if "India" in countries else countries[:3]
)

if not selected_countries:
    st.warning("⚠️ Please select at least one country")
    st.stop()

# -----------------------------
# Filter Data
filtered_df = df[
    (df['Country Name'].isin(selected_countries)) &
    (df['Year'] >= from_year) &
    (df['Year'] <= to_year)
]

# -----------------------------
# Line Chart
st.subheader("📈 GDP Over Time")

st.line_chart(
    filtered_df,
    x="Year",
    y="GDP",
    color="Country Name"
)

# -----------------------------
# Metrics Section
st.subheader(f"📊 GDP in {to_year}")

first_year_df = df[df['Year'] == from_year]
last_year_df = df[df['Year'] == to_year]

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % 4]

    with col:
        try:
            first_val = first_year_df[first_year_df['Country Name'] == country]['GDP'].values[0] / 1e9
            last_val = last_year_df[last_year_df['Country Name'] == country]['GDP'].values[0] / 1e9

            if math.isnan(first_val) or first_val == 0:
                growth = "n/a"
                delta_color = "off"
            else:
                growth = f"{last_val / first_val:.2f}x"
                delta_color = "normal"

            st.metric(
                label=country,
                value=f"{last_val:,.0f} B",
                delta=growth,
                delta_color=delta_color
            )

        except:
            st.metric(label=country, value="No data")

# -----------------------------
# Footer
st.divider()
st.markdown("👨‍💻 Developed by **Kalyan** | Cloud Lab Project 🚀")
