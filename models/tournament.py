# Tournament


import json
import os
from models.round import Round

TOURNAMENT_DATA_DIR = "v:\\Projet 4\\Projet 4\\data\\tournois"

class Tournament:
    counter = 1  # Initialiser le compteur à 1

    def __init__(self):
        pass

    def create(
        self,
        name,
        location,
        start_date,
        end_date,
        number_of_rounds,
        current_round=0,
        players=[],
        rounds=[],
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.players = players
        self.current_round = current_round
        self.rounds = rounds

        self.tournament_id = self.generate_tournament_id()

    def generate_tournament_id(self):
        tournament_id = f"{self.name}_{Tournament.counter}"
        Tournament.counter += 1
        return tournament_id

    def load_all(self):
        pass

    def load(self, id):
        self.tournament_id = id

    def save(self):
        data = self.to_dict()

        if not os.path.exists(TOURNAMENT_DATA_DIR):
            os.makedirs(TOURNAMENT_DATA_DIR)

        file_path = os.path.join(TOURNAMENT_DATA_DIR, f"{self.tournament_id}.json")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def next_round(self):
        if self.current_round < self.number_of_rounds:
            self.current_round += 1
            new_round = Round()
            self.rounds.append(new_round.generate_new_round_from_tournament(self))
            self.save()

    def to_dict(self):
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": [player.to_dict() for player in self.players],  # Convertir les joueurs en dictionnaires
            "rounds": [round.to_dict() for round in self.rounds]  # Convertir les rounds en dictionnaires
        }
