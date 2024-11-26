import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime
import random
import string
from classifier import Classifier


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, tag=None, **kwargs):
    """Dessine un rectangle aux coins arrondis."""
    points = [
        (x1 + radius, y1), (x2 - radius, y1),
        (x2, y1), (x2, y1 + radius),
        (x2, y2 - radius), (x2, y2),
        (x2 - radius, y2), (x1 + radius, y2),
        (x1, y2), (x1, y2 - radius),
        (x1, y1 + radius), (x1, y1)
    ]
    return canvas.create_polygon(points, smooth=True, tag=tag, **kwargs)

class App:

    def __init__(self, root, classifier):
        # Configuration principale
        self.root = root
        self.root.title("Sign language app")
        self.root.geometry("400x600")
        self.root.configure(bg="#335379")  # Fond bleu foncé

        #Initialisation modules
        self.Classifier = classifier

        # Canvas pour dessiner les rectangles
        self.canvas = tk.Canvas(self.root, bg="#335379", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Rectangle pour le titre
        self.main_rectangle = create_rounded_rectangle(self.canvas, 50, 50, 350, 150, radius=20, tag="main_rectangle",
                                                  fill="white", outline="", width=4)
        self.canvas.create_text(200, 90, text="Sign the letter:", font=("Helvetica", 18, "bold"), fill="#1E1E2E")
        self.letter_text = self.canvas.create_text(200, 120, text="A", font=("Helvetica", 24, "bold"), fill="#1E1E2E")

        # Rectangle pour le flux de la webcam
        create_rounded_rectangle(self.canvas, 50, 180, 350, 450, radius=20, fill="white", outline="")

        # Bouton "OK"
        self.ok_button = ttk.Button(self.root, text="Verify", command=self.save_image_and_validate)
        self.ok_button.place(relx=0.5, rely=0.85, anchor="center")

        # Label pour les messages de feedback
        self.feedback_label = tk.Label(self.root, font=("Helvetica", 14, "bold"), bg="#1E1E2E")

        # Initialisation de la webcam
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None  # Stocke l'image actuelle
        self.current_letter = "A"  # Lettre actuelle affichée

        # Démarrer la mise à jour du flux webcam
        self.update_webcam()


    def update_webcam(self):
        """Capture une image depuis la webcam et l'affiche sur le Canvas."""
        global current_frame  # Stocke le frame actuel
        ret, frame = self.cap.read()  # Capture une image
        if ret:
            frame = cv2.flip(frame, 1)  # Applique un effet miroir horizontal
            current_frame = frame  # Stocke l'image pour l'enregistrement
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertit en RGB
            frame_resized = cv2.resize(frame_rgb, (280, 240))  # Ajuste à la taille du rectangle
            image = ImageTk.PhotoImage(Image.fromarray(frame_resized))
            self.canvas.image = image  # Garde une référence pour éviter le garbage collection
            self.canvas.create_image(200, 315, image=image)
        # Relance la mise à jour
        self.root.after(10, self.update_webcam)

    def save_image_and_validate(self):
        """Enregistre l'image actuelle, exécute la validation et met à jour l'interface."""
        if current_frame is not None:
            # Chemin du dossier où enregistrer les images
            save_dir = "captures"
            os.makedirs(save_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

            # Génère un nom de fichier unique avec horodatage
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(save_dir, f"capture_{self.current_letter}_{timestamp}.png")

            # Sauvegarde l'image
            cv2.imwrite(file_path, current_frame)
            print(f"Image enregistrée : {file_path}")

            # Appelle la fonction de validation
            is_valid = self.Classifier.validate_image(file_path)

            # Met à jour l'interface selon le résultat de la validation
            if is_valid:
                self.show_feedback("Success!", "green", self.change_letter)
            else:
                self.show_feedback("Try Again", "red")


    def show_feedback(self, message, color, callback=None):
        """
        Affiche un feedback temporaire et met à jour le contour.
        """
        # Met à jour le contour du rectangle principal
        self.canvas.itemconfig(self.main_rectangle, outline=color)

        # Affiche le message de feedback

        self.feedback_label.config(text=message, foreground=color, bg="white")
        self.feedback_label.place(relx=0.5, rely=0.2, anchor="center")


        if callback:  # Si une action doit être effectuée après le feedback
            self.root.after(1000, lambda: [callback(), self.clear_feedback()])
        else:  # Si aucun callback, efface le feedback
            self.root.after(1000, self.clear_feedback)

    def clear_feedback(self, ):
        """Efface le feedback et réinitialise le contour."""
        self.canvas.itemconfig(self.main_rectangle, outline="")
        self.feedback_label.place_forget()

    def change_letter(self):
        """Change la lettre demandée pour une autre lettre aléatoire."""
        new_letter = random.choice(string.ascii_uppercase)  # Choisit une lettre aléatoire
        while new_letter == self.current_letter:  # Évite de répéter la même lettre
            new_letter = random.choice(string.ascii_uppercase)
        self.current_letter = new_letter
        self.canvas.itemconfig(self.letter_text, text=self.current_letter)


# Fonction de démarrage
def start_app(classifier):
    root = tk.Tk()
    app = App(root, classifier)
    root.protocol("WM_DELETE_WINDOW")
    root.mainloop()

if __name__ == "__main__":
    Classifier = Classifier()
    start_app(Classifier)
