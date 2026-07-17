- **Deskripsi** : WebGIS (Web-based Geographic Information System) interaktif yang dirancang untuk memetakan lokasi secara visual dengan fitur klasterisasi marker (Marker Cluster), visualisasi wilayah kecamatan menggunakan GeoJSON, pencarian rute dinamis berdasarkan moda transportasi (mobil, motor, sepeda, jalan kaki) menggunakan API OpenRouteService, analisis wawasan data (Data Insights) berbasis grafik, serta integrasi sistem feedback pengguna.

- **Tech Stack** : Streamlit, Folium, Streamlit-Folium, OpenRouteService, Plotly, Pandas, NumPy, Polyline, JSON, CSS.

- **Arsitektur** :
  - `app.py` : Berfungsi sebagai entry point utama aplikasi Streamlit yang menyusun layout, tab, dan alur integrasi peta.
  - `requirements.txt` : Menyimpan daftar pustaka (library) dan dependensi Python yang dibutuhkan proyek.
  - `style.css` : Menyimpan konfigurasi gaya (styling) kustom untuk antarmuka kartu feedback.
  - `dataset/` : Folder penyimpanan data (dataset lokasi, data tim, dan log umpan balik pengguna dalam format JSON).
  - `static/` :
    - `feat/` : Menyimpan modul fitur modular seperti visualisasi (`Visualization.py`), menu samping (`sidebar.py`), dan penampilan umpan balik (`displayFeedback.py`).
    - `layer/` : Berisi data spasial batas wilayah kecamatan (`wilayah.geojson`).
    - `img/` : Aset gambar proyek.

- **Solusi Teknis** :
  - *Tantangan* : Menampilkan rute perjalanan yang dinamis serta memproses data spasial GeoJSON berukuran besar tanpa menurunkan performa rendering peta pada aplikasi Streamlit yang bersifat reaktif.
  - *Penyelesaian* : Integrasi API klien OpenRouteService (ORS) untuk kalkulasi rute yang fleksibel dan efisien. Optimalisasi performa pemuatan data dilakukan dengan memanfaatkan fitur caching Streamlit (`@st.cache_data`) pada proses parsing data JSON dan pemanggilan rute, serta menggunakan Leaflet MarkerCluster bawaan Folium untuk mereduksi beban render marker dalam jumlah besar.

- **Durasi** : 2 Minggu

- **Tingkat Kompleksitas** : 7/10

- **Status** : Completed / Under Development

- **Tipe Pengerjaan Project** : Solo
