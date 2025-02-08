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
from dotenv import load_dotenv
from static.feat.Visualization import create_data_visualization_tab
import polyline
import plotly.graph_objs as go
import numpy as np


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
@st.cache_data
def get_route(start_coords, end_coords, api_key, profile='driving-car'):
    """
    Mendapatkan rute menggunakan OpenRouteService dengan berbagai moda transportasi
    
    :param start_coords: Koordinat awal [longitude, latitude]
    :param end_coords: Koordinat akhir [longitude, latitude]
    :param api_key: API key OpenRouteService
    :param profile: Profil transportasi (default: driving-car)
    :return: Data rute atau None jika gagal
    """
    client = ors.Client(key=api_key)
    
    try:
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile=profile,
            format='geojson',
            optimize_waypoints=True
        )
        return route
    except Exception as e:
        st.error(f"Error getting route for {profile}: {e}")
        return None

def initialize_session_state():
    """Inisialisasi session state yang diperlukan"""
    if 'route_data' not in st.session_state:
        st.session_state.route_data = None
    if 'show_route' not in st.session_state:
        st.session_state.show_route = False
    if 'last_start' not in st.session_state:
        st.session_state.last_start = None
    if 'last_end' not in st.session_state:
        st.session_state.last_end = None

def create_base_map():
    """Membuat peta dasar dengan plugin standar"""
    m = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
    Geocoder().add_to(m)
    
    # Tambahkan layer satelit
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite'
    ).add_to(m)
    
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
    ).add_to(m)
    
    MiniMap().add_to(m)
    return m
kecamatan_colors = {
    "BANDARSEIKIJANG": "#FF5733",
    "BUKITRAYA": "#33FF57",
    "KAMPARKIRI HILIR": "#3357FF",
    "KAMPARKIRI TENGAH": "#FF33A1",
    "KERINCIKANAN": "#F4A460",
    "KOTOGASIB": "#6A5ACD",
    "LANGGAM": "#FF4500",
    "LIMAPULUH": "#7FFF00",
    "LUBUKDALAM": "#FF6347",
    "MARPOYANDAMAI": "#4682B4",
    "MINAS": "#B22222",
    "PAYUNGSEKAKI": "#ADFF2F",
    "PEKANBARUKOTA": "#FF69B4",
    "PERHENTIANRAJA": "#5F9EA0",
    "RUMBAI": "#FFD700",
    "RUMBAIPESISIR": "#6495ED",
    "SAIL": "#DC143C",
    "SENAPELAN": "#7B68EE",
    "SIAK HULU": "#008080",
    "SUKAJADI": "#DA70D6",
    "TAMBANG": "#EE82EE",
    "TAMPAN": "#00FA9A",
    "TAPUNG": "#FFA500",
    "TAPUNG HILIR": "#D2691E",
    "TENAYANRAYA": "#1E90FF",
    "TUALANG": "#32CD32",
}
def style_function(feature):
    """Fungsi untuk mengatur style layer wilayah"""
    kecamatan_name = feature['properties']['Name']
    color = kecamatan_colors.get(kecamatan_name, "#CCCCCC")  # Default: abu-abu
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.3,
    }
##! load layer wilayah
@st.cache_data
def load_geojson():
    """Load data GeoJSON wilayah"""
    try:
        with open("static/layer/wilayah.geojson", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading GeoJSON: {e}")
        return None
def main():
    # Inisialisasi session state
    initialize_session_state()
    
    # Judul aplikasi
    st.title("Peta Lokasi dengan Cluster dan Rute")
    
    # Load data lokasi
    try:
        locations = load_data_from_json("dataset.json")
    except Exception as e:
        st.error(f"Error: Pastikan file dataset.json ada di folder yang sama dengan aplikasi")
        st.stop()
    
    # Input API key untuk routing
    # api_key = st.sidebar.text_input("OpenRouteService API Key", type="password") ##? yang ini diaktifkan kalau mau input api key nya manual, tapi dua baris dibawahnya harus di command 
    load_dotenv()
    api_key = os.getenv('OPENROUTESERVICE_API_KEY')
    
    # Buat dua tab
    tab1, tab2, tab3, tab4 = st.tabs(["Peta Utama", "Peta Rute", "Para Pejuang 👑", "📊 Data Insights"])
    
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
        m1 = create_base_map()
        ##! ini layer wilayah ya
        geojson_data = load_geojson()
        if geojson_data:
            geojson_layer = folium.GeoJson(
                geojson_data,
                name="Wilayah Kecamatan",
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(
                    fields=["Name", "SHAPE_Leng", "SHAPE_Area"],
                    aliases=["Kecamatan:", "Panjang:", "Luas:"],
                ),
                zoom_on_click=True,
            ).add_to(m1)
        # Buat cluster untuk setiap kategori
        marker_clusters = {}
        for category in categories:
            marker_clusters[category] = MarkerCluster(
                name=category,
                overlay=True,
                control=True,
                options={
                    'maxClusterRadius': 50,
                    'disableClusteringAtZoom': 11,
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
        st_folium(m1, height=500, width="100vw", key="main_map")
    
    with tab2:  
        st.subheader("Pencarian Rute")
    
        # Pemilihan lokasi untuk rute
        location_names = [loc["Nama"] for loc in locations]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_location_name = st.selectbox("Lokasi Awal", location_names, key='start_loc_select')
        with col2:
            end_location_name = st.selectbox("Lokasi Tujuan", location_names, key='end_loc_select')
        with col3:
            transportation_mode = st.selectbox("Moda Transportasi", [
                "Mobil (Tercepat)", 
                "Sepeda Motor", 
                "Berjalan Kaki", 
                "Sepeda"
            ], key='transport_mode_select')
        
        # Pemetaan moda transportasi ke profil OpenRouteService
        transport_profiles = {
            "Mobil (Tercepat)": "driving-car",
            "Sepeda Motor": "driving-car",  # OpenRouteService tidak memiliki profil spesifik untuk motor
            "Berjalan Kaki": "foot-walking",
            "Sepeda": "cycling-regular"
        }
        
        # Fungsi callback untuk tombol
        def on_route_button_click():
            st.session_state.show_route = True
            st.session_state.last_start = start_location_name
            st.session_state.last_end = end_location_name
            st.session_state.last_mode = transportation_mode
        
        show_route = st.button("Tampilkan Rute", on_click=on_route_button_click)
        
        # Inisialisasi peta rute
        m2 = create_base_map()
        
        # Tambahkan marker untuk semua lokasi
        for loc in locations:
            folium.Marker(
                [loc["Latitude"], loc["Longitude"]],
                popup=loc["Nama"],
                tooltip=loc["Nama"],
                icon=folium.Icon(color="gray", icon="info-sign")
            ).add_to(m2)
        
        # Logika untuk menampilkan rute
        if st.session_state.show_route and api_key:
            try:
                # Cari data lokasi awal dan tujuan
                start_location = next(loc for loc in locations if loc["Nama"] == start_location_name)
                end_location = next(loc for loc in locations if loc["Nama"] == end_location_name)
                
                # Persiapkan koordinat
                start_coords = [start_location["Longitude"], start_location["Latitude"]]
                end_coords = [end_location["Longitude"], end_location["Latitude"]]
                
                # Pilih profil berdasarkan moda transportasi
                selected_profile = transport_profiles.get(transportation_mode, "driving-car")
                
                # Dapatkan rute
                route = get_route(start_coords, end_coords, api_key, selected_profile)
                
                if route:
                    # Tentukan warna rute berdasarkan moda transportasi
                    route_colors = {
                        "Mobil (Tercepat)": '#0000FF',
                        "Sepeda Motor": '#FF0000',
                        "Berjalan Kaki": '#00FF00',
                        "Sepeda": '#FFA500'
                    }
                    
                    # Tambahkan rute ke peta
                    folium.GeoJson(
                        route,
                        name=f'Rute {transportation_mode}',
                        style_function=lambda x: {
                            'color': route_colors.get(transportation_mode, '#0000FF'),
                            'weight': 4,
                            'opacity': 0.8
                        }
                    ).add_to(m2)
                    
                    # Marker untuk titik awal dan akhir
                    folium.Marker(
                        [start_location["Latitude"], start_location["Longitude"]],
                        popup='Start: ' + start_location_name,
                        icon=folium.Icon(color='green', icon='info-sign')
                    ).add_to(m2)
                    
                    folium.Marker(
                        [end_location["Latitude"], end_location["Longitude"]],
                        popup='End: ' + end_location_name,
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m2)
                    
                    # Sesuaikan tampilan peta untuk menampilkan seluruh rute
                    coordinates = route['features'][0]['geometry']['coordinates']
                    bounds = [[coord[1], coord[0]] for coord in coordinates]
                    m2.fit_bounds(bounds)
                    
                    # Tampilkan informasi rute
                    distance = route['features'][0]['properties']['segments'][0]['distance']
                    duration = route['features'][0]['properties']['segments'][0]['duration']
                    
                    st.success(f"""
                        Informasi Rute {transportation_mode}:
                        - Jarak: {distance/1000:.2f} km
                        - Waktu Tempuh: {duration/60:.0f} menit
                    """)
            
            except Exception as e:
                st.error(f"Error menampilkan rute: {str(e)}")
        
        # Tampilkan peta rute
        st_folium(m2, height=500, width="100vw", key="route_map")

    ##! tab 3 ygy
    with tab3:
        st.markdown("""
            <style>
            .profile-name p{
                color : red;
                    }
            .about-header {
                text-align: center;
                padding: 2rem 0;
            }
            .profile-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 1rem;
                padding: 1rem;
            }
            .profile-card {
                width: 300px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                background: white;
                margin: 1rem;
            }
            .profile-image {
                width: 100%;
                height: 300px;
                object-fit: cover;
            }
            .profile-info {
                padding: 1rem;
                text-align: center;
            }
            .profile-name {
                font-size: 1.25rem;
                font-weight: bold;
                margin-bottom: 5px;
                color : black;
            }
            .social-links {
                display: flex;
                justify-content: center;
                gap: 1rem;
            }
            .social-link {
                text-decoration: none;
                color: inherit;
                transition: opacity 0.2s;
            }
            .social-link:hover {
                opacity: 0.7;
            }
            </style>
    """, unsafe_allow_html=True)
        
    

        # Header
        st.markdown('<h1 class="about-header">⭐ Tim Season Depan Pasti Immortal ⭐</h1>', unsafe_allow_html=True)
        
        # Container untuk profile cards
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        # Data anggota tim
        # team_members = [
        #     {
        #         "name": "Nama Anggota 1",
        #         "nim"   : "210401227",
        #         "image": "https://i.imgur.com/qZw1MOb.jpeg",  # Ganti dengan URL foto anggota
        #         "linkedin": "https://linkedin.com/in/username1",
        #         "github": "https://github.com/username1"
        #     },
        #     {
        #         "name": "Nama Anggota 2",
        #         "nim"   : "210401227",
        #         "image": "/static/img/city.png",  # Ganti dengan URL foto anggota
        #         "linkedin": "https://linkedin.com/in/username2",
        #         "github": "https://github.com/username2"
        #     },
        #     {
        #         "name": "Nama Anggota 3",
        #         "nim"   : "210401227",
        #         "image": "https://i.imgur.com/jbtARaK.jpeg",  # Ganti dengan URL foto anggota
        #         "linkedin": "https://linkedin.com/in/username3",
        #         "github": "https://github.com/username3"
        #     }
        # ]
        with open('dataset/team.json', 'r') as file:
            team_members = json.load(file)
        
        # Buat columns untuk layout yang responsif
        cols = st.columns(5)
        
        # Tampilkan profile cards
        for idx, member in enumerate(team_members):
            with cols[idx % 5]:
                st.markdown(f"""
                    <div class="profile-card">
                        <img src="{member['image']}" alt="{member['name']}" class="profile-image">
                        <div class="profile-info">
                            <div class="profile-name">👑{member['name']}</div>
                            <div class="profile-name"><p>{member['nim']}<p></div>
                            <div class="social-links">
                                <a href="{member['linkedin']}" target="_blank" class="social-link">
                                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30">
                                </a>
                                <a href="{member['github']}" target="_blank" class="social-link">
                                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="30">
                                </a>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    with tab4:
        create_data_visualization_tab(locations)   

    st.markdown('</div>', unsafe_allow_html=True) 
    ##? DIBAWAH INI UNTUK SIDEBAR AJA YGY
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