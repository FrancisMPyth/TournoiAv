# round.py
from .match import Match
from datetime import datetime

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
