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
    
    