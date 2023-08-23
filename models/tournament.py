# tournament.py


class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date, number_of_rounds, players):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.players = players
        self.rounds = []
        self.first_round_results_recorded = False  
