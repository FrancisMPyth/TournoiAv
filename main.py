# main.py

import os
from views.main_menu import main_menu 
from config.config import Config

DATA_DIR = "data"
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
JOUEURS_FILE = os.path.join(JOUEURS_DIR, "joueurs.json")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNOIS_FILE = os.path.join(TOURNOIS_DIR, "tournois.json")


def setup_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(JOUEURS_DIR):
        os.makedirs(JOUEURS_DIR)

    if not os.path.exists(TOURNOIS_DIR):
        os.makedirs(TOURNOIS_DIR)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    setup_directories()

    main_menu()
