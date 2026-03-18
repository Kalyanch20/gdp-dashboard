import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Page config
st.set_page_config(
    page_title='GDP Dashboard - Kalyan',
    page_icon='🌍',
    layout='wide'
)

# -----------------------------
# Function to load data
@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------
# UI START

st.title("🌍 GDP Dashboard - Kalyan")

st.markdown("""
Explore GDP data from the **World Bank Open Data**.

Select years and countries to visualize economic growth.
""")

st.divider()

# -----------------------------
# Year Selection

min_year = int(gdp_df['Year'].min())
max_year = int(gdp_df['Year'].max())

from_year, to_year = st.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# -----------------------------
# Country Selection

countries = sorted(gdp_df['Country Code'].unique())

selected_countries = st.multiselect(
    "Select Countries",
    countries,
    default=['IND', 'USA', 'CHN'] if 'IND' in countries else countries[:3]
)

if not selected_countries:
    st.warning("⚠️ Please select at least one country")
    st.stop()

# -----------------------------
# Filter Data

filtered_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries)) &
    (gdp_df['Year'] >= from_year) &
    (gdp_df['Year'] <= to_year)
]

# -----------------------------
# Chart

st.subheader("📈 GDP Over Time")
st.line_chart(
    filtered_df,
    x="Year",
    y="GDP",
    color="Country Code"
)

# -----------------------------
# Metrics

st.subheader(f"📊 GDP in {to_year}")

first_year_df = gdp_df[gdp_df['Year'] == from_year]
last_year_df = gdp_df[gdp_df['Year'] == to_year]

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % 4]

    with col:
        try:
            first_gdp = first_year_df[first_year_df['Country Code'] == country]['GDP'].values[0] / 1e9
            last_gdp = last_year_df[last_year_df['Country Code'] == country]['GDP'].values[0] / 1e9

            if math.isnan(first_gdp) or first_gdp == 0:
                growth = "n/a"
                delta_color = "off"
            else:
                growth = f"{last_gdp / first_gdp:.2f}x"
                delta_color = "normal"

            st.metric(
                label=f"{country}",
                value=f"{last_gdp:,.0f} B",
                delta=growth,
                delta_color=delta_color
            )

        except:
            st.metric(label=country, value="No data")

# -----------------------------
# Footer

st.divider()
st.markdown("👨‍💻 Developed by **Kalyan** | Cloud Lab Project 🚀")
