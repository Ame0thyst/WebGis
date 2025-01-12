
# ##! gas lagii trial and error
import streamlit as st
import os
import folium
from streamlit_folium import st_folium
import json
import folium.plugins
from folium.plugins import Geocoder, MousePosition, MiniMap
from folium.plugins import Search
from folium import LayerControl

st.set_page_config(layout="wide")


##? SCRIPT POP UP DAN NOTIF KALAU GA DITEMUKAN
@st.cache_data
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
@st.cache_data
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
                    
                    st.image(loc["Gambar"], caption=loc["Nama"],  use_container_width=True)
                except Exception as e:
                    st.error("Gambar tidak dapat dimuat")

if __name__ == "__main__":
    main()

###!! DANGERRR !!!
# import streamlit as st
# import os
# import folium
# from streamlit_folium import st_folium
# import json
# import folium.plugins
# from folium.plugins import Geocoder, MousePosition, MiniMap
# from folium.plugins import Search
# from folium import LayerControl

# st.set_page_config(layout="wide")

# @st.cache_data
# def create_popup_content(title, description, image_path, address):
#     try:
#         return f"""
#             <div style="width:300px; padding:10px;">
#                 <h3 style="color:#1f77b4;">{title}</h3>
#                 <p>{description}</p>
#                 <img src="{image_path}" style="width:100%; margin-top:10px; border-radius:5px;">
#                 <p>{address}</p>
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

# @st.cache_data
# def load_data_from_json(json_file):
#     try:
#         with open(json_file, "r") as file:
#             data = json.load(file)
#         return data
#     except Exception as e:
#         st.error(f"Error loading data from JSON: {e}")
#         return []

# @st.cache_data
# def load_geojson():
#     with open("static/layer/wilayah.geojson") as f:
#         return json.load(f)

# @st.cache_data
# def get_kecamatan_colors():
#     return {
#         "BANDARSEIKIJANG": "#FF5733",
#         "BUKITRAYA": "#33FF57",
#         "KAMPARKIRI HILIR": "#3357FF",
#         "KAMPARKIRI TENGAH": "#FF33A1",
#         "KERINCIKANAN": "#F4A460",
#         "KOTOGASIB": "#6A5ACD",
#         "LANGGAM": "#FF4500",
#         "LIMAPULUH": "#7FFF00",
#         "LUBUKDALAM": "#FF6347",
#         "MARPOYANDAMAI": "#4682B4",
#         "MINAS": "#B22222",
#         "PAYUNGSEKAKI": "#ADFF2F",
#         "PEKANBARUKOTA": "#FF69B4",
#         "PERHENTIANRAJA": "#5F9EA0",
#         "RUMBAI": "#FFD700",
#         "RUMBAIPESISIR": "#6495ED",
#         "SAIL": "#DC143C",
#         "SENAPELAN": "#7B68EE",
#         "SIAK HULU": "#008080",
#         "SUKAJADI": "#DA70D6",
#         "TAMBANG": "#EE82EE",
#         "TAMPAN": "#00FA9A",
#         "TAPUNG": "#FFA500",
#         "TAPUNG HILIR": "#D2691E",
#         "TENAYANRAYA": "#1E90FF",
#         "TUALANG": "#32CD32",
#     }

# def main():
#     st.title("Peta Lokasi dengan Gambar")

#     # Load data
#     locations = load_data_from_json("dataset.json")
    
#     # Search functionality
#     search_query = st.text_input("Cari lokasi berdasarkan nama:")
    
#     # Filter locations based on search
#     if search_query:
#         locations = [loc for loc in locations if search_query.lower() in loc["Nama"].lower()]
    
#     # Get unique categories
#     categories = list(set(loc["Kategori"] for loc in locations))
    
#     # Sidebar filters
#     st.sidebar.header("Filter Kategori")
#     selected_categories = {
#         category: st.sidebar.checkbox(category, True) 
#         for category in categories
#     }

#     # Initialize map
#     m = folium.Map(location=[0.5071, 101.4478], zoom_start=9)
    
#     # Add base features
#     Geocoder().add_to(m)
#     folium.TileLayer(
#         tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#         attr='Esri',
#         name='Esri Satellite'
#     ).add_to(m)
    
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
    
#     MiniMap().add_to(m)
    
#     # Create feature groups for categories
#     feature_groups = {}
#     for category in categories:
#         feature_groups[category] = folium.FeatureGroup(name=category)
    
#     # Add markers in batches
#     BATCH_SIZE = 10
#     visible_locations = [
#         loc for loc in locations 
#         if selected_categories.get(loc["Kategori"], True)
#     ]
    
#     for i in range(0, len(visible_locations), BATCH_SIZE):
#         batch = visible_locations[i:i + BATCH_SIZE]
#         for loc in batch:
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
#             feature_groups[loc["Kategori"]].add_child(marker)
    
#     # Add feature groups to map
#     for fg in feature_groups.values():
#         fg.add_to(m)

#     # Add GeoJSON data
#     geojson_data = load_geojson()
#     kecamatan_colors = get_kecamatan_colors()
    
#     def style_function(feature):
#         kecamatan_name = feature['properties']['Name']
#         color = kecamatan_colors.get(kecamatan_name, "#CCCCCC")
#         return {
#             'fillColor': color,
#             'color': 'black',
#             'weight': 1,
#             'fillOpacity': 0.3,
#         }
    
#     geojson_layer = folium.GeoJson(
#         geojson_data,
#         name="wilayah",
#         style_function=style_function,
#         tooltip=folium.GeoJsonTooltip(
#             fields=["Name", "SHAPE_Leng", "SHAPE_Area"],
#             aliases=["Kecamatan:", "Panjang:", "Luas:"],
#         ),
#         zoom_on_click=True,
#     ).add_to(m)

#     # Add kecamatan labels
#     for feature in geojson_data["features"]:
#         properties = feature["properties"]
#         geometry = feature["geometry"]
        
#         if geometry["type"] == "Polygon":
#             coords = geometry["coordinates"][0]
#         elif geometry["type"] == "MultiPolygon":
#             coords = geometry["coordinates"][0][0]
#         else:
#             continue

#         centroid = [sum(x) / len(x) for x in zip(*coords)]
        
#         folium.Marker(
#             location=[centroid[1], centroid[0]],
#             icon=folium.DivIcon(
#                 html=f"""<div style="font-size: 10px; color: black;">{properties["Name"]}</div>"""
#             ),
#         ).add_to(m)

#     folium.LayerControl().add_to(m)
    
#     # Display map
#     st_folium(m, height=500, width="100vw", key="map")
    
#     # Display sidebar information
#     st.sidebar.header("Informasi Lokasi")
#     for loc in visible_locations:
#         with st.sidebar.expander(loc["Nama"]):
#             st.write(f"**Kategori**: {loc['Kategori']}")
#             st.write(f"**Alamat**: {loc['Alamat']}")
#             st.write(loc["Deskripsi"])
#             try:
#                 st.image(loc["Gambar"], caption=loc["Nama"], use_container_width=True)
#             except Exception as e:
#                 st.error("Gambar tidak dapat dimuat")

# if __name__ == "__main__":
#     main()