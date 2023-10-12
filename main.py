# main_menu.py

import os
from controllers.tournament_controller import enregistrer_tournoi, afficher_liste_tournois, gestion_tournois
from controllers.player_controller import enregistrer_joueur, afficher_liste_joueurs
from config.config import Config

DATA_DIR = "data"
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
JOUEURS_FILE = os.path.join(JOUEURS_DIR, "joueurs.json")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNOIS_FILE = os.path.join(TOURNOIS_DIR, "tournois.json")


def main_menu():
    clear_screen()
    print("Menu Principal :")
    print("1. Enregistrement des joueurs")
    print("2. Afficher la liste des joueurs")
    print("3. Enregistrer un tournoi")
    print("4. Afficher la liste des tournois")
    print("5. Gestion des tournois")
    print("q. Quitter")

    choix = input("Entrez votre choix : ")

    if choix == "1":
        enregistrer_joueur()
    elif choix == "2":
        afficher_liste_joueurs()

    elif choix == "3":
        enregistrer_tournoi()
    elif choix == "4":
        afficher_liste_tournois()
        input("Appuyez sur une touche pour retourner au Menu...")

    elif choix == "5":
        gestion_tournois()

    elif choix.lower() == "q":
        exit()
    else:
        print("Choix invalide. Veuillez réessayer.")

    main_menu()


# Fonctions utilisées dans main_menu()
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
