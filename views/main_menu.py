# main_menu.py

import os

from controllers.tournament_controller import register_tournament, display_tournament_list, manage_tournaments
from controllers.player_controller import register_player, display_players_list
from config.config import Config

DATA_DIR = "data"
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
JOUEURS_FILE = os.path.join(JOUEURS_DIR, "joueurs.json")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNOIS_FILE = os.path.join(TOURNOIS_DIR, "tournois.json")


def main_menu():
    while True:
        clear_screen()
        print("Menu Principal :")
        print("1. Enregistrement des joueurs")
        print("2. Afficher la liste des joueurs")
        print("3. Enregistrer un tournoi")
        print("4. Historique des tournois")
        print("5. Gestion des tournois")
        print("q. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            register_player()
        elif choix == "2":
            display_players_list()

        elif choix == "3":
            register_tournament()
        elif choix == "4":
            display_tournament_list()

        elif choix == "5":
            manage_tournaments()

        elif choix.lower() == "q":
            exit()
        else:
            print("Choix invalide. Veuillez réessayer.")

        input("Appuyez sur une touche pour continuer...")

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
