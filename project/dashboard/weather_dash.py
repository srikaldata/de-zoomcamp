import streamlit as st
from google.cloud import bigquery
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Weather Intelligence", layout="wide")

# Define our strict color mapping
CITY_COLORS = {"New York": "blue", "San Francisco": "red"}

client = bigquery.Client()

@st.cache_data(ttl=600)
def load_data():
    metrics_query = "SELECT * FROM `weather_analytics.weather_metrics`"
    summary_query = "SELECT * FROM `weather_analytics.weather_summary`"
    
    metrics = client.query(metrics_query).to_dataframe()
    summary = client.query(summary_query).to_dataframe()
    
    metrics['date'] = pd.to_datetime(metrics['date'])
    # Filter for the 2021-2025 window
    metrics = metrics[(metrics['date'].dt.year >= 2021) & (metrics['date'].dt.year <= 2025)]
    return metrics, summary

# Helper function for Pie Charts
def plot_weather_pie(df, city_name):
    city_df = df[df['city'] == city_name]
    fig = px.pie(
        city_df, 
        names='weather_category', 
        title=f"{city_name} Conditions",
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    # Include legend and adjust padding (margins)
    fig.update_layout(
        showlegend=True, 
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    ) 
    return fig

try:
    df_metrics, df_summary = load_data()

    st.title("☀️ Weather Intelligence: NY vs SF (2021-2025)")

    # --- 1. Top Level Metrics ---
    ny_data = df_metrics[df_metrics['city'] == 'New York']
    sf_data = df_metrics[df_metrics['city'] == 'San Francisco']

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("NY Max", f"{ny_data['temp_max'].max()}°C")
    m2.metric("NY Min", f"{ny_data['temp_min'].min()}°C")
    m3.metric("SF Max", f"{sf_data['temp_max'].max()}°C")
    m4.metric("SF Min", f"{sf_data['temp_min'].min()}°C")

    st.markdown("---")

    # --- 2. Side-by-Side Charts Section ---
    st.subheader("Comparative Visualizations")
    
    # Create three columns
    col_line, col_pie_ny, col_pie_sf = st.columns([2, 1, 1]) # Line chart gets more width

    with col_line:
        # Resample to Monthly Average per City
        monthly_df = df_metrics.groupby(['city', pd.Grouper(key='date', freq='M')])['temp_avg'].mean().reset_index()
        
        fig_line = px.line(
            monthly_df, 
            x='date', 
            y='temp_avg', 
            color='city',
            color_discrete_map=CITY_COLORS,
            title="Monthly Avg Temp",
            labels={'temp_avg': '°C', 'date': 'Year'},
            template="plotly_dark"
        )
        fig_line.update_layout(hovermode="x unified", margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_line, use_container_width=True)

    with col_pie_ny:
        st.plotly_chart(plot_weather_pie(df_metrics, "New York"), use_container_width=True)

    with col_pie_sf:
        st.plotly_chart(plot_weather_pie(df_metrics, "San Francisco"), use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")