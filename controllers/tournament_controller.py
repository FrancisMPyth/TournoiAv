# tournament_controller.py

import os
import json
import random
from models.tournament import Tournament
from controllers.player_controller import afficher_liste_joueurs
from config.config import Config
from models.match import Match
import datetime

DATA_DIR = "data"
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNAMENT_DATA_DIR = Config.TOURNOIS_DIR

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        if validate_date_format(date_input):
            return date_input
        else:
            print("Format de date invalide. Veuillez utiliser jj/mm/aaaa.")

def afficher_joueurs_disponibles(joueurs):
    print("Liste des joueurs disponibles :\n")
    for joueur in joueurs:
        print(f"ID: {joueur['id']}, Prénom: {joueur['first_name']}, Nom: {joueur['last_name']}")
    print("\n")

def enregistrer_tournoi():
    setup_directories()
    clear_screen()

    name = input("Nom du tournoi : ")
    location = input("Lieu : ")

    start_date = get_valid_date("Date de début (jj/mm/aaaa) : ")
    end_date = get_valid_date("Date de fin (jj/mm/aaaa) : ")

    number_of_rounds = int(input("Nombre de rondes : "))

    joueurs = []
    if os.path.exists(Config.JOUEURS_FILE):
        with open(Config.JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)

    joueurs_selectionnes = []
    afficher_liste_joueurs(avec_message=False)

    while True:
        afficher_joueurs_disponibles(joueurs)
        print("Sélectionnez un joueur par son ID (appuyez sur Entrée pour terminer) : ")
        choix_id = input().strip()

        if not choix_id:
            if len(joueurs_selectionnes) % 2 != 0:
                print("Le nombre de joueurs sélectionnés doit être pair.")
                continuer = input("Voulez-vous ajouter un joueur supplémentaire ? (Oui/Non) : ")
                if continuer.lower() == "oui":
                    continue
                else:
                    break
            else:
                break
        elif choix_id.isdigit():
            id_joueur = int(choix_id)
            joueur_selectionne = next((joueur for joueur in joueurs if joueur['id'] == id_joueur), None)

            if joueur_selectionne:
                joueurs_selectionnes.append(joueur_selectionne)
                joueurs.remove(joueur_selectionne)
                print(f"Joueur sélectionné : {joueur_selectionne['first_name']} {joueur_selectionne['last_name']}")
            else:
                print("ID de joueur invalide. Veuillez réessayer.")
        else:
            print("ID de joueur invalide. Veuillez réessayer.")

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

def validate_date_format(date):
    try:
        datetime.datetime.strptime(date, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validate_end_date(start_date, end_date):
    start_date_obj = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    end_date_obj = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    return end_date_obj >= start_date_obj

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

        print("\n" + "-" * 40 + "\n")

    input("Appuyez sur Entrée pour continuer...")

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
    while True:
        clear_screen()
        print("Gestion des tournois en cours...\n")
        print("1. Lancer un Tournoi")
        print("2. Saisir les résultats des matchs")
        print("3. Autre option (à compléter)")
        print("4. Quitter")

        choix = input("\nEntrez le numéro de votre choix : ")

        if choix == "1":
            tournoi = choisir_tournoi()
            if tournoi:
                lancer_rounds(tournoi)
        elif choix == "2":
            saisir_resultats()
        elif choix == "3":
            pass
        elif choix == "4":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

        print("\nListe des tournois enregistrés :")
        afficher_liste_tournois()

        input("Appuyez sur une touche pour continuer...")

def lancer_rounds(tournoi):
    print(f"Lancement des rounds pour le tournoi : {tournoi['name']}")

    if tournoi.get('round_results') is None:
        random.shuffle(tournoi['players'])
    else:
        tournoi['players'].sort(key=lambda x: x['score'], reverse=True)

    for round_number in range(tournoi['number_of_rounds']):
        matches = generate_matches(tournoi['players'])
        
        print(f"\nDébut du Round {round_number + 1}\n")

        for match in matches:
            print(f"Match entre {match['player1']['first_name']} {match['player1']['last_name']} "
                  f"et {match['player2']['first_name']} {match['player2']['last_name']}")

            score_player1 = float(input("Score pour le joueur 1 : "))
            score_player2 = float(input("Score pour le joueur 2 : "))
            
            match['match'].set_result(score_player1, score_player2)
            update_player_scores(match['player1'], match['player2'], score_player1, score_player2)

            print(f"\nScores mis à jour :\n"
                  f"  {match['player1']['first_name']} {match['player1']['last_name']}: {match['player1']['score']}\n"
                  f"  {match['player2']['first_name']} {match['player2']['last_name']}: {match['player2']['score']}\n")

        if 'round_results' not in tournoi:
            tournoi['round_results'] = []
        tournoi['round_results'].append(matches)

        print(f"\nFin du Round {round_number + 1}\n")

    print("Rounds terminés.")
    
def afficher_suivi_rounds(tournoi):
    if 'round_results' not in tournoi or not tournoi['round_results']:
        print("Aucun round n'a encore été joué.")
        return

    for round_number, matches in enumerate(tournoi['round_results']):
        print(f"\nRound {round_number + 1} - Début : {matches[0]['match'].start_time}, Fin : {matches[-1]['match'].end_time}\n")

        for match in matches:
            print(f"Match entre {match['player1']['first_name']} {match['player1']['last_name']} "
                  f"et {match['player2']['first_name']} {match['player2']['last_name']}")
            print(f"Score : {match['match'].score_player1} - {match['match'].score_player2}\n")

def saisir_resultats():
    tournoi = choisir_tournoi()
    if tournoi:
        lancer_rounds(tournoi)

def update_player_scores(player1, player2, score_player1, score_player2):
    pass

def generate_matches(players):
    matches = []
    num_players = len(players)

    for i in range(num_players - 1):
        for j in range(i + 1, num_players):
            match = Match(players[i]['id'], players[j]['id'])
            matches.append({'match': match, 'player1': players[i], 'player2': players[j]})

    return matches

def choisir_tournoi():
    clear_screen()
    print("Choisir un tournoi par son ID :")

    tournois = load_all_tournaments()
    for tournoi in tournois:
        print(f"ID: {tournoi['tournament_id']}, Nom: {tournoi['name']}")

    tournoi_id = input("Saisissez l'ID du tournoi choisi : ")
    selected_tournoi = next((tournoi for tournoi in tournois if tournoi['tournament_id'] == tournoi_id), None)

    if selected_tournoi:
        print(f"Tournoi choisi : {selected_tournoi['name']}")
        return selected_tournoi
    else:
        print("ID de tournoi invalide. Veuillez réessayer.")
        return None

def setup_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(TOURNOIS_DIR):
        os.makedirs(TOURNOIS_DIR)

if __name__ == "__main__":
    gestion_tournois()
