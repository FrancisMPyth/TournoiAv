# player_list_view.py

from datetime import datetime
import re



class PlayerListView:
    def generate_chess_id(self, players):
        existing_ids = [player.chess_id for player in players]
        max_id = max(existing_ids, default="J0")
        match = re.match(r"J(\d+)", max_id)
        if match:
            next_id = int(match.group(1)) + 1
        else:
            next_id = 1
        return f"J{next_id:03d}"

    def create_player(self, player_controller):
        print("\nEnregistrement des Joueurs :")
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        date_of_birth_str = input("Date de naissance (jj/mm/aaaa) : ")
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, "%d/%m/%Y")
        except ValueError:
            print("Format de date incorrect. Assurez-vous de saisir la date au format jj/mm/aaaa.")
            return

        chess_id = self.generate_chess_id(player_controller.get_players())
        national_chess_id = input("Identifiant national d'échecs : ")
        player_controller.add_player(first_name, last_name, date_of_birth, chess_id, national_chess_id)
        print("Joueur enregistré avec succès!")

    def display_player_list(self, player_controller):
        players = player_controller.get_players()
        players_sorted = sorted(players, key=lambda player: f"{player.last_name} {player.first_name}")

        print("\nListe des Joueurs :")
        for player in players_sorted:
            print(f"Nom: {player.last_name}")
            print(f"Prénom: {player.first_name}")
            print(f"Date de naissance: {player.date_of_birth.strftime('%d/%m/%Y')}")
            print(f"Identifiant: {player.chess_id}")
            print(f"Identifiant national d'échecs: {player.national_chess_id}\n")