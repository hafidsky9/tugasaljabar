import cv2
import numpy as np

def preprocess_image(path, size=100):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    min_side = min(h, w)
    start_x = (w - min_side) // 2
    start_y = (h - min_side) // 2
    cropped = gray[start_y:start_y+min_side, start_x:start_x+min_side]

    resized = cv2.resize(cropped, (size, size))
    normalized = resized / 255.0
    flattened = normalized.flatten()

    return flattened
