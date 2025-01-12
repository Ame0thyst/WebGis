
##! gas lagii trial and error
import streamlit as st
import os
import folium
from streamlit_folium import st_folium
import json
import folium.plugins
from folium.plugins import Geocoder
from folium.plugins import Search
# from folium.plugins import LayerControl
from folium import LayerControl

st.set_page_config(layout="wide")

##? SCRIPT POP UP DAN NOTIF KALAU GA DITEMUKAN

def create_popup_content(title, description, image_path,address):
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
##?

##? LOAD DATASET
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
    locations = load_data_from_json("dataset.json")
##?

    # Fitur pencarian berdasarkan nama
    search_query = st.text_input("Cari lokasi berdasarkan nama:")
    
    # Filter lokasi berdasarkan pencarian
    if search_query:
        locations = [loc for loc in locations if search_query.lower() in loc["Nama"].lower()]
    
    # Dapatkan semua kategori unik
    categories = list(set(loc["Kategori"] for loc in locations))
    
    ##? INI SIDE BAR YGY
    st.sidebar.header("Filter Kategori")
    selected_categories = {}
    for category in categories:
        selected_categories[category] = st.sidebar.checkbox(category, True)
    
    ##? DEKLARASI LUAS FOLIUMNYA
    m = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
    Geocoder().add_to(m)

# Menampilkan peta
    
    
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
                loc["Gambar"],
                loc["Alamat"]
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
    # jalan_style = {
    #     'color': '#0000FF',
    #     'weight': 2,
    #     'opacity': 0.3
    # }
    # geojson_path = "static/layer/jalan.geojson"
    # if not os.path.exists(geojson_path):
    #     st.error(f"File {geojson_path} tidak ditemukan.")
    # else:
    #     folium.GeoJson(
    #         geojson_path,
    #         name='Jalur Jalan',
    #         style_function=lambda x: jalan_style
    # ).add_to(m)

    # folium.GeoJson(
    #     "static/layer/jalan.geojson",  # Sesuaikan dengan file GeoJSON Anda
    #     name='Jalur Jalan',
    #     style_function=lambda x: jalan_style
    # ).add_to(m)

    # Contoh menambahkan kawasan (GeoJSON)
    # kawasan_style = {
    #     'fillColor': '#FF0000',
    #     'color': '#FF0000',
    #     'weight': 1,
    #     'fillOpacity': 0.3
    # }
##! yang ini untuk layer wilayah / kawasan
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
        kecamatan_name = feature['properties']['Name']
        color = kecamatan_colors.get(kecamatan_name, "#CCCCCC")  # Default: abu-abu
        return {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.3,
        }
    with open("static/layer/wilayah.geojson") as f:
        geojson_data = json.load(f)

    geojson_layer = folium.GeoJson(
        geojson_data,
        name="wilayah",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["Name", "SHAPE_Leng", "SHAPE_Area"],  # Kolom atribut untuk tooltip
            aliases=["Kecamatan:", "Panjang:", "Luas:"], 
        # Label untuk tooltip
        ),
    zoom_on_click=True,
    ).add_to(m)

    # Tambahkan label (nama kecamatan)
    for feature in geojson_data["features"]:
        properties = feature["properties"]
        geometry = feature["geometry"]
        
        # Koordinat pusat label
        if geometry["type"] == "Polygon":
            coords = geometry["coordinates"][0]  # Ambil koordinat pertama dari Polygon
        elif geometry["type"] == "MultiPolygon":
            coords = geometry["coordinates"][0][0]  # Ambil koordinat pertama dari MultiPolygon
        else:
            continue

        centroid = [sum(x) / len(x) for x in zip(*coords)]
        
        # Tambahkan label sebagai marker
        folium.Marker(
            location=[centroid[1], centroid[0]],  # Folium membutuhkan format [lat, lon]
            icon=folium.DivIcon(
                html=f"""<div style="font-size: 10px; color: black;">{properties["Name"]}</div>"""
            ),
        
        ).add_to(m)

  
    folium.LayerControl().add_to(m)
    m.save("peta_kecamatan.html")
##!
   
    
    st_folium(m, height=500, width="100vw")
    
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