import streamlit as st
import folium
import openrouteservice as ors
import polyline
import plotly.graph_objs as go
import numpy as np

def calculate_route_elevation(route, client):
    """Calculate elevation profile for a route"""
    try:
        # Extract coordinates from route
        coordinates = route['features'][0]['geometry']['coordinates']
        
        # Convert coordinates to list of [lon, lat]
        coordinates_list = [[coord[0], coord[1]] for coord in coordinates]
        
        # Request elevation data
        elevation_response = client.elevation_line(
            geometry=coordinates_list, 
            format_in='point', 
            format_out='geojson'
        )
        
        return elevation_response
    except Exception as e:
        st.error(f"Elevation data error: {e}")
        return None

def create_elevation_profile(elevation_data):
    """Create elevation profile chart"""
    if not elevation_data:
        return None
    
    # Extract elevation and calculate cumulative distance
    elevations = [coord[2] for coord in elevation_data['coordinates']]
    distances = np.cumsum([
        np.sqrt((elevation_data['coordinates'][i][0] - elevation_data['coordinates'][i-1][0])**2 + 
                (elevation_data['coordinates'][i][1] - elevation_data['coordinates'][i-1][1])**2) 
        for i in range(1, len(elevation_data['coordinates']))
    ])
    distances = np.insert(distances, 0, 0)
    
    # Create elevation profile plot
    fig = go.Figure(data=go.Scatter(
        x=distances/1000,  # Convert to kilometers
        y=elevations, 
        mode='line',
        name='Elevation',
        line=dict(color='green', width=2)
    ))
    fig.update_layout(
        title='Route Elevation Profile',
        xaxis_title='Distance (km)',
        yaxis_title='Elevation (m)',
        height=300
    )
    
    return fig

def get_alternative_routes(client, start_coords, end_coords):
    """Get alternative routing options"""
    try:
        # Request routes with specific parameters
        routes = client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',
            format='geojson',
            alternative_routes={
                'share_factors': ['DURATION', 'DISTANCE'],
                'max_alternatives': 2
            }
        )
        return routes['features']
    except Exception as e:
        st.error(f"Alternative routes error: {e}")
        return []

def display_route_details(route):
    """Extract and display detailed route information"""
    properties = route['properties']['summary']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Distance", f"{properties['distance']/1000:.2f} km")
    with col2:
        st.metric("Duration", f"{properties['duration']/60:.0f} mins")
    with col3:
        st.metric("Expected Fuel", f"{(properties['distance']/1000)*0.1:.2f} L")

def advanced_routing_features(m2, route, client, start_location, end_location):
    """Add advanced routing features to the map and Streamlit app"""
    
    # Elevation Profile
    elevation_data = calculate_route_elevation(route, client)
    if elevation_data:
        elevation_fig = create_elevation_profile(elevation_data)
        if elevation_fig:
            st.plotly_chart(elevation_fig, use_container_width=True)
    
    # Alternative Routes
    start_coords = [start_location["Longitude"], start_location["Latitude"]]
    end_coords = [end_location["Longitude"], end_location["Latitude"]]
    alternative_routes = get_alternative_routes(client, start_coords, end_coords)
    
    # Display Alternative Routes
    if alternative_routes:
        st.subheader("Alternative Routes")
        for idx, alt_route in enumerate(alternative_routes, 1):
            with st.expander(f"Route {idx}"):
                # Add alternative route to map
                folium.GeoJson(
                    alt_route,
                    name=f'Alternative Route {idx}',
                    style_function=lambda x: {
                        'color': '#FF0000',  # Red color for alternative routes
                        'weight': 3,
                        'opacity': 0.7
                    }
                ).add_to(m2)
                
                # Display route details
                display_route_details(alt_route)

