# TournamentCreationView.py

class TournamentCreationView:
    def create_tournament(self, tournament_controller, player_controller):
        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date_str = input("Date de début (format jj/mm/aaaa) : ")
        end_date_str = input("Date de fin (format jj/mm/aaaa) : ")
        number_of_rounds = int(input("Nombre de rounds : "))

        # Ajoutez le code ici pour créer un nouveau tournoi en utilisant les informations ci-dessus.
        # Par exemple :
        tournament_controller.create_tournament(name, location, start_date_str, end_date_str, number_of_rounds)

        print(f"Le tournoi '{name}' a été enregistré.")
