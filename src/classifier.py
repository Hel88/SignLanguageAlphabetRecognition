import os
import cv2
import numpy as np
from skimage.feature import hog
from joblib import load


class Classifier:
    def __init__(self):
        model_path = "svm_hog_model.joblib"
        scaler_path = "scaler.joblib"
        assert os.path.exists(model_path), f"Model file not found at {model_path}"
        assert os.path.exists(scaler_path), f"Scaler file not found at {scaler_path}"

        self.model = load(model_path)
        self.scaler = load(scaler_path)

        # Mapping numbers to letters
        self.num_to_letter = {i: chr(65 + i) for i in range(26)}

    """def preprocess_image(self, image_path, size=(28, 28)):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        assert image is not None, f"Image file not found or invalid: {image_path}"

        # Crop and resize the image
        height, width = image.shape
        crop_size = min(height, width)
        start_x = (width - crop_size) // 2
        start_y = (height - crop_size) // 2
        cropped_image = image[start_y:start_y + crop_size, start_x:start_x + crop_size]
        resized_image = cv2.resize(cropped_image, size)
        return resized_image
"""

    def preprocess_image(self, image_path, size=(28, 28)):
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
