import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# Set page config
st.set_page_config(page_title="Web GIS Sederhana", layout="wide")

# Judul aplikasi
st.title("Sistem Informasi Geografis")

# Sidebar untuk filter atau kontrol
st.sidebar.title("Kontrol")
show_layer = st.sidebar.checkbox("Tampilkan Semua Lokasi", True)

# Data lokasi (contoh - ganti dengan 20 titik Anda)
data = {
    'Nama': ['Lokasi 1', 'Lokasi 2'],
    'Latitude': [-7.797068, -7.798068],
    'Longitude': [110.370529, 110.371529],
    'Kategori': ['Kategori A', 'Kategori B']
}
df = pd.DataFrame(data)

# Membuat peta dengan Folium
m = folium.Map(location=[-7.797068, 110.370529], zoom_start=13)

# Menambahkan marker untuk setiap lokasi
if show_layer:
    for idx, row in df.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=row['Nama'],
            tooltip=row['Kategori']
        ).add_to(m)

# Menampilkan peta di Streamlit
folium_static(m, width=1000, height=600)

# Menampilkan data dalam tabel
if st.checkbox("Tampilkan Data Tabel"):
    st.dataframe(df)

# Fitur pencarian
search_query = st.text_input("Cari Lokasi")
if search_query:
    filtered_df = df[df['Nama'].str.contains(search_query, case=False)]
    st.write("Hasil Pencarian:")
    st.dataframe(filtered_df)

# Download data
if st.button("Download Data CSV"):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download",
        data=csv,
        file_name="lokasi_data.csv",
        mime="text/csv"
    )