import cv2
import numpy as np
from skimage.feature import hog
from joblib import load  # Pour charger le modèle SVM

# Charger le modèle SVM pré-entraîné
svm_model = load("../svm_hog_model.joblib")  # Remplacez par le chemin de votre modèle sauvegardé

# Paramètres HOG utilisés pendant l'entraînement
hog_params = {
    "orientations": 9,
    "pixels_per_cell": (8, 8),
    "cells_per_block": (2, 2),
    "block_norm": 'L2-Hys'
}

# Correspondance entre les indices des lettres et les lettres de l'alphabet
label_to_letter = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
    19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}

def preprocess_image(frame, size=(28, 28)):
    """Convertit une image en niveaux de gris et la redimensionne."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, size)
    return resized

def extract_hog_features(image):
    """Extrait les descripteurs HOG d'une image."""
    features = hog(image, **hog_params)
    return features

# Initialiser la caméra
cap = cv2.VideoCapture(0)  # 0 pour la webcam par défaut

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra.")
    exit()

print("Appuyez sur 'q' pour quitter.")

while True:
    ret, frame = cap.read()  # Lire une frame depuis la caméra
    if not ret:
        print("Erreur : Impossible de lire la vidéo.")
        break

    # Prétraiter la frame
    preprocessed_image = preprocess_image(frame)

    # Extraire les caractéristiques HOG
    hog_features = extract_hog_features(preprocessed_image).reshape(1, -1)

    # Prédire le label avec le modèle SVM
    prediction = svm_model.predict(hog_features)[0]

    # Convertir le numéro prédit en lettre
    predicted_letter = label_to_letter.get(prediction, "?")  # Retourne "?" si l'étiquette n'est pas dans le dictionnaire

    # Afficher la prédiction sur la vidéo
    cv2.putText(frame, f"Predicted Gesture: {predicted_letter}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Afficher la vidéo en temps réel
    cv2.imshow("Hand Gesture Detection", frame)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
