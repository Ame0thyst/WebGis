import streamlit as st

def display_sidebar(filtered_locations, selected_categories):
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