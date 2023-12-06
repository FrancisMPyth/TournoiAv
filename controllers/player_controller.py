# player_controller.py

import json
import os
from models.player import Player
from config.config import Config
import datetime

DATA_DIR = "data"
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
JOUEURS_FILE = os.path.join(JOUEURS_DIR, "joueurs.json")

def setup_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(JOUEURS_DIR):
        os.makedirs(JOUEURS_DIR)

def register_player():
    setup_directories()
    clear_screen()

    joueurs = []
    if os.path.exists(JOUEURS_FILE):
        with open(JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)

    while True:
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        date_of_birth = input("Date de naissance (jj/mm/aaaa) : ")

        while True:
            chess_id = input("Identifiant national d'échecs (2 lettres + 5 chiffres) : ")
            if len(chess_id) == 7 and chess_id[:2].isalpha() and chess_id[2:].isdigit():
                break
            else:
                print("Erreur: L'identifiant d'échecs doit être composé de 2 lettres suivies de 5 chiffres.")

        joueur_id = len(joueurs) + 1  

        player = Player(first_name, last_name, date_of_birth, chess_id, joueur_id)

        joueur_data = {
            "id": joueur_id,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "date_of_birth": player.date_of_birth,
            "chess_id": player.chess_id,
            "score": player.score,
        }
        joueurs.append(joueur_data)

        with open(JOUEURS_FILE, 'w') as file:
            json.dump(joueurs, file, indent=4)

        print(f"Joueur enregistré avec succès! Identifiant : {joueur_id}")

        continuer = input("Voulez-vous enregistrer un autre joueur ? (Oui/Non) : ")
        if continuer.lower() != "oui":
            break

def return_to_menu():
    input("Appuyez sur une touche pour retourner au menu...")
    clear_screen()

def display_players_list(avec_message=True):
    if avec_message:
        clear_screen()
        print("Affichage de la liste des joueurs...")

    joueurs = []
    if os.path.exists(JOUEURS_FILE):
        with open(JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)

    for joueur in joueurs:
        print(f"ID: {joueur.get('id', 'N/A')}, Prénom: {joueur.get('first_name', 'N/A')}, "
              f"Nom: {joueur.get('last_name', 'N/A')}, Date de naissance: {joueur.get('date_of_birth', 'N/A')}, "
              f"ID d'échecs: {joueur.get('chess_id', 'N/A')}, Score: {joueur.get('score', 'N/A')}")

    if avec_message:
        input("Appuyez sur une touche pour retourner au menu...")

    clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
