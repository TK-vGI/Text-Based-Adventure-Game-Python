from character import Character
from gameplay import *


def greeting() -> None:
    print("***Welcome to the Journey to Mount Qaf***\n")
    print("""1. Start a new game (START)\n2. Load your progress (LOAD)\n3. Quit the game (QUIT)""")


def start_game() -> bool:
    print("Starting a new game...")
    username = create_username()
    if not username:
        return False  # User backed out

    character = create_character()
    user_profiles[username] = character  # Store in dict {"username" : Character.instance}

    # Output comprehensive info about created character at the beginning
    print(colored(f"\nGood luck on your journey, {username}!","light_green"))
    character.character_summary()

    # Proceed to actual game loop
    game = Game(username, character)
    game.play()  # This would be your main game loop
    return True


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


def create_character() -> Character:
    print("Create your character:")
    name = input("\tName: ")
    species = input("\tSpecies: ")
    gender = input("\tGender: ")
    print("Pack your bag for the journey:")
    snack = input("\tSnack: ")
    weapon = input("\tWeapon: ")
    tool = input("\tTool: ")
    difficulty_map = {"1": ("easy", 5), "2": ("medium", 3), "3": ("hard", 1),
                      "easy": ("easy", 5), "medium": ("medium", 3), "hard": ("hard", 1)}
    while True:
        print("Choose your difficulty:\n\t1. Easy\n\t2. Medium\n\t3. Hard")
        choice = input()
        if choice.lower() in difficulty_map:
            difficulty, lives = difficulty_map[choice.lower()]
            break
        else:
            print("Unknown input! Please enter a valid one.")
    return Character(name, species, gender, snack, weapon, tool, difficulty, lives)


def load_game() -> Game| bool:
    save_dir = "data/saves"

    files = [f[:-5] for f in os.listdir(save_dir) if f.endswith(".json")]
    if not files:
        print("No saved games available.")
        return False

    print("Choose username (/b - back):\n")
    for f in files:
        print(f)
    print()

    while True:
            user_input = input("> ").strip().lower()
            if user_input.lower() == "/b":
                return False # Return to main menu
            elif user_input in [name.lower() for name in files]:
                filename = f"{user_input}.json"
                filepath = os.path.join(save_dir, filename)

                with open(filepath, "r") as f:
                    data = json.load(f)
                print("Loading your progress...\n")

                # Rebuild character and progress
                username = user_input
                character = Character(
                    name=data["character"]["name"],
                    species=data["character"]["species"],
                    gender=data["character"]["gender"],
                    snack=data["inventory"]["snack_name"],
                    weapon=data["inventory"]["weapon_name"],
                    tool=data["inventory"]["tool_name"],
                    difficulty=data["difficulty"],
                    lives=data["lives"],
                    content=data["inventory"]["content"],
                )

                game_state = [str(data["progress"]["level"]), str(data["progress"]["scene"])]
                game_loaded = Game(username, character,game_state)

                print(f"------ Level {game_loaded.current_level[-1]} ------")
                game_loaded.play()

                return True  # All loaded

            else:
                print("Unknown input! Please enter a valid one.")

user_profiles = {}


def main():
    while True:
        greeting()
        user_input = input()
        if user_input == "1" or user_input.casefold() == "start":
            start_game()
        elif user_input == "2" or user_input.casefold() == "load":
            load_game()
        elif user_input == "3" or user_input.casefold() in ["quit", "exit"]:
            print("Goodbye!")
            return None
        else:
            print("Unknown input! Please enter a valid one.")


if __name__ == "__main__":
    main()
