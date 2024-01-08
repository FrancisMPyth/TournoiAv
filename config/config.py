# config.py

import os


class Config:
    DATA_DIR = "data"
    JOUEURS_DIR = "data/joueurs"
    JOUEURS_FILE = "data/joueurs/joueurs.json"
    TOURNOIS_DIR = "data/tournois"

    @staticmethod
    def setup_directories():
        if not os.path.exists(Config.DATA_DIR):
            os.makedirs(Config.DATA_DIR)

        if not os.path.exists(Config.JOUEURS_DIR):
            os.makedirs(Config.JOUEURS_DIR)

        if not os.path.exists(Config.TOURNOIS_DIR):
            os.makedirs(Config.TOURNOIS_DIR)
