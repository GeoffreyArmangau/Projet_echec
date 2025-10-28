import random
import json
from datetime import datetime

class Round:
    def __init__(self, round_number = int, matches=None):
        """
        Initialise un tour.
               
        """
        
        self.name = f'Ronde n°{round_number}'
        self.matches = matches if matches is not None else []
        self.start_datetime = None
        self.end_datetime = None
        self.is_started = False
        self.is_completed = False
    
    #sans doute à décaler dans le contrôleur
    def add_match(self, match):
        """
        Ajoute un match au tour.
        
        """
        if self.is_completed:
            raise ValueError("Impossible d'ajouter un match à un tour terminé")
            
        self.matches.append(match)
    
    # A voir si c'est dans le contrôleur
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
    
    # A regrouper et exécuter dans le contrôleur
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

    # A mettre dans le controleur
    def start_round(self):
        """
        Démarre le tour en enregistrant la date et heure de début.
        """
        if self.is_started:
            raise ValueError("Le tour a déjà été démarré")
            
        self.start_datetime = datetime.now()
        self.is_started = True
        print(f"Tour '{self.name}' démarré le {self.start_datetime.strftime('%d/%m/%Y à %H:%M:%S')}")
    
    #A mettre dans le contrôleur
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