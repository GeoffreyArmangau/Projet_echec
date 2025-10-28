import random
import json
from datetime import datetime
       
class Match:
    """
    Un match unique stocké sous forme de tuple contenant deux listes.
    Chaque liste contient [joueur, score].
    """
    def __init__(self, player1, player2, score1=0, score2=0):
        """
        Initialise un match entre deux joueurs.
       
        """
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
    
    def get_match_tuple(self):
        """
        Retourne le match sous forme de tuple contenant deux listes.
        Format: ([joueur1, score1], [joueur2, score2])
        """
        return ([self.player1, self.score1], [self.player2, self.score2])
    
    # A voir si c'est dans le contrôleur
    def set_scores(self, score1, score2):
        """
        Définit les scores du match.
            
        """
        # Validation des scores (0 = défaite, 0.5 = nul, 1 = victoire)
        valid_scores = [0, 0.5, 1]
        if score1 not in valid_scores or score2 not in valid_scores:
            raise ValueError("Les scores doivent être 0, 0.5 ou 1")
        
        # Les scores doivent totaliser 1 (sauf en cas d'égalité où chacun a 0.5)
        if score1 + score2 != 1:
            raise ValueError("La somme des scores doit être égale à 1")
            
        self.score1 = score1
        self.score2 = score2
    
    # A voir si c'est dans le contrôleur
    def get_winner(self):
        """
        Retourne le joueur gagnant ou None en cas d'égalité.
        """
        if self.score1 > self.score2:
            return f'{self.player1.first_name} {self.player1.last_name}; {self.score1}'
        elif self.score2 > self.score1:
            return f'{self.player2.first_name} {self.player2.last_name}; {self.score2}'
        else:
            return f'Égalité entre {self.player1.first_name} et {self.player2.first_name}'
    
    def is_completed(self):
        """
        Vérifie si le match a été joué (scores différents de 0-0).
        """
        return self.score1 != 0 or self.score2 != 0
    
    #grouper et exécuter lors du contrôleur
    def match_dictionary(self):
        """
        Convertit le match en dictionnaire pour la sauvegarde JSON.
        """
        return {
            "player1_id": self.player1.identification,
            "player2_id": self.player2.identification,
            "score1": self.score1,
            "score2": self.score2
        }
    
    def __str__(self):
        """Représentation textuelle du match."""
        status = "Terminé" if self.is_completed() else "En attente"
        return f"{self.player1.first_name} {self.player1.last_name} ({self.score1}) vs {self.player2.first_name} {self.player2.last_name} ({self.score2}) - {status}"
