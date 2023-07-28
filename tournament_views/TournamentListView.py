# tournamentListiews.py

class TournamentListView:
    def display_tournaments(self, tournament_controller):
        tournaments = tournament_controller.get_tournaments()
        print("Liste des tournois :")
        for tournament in tournaments:
            print(f"Identifiant : {tournament.tournament_id}")
            print(f"Nom : {tournament.name}")
            print(f"Lieu : {tournament.location}")
            print(f"Début : {tournament.start_date.strftime('%d/%m/%Y')}")
            print(f"Fin : {tournament.end_date.strftime('%d/%m/%Y')}")
            print(f"Nombre de rounds : {tournament.number_of_rounds}")
            print("Joueurs inscrits :")
            if tournament.players:
                for player in tournament.players:
                    print(f" - {player.first_name} {player.last_name} (ID: {player.chess_id})")
            else:
                print(" - Aucun joueur inscrit.")
            print("=" * 40)

    def display_players(self, tournament):
        print(f"Joueurs inscrits au tournoi '{tournament.name}' :")
        if tournament.players:
            for player in tournament.players:
                print(f"- {player.first_name} {player.last_name} (ID: {player.chess_id})")
        else:
            print("Aucun joueur inscrit dans ce tournoi.")

    def display_tournament_details(self, tournament):
        print(f"Identifiant : {tournament.tournament_id}")
        print(f"Nom : {tournament.name}")
        print(f"Lieu : {tournament.location}")
        print(f"Début : {tournament.start_date.strftime('%d/%m/%Y')}")
        print(f"Fin : {tournament.end_date.strftime('%d/%m/%Y')}")
        print(f"Nombre de rounds : {tournament.number_of_rounds}")

    def save_tournament_to_file(self, tournament):
        filepath = f"Data/Tournois/{tournament.name}/info_{tournament.name}.json"
        pass

