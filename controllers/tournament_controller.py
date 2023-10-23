# tournament_controller.py

import os
import json
import random
from models.tournament import Tournament
from controllers.player_controller import afficher_liste_joueurs
from config.config import Config
from models.match import Match
import datetime
from itertools import combinations
import itertools

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

def generer_suffixe_unique(name, existing_tournaments):
    i = 1
    new_name = name
    while any(t['name'] == new_name for t in existing_tournaments):
        new_name = f"{name}_{i}"
        i += 1
    return new_name

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

    while True:
        end_date = get_valid_date("Date de fin (jj/mm/aaaa) : ")
        if validate_end_date(start_date, end_date):
            break
        else:
            print("La date de fin doit être égale ou postérieure à la date de début. Veuillez réessayer.")

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

    for joueur in joueurs_selectionnes:
        joueur['name'] = f"{joueur['first_name']} {joueur['last_name']}"

    # Récupération des tournois existants pour générer un suffixe unique
    existing_tournaments = load_all_tournaments()

    # Génération du nom du tournoi avec un suffixe unique
    unique_name = generer_suffixe_unique(name, existing_tournaments)

    tournament = Tournament()
    tournament.create(
        name=unique_name,
        location=location,
        start_date=start_date,
        end_date=end_date,
        number_of_rounds=number_of_rounds,
        players=joueurs_selectionnes
    )

    tournament.save()

    print(f"Tournoi '{unique_name}' enregistré.")

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

    tournois = []
    if os.path.exists(Config.TOURNOIS_DIR):
        for filename in os.listdir(Config.TOURNOIS_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(Config.TOURNOIS_DIR, filename), 'r') as file:
                    tournoi = json.load(file)
                    tournois.append(tournoi)

    if not tournois:
        print("Aucun tournoi enregistré.")
    else:
        print("Liste des tournois :\n")
        for tournoi in tournois:
            print(f"ID: {tournoi['tournament_id']}")
            print(f"Nom: {tournoi['name']}")
            print(f"Lieu: {tournoi['location']}")
            print(f"Date début: {tournoi['start_date']}")
            print(f"Date fin: {tournoi['end_date']}")
            print(f"Nombre de rondes: {tournoi['number_of_rounds']}")

            if 'current_round' in tournoi and tournoi['current_round'] > 0:
                print(f"Round en cours: {tournoi['current_round']}")
            else:
                print("Le tournoi n'a pas encore commencé.")

            print("\nJoueurs:")
            for joueur in tournoi['players']:
                print(f"  ID: {joueur['id']}, Prénom: {joueur['first_name']}, Nom: {joueur['last_name']}, "
                      f"Date de naissance: {joueur['date_of_birth']}, ID d'échecs: {joueur['chess_id']}, "
                      f"Score: {joueur['score']}, Nom complet: {joueur['name']}")

            print("\n" + "-" * 40 + "\n")

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

    tournoi['current_round'] += 1  # Mise à jour du nombre de rounds actuel
    tournoi['rounds'] = []  # Initialisation de la liste des rounds pour le tour actuel
    retour_sous_menu = False

    for round_number in range(tournoi['number_of_rounds']):
        current_round_start_time = datetime.datetime.now()
        print(f"\nDébut du Round {round_number + 1} - {current_round_start_time}\n")

        matches = generate_matches(tournoi['players'])

        round_details = {'round_number': round_number + 1, 'matches': []}  # Détails du round

        for match in matches:
            print(f"Match entre {match['player1']['first_name']} {match['player1']['last_name']} "
                  f"et {match['player2']['first_name']} {match['player2']['last_name']}")

            match_details = {
                'player1': {'id': match['player1']['id'], 'score': 0,
                            'name': f"{match['player1']['first_name']} {match['player1']['last_name']}"},
                'player2': {'id': match['player2']['id'], 'score': 0,
                            'name': f"{match['player2']['first_name']} {match['player2']['last_name']}"}
            }
            round_details['matches'].append(match_details)

        tournoi['rounds'].append(round_details)  # Ajout des détails du round à la liste

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

def generate_matches(players):
    matches = []
    num_players = len(players)

    if num_players % 2 != 0:
        raise ValueError("Le nombre de joueurs doit être pair.")

    random.shuffle(players)

    while len(players) >= 2:
        player1 = players.pop(0)
        player2 = players.pop(0)

        match = Match(player1['id'], player2['id'])
        matches.append({'match': match, 'player1': player1, 'player2': player2})

    return matches

def choisir_tournoi():
    clear_screen()
    print("Choisir un tournoi par son ID :")

    tournois = load_all_tournaments()

    tournois_disponibles = [tournoi for tournoi in tournois if tournoi.get('current_round', 0) == 0]

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
