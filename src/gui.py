import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime
import random
import string
from classifier import Classifier

#print("Scikit-learn est correctement installé.")

class App:
    """
    Classe gérant l'interface graphique
    """
    def __init__(self, root, classifier):
        """
        Initialisation
        :param root: root tkinter
        :param classifier: classe gérant la classification des images
        """
        self.root = root
        self.root.title("Sign Language App")
        self.root.geometry("400x600")
        self.root.configure(bg="#335379")

        self.Classifier = classifier

        # Canvas pour le rendu graphique
        self.canvas = tk.Canvas(self.root, bg="#335379", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Rectangle pour le titre
        self.main_rectangle = self.create_rounded_rectangle(50, 50, 350, 150, radius=20, fill="white", outline="")
        self.canvas.create_text(200, 90, text="Sign the letter:", font=("Helvetica", 18, "bold"), fill="#1E1E2E")
        self.letter_text = self.canvas.create_text(200, 120, text="B", font=("Helvetica", 24, "bold"), fill="#1E1E2E")

        # Rectangle pour la webcam
        self.create_rounded_rectangle(50, 180, 350, 450, radius=20, fill="white", outline="")

        # Bouton "Verify"
        self.ok_button = ttk.Button(self.root, text="Verify", command=self.save_image_and_validate)
        self.ok_button.place(relx=0.5, rely=0.85, anchor="center")

        # Bouton "Change Letter"
        self.change_button = ttk.Button(self.root, text="Change Letter", command=self.change_letter)
        self.change_button.place(relx=0.7, rely=0.85, anchor="center")

        # Label pour le feedback
        self.feedback_label = tk.Label(self.root, font=("Helvetica", 14, "bold"), bg="#335379")

        # Initialisation webcam
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None
        self.current_letter = "Y"

        self.update_webcam()

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """
        Crée un rectangle aux coins arrondis qui sera affiché sur l'interface.

        :param x1: Coordonnée x du coin supérieur gauche du rectangle.
        :param y1: Coordonnée y du coin supérieur gauche du rectangle.
        :param x2: Coordonnée x du coin inférieur droit du rectangle.
        :param y2: Coordonnée y du coin inférieur droit du rectangle.
        :param radius: Rayon des coins arrondis (par défaut : 25).
        :param kwargs: Arguments supplémentaires passés à la méthode `create_polygon`
                       de tkinter, comme les couleurs ou le style de bordure.
        :return: L'identifiant de l'objet graphique créé par tkinter (entier).
        """
        points = [
            (x1 + radius, y1), (x2 - radius, y1),
            (x2, y1), (x2, y1 + radius),
            (x2, y2 - radius), (x2, y2),
            (x2 - radius, y2), (x1 + radius, y2),
            (x1, y2), (x1, y2 - radius),
            (x1, y1 + radius), (x1, y1)
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def update_webcam(self):
        """
        Met à jour l'affichage en temps réel de la webcam sur l'interface graphique.
        :return: None
        """
        # Capture une image depuis la webcam
        ret, frame = self.cap.read()
        if ret:
            # effet miroir horizontal
            frame = cv2.flip(frame, 1)
            self.current_frame = frame

            # Dessiner un rectangle pour indiquer la zone de capture
            height, width, _ = frame.shape
            x1, y1, x2, y2 = width // 3, height // 4, (2 * width) // 3, (3 * height) // 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Convertit l'image de BGR (format OpenCV) à RGB (format tkinter)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Redimensionne l'image pour s'adapter à l'espace d'affichage
            frame_resized = cv2.resize(frame_rgb, (280, 240))
            # Convertit l'image en un objet compatible tkinter
            image = ImageTk.PhotoImage(Image.fromarray(frame_resized))
            # Ajoute l'image au canvas et l'affiche à une position donnée
            self.canvas.image = image
            self.canvas.create_image(200, 315, image=image)

        # Relance la mise à jour toutes les 10 ms pour maintenir un flux vidéo
        self.root.after(10, self.update_webcam)

    """def save_image_and_validate(self):
        if self.current_frame is not None:
            # Sauvegarde et traitement de l'image
            height, width, _ = self.current_frame.shape
            x1, y1, x2, y2 = width // 3, height // 4, (2 * width) // 3, (3 * height) // 4
            cropped_frame = self.current_frame[y1:y2, x1:x2]

            save_dir = "../data/captures"
            os.makedirs(save_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(save_dir, f"capture_{self.current_letter}_{timestamp}.png")
            cv2.imwrite(file_path, cropped_frame)

            # Validation
            predicted_letter = self.Classifier.validate_image(file_path)
            print(f"Expected letter: {self.current_letter}")
            print(f"Predicted letter: {predicted_letter}")

            if predicted_letter == self.current_letter:
                self.show_feedback(f"Correct! {predicted_letter}", "green", self.change_letter)
            else:
                self.show_feedback(f"Incorrect: {predicted_letter}", "red")
    """

    def save_image_and_validate(self):
        """
        Capture une image de la webcam, la sauvegarde et la valide (ou non) en la classifiant
        :return:
        """
        if self.current_frame is not None:
            # Sauvegarde et traitement de l'image
            height, width, _ = self.current_frame.shape
            x1, y1, x2, y2 = width // 3, height // 4, (2 * width) // 3, (3 * height) // 4
            cropped_frame = self.current_frame[y1:y2, x1:x2]

            # Convertir en niveaux de gris
            gray_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            # Créer le dossier de sauvegarde si il n'existe pas
            save_dir = "../data/captures"
            os.makedirs(save_dir, exist_ok=True)

            # Donne un nom aléatoire unique à l'image (en fonction de la date) et la sauvegarde
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(save_dir, f"capture_{self.current_letter}_{timestamp}.png")
            cv2.imwrite(file_path, gray_frame)  # Enregistrer l'image en niveaux de gris

            # Validation
            predicted_letter = self.Classifier.validate_image(file_path)
            print(f"Expected letter: {self.current_letter}")
            print(f"Predicted letter: {predicted_letter}")

            # Feedback visuel pour l'utilisateur
            if predicted_letter == self.current_letter:
                self.show_feedback(f"Correct! {predicted_letter}", "green", self.change_letter)
            else:
                self.show_feedback(f"Incorrect: {predicted_letter}", "red")

    def show_feedback(self, message, color, callback=None):
        """
        Affichage d'un feedback sur l'interface
        :param message: stexte du msg à afficher
        :param color: couleur du msg
        :param callback: fonction à exécuter après avoir affiché le msg
        :return: None
        """
        self.feedback_label.config(text=message, foreground=color, bg="white")
        self.feedback_label.place(relx=0.5, rely=0.2, anchor="center")

        if callback:
            self.root.after(1000, lambda: [callback(), self.clear_feedback()])
        else:
            self.root.after(1000, self.clear_feedback)

    def clear_feedback(self):
        """
        Supprime le feedback affiché
        :return: None
        """
        self.feedback_label.place_forget()

    def change_letter(self):
        """
        Choisit une lettre au hasard en dehors des lettres J et Z (puisqu'on n'a pas d'image pour celles-là)
        :return: None
        """
        # Exclure les lettres 'J' et 'Z'
        excluded_letters = ['J', 'Z']
        available_letters = [letter for letter in string.ascii_uppercase if letter not in excluded_letters]
        new_letter = random.choice(available_letters)
        self.current_letter = new_letter
        self.canvas.itemconfig(self.letter_text, text=self.current_letter)


def start_app(Classifier):
    # Démarrage de l'application
    root=tk.Tk()
    app=App(root, Classifier)
    root.mainloop()

# Démarrage de l'application
if __name__ == "__main__":
    classifier = Classifier()
    root = tk.Tk()
    app = App(root, classifier)
    root.mainloop()
