import streamlit as st
import os
import folium
from streamlit_folium import st_folium
import json
import folium.plugins
from folium.plugins import Geocoder, MousePosition, MiniMap, MarkerCluster
from folium.plugins import Search
from folium import LayerControl
import openrouteservice as ors

# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide")

# Fungsi untuk membuat popup content
@st.cache_data
def create_popup_content(title, description, image_path, address):
    try:
        return f"""
            <div style="width:300px; padding:10px;">
                <h3 style="color:#1f77b4;">{title}</h3>
                <p>{description}</p>
                <img src="{image_path}" style="width:100%; margin-top:10px; border-radius:5px;">
                <p>{address}</p>
            </div>
        """
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return f"""
            <div style="width:300px">
                <h3>{title}</h3>
                <p>{description}</p>
                <p style="color:red;">Image not available</p>
            </div>
        """

# Fungsi untuk load data dari JSON
@st.cache_data
def load_data_from_json(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        st.error(f"Error loading data from JSON: {e}")
        return []

# Fungsi untuk mendapatkan rute
def get_route(start_coords, end_coords, api_key):
    """
    Mendapatkan rute menggunakan OpenRouteService
    """
    client = ors.Client(key=api_key)
    
    try:
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',
            format='geojson',
            optimize_waypoints=True
        )
        return route
    except Exception as e:
        st.error(f"Error getting route: {e}")
        return None

# def main():
#     # Judul aplikasi
#     st.title("Peta Lokasi dengan Cluster dan Rute")
    
#     # Load data lokasi
#     locations = load_data_from_json("dataset.json")
    
#     # Input API key untuk routing
#     api_key = st.sidebar.text_input("OpenRouteService API Key", type="password")
    
#     # Pemilihan lokasi untuk rute
#     st.subheader("Pencarian Rute")
#     location_names = [loc["Nama"] for loc in locations]
    
#     col1, col2 = st.columns(2)
#     with col1:
#         start_location = st.selectbox("Lokasi Awal", location_names)
#     with col2:
#         end_location = st.selectbox("Lokasi Tujuan", location_names)
    
#     show_route = st.button("Tampilkan Rute")
    
#     # Pencarian lokasi
#     search_query = st.text_input("Cari lokasi berdasarkan nama:")
#     if search_query:
#         locations = [loc for loc in locations if search_query.lower() in loc["Nama"].lower()]
    
#     # Filter kategori
#     categories = list(set(loc["Kategori"] for loc in locations))
#     st.sidebar.header("Filter Kategori")
#     selected_categories = {}
#     for category in categories:
#         selected_categories[category] = st.sidebar.checkbox(category, True)
    
#     # Inisialisasi peta
#     m = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
    
#     # Tambahkan plugin
#     Geocoder().add_to(m)
    
#     # Tambahkan layer satelit
#     folium.TileLayer(
#         tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#         attr='Esri',
#         name='Esri Satellite'
#     ).add_to(m)
    
#     # Tambahkan koordinat mouse
#     formatter = "function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};"
#     MousePosition(
#         position="bottomright",
#         separator=" | ",
#         empty_string="NaN",
#         lng_first=True,
#         num_digits=20,
#         prefix="Coordinates:",
#         lat_formatter=formatter,
#         lng_formatter=formatter,
#     ).add_to(m)
    
#     # Tambahkan mini map
#     MiniMap().add_to(m)
    
#     # Buat cluster untuk setiap kategori
#     marker_clusters = {}
#     for category in categories:
#         marker_clusters[category] = MarkerCluster(
#             name=category,
#             overlay=True,
#             control=True,
#             options={
#                 'maxClusterRadius': 50,
#                 'disableClusteringAtZoom': 16,
#                 'spiderfyOnMaxZoom': True,
#                 'showCoverageOnHover': True,
#                 'zoomToBoundsOnClick': True,
#                 'animate': True
#             }
#         )
#         marker_clusters[category].add_to(m)
    
#     # Tambahkan marker ke cluster
#     for loc in locations:
#         if selected_categories[loc["Kategori"]]:
#             popup_content = create_popup_content(
#                 loc["Nama"],
#                 loc["Deskripsi"],
#                 loc["Gambar"],
#                 loc["Alamat"]
#             )
            
#             marker = folium.Marker(
#                 [loc["Latitude"], loc["Longitude"]],
#                 popup=folium.Popup(popup_content, max_width=350),
#                 tooltip=loc["Nama"],
#                 icon=folium.Icon(color="red", icon="info-sign")
#             )
            
#             marker_clusters[loc["Kategori"]].add_child(marker)
    
#     # Tampilkan rute jika diminta
#     if show_route and api_key:
#         start_loc = next(loc for loc in locations if loc["Nama"] == start_location)
#         end_loc = next(loc for loc in locations if loc["Nama"] == end_location)
        
#         start_coords = [start_loc["Longitude"], start_loc["Latitude"]]
#         end_coords = [end_loc["Longitude"], end_loc["Latitude"]]
        
#         route = get_route(start_coords, end_coords, api_key)
        
#         if route:
#             # Tambahkan rute ke peta
#             folium.GeoJson(
#                 route,
#                 name='Route',
#                 style_function=lambda x: {
#                     'color': '#0000FF',
#                     'weight': 4,
#                     'opacity': 0.8
#                 }
#             ).add_to(m)
            
#             # Marker untuk titik awal dan akhir
#             folium.Marker(
#                 [start_loc["Latitude"], start_loc["Longitude"]],
#                 popup='Start: ' + start_location,
#                 icon=folium.Icon(color='green', icon='info-sign')
#             ).add_to(m)
            
#             folium.Marker(
#                 [end_loc["Latitude"], end_loc["Longitude"]],
#                 popup='End: ' + end_location,
#                 icon=folium.Icon(color='red', icon='info-sign')
#             ).add_to(m)
            
#             # Informasi rute
#             distance = route['features'][0]['properties']['segments'][0]['distance']
#             duration = route['features'][0]['properties']['segments'][0]['duration']
            
#             st.success(f"""
#                 Informasi Rute:
#                 - Jarak: {distance/1000:.2f} km
#                 - Waktu Tempuh: {duration/60:.0f} menit
#             """)
    
#     # Tambahkan kontrol layer
#     folium.LayerControl().add_to(m)
    
#     # Tampilkan peta
#     st_folium(m, height=500, width="100vw")
    
#     # Informasi lokasi di sidebar
#     st.sidebar.header("Informasi Lokasi")
#     for loc in locations:
#         if selected_categories[loc["Kategori"]]:
#             with st.sidebar.expander(loc["Nama"]):
#                 st.write(f"**Kategori**: {loc['Kategori']}")
#                 st.write(f"**Alamat**: {loc['Alamat']}")
#                 st.write(loc["Deskripsi"])
#                 try:
#                     st.image(loc["Gambar"], caption=loc["Nama"], use_container_width=True)
#                 except Exception as e:
#                     st.error("Gambar tidak dapat dimuat")

# if __name__ == "__main__":
#     main()


def main():
    # Judul aplikasi
    st.title("Peta Lokasi dengan Cluster dan Rute")
    
    # Load data lokasi
    try:
        locations = load_data_from_json("dataset.json")
    except Exception as e:
        st.error(f"Error: Pastikan file dataset.json ada di folder yang sama dengan aplikasi")
        st.stop()
    
    # Input API key untuk routing
    api_key = st.sidebar.text_input("OpenRouteService API Key", type="password")
    
    # Buat dua tab
    tab1, tab2 = st.tabs(["Peta Utama", "Peta Rute"])
    
    with tab1:
        # Pencarian lokasi
        search_query = st.text_input("Cari lokasi berdasarkan nama:")
        filtered_locations = locations
        if search_query:
            filtered_locations = [loc for loc in locations if search_query.lower() in loc["Nama"].lower()]
        
        # Filter kategori
        categories = list(set(loc["Kategori"] for loc in locations))
        st.sidebar.header("Filter Kategori")
        selected_categories = {}
        for category in categories:
            selected_categories[category] = st.sidebar.checkbox(category, True)
        
        # Inisialisasi peta utama
        m1 = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
        
        # [Tambahkan semua plugin dan layer untuk peta utama seperti sebelumnya...]
        Geocoder().add_to(m1)
        
        # Tambahkan layer satelit
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite'
        ).add_to(m1)
        
        # Tambahkan koordinat mouse
        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};"
        MousePosition(
            position="bottomright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m1)
        
        MiniMap().add_to(m1)
        
        # Buat cluster untuk setiap kategori
        marker_clusters = {}
        for category in categories:
            marker_clusters[category] = MarkerCluster(
                name=category,
                overlay=True,
                control=True,
                options={
                    'maxClusterRadius': 50,
                    'disableClusteringAtZoom': 16,
                    'spiderfyOnMaxZoom': True,
                    'showCoverageOnHover': True,
                    'zoomToBoundsOnClick': True,
                    'animate': True
                }
            )
            marker_clusters[category].add_to(m1)
        
        # Tambahkan marker ke cluster
        for loc in filtered_locations:
            if selected_categories[loc["Kategori"]]:
                popup_content = create_popup_content(
                    loc["Nama"],
                    loc["Deskripsi"],
                    loc["Gambar"],
                    loc["Alamat"]
                )
                
                marker = folium.Marker(
                    [loc["Latitude"], loc["Longitude"]],
                    popup=folium.Popup(popup_content, max_width=350),
                    tooltip=loc["Nama"],
                    icon=folium.Icon(color="red", icon="info-sign")
                )
                
                marker_clusters[loc["Kategori"]].add_child(marker)
        
        folium.LayerControl().add_to(m1)
        
        # Tampilkan peta utama
        st_folium(m1, height=500, width="100vw")
    
    with tab2:
        st.subheader("Pencarian Rute")
        
        # Pemilihan lokasi untuk rute
        location_names = [loc["Nama"] for loc in locations]
        
        col1, col2 = st.columns(2)
        with col1:
            start_location = st.selectbox("Lokasi Awal", location_names)
        with col2:
            end_location = st.selectbox("Lokasi Tujuan", location_names)
        
        show_route = st.button("Tampilkan Rute")
        
        # Inisialisasi peta rute
        m2 = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
        Geocoder().add_to(m2)
        
        if show_route and api_key:
            start_loc = next(loc for loc in locations if loc["Nama"] == start_location)
            end_loc = next(loc for loc in locations if loc["Nama"] == end_location)
            
            # Tambahkan marker untuk semua lokasi (opsional, bisa dikomentari jika tidak diperlukan)
            for loc in locations:
                folium.Marker(
                    [loc["Latitude"], loc["Longitude"]],
                    popup=loc["Nama"],
                    tooltip=loc["Nama"],
                    icon=folium.Icon(color="gray", icon="info-sign")
                ).add_to(m2)
            
            start_coords = [start_loc["Longitude"], start_loc["Latitude"]]
            end_coords = [end_loc["Longitude"], end_loc["Latitude"]]
            
            route = get_route(start_coords, end_coords, api_key)
            
            if route:
                # Tambahkan rute ke peta
                folium.GeoJson(
                    route,
                    name='Route',
                    style_function=lambda x: {
                        'color': '#0000FF',
                        'weight': 4,
                        'opacity': 0.8
                    }
                ).add_to(m2)
                
                # Marker untuk titik awal dan akhir
                folium.Marker(
                    [start_loc["Latitude"], start_loc["Longitude"]],
                    popup='Start: ' + start_location,
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m2)
                
                folium.Marker(
                    [end_loc["Latitude"], end_loc["Longitude"]],
                    popup='End: ' + end_location,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m2)
                
                # Fit bounds to show the entire route
                coordinates = route['features'][0]['geometry']['coordinates']
                bounds = [[coord[1], coord[0]] for coord in coordinates]
                m2.fit_bounds(bounds)
                
                # Informasi rute
                distance = route['features'][0]['properties']['segments'][0]['distance']
                duration = route['features'][0]['properties']['segments'][0]['duration']
                
                st.success(f"""
                    Informasi Rute:
                    - Jarak: {distance/1000:.2f} km
                    - Waktu Tempuh: {duration/60:.0f} menit
                """)
        
        # Tampilkan peta rute
        st_folium(m2, height=500, width="100vw")
    
    # Informasi lokasi di sidebar
    st.sidebar.header("Informasi Lokasi")
    for loc in filtered_locations:
        if selected_categories[loc["Kategori"]]:
            with st.sidebar.expander(loc["Nama"]):
                st.write(f"**Kategori**: {loc['Kategori']}")
                st.write(f"**Alamat**: {loc['Alamat']}")
                st.write(loc["Deskripsi"])
                try:
                    st.image(loc["Gambar"], caption=loc["Nama"], use_container_width=True)
                except Exception as e:
                    st.error("Gambar tidak dapat dimuat")

if __name__ == "__main__":
    main()