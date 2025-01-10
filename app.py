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

import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from folium.plugins import MarkerCluster
import base64
import os

# Set page config
st.set_page_config(page_title="Web GIS", layout="wide")

# Load data langsung dari file local
def load_data():
    # Ganti 'dataset.json' dengan nama file JSON Anda
    return pd.read_json('dataset.json')

# Fungsi untuk encode gambar ke Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Load data
df = load_data()

# Title
st.title("Sistem Informasi Geografis")

# Sidebar untuk filter
st.sidebar.title("Filter")
# Filter berdasarkan kategori
all_categories = ['Semua'] + list(df['Kategori'].unique())
selected_category = st.sidebar.selectbox('Pilih Kategori:', all_categories)

# Filter data
if selected_category != 'Semua':
    filtered_df = df[df['Kategori'] == selected_category]
else:
    filtered_df = df

# Buat peta
m = folium.Map(
    location=[df['Latitude'].mean(), df['Longitude'].mean()],
    zoom_start=12
)

# Tambah marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Tambah markers
for idx, row in filtered_df.iterrows():
    # Encode gambar ke Base64
    image_base64 = encode_image(row['Gambar'])
    
    # Popup HTML dengan gambar Base64
    popup_html = f"""
        <div style="width: 300px;">
            <img src="data:image/jpeg;base64,{image_base64}" alt="Gambar Tidak Tersedia" style="width: 100%; height: auto; border-radius: 5px;">
            <b>{row['Nama']}</b><br>
            Kategori: {row['Kategori']}<br>
            Alamat: {row['Alamat']}<br>
            Deskripsi: {row['Deskripsi']}
        </div>
    """
    
    # Tambah marker
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['Nama']
    ).add_to(marker_cluster)

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    # Tampilkan peta
    folium_static(m, width=800)

with col2:
    # Fitur pencarian
    st.subheader("Cari Lokasi")
    search_term = st.text_input("Masukkan nama lokasi:")
    if search_term:
        search_results = df[df['Nama'].str.contains(search_term, case=False)]
        st.dataframe(search_results)

    # Tampilkan statistik
    st.subheader("Statistik")
    st.write(f"Total lokasi: {len(filtered_df)}")
    st.write("Jumlah per Kategori:")
    st.dataframe(df['Kategori'].value_counts())

