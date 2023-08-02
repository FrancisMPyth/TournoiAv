# TournamentCreationView.py

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

        
        self.tournament_controller.create_tournament(name, location, start_date_str, end_date_str, number_of_rounds)

        print(f"Le tournoi '{name}' a été enregistré.")
