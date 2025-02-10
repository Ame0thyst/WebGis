import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

def create_folium_heatmap(df):
    # Create a base map
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=13, width='100%', height='600px')
    
    # Prepare data for HeatMap
    heat_data = df[['Latitude', 'Longitude']].values.tolist()
    
    # Add heatmap layer
    HeatMap(heat_data).add_to(m)
    
    return m

def create_data_visualization_tab(locations):
    # Convert locations to DataFrame
    df = pd.DataFrame(locations)
    
    # Tab4 Visualization
    st.header("📊 Location Data Insights")
    
    # Visualization Columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie Chart: Location Distribution by Category
        st.subheader("Location Distribution")
        category_counts = df['Kategori'].value_counts()
        fig_pie = px.pie(
            values=category_counts.values, 
            names=category_counts.index, 
            title='Locations by Category',
            hole=0.3
        )
        st.plotly_chart(fig_pie)
        
    with col2:
        # Bar Chart: Top Locations by Category
        st.subheader("Category Breakdown")
        fig_bar = px.bar(
            x=category_counts.index, 
            y=category_counts.values, 
            title='Number of Locations per Category',
            labels={'x':'Category', 'y':'Number of Locations'}
        )
        st.plotly_chart(fig_bar)
    
    # Heatmap for Geographical Distribution
    st.subheader("Geographical Heatmap")
    heatmap = create_folium_heatmap(df)
    st.write("###")  # Adding some spacing
    folium_static(heatmap, width=1200, height=600)

    # Additional Statistics
    st.subheader("Quick Statistics")
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.metric("Total Locations", len(df))
        st.metric("Total Categories", len(category_counts))
    
    with col_stats2:
        st.metric("Most Common Category", category_counts.index[0])
        st.metric("Locations in Most Common Category", category_counts.values[0])
