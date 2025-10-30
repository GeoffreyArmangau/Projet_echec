import json 

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

    # ce qui suit est surement à décaler dans le contrôleur, car cela doit se faire en dernier
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