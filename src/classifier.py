import os
import cv2
from skimage.feature import hog
from joblib import load


class Classifier:
    """
    Classe s'occupant de charger un modèle, et de classifier les images prises par l'utilisateur
    """
    def __init__(self):
        # Chargement des modèles
        model_path = "model.joblib"
        scaler_path = "scaler.joblib"
        assert os.path.exists(model_path), f"Model file not found at {model_path}"
        assert os.path.exists(scaler_path), f"Scaler file not found at {scaler_path}"

        self.model = load(model_path)
        self.scaler = load(scaler_path)

        # Mapping numbers to letters
        self.num_to_letter = {i: chr(65 + i) for i in range(26)}

    def preprocess_image(self, image_path, size=(28, 28)):
        """
        Traite l'image prise par l'utilisateur (la met en noir et blanc, à la bonne taille, et normalise les pixels)
        :param image_path: Chemin vers l'image à traiter
        :param size: taille de l'image
        :return: image au bon format
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        assert image is not None, f"Image file not found or invalid: {image_path}"

        # Recadrer et redimensionner l'image
        height, width = image.shape
        crop_size = min(height, width)
        start_x = (width - crop_size) // 2
        start_y = (height - crop_size) // 2
        cropped_image = image[start_y:start_y + crop_size, start_x:start_x + crop_size]
        resized_image = cv2.resize(cropped_image, size)

        # Normalisation entre 0 et 1
        normalized_image = resized_image / 255.0
        return normalized_image

    def extract_hog_features(self, image):
        # Extract HOG features for the preprocessed image
        features = hog(image, orientations=9, pixels_per_cell=(8, 8),
                       cells_per_block=(2, 2), block_norm='L2-Hys', transform_sqrt=True)
        return features

    def validate_image(self, image_path):
        """
        Fonction de validation de l'image
        :param image_path: image à classer
        :return: lettre désignée par l'image
        """
        # Preprocess the image and extract HOG features
        preprocessed_image = self.preprocess_image(image_path)
        hog_features = self.extract_hog_features(preprocessed_image)

        # Scale the features
        scaled_features = self.scaler.transform([hog_features])

        # Predict the label
        prediction = self.model.predict(scaled_features)[0]

        # Convert numeric prediction to letter
        predicted_letter = self.num_to_letter.get(prediction, "?")
        print(f"Numeric prediction: {prediction}, Letter prediction: {predicted_letter}")
        return predicted_letter
