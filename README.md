# 2025_2026_nsi_1e02_projet2_gp3
# 🚀 Équipe NSI Prem P03 – 2025/2026

### 👥 Membres de l’équipe

| Prénom   | Pseudo GitHub    |
|-----------|------------------|
| Timothée | `timothee.chps` |
| Haron     | `HaronElmz`     |
| Victor    | `frst_304`      |

## 📌 Présentation du projet

Ce projet est une application **Python (Tkinter)** d’exploration de données COVID-19 en France.
Elle permet d’afficher des indicateurs nationaux, de comparer deux régions, et de visualiser des valeurs par département sur une carte.

## ✨ Fonctionnalités principales

### 1) Accueil – résumé national
- Affiche un aperçu rapide des données les plus récentes disponibles.
- Met en avant :
  - les hospitalisations actuelles,
  - les décès hospitaliers cumulés.

### 2) Comparer les régions
- Sélection de **2 régions** à comparer.
- Choix d’un indicateur (hospitalisations, réanimations, décès, etc.).
- Filtrage possible par **date de début** et **date de fin**.
- Affichage d’un **graphique comparatif** (évolution temporelle).

### 3) France entière
- Sélection d’un indicateur national.
- Filtrage par intervalle de dates.
- Affichage d’un **graphique d’évolution** de l’indicateur pour toute la France.

### 4) Carte des départements
- Sélection d’un indicateur et d’une date.
- Génération d’une **carte choroplèthe** des départements (via Folium), ouverte dans le navigateur.

## 🧱 Architecture

Le projet suit une architecture **MVC** :
- `models/` : chargement et traitement des données,
- `views/` : interface graphique Tkinter,
- `controllers/` : logique métier et interactions entre vues et données.

## ▶️ Lancer le projet

### Prérequis
- Python 3.10+

### Installation
```bash
pip install -r requirements.txt
```

> Pour la fonctionnalité de carte, installer aussi `folium` :
```bash
pip install folium
```

### Exécution
```bash
python main.py
```