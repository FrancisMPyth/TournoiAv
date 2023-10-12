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

    print("Sélectionnez les joueurs par leur ID (séparés par des virgules) : ")

    choix_ids = input().strip()  
    if choix_ids and all(char.isdigit() or char == ',' for char in choix_ids):
        ids = [int(id.strip()) for id in choix_ids.split(',')]
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
    else:
        print("Saisie incorrecte. Aucun joueur sélectionné. Le tournoi ne sera pas enregistré.")
        input("Appuyez sur une touche pour continuer...")


def afficher_liste_tournois():
    clear_screen()
    tournois = load_all_tournaments()
    print("Affichage de la liste des tournois...\n")

    for tournoi in tournois:
        print(f"ID: {tournoi['tournament_id']}")
        print(f"Nom: {tournoi['name']}")
        print(f"Lieu: {tournoi['location']}")
        print(f"Date début: {tournoi['start_date']}")
        print(f"Date fin: {tournoi['end_date']}")
        print(f"Nombre de rondes: {tournoi['number_of_rounds']}")

        print("\nJoueurs:")
        for joueur in tournoi['players']:
            print(f"  ID: {joueur['id']}, Prénom: {joueur['first_name']}, "
                  f"Nom: {joueur['last_name']}, Date de naissance: {joueur['date_of_birth']}, "
                  f"ID d'échecs: {joueur['chess_id']}, Score: {joueur['score']}")

        print("\n" + "-"*40 + "\n")


def load_all_tournaments():
    tournois = []
    if os.path.exists(TOURNOIS_DIR):
        for filename in os.listdir(TOURNOIS_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(TOURNOIS_DIR, filename)
                with open(file_path, 'r') as file:
                    tournoi_data = json.load(file)
                    tournois.append(tournoi_data)
    return tournois


def gestion_tournois():
    clear_screen()
    print("Gestion des tournois en cours...\n")
    print("1. Lancer un Tournoi")
    print("2. Autre option (à compléter)")
    
    choix = input("Entrez votre choix : ")
    
    if choix == "1":
        from .tournament_controller import lancer_tournoi  
        lancer_tournoi()
    elif choix == "2":
        pass
    else:
        print("Choix invalide. Veuillez réessayer.")
    
    input("Appuyez sur une touche pour continuer...")

def setup_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(TOURNOIS_DIR):
        os.makedirs(TOURNOIS_DIR)


if __name__ == "__main__":
    enregistrer_tournoi()
