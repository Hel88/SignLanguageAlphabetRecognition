# Sign language alphabet recognition

Projet final du cours *Fondamentaux de l'apprentissage automatique 8INF867* de l'UQAC.

Cette application aide à apprendre l'alphabet de la langue des signes américaine (ASL) en détectant les signes réalisés par l'utilisateur à l'aide de sa webcam.

Dataset: https://www.kaggle.com/datasets/datamunge/sign-language-mnist

## Membres du groupe

- Héléna Barbillon - BARH30530200
- Chaimaa Oulmalme - OULC12590000
- Samia Carchaf - CARS05550300

## Installation des dépendances
````shell
pip install -r requirements.txt
````
 Mise à jour des dépendances:
 ````shell
 pip freeze > requirements.txt
 ````
Environnement virtuel venv:
````shell
# Créer un environnement virtuel
python -m venv venv

# L'activer avec Windows
env\Scripts\activate

# L'activer avec maxOS/Linus
env/bin/activate
````

## Lancer le projet
Le projet se lance en exacutant le fichier ``main.py`` en se placant dans le dossier ``src``.
````shell
python main.py 
````

Un nouveau modèle peut être entraîné en lançant le fichier ``SVM.py``.

## Fichiers du projet
Dans le dossier``src/`` :
- ``main.py`` : lance le projet
- ``gui.py`` : gère l'interface graphique
- ``classifier.py`` : gère les prédictions des images prises par la webcam de l'utilisateur
- ``SVM.py`` : entraîne un SVM sur les images du dataset
- ``CNN.V2.py`` : entraîne un réseau de neurones CNN sur les images du dataset
- ``CustomData.py`` : permet de créer des données personnalisées pour le dataset

Dans le dossier ``data/``:
- dossier ``captures``: dossier où sont stockées les images prises par la webcam de l'utilisateur
- dossier ``custom_data_images``: images additionnelles qui ont été ajoutées au dataset
- ``dataset/sign_mnist_test.csv``: données de tests du dataset
- ``dataset/sign_mnist_train.csv``: données d'entrainement du dataset
- dossier ``models`` : sauvegardes de modèles
- ``custom_data.csv``: images (sous format csv) additionnelles (prises par nous) ajoutées au dataset d'entrainement