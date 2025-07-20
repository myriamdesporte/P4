# P4 : Développer un programme logiciel en Python<br>- Gestionnaire de Tournois d'Échecs

## Description

Ce projet est une application en ligne de commande (CLI) permettant de gérer des tournois d'échecs.
<br>Il intègre la gestion des joueurs, des tournois, des rounds et des matchs, le tout en respectant une architecture 
MVC couplée à une architecture hexagonale.<br>Les données sont persistées localement en JSON, dans le dossier **data**, et synchronisées après 
chaque opération.

## Pré-requis

Avant de commencer, assurez-vous d'utiliser les versions suivantes de Python et pip :

- Python 3.13.2
- pip 25.1.1

## Installation

1. **Clonez le dépôt** sur votre machine locale :

``` 
git clone https://github.com/myriamdesporte/P4.git
```

2. **Créez un environnement virtuel** :

```
python -m venv env
```

3. **Activez l'environnement virtuel** :

- Sur Linux/macOS :
  ```
  source env/bin/activate
  ```
- Sur Windows :
  ```
  .\env\Scripts\activate
  ```

4. **Installez les dépendances** à partir du fichier `requirements.txt`:

```
pip install -r requirements.txt
```

## Lancer l'application

Une fois l'environnement virtuel activé et les dépendances installées,
exécutez la commande suivante depuis la racine du projet :

```
python main.py
```

Un menu interactif vous guidera pour gérer les joueurs, les tournois, saisir les résultats des matchs et générer
des rapports.


## Génération des rapports HTML

Les rapports HTML (pour les joueurs et les tournois) sont générés via le menu **"3 - Rapports"** de l’application et 
sont enregistrés dans le dossier `generated_reports/`.


## Vérification de la syntaxe avec Flake8

Pour assurer la qualité du code et sa conformité à la norme **PEP 8**, ce projet utilise `flake8` 
avec le plugin `flake8-html`, tous les deux inclus dans `requirements.txt` déjà installés précédemment.

Cela permet de générer automatiquement un rapport HTML à chaque exécution de la commande `flake8 .`
Ce rapport est disponible dans le dossier `flake8_rapport/`.

### Génération du rapport HTML flake8

Voici les étapes pour générer un nouveau rapport **flake8**: 

1. Exécutez la commande suivante depuis la racine du projet :
```
flake8 .
 ```
2. Ouvrez le rapport généré dans votre navigateur :

- Sur Linux/macOS :
```
open flake8_rapport/index.html
```

- Sur Windows :
```
start flake8-rapport\index.html
```
