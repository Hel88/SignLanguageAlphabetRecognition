"""Modèle CNN ( vf )
    chiant et résulats un peu meilleur que svm mais bon . . .
"""
import pandas as pd
import numpy as np
from sklearn.utils import compute_class_weight
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report

# Charger les données
train_data = pd.read_csv("../data/dataset/sign_mnist_train.csv")
test_data = pd.read_csv("../data/dataset/sign_mnist_test.csv")

# Extraire les labels et les données d'image
y_train = train_data['label'].values
X_train = train_data.drop(['label'], axis=1).values

y_test = test_data['label'].values
X_test = test_data.drop(['label'], axis=1).values

# Prétraitement: Normaliser les valeurs de pixels (0 à 1)
X_train = X_train / 255.0
X_test = X_test / 255.0

# Redimensionner les images pour qu'elles soient en 28x28x1 (format attendu par Conv2D)
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# Conversion des labels en one-hot encoding
num_classes = 26
y_train = np.eye(num_classes)[y_train]  # Convertit les indices de classes en one-hot
y_test = np.eye(num_classes)[y_test]



# Définir le modèle CNN
model = Sequential([
    Conv2D(75, 3, activation="relu", strides=1, padding='same', input_shape=(28, 28, 1)),
    BatchNormalization(),
    MaxPool2D(strides=2, padding='same'),
    Conv2D(50, 3, activation="relu", strides=1, padding='same'),
    Dropout(0.5),
    BatchNormalization(),
    MaxPool2D(strides=2, padding='same'),
    Conv2D(25, 3, activation="relu", strides=1, padding='same'),
    BatchNormalization(),
    MaxPool2D(strides=2, padding='same'),
    Flatten(),
    Dense(512, activation="relu"),
    Dropout(0.5),
    Dense(26, activation="softmax")  # 26 sorties correspondant aux lettres de l'alphabet
])

# Compiler le modèle
model.compile(loss="categorical_crossentropy", optimizer=Adam(), metrics=["accuracy"])

# Afficher un résumé du modèle
model.summary()

# Calculer les poids des classes
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train.argmax(axis=1)),
    y=y_train.argmax(axis=1)
)
class_weights_dict = dict(enumerate(class_weights))

# Entraîner le modèle avec des poids de classe
history = model.fit(
    X_train, y_train,
    batch_size=64,
    epochs=10,
    validation_data=(X_test, y_test),
    class_weight=class_weights_dict
)

# Effectuer des prédictions sur les données de test
predictions = np.argmax(model.predict(X_test), axis=1)  # Retourne les indices des classes
true_labels = np.argmax(y_test, axis=1)  # Retourne les indices des classes réelles

# Afficher un rapport de classification
# Vérifier les classes présentes dans les données
present_classes = np.unique(true_labels)
print(f"Classes présentes dans les données de test : {present_classes}")

# Ajuster les noms des classes pour ne garder que celles présentes
classes = [chr(65 + i) for i in present_classes]  # 'A' à 'Z' pour les classes présentes

# Afficher le rapport de classification
print(classification_report(true_labels, predictions, target_names=classes))


# Visualisation des prédictions correctes et incorrectes
correct = np.nonzero(predictions == true_labels)[0]
incorrect = np.nonzero(predictions != true_labels)[0]