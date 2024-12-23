import numpy as np
from skimage.feature import hog
from joblib import dump
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import pandas as pd
from sklearn.metrics import  confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Charger les données
train_data = pd.read_csv("../data/dataset/sign_mnist_train.csv")
test_data = pd.read_csv("../data/dataset/sign_mnist_test.csv")

# Charger les données supplémentaires
custom_data = pd.read_csv("../data/custom_data.csv")

# Ajouter les données custom aux données d'entrainement
train_data = pd.concat([train_data, custom_data])


# Extraire les labels et les données d'image
y_train = train_data['label'].values
X_train = train_data.drop(['label'], axis=1).values

y_test = test_data['label'].values
X_test = test_data.drop(['label'], axis=1).values

# Prétraitement: Normaliser les valeurs de pixels (0 à 1)
X_train = X_train / 255.0
X_test = X_test / 255.0

# Redimensionner les images et calculer les descripteurs HOG
def extract_hog_features(images):
    hog_features = []
    for image in images:
        image_reshaped = image.reshape(28, 28)
        features = hog(image_reshaped, orientations=9, pixels_per_cell=(8, 8),
                       cells_per_block=(2, 2), block_norm='L2-Hys', transform_sqrt=True)
        hog_features.append(features)
    return np.array(hog_features)

print("Extraction des descripteurs HOG...")
X_train_hog = extract_hog_features(X_train)
X_test_hog = extract_hog_features(X_test)

# Mise à l'échelle des caractéristiques
scaler = StandardScaler()
X_train_hog_scaled = scaler.fit_transform(X_train_hog)
X_test_hog_scaled = scaler.transform(X_test_hog)

# Entraîner le modèle SVM
print("Entraînement du modèle SVM...")
model = SVC(kernel='rbf', probability=True, random_state=101)
model.fit(X_train_hog_scaled, y_train)

# Évaluer le modèle
print("Évaluation du modèle...")
y_pred = model.predict(X_test_hog_scaled)
print(classification_report(y_test, y_pred))

# Affichage de la matrice de confusion
conf_matrix = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :\n", conf_matrix)

# Visualisation de la matrice de confusion
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=np.unique(y_test))
disp.plot(cmap="Blues")
plt.show()


# Sauvegarder le modèle et le scaler
print("Sauvegarde du modèle et du scaler...")
dump(model, "model.joblib")
dump(scaler, "scaler.joblib")

print("Modèle et scaler sauvegardés avec succès.")