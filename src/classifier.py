import random

import cv2


class Classifier:
    def __init__(self):
        self.image = None
        self.model = None # charger le modèle à partir d'un modèle enregistré


    def validate_image(self, image_path):
        """Simule une validation d'image."""

        self.image = cv2.imread(image_path)
        cv2.imshow('image', self.image)  # afficher l'image

        # TODO

        return random.choice([True, False])  # Retourne aléatoirement True ou False

