# main.py



import os
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from tournament_views.PlayerListView import PlayerListView
from tournament_views.TournamentCreationView import TournamentCreationView
from tournament_views.TournamentListView import TournamentListView
from tournament_views.TournamentManagementView import TournamentManagementView
from config import DATA_DIR, TOURNOIS_DIR, GESTION_TOURNOIS_DIR, JOUEURS_DIR






def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    player_controller = PlayerController()
    tournament_controller = TournamentController(player_controller)

    player_list_view = PlayerListView()
    tournament_creation_view = TournamentCreationView(tournament_controller, player_controller)
    tournament_list_view = TournamentListView()
    tournament_management_view = TournamentManagementView(tournament_controller, player_controller)

    while True:
        clear_screen()
        print("Menu Principal:")
        print("1. Enregistrement des Joueurs")
        print("2. Afficher la liste des joueurs")
        print("3. Enregistrer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Gestion des Tournois")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")

        if choice == "1":
            player_list_view.create_player(player_controller)
        elif choice == "2":
            player_list_view.display_player_list(player_controller)
        elif choice == "3":
            tournament_creation_view.create_tournament()
        elif choice == "4":
            tournament_list_view.display_tournaments(tournament_controller)
            input("Appuyez sur une touche pour continuer...")
        elif choice == "5":
            tournament_list_view.display_tournaments(tournament_controller)
            tournament_id = input("Spécifiez l'identifiant du tournoi à gérer ('q' pour quitter) : ")
            if tournament_id.lower() == "q":
                continue
            tournament = None
            for t in tournament_controller.get_tournaments():
                if t.tournament_id == tournament_id:
                    tournament = t
                    break
            if tournament is not None:
                tournament_management_view.tournament_sub_menu(tournament)  
        elif choice.lower() == "q":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
