# Tournament

import json
import os
from models.round import Round
from config.config import Config

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
        if not os.path.exists(Config.TOURNOIS_DIR):
            os.makedirs(Config.TOURNOIS_DIR)

        file_path = os.path.join(Config.TOURNOIS_DIR, f"{self.tournament_id}.json")

        with open(file_path, "w") as file:
            json.dump(self.__dict__, file, indent=4)

    def next_round(self):
        if self.current_round < self.number_of_rounds:
            self.current_round += 1
            new_round = Round()
            self.rounds.append(new_round.generate_new_round_from_tournament(self))
            self.save()
