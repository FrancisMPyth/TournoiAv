# player.py

from datetime import datetime

class Player:
    def __init__(self):
        pass

    def load_all(self):
        # affiche la liste
        pass
    
    def load(self, id):
        # load un joueur spécifique
        pass
    
    def create(self, first_name, last_name, date_of_birth, chess_id, national_chess_id):
        # creer un joueur
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id
        self.national_chess_id = national_chess_id
        self.score = 0 
        pass

    def save(self):
        # sauvegarde 1 seul joueur dans la liste
        pass

    def update_one(self):
        # update 1 seul joueur dans la liste
        pass

    