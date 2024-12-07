"""Modèle CNN ( v1 )"""
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report

train_data = pd.read_csv("../data/dataset/sign_mnist_train.csv")
test_data = pd.read_csv("../data/dataset/sign_mnist_test.csv")

y_train = train_data['label'].values
X_train = train_data.drop(['label'], axis=1).values

y_test = test_data['label'].values
X_test = test_data.drop(['label'], axis=1).values

# Normaliser les valeurs de pixels (0 à 1)
X_train = X_train / 255.0
X_test = X_test / 255.0

# Redimensionner les images pour qu'elles soient en 28x28x1
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# Conversion des labels en one-hot encoding
num_classes = 26
y_train = np.eye(num_classes)[y_train]
y_test = np.eye(num_classes)[y_test]

# Modèle CNN
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

# Entraîner le modèle
history = model.fit(
    X_train, y_train,
    batch_size=64,
    epochs=10,
    validation_data=(X_test, y_test),
)

# Effectuer des prédictions sur les données de test
predictions = np.argmax(model.predict(X_test), axis=1)
true_labels = np.argmax(y_test, axis=1)

# Vérifier les classes présentes dans les données
present_classes = np.unique(true_labels)
print(f"Classes présentes dans les données de test : {present_classes}")

# Ajuster les noms des classes pour ne garder que celles présentes
classes = [chr(65 + i) for i in present_classes]  # 'A' à 'Z' pour les classes présentes

# Rapport de classification
print(classification_report(true_labels, predictions, target_names=classes))


# Visualisation des prédictions correctes et incorrectes
correct = np.nonzero(predictions == true_labels)[0]
incorrect = np.nonzero(predictions != true_labels)[0]