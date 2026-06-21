import cv2
import numpy as np
from sklearn.decomposition import PCA


def compress_image(image_path, n_components=50, mode="RGB (Berwarna)"):

    # ==========================
    # MODE RGB
    # ==========================
    if mode == "RGB (Berwarna)":

        img = cv2.imread(image_path)

        img = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        channels = []

        total_compressed = 0

        for i in range(3):

            channel = img[:, :, i]

            comp = min(
                n_components,
                channel.shape[0],
                channel.shape[1]
            )

            pca = PCA(
                n_components=comp
            )

            transformed = pca.fit_transform(
                channel
            )

            reconstructed = pca.inverse_transform(
                transformed
            )

            reconstructed = np.clip(
                reconstructed,
                0,
                255
            ).astype(np.uint8)

            channels.append(
                reconstructed
            )

            total_compressed += transformed.nbytes

        compressed_img = np.dstack(
            channels
        )

        ratio = (
            total_compressed /
            img.nbytes
        ) * 100

        original_size = img.nbytes / 1024 / 1024
        compressed_size = total_compressed / 1024 / 1024

        return (
            img,
            compressed_img,
            ratio,
            original_size,
            compressed_size
        )

    # ==========================
    # MODE GRAYSCALE
    # ==========================
    else:

        img = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        comp = min(
            n_components,
            img.shape[0],
            img.shape[1]
        )

        pca = PCA(
            n_components=comp
        )

        transformed = pca.fit_transform(
            img
        )

        reconstructed = pca.inverse_transform(
            transformed
        )

        reconstructed = np.clip(
            reconstructed,
            0,
            255
        ).astype(np.uint8)

        ratio = (
            transformed.nbytes /
            img.nbytes
        ) * 100

        original_size = img.nbytes / 1024 / 1024
        compressed_size = transformed.nbytes / 1024 / 1024

        return (
            img,
            reconstructed,
            ratio,
            original_size,
            compressed_size
        )