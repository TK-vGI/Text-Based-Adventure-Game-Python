from character import Character
from config import DIFFICULTY_MAP

def create_username() -> str | None:
    while True:
        username = input("Enter a username ('/b' to go back): ")
        if username.lower() == "/b":
            return None
        elif not username.strip():
            print("Username cannot be empty.")
        else:
            break
    return username

def create_character() -> Character | None:
    print("Create your character:")
    name = input("\tName: ")
    species = input("\tSpecies: ")
    gender = input("\tGender: ")
    print("Pack your bag for the journey:")
    snack = input("\tSnack: ")
    weapon = input("\tWeapon: ")
    tool = input("\tTool: ")

    while True:
        print("Choose your difficulty:\n\t1. Easy\n\t2. Medium\n\t3. Hard")
        choice = input()
        if choice.lower() in DIFFICULTY_MAP:  # Use the map
            difficulty, lives = DIFFICULTY_MAP[choice.lower()]
            break
        else:
            print("Unknown input! Please enter a valid one.")
    return Character(name, species, gender, snack, weapon, tool, difficulty, lives)