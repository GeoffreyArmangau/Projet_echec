from Models import Player, Tournament, Round, Match
import json
"""Menu principal de gestion des tournois d'echecs."""

class MainMenu:
    def display(self):
        print("=== Menu Principal ===")
        print("1. Gérer les joueurs")
        print("2. Gérer les tournois")
        print("3. Gérer les rondes")
        print("4. Gérer les matchs")
        print("5. Quitter")

    def get_user_choice(self):
        choice = input("Veuillez choisir une option (1-5): ")
        return choice
    
    def handle_choice(self, choice):
        if choice == '1':
            self.manage_players()
        elif choice == '2':
            self.manage_tournaments()
        elif choice == '3':
            self.manage_rounds()
        elif choice == '4':
            self.manage_matches()
        elif choice == '5':
            print("Au revoir!")
        else:
            print("Choix invalide. Veuillez réessayer.")
    
    