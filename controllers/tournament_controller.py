# tournament_controller.py

import os
import json
from models.tournament import Tournament
from controllers.player_controller import afficher_liste_joueurs
from config.config import Config

DATA_DIR = "data"
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNOIS_FILE = os.path.join(TOURNOIS_DIR, "tournois.json")
TOURNAMENT_DATA_DIR = Config.TOURNOIS_DIR


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def enregistrer_tournoi():
    setup_directories()
    clear_screen()

    name = input("Nom du tournoi : ")
    location = input("Lieu : ")
    start_date = input("Date de début (jj/mm/aaaa) : ")
    end_date = input("Date de fin (jj/mm/aaaa) : ")
    number_of_rounds = int(input("Nombre de rondes : "))

    joueurs = []
    if os.path.exists(Config.JOUEURS_FILE):
        with open(Config.JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)

    joueurs_selectionnes = afficher_liste_joueurs(avec_message=False)

    ids = []
    while True:
        choix_id = input("ID (appuyez sur Entrée après chaque ID, terminer avec une ligne vide) : ")
        if choix_id.strip():
            try:
                joueur_id = int(choix_id.strip())
                if joueur_id in ids:
                    print("Ce joueur a déjà été sélectionné. Veuillez entrer un autre ID.")
                else:
                    ids.append(joueur_id)
            except ValueError:
                print("Veuillez entrer un ID valide (nombre entier).")
        else:
            if len(ids) % 2 == 0 and len(ids) > 0:
                break
            else:
                print("Le nombre d'IDs doit être pair et supérieur à zéro. Ajoutez plus de joueurs.")

    joueurs_selectionnes = [joueur for joueur in joueurs if joueur['id'] in ids]

    tournament = Tournament()
    tournament.create(
        name=name,
        location=location,
        start_date=start_date,
        end_date=end_date,
        number_of_rounds=number_of_rounds,
        players=joueurs_selectionnes
    )

    tournament.save()

    print("Tournoi enregistré.")
    input("Appuyez sur une touche pour continuer...")


def afficher_liste_tournois():
    clear_screen()
    tournois = load_all_tournaments()

    if not tournois:
        print("Aucun tournoi enregistré.")
    else:
        print("Affichage de la liste des tournois...")
        for tournoi in tournois:
            print(f"ID: {tournoi['tournament_id']}, Nom: {tournoi['name']}, Lieu: {tournoi['location']}, "
                  f"Date début: {tournoi['start_date']}, Date fin: {tournoi['end_date']}, "
                  f"Nombre de rondes: {tournoi['number_of_rounds']}, Joueurs: {tournoi['players']}")

    input("Appuyez sur une touche pour continuer...")


def gestion_tournois(tournament):
    clear_screen()
    print("Gestion des tournois en cours...")
    input("Appuyez sur une touche pour continuer...")


def setup_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(TOURNOIS_DIR):
        os.makedirs(TOURNOIS_DIR)


def load_all_tournaments():
    tournois = []

    if os.path.exists(TOURNOIS_DIR):
        tournament_files = [f for f in os.listdir(TOURNOIS_DIR) if f.endswith('.json')]

        for file_name in tournament_files:
            file_path = os.path.join(TOURNOIS_DIR, file_name)
            with open(file_path, 'r') as file:
                tournament_data = json.load(file)
                tournois.append(tournament_data)

    return tournois


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
