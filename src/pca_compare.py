import joblib
import numpy as np
from dataset_loader import preprocess_image

pca = joblib.load("pca_model.pkl")

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2.T)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    sim = dot / (norm1 * norm2)
    return float(sim.squeeze())

def compare_faces(path1, path2, threshold=0.85):
    foto1 = preprocess_image(path1, size=100)
    foto2 = preprocess_image(path2, size=100)

    proj1 = pca.transform([foto1])
    proj2 = pca.transform([foto2])

    sim = cosine_similarity(proj1, proj2)

    result = "Mirip ✅" if sim >= threshold else "Tidak mirip ❌"

    return sim, result


if __name__ == "__main__":

    pairs = [
        ("test/ZK.JPG", "test/kecil.jpeg")
    ]

    print("=== Hasil Uji Batch ===")

    for f1, f2 in pairs:
        try:
            sim, result = compare_faces(f1, f2)
            print(f"{f1} vs {f2} -> {sim:.4f} | {result}")
        except Exception as e:
            print(f"Error pada {f1} vs {f2}: {e}")
