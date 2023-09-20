# tournament_views.py

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
            if tournament.first_round_launched:
                print("Le premier round a été lancé.")
            else:
                print("Le premier round n'a pas été lancé.")
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
        if tournament.first_round_launched:
            print("Le premier round a été lancé.")
        else:
            print("Le premier round n'a pas été lancé.")

    def save_tournament_to_file(self, tournament):
        filepath = f"Data/Tournois/{tournament.name}/info_{tournament.name}.json"
        # Vous pouvez ajouter ici la logique pour enregistrer les détails du tournoi dans un fichier JSON
        pass
