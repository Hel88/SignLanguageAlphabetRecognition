import classifier
import cv2
import os
import csv

def matrix_to_list(matrix):
    list=[]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            list.append(matrix[i][j])
    return list


def preprocess_image(image_path, size=(28, 28)):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    assert image is not None, f"Image file not found or invalid: {image_path}"

    # Recadrer et redimensionner l'image
    height, width = image.shape
    crop_size = min(height, width)
    start_x = (width - crop_size) // 2
    start_y = (height - crop_size) // 2
    cropped_image = image[start_y:start_y + crop_size, start_x:start_x + crop_size]
    resized_image = cv2.resize(cropped_image, size)
    return resized_image

# Prend chaque image du dossier captures et l'ajoute comme donnée au fichier  custom_data.csv

images_file_path = "../data/captures/"
new_data = []
for image_path in os.listdir(images_file_path):
    label = image_path.split("_")[1]
    label = ord(label.upper()) - ord('A') # récupérer numero correspondant à la lettre
    preprocessed_image = preprocess_image(images_file_path+image_path)
    preprocessed_image = matrix_to_list(preprocessed_image)
    preprocessed_image.insert(0, label)
    new_data.append(preprocessed_image)


print(new_data)
# open csv
csv_path = "../data/custom_data.csv"
with open(csv_path, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(new_data)


# Récupérer le nombre d'instances pour chaque label
label_counts = {}

with open(csv_path, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if row:  # Vérifier si la ligne n'est pas vide
            label = int(row[0])  # Le label est la première colonne
            if label not in label_counts:
                label_counts[label] = 0
            label_counts[label] += 1

# Afficher les résultats
print("Nombre d'instances par lettre :")
for label in sorted(label_counts.keys()):
    print(f"Lettre {label} : {label_counts[label]} instances")
