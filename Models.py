import random
import json
from datetime import datetime

class Player:
    def __init__(self, first_name, last_name, date_of_birth, age, identification):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.age = age
        self.identification = identification
    
    def Player_Dictionary(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "age": self.age,
            "identification": self.identification
        }

    def Save_player_to_json(self):
        try:
            with open('players.json', 'r') as file:
                players = json.load(file)
        except FileNotFoundError:
            players = []
        
        players.append(self.Player_Dictionary())
        
        with open('players.json', 'w') as file:
            json.dump(players, file, indent=4)

    def load_players_from_json():
        try:
            with open('players.json', 'r') as file:
                players_data = json.load(file)
                players = []
                for Player_data in players_data:
                    player = Player(
                        Player_data['first_name'],
                        Player_data['last_name'],
                        Player_data['date_of_birth'],
                        Player_data['age'],
                        Player_data['identification']
                    )
                    players.append(player)
                return players
        except FileNotFoundError:
            return []
        
class Match:
    """
    Un match unique stocké sous forme de tuple contenant deux listes.
    Chaque liste contient [joueur, score].
    """
    def __init__(self, player1, player2, score1=0, score2=0):
        """
        Initialise un match entre deux joueurs.
        
        Args:
            player1 (Player): Premier joueur
            player2 (Player): Deuxième joueur  
            score1 (float): Score du premier joueur (0, 0.5 ou 1)
            score2 (float): Score du deuxième joueur (0, 0.5 ou 1)
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
    
    def set_scores(self, score1, score2):
        """
        Définit les scores du match.
        
        Args:
            score1 (float): Score du premier joueur
            score2 (float): Score du deuxième joueur
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
    
    def get_winner(self):
        """
        Retourne le joueur gagnant ou None en cas d'égalité.
        """
        if self.score1 > self.score2:
            return self.player1
        elif self.score2 > self.score1:
            return self.player2
        else:
            return None  # Égalité
    
    def is_completed(self):
        """
        Vérifie si le match a été joué (scores différents de 0-0).
        """
        return self.score1 != 0 or self.score2 != 0
    
    def match_dictionary_to_json(self):
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


