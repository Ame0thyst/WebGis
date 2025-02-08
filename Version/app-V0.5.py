import streamlit as st
import os
import folium
from streamlit_folium import st_folium
import json
import folium.plugins
from folium.plugins import Geocoder, MousePosition, MiniMap, MarkerCluster
from folium.plugins import Search
from folium import LayerControl

st.set_page_config(layout="wide")

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

@st.cache_data
def load_data_from_json(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        st.error(f"Error loading data from JSON: {e}")
        return []

def main():
    st.title("Peta Lokasi dengan Gambar")
    locations = load_data_from_json("dataset.json")

    search_query = st.text_input("Cari lokasi berdasarkan nama:")
    
    if search_query:
        locations = [loc for loc in locations if search_query.lower() in loc["Nama"].lower()]
    
    categories = list(set(loc["Kategori"] for loc in locations))
    
    st.sidebar.header("Filter Kategori")
    selected_categories = {}
    for category in categories:
        selected_categories[category] = st.sidebar.checkbox(category, True)
    
    m = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
    Geocoder().add_to(m)
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite'
    ).add_to(m)
    
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
    
    # Create marker clusters for each category
    marker_clusters = {}
    for category in categories:
        marker_clusters[category] = MarkerCluster(
            name=category,
            overlay=True,
            control=True,
            options={
                'maxClusterRadius': 50,  # Radius maksimum cluster dalam pixels
                'disableClusteringAtZoom': 16,  # Zoom level dimana clustering dinonaktifkan
                'spiderfyOnMaxZoom': True,  # Membuat marker menyebar saat max zoom
                'showCoverageOnHover': True,  # Menampilkan area coverage cluster saat hover
                'zoomToBoundsOnClick': True,  # Zoom ke batas cluster saat diklik
                'animate': True
            })
        
        marker_clusters[category].add_to(m)
    
    # Add markers to appropriate clusters
    for loc in locations:
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
            
            # Add marker to its category cluster
            marker_clusters[loc["Kategori"]].add_child(marker)

    # Add GeoJSON layer for regions
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
        color = kecamatan_colors.get(kecamatan_name, "#CCCCCC")
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
            fields=["Name", "SHAPE_Leng", "SHAPE_Area"],
            aliases=["Kecamatan:", "Panjang:", "Luas:"],
        ),
        zoom_on_click=True,
    ).add_to(m)

    # Add kecamatan labels
    for feature in geojson_data["features"]:
        properties = feature["properties"]
        geometry = feature["geometry"]
        
        if geometry["type"] == "Polygon":
            coords = geometry["coordinates"][0]
        elif geometry["type"] == "MultiPolygon":
            coords = geometry["coordinates"][0][0]
        else:
            continue

        centroid = [sum(x) / len(x) for x in zip(*coords)]
        
        folium.Marker(
            location=[centroid[1], centroid[0]],
            icon=folium.DivIcon(
                html=f"""<div style="font-size: 10px; color: black;">{properties["Name"]}</div>"""
            ),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save("peta_kecamatan.html")
    
    st_folium(m, height=500, width="100vw")
    
    st.sidebar.header("Informasi Lokasi")
    for loc in locations:
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