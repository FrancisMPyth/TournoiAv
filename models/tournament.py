# tournament.py

import json
import os
from models.round import Round

TOURNAMENT_DATA_DIR = "v:\\Projet 4\\Projet 4\\data\\tournois"

class Tournament:
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
        # récupération en BDD du dernier id de tournoi (last_tournament_id)
        # self.tournament_id = last_tournament_id + 1
        self.tournament_id = None 
        self.name = name  # Ajoute cette ligne
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.players = players
        self.current_round = current_round
        self.rounds = rounds


    def load_all(self):
        pass

    def load(self, id):
        self.tournament_id = id
        # récupération du reste depuis le fichier
        # self.name = name
        # self.location = location
        # self.start_date = start_date
        # self.end_date = end_date
        # self.number_of_rounds = number_of_rounds
        # self.players = players
        # self.current_round = current_round
        # self.rounds = rounds

    def save(self):
        data = self.to_dict()

        if not os.path.exists(TOURNAMENT_DATA_DIR):
            os.makedirs(TOURNAMENT_DATA_DIR)

        file_path = os.path.join(TOURNAMENT_DATA_DIR, f"{self.name}_{self.tournament_id}.json")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def next_round(self):
        if self.current_round < self.number_of_rounds:
            self.current_round += 1
            # 1 -> créer le round
            new_round = Round()
            self.rounds.append(new_round.generate_new_round_from_tournament(self))
            # 2 -> save le tournoi
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
            "players": self.players,
            "rounds": self.rounds
        }
