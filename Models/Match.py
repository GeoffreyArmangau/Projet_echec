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
    
   