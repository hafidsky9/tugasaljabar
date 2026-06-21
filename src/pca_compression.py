import cv2
import numpy as np
from sklearn.decomposition import PCA

def compress_image(image_path, n_components=50):

    # Baca gambar grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Gambar tidak ditemukan")

    # PCA
    pca = PCA(n_components=n_components)

    transformed = pca.fit_transform(img)

    reconstructed = pca.inverse_transform(transformed)

    reconstructed = np.clip(
        reconstructed,
        0,
        255
    ).astype(np.uint8)

    # ukuran data
    original_size = img.nbytes
    compressed_size = transformed.nbytes

    compression_ratio = (
        compressed_size / original_size
    ) * 100

    return (
        img,
        reconstructed,
        compression_ratio
    )