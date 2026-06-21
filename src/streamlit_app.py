import streamlit as st
import os
from main import compare_faces
from pca_compression import compress_image

st.set_page_config(
    page_title="PCA Application",
    layout="wide"
)

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title{
    text-align:center;
    color:#1f2937;
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#6b7280;
    margin-bottom:30px;
}

.stButton > button{
    width:100%;
    height:55px;
    font-size:18px;
    border-radius:10px;
    background:#2563eb;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# Sidebar
# ==========================

menu = st.sidebar.radio(
    "Pilih Fitur",
    [
        "Deteksi Kemiripan Wajah",
        "Kompresi Gambar PCA"
    ]
)

os.makedirs("uploads", exist_ok=True)

# ==========================
# MENU 1
# ==========================

if menu == "Deteksi Kemiripan Wajah":

    st.markdown(
        '<div class="title">Face Similarity Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Perbandingan Foto Masa Kecil dan Dewasa Menggunakan PCA</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Foto Masa Kecil")

        foto1 = st.file_uploader(
            "Upload Foto Masa Kecil",
            type=["jpg", "jpeg", "png"],
            key="foto1"
        )

    with col2:
        st.markdown("### Foto Masa Dewasa")

        foto2 = st.file_uploader(
            "Upload Foto Masa Dewasa",
            type=["jpg", "jpeg", "png"],
            key="foto2"
        )

    if foto1 and foto2:

        path1 = os.path.join(
            "uploads",
            "foto_kecil.jpg"
        )

        path2 = os.path.join(
            "uploads",
            "foto_dewasa.jpg"
        )

        with open(path1, "wb") as f:
            f.write(foto1.getbuffer())

        with open(path2, "wb") as f:
            f.write(foto2.getbuffer())

        st.image(
            [path1, path2],
            width=250
        )

        if st.button("Bandingkan Wajah"):

            sim, result = compare_faces(
                path1,
                path2
            )

            persen = sim * 100

            st.subheader(
                "Hasil Analisis"
            )

            st.metric(
                "Tingkat Kemiripan",
                f"{persen:.2f}%"
            )

            st.progress(
                min(
                    int(persen),
                    100
                )
            )

            if "Mirip" in result:
                st.success(result)
            else:
                st.error(result)

# ==========================
# MENU 2
# ==========================

elif menu == "Kompresi Gambar PCA":

        st.markdown(
    '<div class="title">Kompresi Gambar PCA</div>',
    unsafe_allow_html=True
        )   

uploaded = st.file_uploader(
    "Upload Gambar",
    type=["jpg", "jpeg", "png"],
    key="compress"
)

mode = st.radio(
    "Mode Kompresi",
    [
        "RGB (Berwarna)",
        "Grayscale"
    ]
)

komponen = st.slider(
    "Jumlah Komponen PCA",
    min_value=10,
    max_value=200,
    value=50
)

if uploaded:

    path = os.path.join(
        "uploads",
        uploaded.name
    )

    with open(path, "wb") as f:
        f.write(uploaded.getbuffer())

    if st.button("🗜️ Kompres Gambar"):

        original, compressed, ratio, original_size, compressed_size = compress_image(
            path,
            komponen,
            mode
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original")
            st.image(
                original,
                use_container_width=True
            )

            st.info(
                f"Ukuran : {original_size:.2f} MB\n\n"
                f"Resolusi : {original.shape[1]} x {original.shape[0]}"
            )

        with col2:
            st.subheader("Hasil PCA")
            st.image(
                compressed,
                use_container_width=True
            )

            st.info(
                f"Ukuran : {compressed_size:.2f} MB\n\n"
                f"Resolusi : {compressed.shape[1]} x {compressed.shape[0]}"
            )

        st.divider()

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric(
                "Ukuran Awal",
                f"{original_size:.2f} MB"
            )

        with colB:
            st.metric(
                "Ukuran PCA",
                f"{compressed_size:.2f} MB"
            )

        with colC:
            st.metric(
                "Rasio Kompresi",
                f"{ratio:.2f}%"
            )
