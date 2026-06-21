import streamlit as st
import os
from main import compare_faces

st.set_page_config(
    page_title="Face Similarity Detection",
    layout="wide"
)

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

.upload-card{
    border:2px dashed #2563eb;
    border-radius:15px;
    padding:20px;
    text-align:center;
    background:#f8fbff;
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

st.markdown(
    '<div class="title">Face Similarity Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Perbandingan Foto Masa Kecil dan Dewasa Menggunakan PCA</div>',
    unsafe_allow_html=True
)

os.makedirs("uploads", exist_ok=True)

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

    path1 = os.path.join("uploads", "foto_kecil.jpg")
    path2 = os.path.join("uploads", "foto_dewasa.jpg")

    with open(path1, "wb") as f:
        f.write(foto1.getbuffer())

    with open(path2, "wb") as f:
        f.write(foto2.getbuffer())

    st.image([path1, path2], width=250)

    if st.button("Bandingkan Wajah"):

        sim, result = compare_faces(path1, path2)

        persen = sim * 100

        st.subheader("Hasil Analisis")

        st.metric(
            "Tingkat Kemiripan",
            f"{persen:.2f}%"
        )

        st.progress(min(int(persen), 100))

        if "Mirip" in result:
            st.success(result)
        else:
            st.error(result)