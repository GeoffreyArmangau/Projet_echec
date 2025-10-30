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

    def Tournament_Dictionary(self):
        return {
            "name": self.name,
            "location": self.location,
            "beginning_date": self.beginning_date,
            "end_date": self.end_date,
            "lap": self.lap,
            "actual_lap": self.actual_lap,
            "laps": [lap.round_to_dict() for lap in self.laps],
            "players": [player.Player_Dictionary() for player in self.players],
            "description": self.description
        }
    