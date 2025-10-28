from Models.Match import Match
from Models.player import Player
from Models.Tournament import Tournament
from Models.Round import Round
import json
import random
from datetime import datetime

"""
Reste à faire:
    - Créer la première ronde avec les joueurs dans l'ordre (1,2,3,4)
    - Faire les rondes suivantes en fonction des scores (random si scores égaux)
    - Problème de gestion des paires (deux joueurs peuvent se rencontrer deux fois)
    - corriger la sauvegarde
    - Réaliser les rapports
"""

class Controllers:
    def __init__(self):
        pass
    
    #=======================Tournoi======================
    """
    Gère les contrôleurs de tournoi
    """

    def create_tournament(self, name, location, beginning_date, end_date, lap=4, description=""):
        tournament = Tournament(
            name,
            location,
            beginning_date,
            end_date,
            lap=lap, 
            description=description
        )
        return tournament
    
    #======================Joueurs========================
    """
    Gère les contrôleurs de joueurs
    """
    def add_player_to_tournament(self, tournament, player):
        tournament.players.append(player)
        return tournament
    
    #======================Rounds========================
    """
    Gère les contrôleurs de rounds
    """
    def add_match_to_round(self, round_obj, match):
        """
        Ajoute un match au tour.
        
        """
        if round_obj.is_completed:
            raise ValueError("Impossible d'ajouter un match à un tour terminé")
            
        round_obj.matches.append(match)
        return round_obj
    
    def get_round_results(self):
        """
        Retourne les résultats du tour sous forme de dictionnaire.
        """
        results = {}
        for match in self.matches:
            # Ajouter les points pour chaque joueur
            player1_id = match.player1.identification
            player2_id = match.player2.identification
            
            if player1_id not in results:
                results[player1_id] = {"player": match.player1, "points": 0, "matches": 0}
            if player2_id not in results:
                results[player2_id] = {"player": match.player2, "points": 0, "matches": 0}
            
            results[player1_id]["points"] += match.score1
            results[player2_id]["points"] += match.score2
            results[player1_id]["matches"] += 1
            results[player2_id]["matches"] += 1
        
        return results
    
    def round_dictionary(self):
        """
        Convertit le tour en dictionnaire pour la sauvegarde JSON.
        """
        return {
            "name": self.name,
            "start_datetime": self.start_datetime.isoformat() if self.start_datetime else None,
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
            "is_started": self.is_started,
            "is_completed": self.is_completed,
            "matches": [match.match_to_dict() for match in self.matches]
        }

    def start_round(self):
        """
        Démarre le tour en enregistrant la date et heure de début.
        """
        if self.is_started:
            raise ValueError("Le tour a déjà été démarré")
            
        self.start_datetime = datetime.now()
        self.is_started = True
        print(f"Tour '{self.name}' démarré le {self.start_datetime.strftime('%d/%m/%Y à %H:%M:%S')}")
    
    def end_round(self):
        """
        Termine le tour en enregistrant la date et heure de fin.
        """
        if not self.is_started:
            raise ValueError("Le tour doit être démarré avant d'être terminé")
            
        if self.is_completed:
            raise ValueError("Le tour est déjà terminé")
            
        # Vérifier que tous les matchs sont terminés
        if not self.all_matches_completed():
            raise ValueError("Tous les matchs doivent être terminés avant de clôturer le tour")
            
        self.end_datetime = datetime.now()
        self.is_completed = True
        duration = self.end_datetime - self.start_datetime
        print(f"Tour '{self.name}' terminé le {self.end_datetime.strftime('%d/%m/%Y à %H:%M:%S')}")
        print(f"Durée: {duration}")
      
    def all_matches_completed(self):
        """
        Vérifie si tous les matchs du tour sont terminés.
        """
        return all(match.is_completed() for match in self.matches)
               
    def __str__(self):
        """Représentation textuelle du tour."""
        status = "Terminé" if self.is_completed else ("En cours" if self.is_started else "Pas démarré")
        return f"{self.name} - {len(self.matches)} matchs - {status}"


    #=======================Match========================
    """
    Gère les contrôleurs de match
    """
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
    
    def get_winner(self):
        """
        Retourne le joueur gagnant ou égalité.
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
    
    #=======================Save========================

    def save_results_dictionary(self, round):
        results = round.get_round_results()
        return results
    
    def save_to_json(self, tournament, filename='tournaments.json'):
        try:
            with open(filename, 'r') as file:
                tournaments = json.load(file)
        except FileNotFoundError:
            tournaments = []
        
        tournaments.append(tournament.Tournament_Dictionary())
        
        with open(filename, 'w') as file:
            json.dump(tournaments, file, indent=4)
    