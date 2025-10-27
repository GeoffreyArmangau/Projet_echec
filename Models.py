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


class Round:
    """
    Représente un tour de tournoi contenant une liste de matchs.
    """
    def __init__(self, name, matches=None):
        """
        Initialise un tour.
        
        Args:
            name (str): Nom du tour (ex: "Round 1", "Round 2")
            matches (list): Liste des matchs du tour
        """
        self.name = name
        self.matches = matches if matches is not None else []
        self.start_datetime = None
        self.end_datetime = None
        self.is_started = False
        self.is_completed = False
    
    def start_round(self):
        """
        Démarre le tour en enregistrant la date et heure de début.
        """
        if self.is_started:
            raise ValueError("Le tour a déjà été démarré")
            
        self.start_datetime = datetime.now()
        self.is_started = True
        print(f"🚀 Tour '{self.name}' démarré le {self.start_datetime.strftime('%d/%m/%Y à %H:%M:%S')}")
    
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
    
    def add_match(self, match):
        """
        Ajoute un match au tour.
        
        Args:
            match (Match): Le match à ajouter
        """
        if self.is_completed:
            raise ValueError("Impossible d'ajouter un match à un tour terminé")
            
        self.matches.append(match)
    
    def all_matches_completed(self):
        """
        Vérifie si tous les matchs du tour sont terminés.
        """
        return all(match.is_completed() for match in self.matches)
    
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
    
    def round_to_dict(self):
        """
        Convertit le tour en dictionnaire pour la sauvegarde JSON.
        """
        return {
            "name": self.name,
            "start_datetime": self.start_datetime.isoformat() if self.start_datetime else None,
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
            "is_started": self.is_started,
            "is_completed": self.is_completed,
            "matches": [match.match_dictionary_to_json() for match in self.matches]
        }
    
    def get_duration(self):
        """
        Retourne la durée du tour si celui-ci est terminé.
        """
        if self.is_completed and self.start_datetime and self.end_datetime:
            return self.end_datetime - self.start_datetime
        return None
    
    def __str__(self):
        """Représentation textuelle du tour."""
        status = "Terminé" if self.is_completed else ("En cours" if self.is_started else "Pas démarré")
        return f"{self.name} - {len(self.matches)} matchs - {status}"


class Tournament:
    def __init__(self, name, location, beginning_date, end_date, lap = 4, actual_lap=0, laps = [], players = [], description=""):
        self.name = name
        self.location = location
        self.beginning_date = beginning_date
        self.end_date = end_date
        self.lap = lap
        self.actual_lap = actual_lap
        self.laps = laps
        self.players = players
        self.description = description
