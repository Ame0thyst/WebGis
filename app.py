# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import pandas as pd

# # Set page config
# st.set_page_config(page_title="Web GIS Sederhana", layout="wide")

# # Judul aplikasi
# st.title("Sistem Informasi Geografis")

# # Sidebar untuk filter atau kontrol
# st.sidebar.title("Kontrol")
# show_layer = st.sidebar.checkbox("Tampilkan Semua Lokasi", True)

# # Data lokasi (contoh - ganti dengan 20 titik Anda)
# data = {
#     'Nama': ['Lokasi 1', 'Lokasi 2'],
#     'Latitude': [-7.797068, -7.798068],
#     'Longitude': [110.370529, 110.371529],
#     'Kategori': ['Kategori A', 'Kategori B']
# }
# df = pd.DataFrame(data)

# # Membuat peta dengan Folium
# m = folium.Map(location=[-7.797068, 110.370529], zoom_start=13)

# # Menambahkan marker untuk setiap lokasi
# if show_layer:
#     for idx, row in df.iterrows():
#         folium.Marker(
#             [row['Latitude'], row['Longitude']],
#             popup=row['Nama'],
#             tooltip=row['Kategori']
#         ).add_to(m)

# # Menampilkan peta di Streamlit
# folium_static(m, width=1000, height=600)

# # Menampilkan data dalam tabel
# if st.checkbox("Tampilkan Data Tabel"):
#     st.dataframe(df)

# # Fitur pencarian
# search_query = st.text_input("Cari Lokasi")
# if search_query:
#     filtered_df = df[df['Nama'].str.contains(search_query, case=False)]
#     st.write("Hasil Pencarian:")
#     st.dataframe(filtered_df)

# # Download data
# if st.button("Download Data CSV"):
#     csv = df.to_csv(index=False)
#     st.download_button(
#         label="Download",
#         data=csv,
#         file_name="lokasi_data.csv",
#         mime="text/csv"
#     )

##! udah aman, tapi gambar belum ada

# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import pandas as pd
# from folium.plugins import MarkerCluster

# # Set page config
# st.set_page_config(page_title="Web GIS", layout="wide")

# # Load data langsung dari file local
# def load_data():
#     # Ganti 'dataset.csv' dengan nama file CSV Anda
#     return pd.read_csv('dataset.csv')

# # Load data
# df = load_data()

# # Title
# st.title("Sistem Informasi Geografis")

# # Sidebar untuk filter
# st.sidebar.title("Filter")
# # Filter berdasarkan kategori
# all_categories = ['Semua'] + list(df['Kategori'].unique())
# selected_category = st.sidebar.selectbox('Pilih Kategori:', all_categories)

# # Filter data
# if selected_category != 'Semua':
#     filtered_df = df[df['Kategori'] == selected_category]
# else:
#     filtered_df = df

# # Buat peta
# m = folium.Map(
#     location=[df['Latitude'].mean(), df['Longitude'].mean()],
#     zoom_start=12
# )

# # Tambah marker cluster
# marker_cluster = MarkerCluster().add_to(m)

# # Tambah markers
# for idx, row in filtered_df.iterrows():
#     # Popup HTML dengan informasi detail
#     popup_html = f"""
#         <b>{row['Nama']}</b><br>
#         Kategori: {row['Kategori']}<br>
#         Alamat: {row['Alamat']}<br>
#         Deskripsi: {row['Deskripsi']}
#     """
    
#     # Tambah marker
#     folium.Marker(
#         [row['Latitude'], row['Longitude']],
#         popup=folium.Popup(popup_html, max_width=300),
#         tooltip=row['Nama']
#     ).add_to(marker_cluster)

# # Layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     # Tampilkan peta
#     folium_static(m, width=800)

# with col2:
#     # Fitur pencarian
#     st.subheader("Cari Lokasi")
#     search_term = st.text_input("Masukkan nama lokasi:")
#     if search_term:
#         search_results = df[df['Nama'].str.contains(search_term, case=False)]
#         st.dataframe(search_results)

#     # Tampilkan statistik
#     st.subheader("Statistik")
#     st.write(f"Total lokasi: {len(filtered_df)}")
#     st.write("Jumlah per Kategori:")
#     st.dataframe(df['Kategori'].value_counts())

##TODO : adasih gambarnya, tapi icon gambar rusak xxixixiix
# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import pandas as pd
# import json
# from folium.plugins import MarkerCluster

# # Set page config
# st.set_page_config(page_title="Web GIS", layout="wide")

# # Load data dari JSON
# def load_data():
#     with open('dataset.json', 'r') as file:
#         return pd.DataFrame(json.load(file))

# # Load data
# df = load_data()

# # Title
# st.title("Sistem Informasi Geografis")

# # Sidebar untuk filter
# st.sidebar.title("Filter")
# # Filter berdasarkan kategori
# all_categories = ['Semua'] + list(df['Kategori'].unique())
# selected_category = st.sidebar.selectbox('Pilih Kategori:', all_categories)

# # Filter data
# if selected_category != 'Semua':
#     filtered_df = df[df['Kategori'] == selected_category]
# else:
#     filtered_df = df

# # Buat peta
# m = folium.Map(
#     location=[df['Latitude'].mean(), df['Longitude'].mean()],
#     zoom_start=12
# )

# # Tambah marker cluster
# marker_cluster = MarkerCluster().add_to(m)

# # Tambah markers
# for idx, row in filtered_df.iterrows():
#     # Popup HTML dengan informasi dan gambar
#     popup_html = f"""
#         <b>{row['Nama']}</b><br>
#         Kategori: {row['Kategori']}<br>
#         Alamat: {row['Alamat']}<br>
#         Deskripsi: {row['Deskripsi']}<br>
#         <img src="{row['Gambar']}" alt="{row['Nama']}" width="200">
#     """
    
#     # Tambah marker
#     folium.Marker(
#         [row['Latitude'], row['Longitude']],
#         popup=folium.Popup(popup_html, max_width=300),
#         tooltip=row['Nama']
#     ).add_to(marker_cluster)

# # Layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     # Tampilkan peta
#     folium_static(m, width=800)

# with col2:
#     # Fitur pencarian
#     st.subheader("Cari Lokasi")
#     search_term = st.text_input("Masukkan nama lokasi:")
#     if search_term:
#         search_results = df[df['Nama'].str.contains(search_term, case=False)]
#         st.dataframe(search_results)

#     # Tampilkan statistik
#     st.subheader("Statistik")
#     st.write(f"Total lokasi: {len(filtered_df)}")
#     st.write("Jumlah per Kategori:")
#     st.dataframe(df['Kategori'].value_counts())

##? kenapa ya ga muncul gambarnya

# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import pandas as pd
# from folium.plugins import MarkerCluster
# import warnings
# import os

# # Suppress deprecation warnings
# warnings.filterwarnings('ignore', category=DeprecationWarning)

# # Set page config
# st.set_page_config(page_title="Web GIS", layout="wide")

# # Menggunakan st.cache_data untuk mempercepat loading data
# @st.cache_data
# def load_data():
#     return pd.read_json('dataset.json')

# # Load data
# df = load_data()

# # Title
# st.title("Sistem Informasi Geografis")

# # Sidebar untuk filter
# st.sidebar.title("Filter")

# # Filter berdasarkan kategori
# all_categories = ['Semua'] + list(df['Kategori'].unique())
# selected_category = st.sidebar.selectbox('Pilih Kategori:', all_categories)

# # Filter data
# if selected_category != 'Semua':
#     filtered_df = df[df['Kategori'] == selected_category]
# else:
#     filtered_df = df

# # Buat peta
# m = folium.Map(
#     location=[df['Latitude'].mean(), df['Longitude'].mean()],
#     zoom_start=12,
#     control_scale=True
# )

# # Tambah marker cluster
# marker_cluster = MarkerCluster().add_to(m)

# # Tambah markers
# for idx, row in filtered_df.iterrows():
#     # Popup HTML dengan path gambar langsung
#     popup_html = f"""
#     <div style="width:100%; max-width:300px; padding: 10px;">
#         <h4 style="margin-bottom:10px; color: #333;">{row['Nama']}</h4>
#         <img src="{row['Gambar']}" style="width:100%; max-width:280px; height:auto; margin-bottom:10px; border-radius: 5px;">
#         <div style="margin-top: 10px;">
#             <p style="margin: 5px 0;"><strong>Kategori:</strong> {row['Kategori']}</p>
#             <p style="margin: 5px 0;"><strong>Alamat:</strong> {row['Alamat']}</p>
#             <p style="margin: 5px 0;"><strong>Deskripsi:</strong> {row['Deskripsi']}</p>
#         </div>
#     </div>
#     """
    
#     # Tambah marker dengan IFrame untuk better formatting
#     popup = folium.Popup(
#         folium.IFrame(
#             html=popup_html,
#             width=320,
#             height=400
#         ),
#         max_width=320
#     )
    
#     # Tambahkan marker ke peta
#     folium.Marker(
#         location=[row['Latitude'], row['Longitude']],
#         popup=popup,
#         tooltip=row['Nama'],
#         icon=folium.Icon(color='red', icon='info-sign')
#     ).add_to(marker_cluster)

# # Layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     # Tampilkan peta dengan folium_static
#     folium_static(m, width=800, height=500)

# with col2:
#     # Fitur pencarian
#     st.subheader("Cari Lokasi")
#     search_term = st.text_input("Masukkan nama lokasi:")
#     if search_term:
#         search_results = df[df['Nama'].str.contains(search_term, case=False)]
#         st.dataframe(search_results)

#     # Tampilkan statistik
#     st.subheader("Statistik")
#     st.write(f"Total lokasi: {len(filtered_df)}")
#     st.write("Jumlah per Kategori:")
#     st.dataframe(df['Kategori'].value_counts())

##! ayola bisa
# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import pandas as pd
# from folium.plugins import MarkerCluster
# import warnings
# import os
# from PIL import Image

# # Suppress deprecation warnings
# warnings.filterwarnings('ignore', category=DeprecationWarning)

# # Set page config
# st.set_page_config(page_title="Web GIS", layout="wide")

# # Menggunakan st.cache_data untuk mempercepat loading data
# @st.cache_data
# def load_data():
#     return pd.read_json('dataset.json')

# # Function untuk membaca gambar
# @st.cache_data
# def load_image(image_path):
#     try:
#         # Hapus leading slash jika ada
#         image_path = image_path.lstrip('/')
#         return Image.open(image_path)
#     except Exception as e:
#         st.error(f"Error loading image: {str(e)}")
#         return None

# # Load data
# df = load_data()

# # Title
# st.title("Sistem Informasi Geografis")

# # Sidebar untuk filter
# st.sidebar.title("Filter")

# # Filter berdasarkan kategori
# all_categories = ['Semua'] + list(df['Kategori'].unique())
# selected_category = st.sidebar.selectbox('Pilih Kategori:', all_categories)

# # Filter data
# if selected_category != 'Semua':
#     filtered_df = df[df['Kategori'] == selected_category]
# else:
#     filtered_df = df

# # Buat peta
# m = folium.Map(
#     location=[df['Latitude'].mean(), df['Longitude'].mean()],
#     zoom_start=12,
#     control_scale=True
# )

# # Tambah marker cluster
# marker_cluster = MarkerCluster().add_to(m)

# # Tambah markers
# for idx, row in filtered_df.iterrows():
#     # Popup HTML tanpa gambar (gambar akan ditampilkan di sidebar)
#     popup_html = f"""
#     <div style="width:100%; max-width:300px; padding: 10px;">
#         <h4 style="margin-bottom:10px; color: #333;">{row['Nama']}</h4>
#         <div style="margin-top: 10px;">
#             <p style="margin: 5px 0;"><strong>Kategori:</strong> {row['Kategori']}</p>
#             <p style="margin: 5px 0;"><strong>Alamat:</strong> {row['Alamat']}</p>
#             <p style="margin: 5px 0;"><strong>Deskripsi:</strong> {row['Deskripsi']}</p>
#         </div>
#         <p style="margin: 5px 0; color: #666;"><i>Klik marker untuk melihat detail di panel kanan</i></p>
#     </div>
#     """
    
#     # Tambah marker dengan IFrame untuk better formatting
#     popup = folium.Popup(
#         folium.IFrame(
#             html=popup_html,
#             width=320,
#             height=250
#         ),
#         max_width=320
#     )
    
#     # Tambahkan marker ke peta
#     folium.Marker(
#         location=[row['Latitude'], row['Longitude']],
#         popup=popup,
#         tooltip=row['Nama'],
#         icon=folium.Icon(color='red', icon='info-sign')
#     ).add_to(marker_cluster)

# # Layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     # Tampilkan peta dengan folium_static
#     map_data = folium_static(m, width=800, height=500)
    
#     # Jika marker diklik, tampilkan detail di bawah peta
#     if map_data:
#         selected_location = st.empty()

# with col2:
#     # Fitur pencarian
#     st.subheader("Cari Lokasi")
#     search_term = st.text_input("Masukkan nama lokasi:")
    
#     if search_term:
#         search_results = df[df['Nama'].str.contains(search_term, case=False)]
#         if not search_results.empty:
#             for idx, row in search_results.iterrows():
#                 st.write(f"### {row['Nama']}")
                
#                 # Tampilkan gambar menggunakan Streamlit
#                 image = load_image(row['Gambar'])
#                 if image:
#                     st.image(image, use_column_width=True)
                
#                 st.write(f"**Kategori:** {row['Kategori']}")
#                 st.write(f"**Alamat:** {row['Alamat']}")
#                 st.write(f"**Deskripsi:** {row['Deskripsi']}")
#                 st.markdown("---")
    
#     # Tampilkan statistik
#     st.subheader("Statistik")
#     st.write(f"Total lokasi: {len(filtered_df)}")
#     st.write("Jumlah per Kategori:")
#     st.dataframe(df['Kategori'].value_counts())
    
#     # Tampilkan semua lokasi dengan gambar
#     st.subheader("Semua Lokasi")
#     for idx, row in filtered_df.iterrows():
#         st.write(f"### {row['Nama']}")
        
#         # Tampilkan gambar menggunakan Streamlit
#         image = load_image(row['Gambar'])
#         if image:
#             st.image(image, use_column_width=True)
        
#         st.write(f"**Kategori:** {row['Kategori']}")
#         st.write(f"**Alamat:** {row['Alamat']}")
#         st.write(f"**Deskripsi:** {row['Deskripsi']}")
#         st.markdown("---")


##! yang ini aja buat setoran jaga jaga
# import streamlit as st
# import folium
# from folium import plugins
# import json

# # Sample data (JSON)
# data = {
#     "locations": [
#         {"name": "Location 1", "latitude": 51.5074, "longitude": -0.1278, "description": "This is location 1.", 
#          "image": "https://images.unsplash.com/photo-1576091167746-1e84784621db"},
#         {"name": "Location 2", "latitude": 48.8566, "longitude": 2.3522, "description": "This is location 2.", 
#          "image": "city.png"}
#     ]
# }

# # Function to display map
# def show_map():
#     # Create folium map
#     m = folium.Map(location=[51.5074, -0.1278], zoom_start=2)

#     # Add markers to map
#     for location in data["locations"]:
#         # Create HTML content for the popup
#         popup_content = f"""
#             <b>{location['name']}</b><br>
#             {location['description']}<br>
#             <img src="{location['image']}" width="200" />
#         """
        
#         folium.Marker(
#             [location["latitude"], location["longitude"]],
#             popup=popup_content,
#             icon=folium.Icon(color="blue")
#         ).add_to(m)

#     # Display map
#     return m

# # Streamlit components
# st.title("Interactive Map with Location Details")

# # Show the map
# map_component = show_map()
# folium_map = map_component._repr_html_()

# # Embed map in Streamlit app
# st.components.v1.html(folium_map, height=600)


##? ini udah berhasil muncul gambar di pop upo nyaa. tapi fitur lainnya belum bisa

# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import os
# from PIL import Image
# import base64
# from io import BytesIO

# # Fungsi untuk mengubah gambar ke base64
# def get_image_base64(image_path):
#     img = Image.open(image_path)
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     return f"data:image/png;base64,{img_str}"

# # Fungsi untuk membuat HTML popup dengan gambar
# def create_popup_content(title, description, image_path):
#     try:
#         image_base64 = get_image_base64(image_path)
#         return f"""
#             <div style="width:300px; padding:10px;">
#                 <h3 style="color:#1f77b4;">{title}</h3>
#                 <p>{description}</p>
#                 <img src="{image_base64}" style="width:100%; margin-top:10px; border-radius:5px;">
#             </div>
#         """
#     except Exception as e:
#         st.error(f"Error loading image: {e}")
#         return f"""
#             <div style="width:300px">
#                 <h3>{title}</h3>
#                 <p>{description}</p>
#                 <p style="color:red;">Image not available</p>
#             </div>
#         """

# # Data lokasi
# locations = [
#     {
#         "name": "Lokasi 1",
#         "lat": -6.2088,
#         "lon": 106.8456,
#         "description": "Deskripsi lokasi 1",
#         "image_path": "city.png"  # Sesuaikan dengan path gambar Anda
#     },
#     {
#         "name": "Lokasi 2",
#         "lat": -6.1751,
#         "lon": 106.8650,
#         "description": "Deskripsi lokasi 2",
#         "image_path": "static/img/nt.JPG"  # Sesuaikan dengan path gambar Anda
#     }
# ]

# def main():
#     st.title("Peta Lokasi dengan Gambar")
    
#     # Buat peta dasar
#     m = folium.Map(location=[-6.2088, 106.8456], zoom_start=12)
    
#     # Tambahkan marker untuk setiap lokasi
#     for loc in locations:
#         popup_content = create_popup_content(
#             loc["name"],
#             loc["description"],
#             loc["image_path"]
#         )
        
#         folium.Marker(
#             [loc["lat"], loc["lon"]],
#             popup=folium.Popup(popup_content, max_width=350),
#             tooltip=loc["name"],
#             icon=folium.Icon(color="red", icon="info-sign")
#         ).add_to(m)
    
#     # Tampilkan peta
#     st_folium(m, height=500, width="100%")
    
#     # Tampilkan informasi tambahan
#     st.sidebar.header("Informasi Lokasi")
#     for loc in locations:
#         with st.sidebar.expander(loc["name"]):
#             st.write(loc["description"])
#             try:
#                 st.image(loc["image_path"], caption=loc["name"], use_column_width=True)
#             except Exception as e:
#                 st.error("Gambar tidak dapat dimuat")

# if __name__ == "__main__":
#     main()

##TODO udah GG nih ^_^
# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import json

# # Fungsi untuk membuat HTML popup dengan gambar
# def create_popup_content(title, description, image_path):
#     try:
#         return f"""
#             <div style="width:300px; padding:10px;">
#                 <h3 style="color:#1f77b4;">{title}</h3>
#                 <p>{description}</p>
#                 <img src="{image_path}" style="width:100%; margin-top:10px; border-radius:5px;">
#             </div>
#         """
#     except Exception as e:
#         st.error(f"Error loading image: {e}")
#         return f"""
#             <div style="width:300px">
#                 <h3>{title}</h3>
#                 <p>{description}</p>
#                 <p style="color:red;">Image not available</p>
#             </div>
#         """

# # Fungsi untuk memuat data dari file JSON
# def load_data_from_json(json_file):
#     try:
#         with open(json_file, "r") as file:
#             data = json.load(file)
#         return data
#     except Exception as e:
#         st.error(f"Error loading data from JSON: {e}")
#         return []

# def main():
#     st.title("Peta Lokasi dengan Gambar")
    
#     # Muat data dari dataset.json
#     locations = load_data_from_json("dataset.json")  # Pastikan path file json sesuai
    
#     # Buat peta dasar
#     m = folium.Map(location=[-7.792364, 110.365897], zoom_start=12)
    
#     # Tambahkan marker untuk setiap lokasi
#     for loc in locations:
#         popup_content = create_popup_content(
#             loc["Nama"],
#             loc["Deskripsi"],
#             loc["Gambar"]
#         )
        
#         folium.Marker(
#             [loc["Latitude"], loc["Longitude"]],
#             popup=folium.Popup(popup_content, max_width=350),
#             tooltip=loc["Nama"],
#             icon=folium.Icon(color="red", icon="info-sign")
#         ).add_to(m)
    
#     # Tampilkan peta
#     st_folium(m, height=500, width="100%")
    
#     # Tampilkan informasi tambahan
#     st.sidebar.header("Informasi Lokasi")
#     for loc in locations:
#         with st.sidebar.expander(loc["Nama"]):
#             st.write(f"**Kategori**: {loc['Kategori']}")
#             st.write(f"**Alamat**: {loc['Alamat']}")
#             st.write(loc["Deskripsi"])
#             try:
#                 st.image(loc["Gambar"], caption=loc["Nama"], use_column_width=True)
#             except Exception as e:
#                 st.error("Gambar tidak dapat dimuat")

# if __name__ == "__main__":
#     main()

##! gas lagii trial and error
import streamlit as st
import os
import folium
from streamlit_folium import st_folium
import json
from folium.plugins import Search
# from folium.plugins import LayerControl
from folium import LayerControl

def create_popup_content(title, description, image_path):
    try:
        return f"""
            <div style="width:300px; padding:10px;">
                <h3 style="color:#1f77b4;">{title}</h3>
                <p>{description}</p>
                <img src="{image_path}" style="width:100%; margin-top:10px; border-radius:5px;">
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

def load_data_from_json(json_file):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        st.error(f"Error loading data from JSON: {e}")
        return []

def main():
    st.title("Peta Lokasi dengan Gambar")
    
    # Muat data dari dataset.json
    locations = load_data_from_json("dataset.json")
    
    # Fitur pencarian berdasarkan nama
    search_query = st.text_input("Cari lokasi berdasarkan nama:")
    
    # Filter lokasi berdasarkan pencarian
    if search_query:
        locations = [loc for loc in locations if search_query.lower() in loc["Nama"].lower()]
    
    # Dapatkan semua kategori unik
    categories = list(set(loc["Kategori"] for loc in locations))
    
    # Checkbox untuk filter kategori
    st.sidebar.header("Filter Kategori")
    selected_categories = {}
    for category in categories:
        selected_categories[category] = st.sidebar.checkbox(category, True)
    
    # Buat peta dasar
    m = folium.Map(location=[-7.792364, 110.365897], zoom_start=12)
    
    # Buat feature group untuk setiap kategori
    feature_groups = {}
    for category in categories:
        feature_groups[category] = folium.FeatureGroup(name=category)
    
    # Tambahkan marker untuk setiap lokasi
    for loc in locations:
        if selected_categories[loc["Kategori"]]:  # Cek apakah kategori ini dipilih
            popup_content = create_popup_content(
                loc["Nama"],
                loc["Deskripsi"],
                loc["Gambar"]
            )
            
            marker = folium.Marker(
                [loc["Latitude"], loc["Longitude"]],
                popup=folium.Popup(popup_content, max_width=350),
                tooltip=loc["Nama"],
                icon=folium.Icon(color="red", icon="info-sign")
            )
            
            # Tambahkan marker ke feature group yang sesuai
            feature_groups[loc["Kategori"]].add_child(marker)
    
    # Tambahkan semua feature group ke peta
    for fg in feature_groups.values():
        fg.add_to(m)
    # Tambahkan kode ini setelah pembuatan marker dan sebelum LayerControl

    # Contoh menambahkan jalur jalan (GeoJSON)
    jalan_style = {
        'color': '#0000FF',
        'weight': 2,
        'opacity': 0.7
    }
    geojson_path = "static/layer/jalan.geojson"
    if not os.path.exists(geojson_path):
        st.error(f"File {geojson_path} tidak ditemukan.")
    else:
        folium.GeoJson(
            geojson_path,
            name='Jalur Jalan',
            style_function=lambda x: jalan_style
    ).add_to(m)

    # folium.GeoJson(
    #     "static/layer/jalan.geojson",  # Sesuaikan dengan file GeoJSON Anda
    #     name='Jalur Jalan',
    #     style_function=lambda x: jalan_style
    # ).add_to(m)

    # Contoh menambahkan kawasan (GeoJSON)
    kawasan_style = {
        'fillColor': '#FF0000',
        'color': '#FF0000',
        'weight': 1,
        'fillOpacity': 0.3
    }

    geojson_path = "static/layer/kawasan.geojson"
    if not os.path.exists(geojson_path):
        st.error(f"File {geojson_path} tidak ditemukan.")
    else:
        folium.GeoJson(
            geojson_path,
            name='Kawasan',
            style_function=lambda x: kawasan_style
    ).add_to(m)
    # Tambahkan kontrol layer
    folium.LayerControl().add_to(m)
    
    # Tampilkan peta
    st_folium(m, height=500, width="100%")
    
    # Tampilkan informasi tambahan di sidebar
    st.sidebar.header("Informasi Lokasi")
    for loc in locations:
        if selected_categories[loc["Kategori"]]:  # Tampilkan hanya lokasi dengan kategori yang dipilih
            with st.sidebar.expander(loc["Nama"]):
                st.write(f"**Kategori**: {loc['Kategori']}")
                st.write(f"**Alamat**: {loc['Alamat']}")
                st.write(loc["Deskripsi"])
                try:
                    st.image(loc["Gambar"], caption=loc["Nama"], use_column_width=True)
                except Exception as e:
                    st.error("Gambar tidak dapat dimuat")

if __name__ == "__main__":
    main()