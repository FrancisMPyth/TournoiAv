# Tournament

import json
import os

from models.round import Round
from config.config import Config

class Tournament:
    counter = 1  
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
        players=None,  
        rounds=None,
    ):
        if players is None:
            players = []  
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

    def generate_player_ranking(self):
        ranking = sorted(self.players, key=lambda x: x.score, reverse=True)
        return ranking






    def next_round(self):
        if self.current_round < self.number_of_rounds:
            self.current_round += 1
            new_round = Round(self.current_round)  
            new_round.generate_new_round_from_tournament(self, self.players)  
            self.rounds.append(new_round)

            for match in self.rounds[-1].matches:
                player1 = match.player1
                player2 = match.player2
                player1.update_score(match.score_player1)
                player2.update_score(match.score_player2)

            ranking = self.generate_player_ranking()
            self.save()




    def save_ranking(self, ranking):
        self.ranking = ranking 
        file_path = os.path.join(Config.TOURNOIS_DIR, f"{self.tournament_id}.json")
        with open(file_path, "w") as file:
            json.dump(self.__dict__, file, indent=4)
