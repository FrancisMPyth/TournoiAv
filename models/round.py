# round.py

from datetime import datetime

from .match import Match

class Round:
    def __init__(self, numero_tour, heure_debut=None):
        self.numero_tour = numero_tour
        self.matchs = []
        self.heure_debut = heure_debut
        self.heure_fin = None
        self.score = 0  

    def ajouter_match(self, match):
        self.matchs.append(match)

    def definir_resultat(self, index_match, score_joueur1, score_joueur2):
        match = self.matchs[index_match]
        match.definir_resultat(score_joueur1, score_joueur2)

    def mettre_a_jour_score(self, resultat_match):
        self.score += resultat_match

    def generate_new_round_from_tournament(self, tournament, players):
        if len(players) % 2 != 0:
            raise ValueError("Le nombre de joueurs doit être pair pour créer des matchs.")

        sorted_players = sorted(players, key=lambda x: x.score, reverse=True)

        for i in range(0, len(sorted_players), 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]
            new_match = Match(player1, player2)
            self.ajouter_match(new_match)
