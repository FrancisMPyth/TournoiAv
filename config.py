# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
GESTION_TOURNOIS_DIR = os.path.join(TOURNOIS_DIR, "gestion")
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TOURNOIS_DIR, exist_ok=True)
os.makedirs(GESTION_TOURNOIS_DIR, exist_ok=True)
os.makedirs(JOUEURS_DIR, exist_ok=True)

