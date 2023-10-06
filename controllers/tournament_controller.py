# tournament_controller.py

import os
import json
from models.tournament import Tournament
from controllers.player_controller import afficher_liste_joueurs
from config.config import Config

DATA_DIR = "data"
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNOIS_FILE = os.path.join(TOURNOIS_DIR, "tournois.json")

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

    joueurs_selectionnes = afficher_liste_joueurs()

    choix_ids = input("Sélectionnez les joueurs par leur ID (séparés par des virgules) : ")
    ids = [int(id.strip()) for id in choix_ids.split(',')]

    joueurs_selectionnes = [joueur for joueur in joueurs if joueur['id'] in ids]

    tournament = Tournament()
    tournament.create(name, location, start_date, end_date, number_of_rounds, players=joueurs_selectionnes)

    tournament.save_in_directory()

    print("Tournoi enregistré.")
    input("Appuyez sur une touche pour continuer...")

def afficher_liste_tournois():
    clear_screen()
    tournois = []
    if os.path.exists(TOURNOIS_FILE):
        with open(TOURNOIS_FILE, 'r') as file:
            tournois = json.load(file)

    print("Affichage de la liste des tournois...")
    for tournoi in tournois:
        print(f"ID: {tournoi['id']}, Nom: {tournoi['name']}, Lieu: {tournoi['location']}, "
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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
