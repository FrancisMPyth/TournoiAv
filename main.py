# main.py

import os

from views.main_menu import run_main_menu
from config.config import Config

def setup_directories():
    if not os.path.exists(Config.DATA_DIR):
        os.makedirs(Config.DATA_DIR)

    if not os.path.exists(Config.JOUEURS_DIR):
        os.makedirs(Config.JOUEURS_DIR)

    if not os.path.exists(Config.TOURNOIS_DIR):
        os.makedirs(Config.TOURNOIS_DIR)

def check_existing_directories():
    return os.path.exists(Config.JOUEURS_DIR) and os.path.exists(Config.TOURNOIS_DIR)

def get_available_drives():
    drives = [drive for drive in range(ord('A'), ord('Z') + 1) if os.path.exists(chr(drive) + ':')]
    return [chr(drive) + ':' for drive in drives]

def select_drive():
    available_drives = get_available_drives()

    if len(available_drives) == 1:
        return available_drives[0]

    print("Liste des disques disponibles:")
    for i, drive in enumerate(available_drives, start=1):
        print(f"{i}. {drive}")

    choice = input("Entrez le numéro du disque que vous souhaitez utiliser : ")

    try:
        choice_index = int(choice) - 1
        selected_drive = available_drives[choice_index]
        return selected_drive
    except (ValueError, IndexError):
        print("Choix invalide. Utilisation du premier disque disponible.")
        return available_drives[0]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    setup_directories()

    if not check_existing_directories():
        selected_drive = select_drive()
        Config.DATA_DIR = os.path.join(selected_drive, "data")

    run_main_menu()
