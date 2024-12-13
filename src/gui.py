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
        self.root.geometry("730x680")  # taille de la fenetre
        self.root.configure(bg="#335379")

        self.Classifier = classifier
        self.current_frame = None
        self.current_letter = "Y"

        # Diviser la fenetre principale en 2
        self.left_frame = tk.Frame(self.root, width=300, bg="#F0F0F0")
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = tk.Frame(self.root, bg="#335379")
        self.right_frame.pack(side="right", fill="both", expand=True)

        # interface de gauche (choix des lettres)
        self.create_left_panel()

        # Interface de droite (exercice)
        self.canvas = tk.Canvas(self.right_frame, bg="#335379", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.letter_text = self.canvas.create_text(200, 90, text="", font=("Helvetica", 24, "bold"), fill="white")

        # # Canvas pour le rendu graphique
        # self.canvas = tk.Canvas(self.root, bg="#335379", highlightthickness=0)
        # self.canvas.pack(fill="both", expand=True)

        # Rectangle pour le titre
        self.main_rectangle = self.create_rounded_rectangle(50, 50, 350, 150, radius=20, fill="white", outline="")
        self.title_text = self.canvas.create_text(200, 90, text="", font=("Helvetica", 18, "bold"), fill="#1E1E2E")
        self.letter_text = self.canvas.create_text(200, 120, text="", font=("Helvetica", 24, "bold"), fill="#1E1E2E")

        # Rectangle pour la webcam
        self.create_rounded_rectangle(50, 180, 350, 450, radius=20, fill="white", outline="")


        # Bouton "Verify"
        self.ok_button = ttk.Button(self.right_frame, text="Verify", command=self.save_image_and_validate)
        self.ok_button.place(relx=0.3, rely=0.85, anchor="center")

        # Bouton "Change Letter"
        self.change_button = ttk.Button(self.right_frame, text="Change Letter", command=self.change_letter)
        self.change_button.place(relx=0.5, rely=0.85, anchor="center")

        # Bouton pour afficher une image d'aide
        self.show_image_button = ttk.Button(self.right_frame, text="Help",
                                            command=lambda: self.show_image_window("../data/dataset/amer_sign2.png"))
        #self.show_image_button.pack(side="bottom", pady=10)
        self.show_image_button.place(relx=0.7, rely=0.85, anchor="center")


        # Label pour le feedback
        self.feedback_label = tk.Label(self.root, font=("Helvetica", 14, "bold"), bg="#335379")

        # Initialisation webcam
        self.cap = cv2.VideoCapture(0)
        self.update_webcam()

    def show_image_window(self, image_path):
        """Affiche une fenêtre contenant une image (le guide de language des signes) avec une croix pour la fermer."""
        # Créer une fenêtre secondaire
        image_window = tk.Toplevel(self.root)
        image_window.title("Image Viewer")
        image_window.geometry("500x400")
        image_window.configure(bg="#335379")

        # Charger et afficher l'image
        image = Image.open(image_path)
        image = image.resize((400, 300))  # Redimensionner l'image pour s'adapter
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(image_window, image=photo, bg="#335379")
        label.image = photo  # Conserver une référence pour éviter le garbage collection
        label.pack(pady=10)

        # Bouton pour fermer la fenêtre
        close_button = ttk.Button(image_window, text="Fermer", command=image_window.destroy)
        close_button.pack(pady=10)

    def create_left_panel(self):
        """Crée l'interface à gauche pour choisir les lettres et lancer l'exercice."""
        tk.Label(self.left_frame, text="Choose the letters you want to learn :", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=10)

        # Cases à cocher pour chaque lettre
        self.letter_vars = {}
        for letter in string.ascii_uppercase:
            if (letter != 'J') and (letter != 'Z'):
                var = tk.BooleanVar()
                chk = ttk.Checkbutton(self.left_frame, text=letter, variable=var)
                chk.pack(anchor="w", padx=10)
                self.letter_vars[letter] = var

        # Bouton pour démarrer l'exercice
        self.start_button = ttk.Button(self.left_frame, text="Start training", command=self.start_exercise)
        self.start_button.pack(pady=20)

    def start_exercise(self):
        """Démarre l'exercice avec les lettres sélectionnées."""
        self.letters_to_learn = [letter for letter, var in self.letter_vars.items() if var.get()]
        self.title_text = self.canvas.create_text(200, 90, text="Sign the letter:", font=("Helvetica", 18, "bold"), fill="#1E1E2E")

        if not self.letters_to_learn:
            self.show_feedback("Select at least one letter.", "red")
        else:
            self.change_letter()

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
            aspect_ratio = width / height
            x1, y1, x2, y2 = width // 3, height // 4, (2 * width) // 3, (3 * height) // 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Fixer une largeur ou une hauteur cible
            target_width = 280  # Par exemple, largeur souhaitée
            target_height = int(target_width / aspect_ratio)

            # Convertit l'image de BGR (format OpenCV) à RGB (format tkinter)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Redimensionner en gardant les proportions
            frame_resized = cv2.resize(frame_rgb, (target_width, target_height))
            # Convertit l'image en un objet compatible tkinter
            image = ImageTk.PhotoImage(Image.fromarray(frame_resized))
            # Ajoute l'image au canvas et l'affiche à une position donnée
            self.canvas.image = image
            self.canvas.create_image(200, 315, image=image)

        # Relance la mise à jour toutes les 10 ms pour maintenir un flux vidéo
        self.root.after(10, self.update_webcam)

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
        self.feedback_label.place(relx=0.7, rely=0.7, anchor="center")

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
        """Change la lettre à apprendre aléatoirement parmi les lettres sélectionnées."""
        if self.letters_to_learn:
            self.current_letter = random.choice(self.letters_to_learn)
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
