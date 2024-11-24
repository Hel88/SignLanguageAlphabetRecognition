# Idée de plan

* parler du dataset: 
  * données: complètes ou pas, cb d'instances, classes balancées ou pas,  si pas assez d'instances, est-ce qu'on peut en créer en appliquant des modifs aux images, visu de données
  * images: quel type d'images, taille, couleur ou N&B (il faudra mettre les images à la mm taille, les passer en noir et blanc)
Est-ce qu'il faudra qu'on fasse notre propre dataset de tests avec des images de notre webcam?

* traitement sur les images/extraction des caractéristiques (forme, vecteur, contour, ... qu'est-ce qui est le plus pertinent):
  * les mettre à la mm taille, passer en noir et blanc, d'autres opérations sur les pixels (filtres?)
  * segmentation
  
  <img src="img_1.png"  width="150"/>
  
  * détecter les pts de repères sur la main (cf mediapipe: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=fr)
  
  <img src="img.png"  width="300"/>

  
  * autre ... 
  
* modèles de ML de classification, qu'est-ce qui est le plus efficace (et rapide) sur ces données (SVM, KNN, Random Forest, gradient boosting, logistic reg... )

* interface graphique: 
  * affichage général (maquette?)
  * prise de photo (webcam de l'ordinateur)
  * exercices aléatoires
  
