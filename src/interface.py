import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime
import random
import string

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

def update_webcam():
    """Capture une image depuis la webcam et l'affiche sur le Canvas."""
    global current_frame  # Stocke le frame actuel
    ret, frame = cap.read()  # Capture une image
    if ret:
        frame = cv2.flip(frame, 1)  # Applique un effet miroir horizontal
        current_frame = frame  # Stocke l'image pour l'enregistrement
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertit en RGB
        frame_resized = cv2.resize(frame_rgb, (280, 240))  # Ajuste à la taille du rectangle
        image = ImageTk.PhotoImage(Image.fromarray(frame_resized))
        canvas.image = image  # Garde une référence pour éviter le garbage collection
        canvas.create_image(200, 315, image=image)
    # Relance la mise à jour
    root.after(10, update_webcam)

def save_image_and_validate():
    """Enregistre l'image actuelle, exécute la validation et met à jour l'interface."""
    if current_frame is not None:
        # Chemin du dossier où enregistrer les images
        save_dir = "captures"
        os.makedirs(save_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

        # Génère un nom de fichier unique avec horodatage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(save_dir, f"capture_{current_letter}_{timestamp}.png")

        # Sauvegarde l'image
        cv2.imwrite(file_path, current_frame)
        print(f"Image enregistrée : {file_path}")

        # Appelle la fonction de validation (à définir par l'utilisateur)
        is_valid = validate_image(file_path)

        # Met à jour l'interface selon le résultat de la validation
        if is_valid:
            show_feedback("Success!", "green", change_letter)
        else:
            show_feedback("Try Again", "red")

def validate_image(image_path):
    """
    Simule une validation sur l'image.
    Remplacez par votre logique.
    """
    return random.choice([True, False])  # Retourne aléatoirement vrai ou faux

def show_feedback(message, color, callback=None):
    """
    Affiche un feedback temporaire et met à jour le contour.
    """
    # Met à jour le contour du rectangle principal
    canvas.itemconfig(main_rectangle, outline=color)

    # Affiche le message de feedback

    feedback_label.config(text=message, foreground=color, bg="white")
    feedback_label.place(relx=0.5, rely=0.2, anchor="center")


    if callback:  # Si une action doit être effectuée après le feedback
        root.after(1000, lambda: [callback(), clear_feedback()])
    else:  # Si aucun callback, efface le feedback
        root.after(1000, clear_feedback)

def clear_feedback():
    """Efface le feedback et réinitialise le contour."""
    canvas.itemconfig(main_rectangle, outline="")
    feedback_label.place_forget()

def change_letter():
    """Change la lettre demandée pour une autre lettre aléatoire."""
    global current_letter
    new_letter = random.choice(string.ascii_uppercase)  # Choisit une lettre aléatoire
    while new_letter == current_letter:  # Évite de répéter la même lettre
        new_letter = random.choice(string.ascii_uppercase)
    current_letter = new_letter
    canvas.itemconfig(letter_text, text=current_letter)

# Configuration principale
root = tk.Tk()
root.title("Sign language app")
root.geometry("400x600")
root.configure(bg="#335379")  # Fond bleu foncé

# Canvas pour dessiner les rectangles
canvas = tk.Canvas(root, bg="#335379", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Rectangle pour le titre
main_rectangle = create_rounded_rectangle(canvas, 50, 50, 350, 150, radius=20, tag="main_rectangle", fill="white", outline="", width=4)
canvas.create_text(200, 90, text="Sign the letter:", font=("Helvetica", 18, "bold"), fill="#1E1E2E")
letter_text = canvas.create_text(200, 120, text="A", font=("Helvetica", 24, "bold"), fill="#1E1E2E")

# Rectangle pour le flux de la webcam
create_rounded_rectangle(canvas, 50, 180, 350, 450, radius=20, fill="white", outline="")

# Bouton "OK"
ok_button = ttk.Button(root, text="Verify", command=save_image_and_validate)
ok_button.place(relx=0.5, rely=0.85, anchor="center")

# Label pour les messages de feedback
feedback_label = tk.Label(root, font=("Helvetica", 14, "bold"), bg="#1E1E2E")

# Initialisation de la webcam
cap = cv2.VideoCapture(0)
current_frame = None  # Stocke l'image actuelle
current_letter = "A"  # Lettre actuelle affichée

# Démarrer la mise à jour du flux webcam
update_webcam()

# Quitter proprement l'application
def on_close():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Lancer l'interface
root.mainloop()
