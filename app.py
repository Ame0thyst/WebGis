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
from static.feat.displayFeedback import display_feedback_tab
from static.feat.sidebar import display_sidebar
import polyline
import plotly.graph_objs as go
import numpy as np
from datetime import datetime
import plotly.express as px
import pandas as pd



# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide")
##! buat advanced routes 

def get_advanced_route(start_coords, end_coords, api_key, profile='driving-car'):
    """
    Enhanced route calculation with multiple advanced features
    """
    client = ors.Client(key=api_key)
    
    try:
        # Request extended route information
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile=profile,
            format='geojson',
            optimize_waypoints=True,
            extra_info=['surface', 'steepness', 'tollways']
        )
        
        # Analisis detail rute
        route_details = analyze_route_details(route)
        
        return {
            'route_data': route,
            'details': route_details
        }
    except Exception as e:
        st.error(f"Error getting advanced route: {e}")
        return None

def analyze_route_details(route):
    """
    Ekstrak informasi detail dari rute
    """
    try:
        properties = route['features'][0]['properties']
        segments = properties['segments'][0]
        
        # Perhitungan detail rute
        details = {
            'total_distance': segments['distance'] / 1000,  # km
            'total_duration': segments['duration'] / 60,  # menit
            'route_steps': segments['steps'],
            
            # Informasi tambahan
            'road_surface_types': {},
            'elevation_profile': calculate_elevation_profile(route),
            
            # Analisis karakteristik rute
            'route_complexity': calculate_route_complexity(segments),
            'alternative_routes': suggest_alternative_routes(route)
        }
        
        return details
    except Exception as e:
        st.error(f"Error analyzing route details: {e}")
        return {}

def calculate_elevation_profile(route):
    """
    Hitung profil ketinggian sepanjang rute
    """
    try:
        coordinates = route['features'][0]['geometry']['coordinates']
        elevations = []
        
        for coord in coordinates:
            # Simulasi data ketinggian (koordinat longitude, latitude)
            # Dalam implementasi nyata, gunakan API ketinggian
            elevation = get_elevation(coord[1], coord[0])
            elevations.append({
                'longitude': coord[0],
                'latitude': coord[1],
                'elevation': elevation
            })
        
        return {
            'min_elevation': min(elevations, key=lambda x: x['elevation'])['elevation'],
            'max_elevation': max(elevations, key=lambda x: x['elevation'])['elevation'],
            'elevation_points': elevations
        }
    except Exception as e:
        st.error(f"Error calculating elevation profile: {e}")
        return {}

def get_elevation(latitude, longitude):
    """
    Dapatkan ketinggian dari koordinat (contoh sederhana)
    """
    # Implementasi nyata memerlukan API ketinggian seperti Google Elevation API
    return np.random.randint(0, 500)  # Simulasi ketinggian

def calculate_route_complexity(segments):
    """
    Analisis kompleksitas rute berdasarkan segmen
    """
    complexity_score = 0
    
    # Penilaian kompleksitas
    for step in segments['steps']:
        if 'road_type' in step:
            complexity_score += step.get('road_type_complexity', 0)
    
    return {
        'complexity_score': complexity_score,
        'difficulty_level': 'Mudah' if complexity_score < 5 else 'Sedang' if complexity_score < 10 else 'Sulit'
    }

def suggest_alternative_routes(primary_route):
    """
    Sarankan rute alternatif
    """
    alternatives = [
        {'type': 'Terdekat', 'criteria': 'Jarak minimal'},
        {'type': 'Terhemat', 'criteria': 'Bahan bakar minimal'},
        {'type': 'Tercepat', 'criteria': 'Waktu tercepat'}
    ]
    return alternatives
##!


##! fitur feedback 

def save_feedback(name, email, rating, feedback_text, category):
    """
    Simpan feedback ke file atau database
    """
    feedback_entry = {
        'timestamp': datetime.now().isoformat(),
        'name': name,
        'email': email,
        'rating': rating,
        'category': category,
        'feedback_text': feedback_text
    }
    
    try:
        # Simpan ke file JSON
        feedback_file = 'dataset/user_feedbacks.json'
        
        # Baca feedback yang ada
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r') as f:
                feedbacks = json.load(f)
        else:
            feedbacks = []
        
        # Tambahkan feedback baru
        feedbacks.append(feedback_entry)
        
        # Simpan kembali
        with open(feedback_file, 'w') as f:
            json.dump(feedbacks, f, indent=4)
        
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan feedback: {e}")
        return False
##! ****************************************************************************************************************
##TODO ***********************************************************************************************************
##! fitur like sidebar 
# def load_likes():
#     """Load likes from a JSON file"""
#     try:
#         with open('dataset/location_likes.json', 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}

# def save_likes(likes):
#     """Save likes to a JSON file"""
#     with open('dataset/location_likes.json', 'w') as f:
#         json.dump(likes, f, indent=4)

##! ****************************************************************************************************************
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
    m = folium.Map(location=[0.5071, 101.4478], zoom_start=9, control_scale=True,)
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
    api_key = os.getenv('OPENROUTESERVICE_API_KEY') ##! pakai ini kalau di local
    # api_key = st.secrets["OPENROUTESERVICE_API_KEY"] ##! ini kalau di deploy di streamlit share

    
    # Buat dua tab
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Peta Utama", "Peta Rute", "Para Pejuang 👑", "📊 Data Insights","Feedback", "Display Feedback"])
    
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
            "Sepeda Motor": "driving-car",
            "Berjalan Kaki": "foot-walking",
            "Sepeda": "cycling-regular"
        }
        
        # Warna rute berdasarkan moda transportasi
        route_colors = {
            "Mobil (Tercepat)": '#0000FF',
            "Sepeda Motor": '#FF0000',
            "Berjalan Kaki": '#00FF00',
            "Sepeda": '#FFA500'
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
                
                # Dapatkan rute dengan detail lanjutan
                advanced_route = get_advanced_route(start_coords, end_coords, api_key, selected_profile)
                
                if advanced_route:
                    route_data = advanced_route['route_data']
                    route_details = advanced_route['details']
                    
                    # Tampilkan informasi rute lanjutan
                    st.markdown("### Informasi Rute Lanjutan")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Jarak", f"{route_details['total_distance']:.2f} km")
                    
                    with col2:
                        st.metric("Waktu Tempuh", f"{route_details['total_duration']:.0f} menit")
                    
                    with col3:
                        st.metric("Tingkat Kesulitan", route_details['route_complexity']['difficulty_level'])
                    
                    # Tampilkan rute alternatif
                    st.markdown("### Rute Alternatif")
                    for alt in route_details['alternative_routes']:
                        st.info(f"**{alt['type']}**: {alt['criteria']}")
                    
                    # Tambahkan rute ke peta
                    folium.GeoJson(
                        route_data,
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
                    coordinates = route_data['features'][0]['geometry']['coordinates']
                    bounds = [[coord[1], coord[0]] for coord in coordinates]
                    m2.fit_bounds(bounds)
                    
            except Exception as e:
                st.error(f"Error menampilkan rute lanjutan: {str(e)}")
        
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
##! Tab 4
    with tab4:
        create_data_visualization_tab(locations)   
        
##! Tab 5
    with tab5:
        st.header("Berikan Umpan Balik Anda")
        
        # Kolom input feedback
        col1, col2 = st.columns(2)
        
        with col1:
            feedback_name = st.text_input("Nama Anda", placeholder="Masukkan nama lengkap")
            feedback_email = st.text_input("Email", placeholder="contoh@email.com")
        
        with col2:
            feedback_category = st.selectbox("Kategori Umpan Balik", [
                "Peta",
                "Rute",
                "Desain Antarmuka",
                "Fungsionalitas",
                "Lainnya"
            ])
            feedback_rating = st.slider("Tingkat Kepuasan", 1, 5, 3)
        
        feedback_text = st.text_area("Tuliskan Umpan Balik Anda", placeholder="Ceritakan pengalaman Anda...")
        
        # Tombol kirim feedback
        submit_feedback = st.button("Kirim Umpan Balik")
        
        # Proses feedback
        if submit_feedback:
            # Validasi input
            if not feedback_name or not feedback_email or not feedback_text:
                st.warning("Mohon lengkapi semua field")
            else:
                # Simpan feedback
                if save_feedback(feedback_name, feedback_email, feedback_rating, feedback_text, feedback_category):
                    st.success("Terima kasih! Umpan balik Anda telah tersimpan.")
                else:
                    st.error("Gagal mengirim umpan balik. Silakan coba lagi.")
        
        # Tampilkan statistik feedback (opsional)
        st.markdown("### Statistik Umpan Balik")
        
        try:
            # Baca file feedback
            with open('dataset/user_feedbacks.json', 'r') as f:
                feedbacks = json.load(f)
            
            # Hitung statistik
            total_feedbacks = len(feedbacks)
            avg_rating = sum(feedback['rating'] for feedback in feedbacks) / total_feedbacks if total_feedbacks > 0 else 0
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Umpan Balik", total_feedbacks)
            
            with col2:
                st.metric("Rata-rata Rating", f"{avg_rating:.2f} / 5")
            
            rating_counts = {}
            for feedback in feedbacks:
                rating_counts[feedback['rating']] = rating_counts.get(feedback['rating'], 0) + 1
            
            rating_df = pd.DataFrame.from_dict(rating_counts, orient='index', columns=['Count'])
            rating_df.index.name = 'Rating'
            rating_df.reset_index(inplace=True)
            
            fig = px.bar(rating_df, x='Rating', y='Count', title='Distribusi Rating')
            st.plotly_chart(fig)
        
        except FileNotFoundError:
            st.info("Belum ada umpan balik")
        except Exception as e:
            st.error(f"Gagal memuat statistik: {e}")

    st.markdown('</div>', unsafe_allow_html=True) 
    with tab6:
        display_feedback_tab()
##? ***********************************************************************************************************
##! ***********************************************************************************************************
##TODO ***********************************************************************************************************
    ##? DIBAWAH INI UNTUK SIDEBAR AJA YGY
    # Informasi lokasi di sidebar
    display_sidebar(filtered_locations, selected_categories)
    
if __name__ == "__main__":
    main()