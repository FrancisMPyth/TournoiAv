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

def load_all_players():
    joueurs = []
    if os.path.exists(Config.JOUEURS_FILE):
        with open(Config.JOUEURS_FILE, 'r') as file:
            joueurs = json.load(file)
    return joueurs


def trouver_joueur_par_id(joueur_id):
    joueurs = load_all_players()
    for joueur in joueurs:
        if joueur['id'] == joueur_id:
            return joueur
    return None


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

                print("Appuyez sur Entrée pour continuer...")
                input()  

    print("Fin de l'affichage de l'historique des tournois.")


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

def gerer_tournois_en_cours():
    while True:
        clear_screen()
        print("Gérer les tournois en cours...\n")
        afficher_liste_tournois_en_cours()

        choix = input("\nEntrez le numéro du tournoi que vous souhaitez gérer ou appuyez sur 'M' pour revenir au menu : ")

        if choix.lower() == 'm':
            break
        else:
            tournoi = trouver_tournoi_par_id(choix)
            if tournoi:
                afficher_details_tournoi(tournoi)
                gerer_resultats_matchs(tournoi)

def trouver_tournoi_par_id(tournoi_id):
    tournois_en_cours = load_all_tournaments()
    for tournoi in tournois_en_cours:
        if tournoi['tournament_id'] == tournoi_id:
            return tournoi
    return None

def afficher_details_tournoi(tournoi):
    clear_screen()
    print(f"\nDétails du tournoi en cours :\n")
    print(f"ID: {tournoi['tournament_id']}")
    print(f"Nom: {tournoi['name']}")
    print(f"Lieu: {tournoi['location']}")
    print(f"Date début: {tournoi['start_date']}")
    print(f"Date fin: {tournoi['end_date']}")
    print(f"Nombre de rondes: {tournoi['number_of_rounds']}")
    print(f"Tour en cours: {tournoi['current_round']}/{tournoi['number_of_rounds']}\n")

    if 'rounds' in tournoi and tournoi['rounds']:
        current_round_number = tournoi['current_round']
        current_round_matches = tournoi['rounds'][current_round_number - 1]['matches']

        print(f"Round {current_round_number} :")
        for match in current_round_matches:
            joueur1 = trouver_joueur_par_id(match['player1']['id'])
            joueur2 = trouver_joueur_par_id(match['player2']['id'])

            print(f"\nMatch entre {joueur1['first_name']} {joueur1['last_name']} et {joueur2['first_name']} {joueur2['last_name']}")
            print(f"Score : {match['player1']['score']} - {match['player2']['score']}")
            print(f"Heure de début : {match['start_time']}\n")

        gerer_resultats_matchs(tournoi)

def gerer_resultats_matchs(tournoi):
    current_round_number = tournoi['current_round']
    current_round_matches = tournoi['rounds'][current_round_number - 1]['matches']

    while True:
        clear_screen()
        print("Saisir les résultats des matchs...\n")

        for i, match_details in enumerate(current_round_matches, start=1):
            player1_name = match_details['player1']['name']
            player2_name = match_details['player2']['name']

            resultats_saisis = match_details.get('resultats_saisis', False)

            if resultats_saisis:
                print(f"{i}. Résultats déjà saisis pour le match entre {player1_name} et {player2_name}")
            else:
                print(f"{i}. Saisir les résultats pour le match entre {player1_name} et {player2_name}")

        choix = input("\nEntrez le numéro du match que vous souhaitez gérer (ou appuyez sur 'M' pour revenir au menu) : ")

        if choix.lower() == 'm':
            break
        elif choix.isdigit() and 1 <= int(choix) <= len(current_round_matches):
            selected_match = current_round_matches[int(choix) - 1]

            if selected_match.get('resultats_saisis', False):
                print("Les résultats de ce match ont déjà été saisis. Veuillez choisir un autre match.")
            else:
                saisir_resultats_match(tournoi, selected_match)
        else:
            print("Choix invalide. Veuillez réessayer.")


def saisir_resultats_match(tournoi, match_details):
    clear_screen()
    print("Saisir les résultats du match...\n")

    player1_name = match_details['player1']['name']
    player2_name = match_details['player2']['name']

    print(f"Match entre {player1_name} (1) et {player2_name} (2)")
    gagnant = input("Qui est le gagnant (1, 2, N pour match nul) : ")

    if gagnant.lower() == 'n':
        score_player1 = 0.5
        score_player2 = 0.5
    elif gagnant.isdigit() and int(gagnant) in [1, 2]:
        score_player1 = 1 if int(gagnant) == 1 else 0
        score_player2 = 1 if int(gagnant) == 2 else 0
    else:
        print("Choix invalide. Les scores seront considérés comme nuls.")
        score_player1 = 0.5
        score_player2 = 0.5

    match_details['player1']['score'] = score_player1
    match_details['player2']['score'] = score_player2
    match_details['resultats_saisis'] = True

    save_tournament_data(tournoi)

    print("Résultats enregistrés avec succès !\n")
    input("Appuyez sur Entrée pour continuer...")



def gestion_tournois():
    while True:
        clear_screen()
        print("Gestion des tournois en cours...\n")
        print("1. Lancer le Tournoi")
        print("2. Gérer les Tournois en cours")
        print("3. Menu")

        choix = input("\nEntrez le numéro de votre choix : ")

        if choix == "1":
            tournoi = choisir_tournoi()
            if tournoi:
                lancer_premier_round(tournoi)
        elif choix == "2":
            gerer_tournois_en_cours()
        elif choix == "3":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")




def afficher_liste_tournois_en_cours():
    tournois_en_cours = [tournoi for tournoi in load_all_tournaments() if tournoi.get('current_round', 0) > 0]

    if not tournois_en_cours:
        print("Aucun tournoi en cours.")
    else:
        print("Liste des tournois en cours :\n")
        for tournoi in tournois_en_cours:
            print(f"ID: {tournoi['tournament_id']}")
            print(f"Nom: {tournoi['name']}")
            print(f"Round en cours: {tournoi['current_round']}/{tournoi['number_of_rounds']}\n")

        choix = input("\nSaisissez l'ID du tournoi que vous souhaitez gérer (ou appuyez sur Entrée pour retourner au menu) : ")
        
        if choix:
            tournoi_choisi = trouver_tournoi_par_id(choix)
            if tournoi_choisi:
                afficher_details_tournoi(tournoi_choisi)
                # Appelle la fonction pour gérer le tournoi (à implémenter)
            else:
                print("ID de tournoi invalide. Veuillez réessayer.")
        else:
            print("Retour au menu principal.")




def saisir_resultats_matchs(tournoi, round_details):
    clear_screen()
    print("Saisir les résultats des matchs...\n")

    for match_details in round_details['matches']:
        player1_name = match_details['player1']['name']
        player2_name = match_details['player2']['name']

        print(f"Match entre {player1_name} et {player2_name}")
        score_player1 = int(input(f"Score pour {player1_name} : "))
        score_player2 = int(input(f"Score pour {player2_name} : "))

        match_details['player1']['score'] = score_player1
        match_details['player2']['score'] = score_player2

    save_tournament_data(tournoi)

    print("Résultats enregistrés avec succès !\n")
    input("Appuyez sur Entrée pour revenir au menu...")



def lancer_premier_round(tournoi):
    if tournoi.get('current_round', 0) > 0:
        print(f"Le tournoi '{tournoi['name']}' a déjà commencé. Retour au menu principal.")
        input("Appuyez sur Entrée pour continuer...")
        return

    print(f"Tournoi choisi : {tournoi['name']}")

    print("\nParticipants du tournoi :")
    for joueur in tournoi['players']:
        print(f"ID: {joueur['id']}, Prénom: {joueur['first_name']}, Nom: {joueur['last_name']}")

    input("\nAppuyez sur Entrée pour continuer...")

    print(f"\nLancement du premier round pour le tournoi : {tournoi['name']}")

    if tournoi.get('round_results') is None:
        random.shuffle(tournoi['players'])
    else:
        tournoi['players'].sort(key=lambda x: x['score'], reverse=True)

    tournoi['current_round'] += 1
    tournoi['rounds'] = []
    tournoi['start_time'] = datetime.datetime.now().strftime("%H:%M")  # Ajout de l'heure de début

    formatted_start_time = tournoi['start_time']
    print(f"\nDébut du Premier Round - {formatted_start_time}\n")

    matches = generate_matches(tournoi['players'], formatted_start_time)

    round_details = {'round_number': 1, 'matches': []}

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

    save_tournament_data(tournoi)

    print("Premier Round terminé.")
    input("Appuyez sur Entrée pour revenir au sous-menu...")




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



def update_player_scores(players, player_id, score):
    for player in players:
        if player['id'] == player_id:
            player['score'] += score
    return players

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