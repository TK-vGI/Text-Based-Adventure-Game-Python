from termcolor import colored
from player_setup import create_username, create_character
from save_load import load_game
from gameplay import Game

def greeting() -> None:
    print("***Welcome to the Journey to Mount Qaf***\n")
    print("""1. Start a new game (START)\n2. Load your progress (LOAD)\n3. Quit the game (QUIT)""")

def start_game() -> bool:
    print("Starting a new game...")
    username = create_username()
    if not username:
        return False  # User backed out

    character = create_character()

    # Output comprehensive info about created character at the beginning
    print(colored(f"\nGood luck on your journey, {username}!","light_green"))
    character.character_summary()

    # Proceed to actual game loop
    game = Game(username, character)
    game.play()  # This would be your main game loop
    return True

def main():
    while True:
        greeting()
        user_input = input()
        if user_input == "1" or user_input.casefold() == "start":
            start_game()
        elif user_input == "2" or user_input.casefold() == "load":
            loaded_game = load_game()
            if loaded_game:
                loaded_game.play()
        elif user_input == "3" or user_input.casefold() in ["quit", "exit"]:
            print("Goodbye!")
            return None
        else:
            print("Unknown input! Please enter a valid one.")

if __name__ == "__main__":
    main()