from Models.Match import Match
from Models.player import Player
from Models.Tournament import Tournament
from Models.Round import Round
import json
import random
from datetime import datetime

class Controllers:
    def __init__(self):
        pass

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
    
    def add_player_to_tournament(self, tournament, player):
        tournament.players.append(player)
        return tournament
    
    def generate_pair_of_players(self, player1, player2):
        """
        Genère des paires aléatoires de joueurs mais jamais deux fois la même paire.
        """
        match = Match(player1, player2)
        return match
    
    def beggin_round(self, round):
        round.start_round()
        return round
    
    def end_round(self, round):
        round.end_round()
        return round
    
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

    

    

