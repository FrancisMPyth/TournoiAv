# tournament_controller.py

import os
import json
import random
import datetime 
from models.tournament import Tournament
from controllers.player_controller import afficher_liste_joueurs
from config.config import Config
from models.match import Match
from itertools import combinations
import itertools


DATA_DIR = "data"
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
TOURNAMENT_DATA_DIR = Config.TOURNOIS_DIR 
joueurs = []
joueurs_selectionnes = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        if validate_date_format(date_input):
            return date_input
        else:
            print("Format de date invalide. Veuillez utiliser jj/mm/aaaa.")

def generer_suffixe_unique(name, existing_tournaments):
    i = 1
    new_name = name
    while any(t['name'] == new_name for t in existing_tournaments):
        new_name = f"{name}_{i}"
        i += 1
    return new_name

def afficher_joueurs_disponibles(joueurs_disponibles):
    print("Liste des joueurs disponibles :\n")
    for joueur in joueurs_disponibles:
        print(f"ID: {joueur['id']}, Prénom: {joueur['first_name']}, Nom: {joueur['last_name']}")
    print("\n")

def display_available_players(joueurs_disponibles):
    print("Liste des joueurs disponibles :\n")
    for joueur in joueurs_disponibles:
        print(f"ID: {joueur['id']}, Prénom: {joueur['first_name']}, Nom: {joueur['last_name']}")
    print("\n")

def select_players(joueurs_disponibles, joueurs_selectionnes, min_players, max_players):
    while True:
        display_available_players(joueurs_disponibles)

        print(f"Sélectionnez un joueur par son ID (appuyez sur Entrée pour terminer) : ")
        choice_id = input().strip()

        if not choice_id:
            if len(joueurs_selectionnes) % 2 != 0 or len(joueurs_selectionnes) < min_players:
                print(f"Le nombre de joueurs sélectionnés doit être pair et au moins égal à {min_players}.")
                continue_tournament = input("Voulez-vous ajouter des joueurs supplémentaires ? (Oui/Non) : ")
                if continue_tournament.lower() == "oui":
                    continue
                else:
                    break
            else:
                break
        elif choice_id.isdigit():
            player_id = int(choice_id)

            if any(player['id'] == player_id for player in joueurs_selectionnes):
                print("Ce joueur a déjà été sélectionné. Veuillez réessayer.")
                continue

            selected_player = next((player for player in joueurs_disponibles if player['id'] == player_id), None)

            if selected_player:
                joueurs_selectionnes.append(selected_player)
                joueurs_disponibles.remove(selected_player)
                print(f"Joueur sélectionné : {selected_player['first_name']} {selected_player['last_name']}")
            else:
                print("ID de joueur invalide. Veuillez réessayer.")
        else:
            print("ID de joueur invalide. Veuillez réessayer.")


def enregistrer_joueur():
    setup_directories()
    clear_screen()

    global joueurs_disponibles

    joueurs_disponibles = joueurs.copy()

    if os.path.exists(Config.JOUEURS_FILE):
        with open(Config.JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)

    select_players(joueurs_disponibles, joueurs_selectionnes, min_players=8, max_players=float('inf'))

def update_player_scores(players, matches):
    for match in matches:
        player1_id = match['player1']['id']
        player2_id = match['player2']['id']

        player1_score = match.get('score_player1', 0)
        player2_score = match.get('score_player2', 0)

        matching_player1 = next((p for p in players if p['id'] == player1_id), None)
        matching_player2 = next((p for p in players if p['id'] == player2_id), None)

        if matching_player1 is not None:
            matching_player1['score'] = matching_player1.get('score', 0) + player1_score
        if matching_player2 is not None:
            matching_player2['score'] = matching_player2.get('score', 0) + player2_score

    return players


def enregistrer_tournoi():
    global joueurs

    setup_directories()
    clear_screen()

    name = input("Nom du tournoi : ")
    location = input("Lieu : ")

    start_date = get_valid_date("Date de début (jj/mm/aaaa) : ")

    joueurs_disponibles = joueurs.copy()

    while True:
        end_date = get_valid_date("Date de fin (jj/mm/aaaa) : ")
        if validate_end_date(start_date, end_date):
            break
        else:
            print("La date de fin doit être égale ou postérieure à la date de début. Veuillez réessayer.")

    number_of_rounds = int(input("Nombre de rondes : "))

    afficher_liste_joueurs(avec_message=False)

    if os.path.exists(Config.JOUEURS_FILE):
        with open(Config.JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)

    joueurs_disponibles = joueurs.copy()

    select_players(joueurs_disponibles, joueurs_selectionnes, min_players=2, max_players=float('inf'))

    if len(joueurs_selectionnes) % 2 != 0 or len(joueurs_selectionnes) < 2:
        print("Le nombre de joueurs sélectionnés doit être pair et supérieur ou égal à 2. Annulation de l'enregistrement du tournoi.")
    else:
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
    setup_directories()
    clear_screen()

    tournois = load_all_tournaments()

    if not tournois:
        print("Aucun tournoi enregistré.")
    else:
        print("Liste des tournois :\n")
        for tournoi in tournois:
            print(f"\nID: {tournoi['tournament_id']}")
            print(f"Nom: {tournoi['name']}")
            print(f"Lieu: {tournoi['location']}")
            print(f"Date début: {tournoi['start_date']}")
            print(f"Date fin: {tournoi['end_date']}")
            print(f"Nombre de rondes: {tournoi['number_of_rounds']}")

            if tournoi['current_round'] == 0:
                print("Le tournoi n'a pas encore commencé.")
            else:
                print(f"Tour en cours: {tournoi['current_round']}/{tournoi['number_of_rounds']}")

                print("\nJoueurs:")
                for joueur in tournoi['players']:
                    print(f"ID: {joueur['id']}, Nom: {joueur['first_name']} {joueur['last_name']}, "
                          f"Score: {joueur.get('score', 'N/A')}")

                if 'rounds' in tournoi and tournoi['rounds']:
                    current_round_number = tournoi['current_round']
                    current_round_matches = tournoi['rounds'][current_round_number - 1]['matches']

                    print("\nMatchs en cours :")
                    for match in current_round_matches:
                        print(f"Match entre {match['player1']['name']} et {match['player2']['name']}")
                        print(f"Score : {match['player1']['score']} - {match['player2']['score']}")
                        print(f"Heure de début : {match['start_time']}\n")

        input("Appuyez sur Entrée pour retourner au menu...")


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
        print("1. Gérer le Tournoi")
        print("2. Saisir les résultats des matchs")
        print("3. Menu")

        choix = input("\nEntrez le numéro de votre choix : ")

        if choix == "1":
            tournoi = choisir_tournoi()
            if tournoi:
                lancer_rounds(tournoi)
        elif choix == "2":
            saisir_resultats()
        elif choix == "3":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def lancer_rounds(tournoi):
    if tournoi.get('current_round', 0) > 0:
        print(f"Le tournoi '{tournoi['name']}' a déjà commencé. Retour au menu principal.")
        input("Appuyez sur Entrée pour continuer...")
        return

    print(f"Tournoi choisi : {tournoi['name']}")

    print("\nParticipants du tournoi :")
    for joueur in tournoi['players']:
        print(f"ID: {joueur['id']}, Prénom: {joueur['first_name']}, Nom: {joueur['last_name']}")

    input("\nAppuyez sur Entrée pour continuer...")

    print(f"\nLancement des rounds pour le tournoi : {tournoi['name']}")

    if tournoi.get('round_results') is None:
        random.shuffle(tournoi['players'])
    else:
        tournoi['players'].sort(key=lambda x: x['score'], reverse=True)

    tournoi['current_round'] += 1
    tournoi['rounds'] = []
    tournoi['start_time'] = datetime.datetime.now().strftime("%H:%M")  # Ajout de l'heure de début

    retour_sous_menu = False

    for round_number in range(tournoi['number_of_rounds']):
        formatted_start_time = tournoi['start_time']
        print(f"\nDébut du Round {round_number + 1} - {formatted_start_time}\n")

        matches = generate_matches(tournoi['players'], formatted_start_time)

        round_details = {'round_number': round_number + 1, 'matches': []}

        for match in matches:
            print(f"Match entre {match['player1']['first_name']} {match['player1']['last_name']} "
                  f"et {match['player2']['first_name']} {match['player2']['last_name']} "
                  f"- Début à {match['start_time']}")  # Ajout de l'heure de début du match

            match_details = {
                'player1': {'id': match['player1']['id'], 'score': 0,
                            'name': f"{match['player1']['first_name']} {match['player1']['last_name']}"},
                'player2': {'id': match['player2']['id'], 'score': 0,
                            'name': f"{match['player2']['first_name']} {match['player2']['last_name']}"},
                'start_time': match['start_time']  # Enregistrement de l'heure de début du match
            }
            round_details['matches'].append(match_details)

        tournoi['rounds'].append(round_details)

        retour_menu = input("Appuyez sur 'M' pour revenir au menu, ou appuyez sur Entrée pour revenir au sous-menu...")

        if retour_menu.lower() == 'm':
            retour_sous_menu = True
            break
        elif retour_menu.lower() == '':
            print("Retour au sous-menu...\n")
            retour_sous_menu = True
            break

    if retour_sous_menu:
        print("Retour au sous-menu...\n")
        input("Appuyez sur Entrée pour revenir au sous-menu...")

        save_tournament_data(tournoi)

    print("Rounds terminés.")

def generate_matches(players):
    matches = []
    num_players = len(players)

    if num_players % 2 != 0:
        raise ValueError("Le nombre de joueurs doit être pair.")

    random.shuffle(players)

    while len(players) >= 2:
        player1 = players.pop(0)
        player2 = players.pop(0)

        match_start_time = datetime.datetime.now()
        formatted_match_start_time = match_start_time.strftime("%H:%M")

        match = Match(player1['id'], player2['id'], start_time=formatted_match_start_time)
        matches.append({'match': match, 'player1': player1, 'player2': player2, 'start_time': formatted_match_start_time})

    return matches


def save_tournament_data(tournoi):
    if 'tournament_id' not in tournoi:
        print("Erreur: Impossible de sauvegarder les données du tournoi, l'identifiant du tournoi est manquant.")
        return

    for player in tournoi['players']:
        player_id = player['id']
        matching_player = next((p for p in tournoi['players'] if p['id'] == player_id), None)
        if matching_player:
            player['name'] = f"{matching_player['first_name']} {matching_player['last_name']}"

    file_path = os.path.join(TOURNOIS_DIR, f"{tournoi['tournament_id']}.json")
    with open(file_path, 'w') as file:
        json.dump(tournoi, file, indent=4)

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

def generate_matches(players, formatted_start_time):
    matches = []
    num_players = len(players)

    if num_players % 2 != 0:
        raise ValueError("Le nombre de joueurs doit être pair.")

    random.shuffle(players)

    while len(players) >= 2:
        player1 = players.pop(0)
        player2 = players.pop(0)

        match = Match(player1['id'], player2['id'], start_time=formatted_start_time)
        matches.append({'match': match, 'player1': player1, 'player2': player2, 'start_time': formatted_start_time})

    return matches

def choisir_tournoi():
    clear_screen()
    print("Choisir un tournoi par son ID :")

    tournois = load_all_tournaments()

    tournois_disponibles = tournois


    if not tournois_disponibles:
        print("Aucun tournoi disponible pour le lancement.")
        input("Appuyez sur Entrée pour continuer...")
        return None

    for tournoi in tournois_disponibles:
        print(f"ID: {tournoi['tournament_id']}, Nom: {tournoi['name']}")

    tournoi_id = input("Saisissez l'ID du tournoi choisi : ")
    selected_tournoi = next((tournoi for tournoi in tournois_disponibles if tournoi['tournament_id'] == tournoi_id), None)

    if selected_tournoi:
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