# Yaa Ma Dimbali

Prototype de plateforme permettant à un patient de scanner le devis de son ordonnance,
extrait automatiquement par IA (médicaments, montant), pour qu'un donateur finance
directement le paiement auprès de la pharmacie via mobile money, avec remise d'un code
de retrait sécurisé au patient.

## Application déployée

Le prototype est déployé et testable en ligne, sans compte ni installation :
👉 https://claude.ai/artifact/KaupVb4CJVi1xv8jGjMKu7

## Contenu du dépôt

- `yaa-ma-dimbali.html` — prototype fonctionnel complet (patient / donateur / pharmacien)
- `test_modele.py` — script de test de l'intégration avec le modèle vision NVIDIA Build
- `README.md` — ce fichier

## Installation

Aucune installation n'est nécessaire pour le prototype principal.

1. Télécharger ou cloner ce dépôt.
2. Ouvrir `yaa-ma-dimbali.html` directement dans un navigateur.

Le prototype fonctionne entièrement côté client (HTML/CSS/JavaScript), sans serveur ni base de données.

Pour exécuter `test_modele.py`, Python 3 est requis.

## Dépendances

Pour `test_modele.py` uniquement :

```bash
pip install requests
```

(`json`, `re` et `sys` font partie de la bibliothèque standard de Python.)

## Commandes d'exécution

```bash
# Installer la dépendance
pip install requests

# Placer une image de devis nommée img.jpeg dans le même dossier que le script,
# puis lancer :
python test_modele.py
```

Le script affiche :
1. les données brutes extraites de l'image par le modèle IA,
2. les mêmes données anonymisées (tranche d'âge et type d'établissement génériques), telles qu'affichées à un donateur.

## Configuration des modèles / API

Modèle utilisé : **API NVIDIA Build**, `meta/llama-3.2-11b-vision-instruct`.
Clé API gratuite disponible sur [build.nvidia.com](https://build.nvidia.com).

Dans `test_modele.py`, remplacer la valeur d'exemple par votre propre clé :

```python
# Exemple de configuration — remplacez par votre propre clé, ne jamais committer de vraie clé
api_key = "nvapi-VOTRE_CLE_ICI"
```

⚠️ Aucune vraie clé API n'est incluse dans ce dépôt. La valeur ci-dessus est un espace réservé.

## Limitations connues

- Le paiement mobile money (Wave / Orange Money / Free Money) est simulé dans `yaa-ma-dimbali.html`.
- La liste des pharmacies partenaires est pré-enregistrée en dur pour la démo.
