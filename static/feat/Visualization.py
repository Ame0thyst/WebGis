import pandas as pd
import plotly.express as px
import streamlit as st

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
    
    # Scatter Plot for Geographical Distribution
    st.subheader("Geographical Location Scatter")
    fig_scatter = px.scatter_mapbox(
        df, 
        lat='Latitude', 
        lon='Longitude', 
        color='Kategori', 
        hover_name='Nama',
        hover_data=['Alamat', 'Kategori'],
        zoom=13,
        height=600
    )
    fig_scatter.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Additional Statistics
    st.subheader("Quick Statistics")
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.metric("Total Locations", len(df))
        st.metric("Total Categories", len(category_counts))
    
    with col_stats2:
        st.metric("Most Common Category", category_counts.index[0])
        st.metric("Locations in Most Common Category", category_counts.values[0])