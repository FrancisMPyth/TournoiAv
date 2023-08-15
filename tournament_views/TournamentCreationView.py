# TournamentCreationView.py

from datetime import datetime

class TournamentCreationView:
    def __init__(self, tournament_controller, player_controller):
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def create_tournament(self):
        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date_str = input("Date de début (format jj/mm/aaaa) : ")
        end_date_str = input("Date de fin (format jj/mm/aaaa) : ")
        number_of_rounds = int(input("Nombre de rounds : "))

        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
            if end_date < start_date:
                print("La date de fin ne peut pas être antérieure à la date de début.")
                return
        except ValueError:
            print("Format de date incorrect. Assurez-vous de saisir la date au format jj/mm/aaaa.")
            return

        players = self.player_controller.get_players()
        if not players:
            print("Aucun joueur enregistré. Veuillez enregistrer des joueurs avant de créer un tournoi.")
            return

        print("Joueurs disponibles pour le tournoi :")
        for idx, player in enumerate(players, start=1):
            print(f"{idx}. {player.first_name} {player.last_name}")

        selected_players = []
        while True:
            player_choice = input("Entrez le numéro du joueur à ajouter au tournoi (ou 'q' pour quitter) : ")
            if player_choice.lower() == "q":
                if len(selected_players) % 2 != 0:
                    print("Le nombre de joueurs doit être pair. Voulez-vous continuer à ajouter des joueurs ? (o/n)")
                    continue_choice = input()
                    if continue_choice.lower() == "o":
                        continue
                    else:
                        print("Annulation de la création du tournoi.")
                        return
                else:
                    break

            try:
                player_idx = int(player_choice) - 1
                selected_player = players[player_idx]
                selected_players.append(selected_player)
            except (ValueError, IndexError):
                print("Choix invalide. Veuillez entrer un numéro valide.")

        if not selected_players:
            print("Aucun joueur sélectionné pour le tournoi.")
            return

        self.tournament_controller.create_tournament(name, location, start_date_str, end_date_str, number_of_rounds, selected_players)

        print(f"Le tournoi '{name}' a été enregistré.")
