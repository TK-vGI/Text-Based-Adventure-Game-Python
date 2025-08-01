import json
import os
from termcolor import colored
from Character import Character

COMMANDS = {"/i": "Shows inventory.",
            "/q": "Exits the game.",
            "/c": "Shows the character traits.",
            "/s": "Save the game.",
            "/h": "Shows help."}


class Game:
    def __init__(self, username, character, game_state=None):
        self.username = username
        self.character = character  # carries tool, weapon, snack, name, species, lives, etc.
        self.running = True

        if game_state is None:
            game_state = ["level1", "scene1"]
        self.current_level = game_state[0]
        self.current_scene = game_state[1]

        # Load the structured story
        with open('data/story.json', 'r') as f:
            self.story = json.load(f)

    def save_game(self):
        data = {
            "character": {
                "name": self.character.name,
                "species": self.character.species,
                "gender": self.character.gender
            },
            "inventory": {
                "snack_name": self.character.inventory["snack_name"],
                "weapon_name": self.character.inventory["weapon_name"],
                "tool_name": self.character.inventory["tool_name"],
                "content": self.character.inventory["content"]
            },
            "progress": {
                "level": self.current_level,
                "scene": self.current_scene
            },
            "lives": self.character.lives,
            "difficulty": self.character.difficulty
        }
        save_dir = "data/saves"
        os.makedirs(save_dir, exist_ok=True)  # Ensure the folder exists
        save_path = os.path.join(save_dir, f"{self.username}.json")

        # if os.path.exists(save_path):
        #     print("------ Save file updated! ------")
        # else:
        #     print("------ New save file created! ------")

        with open(save_path, "w") as fd:
            json.dump(data, fd, indent=4)

    def replace_placeholders(self, text):
        return text.replace("{tool}", self.character.inventory["tool_name"]) \
            .replace("{weapon}", self.character.inventory["weapon_name"]) \
            .replace("{snack}", self.character.inventory["snack_name"])

    def get_current_scene(self):
        scenes = self.story[self.current_level]["scenes"]
        return scenes[self.current_scene]

    def display_scene(self):
        scene = self.get_current_scene()
        print(self.replace_placeholders(scene["text"]))
        for i, opt in enumerate(scene["options"]):
            print(f"{i + 1}. {self.replace_placeholders(opt['option_text'])}")

    def choose_option(self, index):
        scene = self.get_current_scene()
        option = scene["options"][index]
        print(self.replace_placeholders(option["result_text"]))
        self.apply_actions(option["actions"])
        next_scene = option["next"]
        if next_scene == "end":
            self.advance_level()
        else:
            self.current_scene = next_scene

    def add_item_to_inventory_content(self, item: str):
        self.character.inventory["content"].append(item)

    def remove_item_from_inventory_content(self, item):
        if item in self.character.inventory["content"]:
            self.character.inventory["content"].remove(item)
            return True
        return False

    def apply_actions(self, actions):
        for action in actions:
            action = self.replace_placeholders(action)
            if action.startswith("+"):
                item = action[1:]
                self.add_item_to_inventory_content(item)
                print(colored(f"------ Item added: {item} ------","black", "on_green"))
            elif action.startswith("-"):
                item = action[1:]
                if self.remove_item_from_inventory_content(item):
                    print(colored(f"------ Item removed: {item} ------","white", "on_red"))
            elif action == "hit":
                self.character.lives -= 1
                if self.character.lives != 0:
                    print(colored(f"------ Lives remaining: {self.character.lives} ------","light_yellow"))
            elif action == "heal":
                self.character.lives += 1
                print(colored(f"------ Lives remaining: {self.character.lives} ------","light_green"))

    def advance_level(self):
        next_level = self.story[self.current_level]["next"]
        if next_level in self.story:
            print(f"Advancing to {next_level}...\n")
            self.current_level = next_level
            self.current_scene = "scene1"
        else:
            print("You've completed the adventure!")

    def play(self):
        # print(f"\nWelcome to Level 1, {self.username}!") # Not in output
        while self.running:
            # Check health before starting scene
            if self.character.lives <= 0:
                print(colored("------ You died ------","black", "on_red",attrs=["bold"]))
                self.character.lives = {
                    "easy": 5,
                    "medium": 3,
                    "hard": 1
                }[self.character.difficulty.lower()]
                self.current_scene = "scene1"

            # Get current scene from story.json
            scene = self.get_current_scene()

            # Display current scene
            print(self.replace_placeholders(scene["text"]))
            color=["blue","magenta","cyan"]
            for i, opt in enumerate(scene["options"]):
                print(colored(f"{i + 1}. {self.replace_placeholders(opt['option_text'])}",color[i]))
            print()

            # Get player input
            user_input = input("> ").strip().lower()

            while user_input in COMMANDS:
                # User chooses game commands
                if user_input in ["/h", "help"]:
                    print(colored("Type the number of the option you want to choose.\nCommands you can use:", "yellow"))
                    print(
                        colored("/i => Shows inventory\n/q => Exits the game.\n/c => Shows the character traits.\n/s => Save the game.\n/h => Shows help.","yellow"))
                elif user_input in ["/q", "quit", "exit"]:
                    print(colored("Thanks for playing!","yellow"))
                    self.running = False
                    return
                elif user_input in ["/i", "inventory"]:
                    inventory_content_txt = ", ".join(self.character.inventory["content"])
                    print(colored(f"Inventory: {inventory_content_txt}",(255, 105, 180)))
                elif user_input in ["/c", "character"]:
                    print(colored(f"Your character: {self.character.name}, {self.character.species}, {self.character.gender}","magenta"))
                    print(colored(f"Lives remaining: {self.character.lives}","magenta"))
                elif user_input in ["/s", "save"]:
                    self.save_game()
                    print(colored(f"Game saved!","yellow"))
                print()
                user_input = input("> ").strip().lower()

            # Validate input - user chooses option from the story
            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(scene["options"]):
                    selected = scene["options"][index]
                    print()
                    text = self.replace_placeholders(selected["result_text"])
                    print(colored(text,"magenta",attrs=["dark","blink","concealed"]))
                    self.apply_actions(selected["actions"])
                    if selected["next"].lower() == "end":
                        print("\n------ Level 2 ------")
                        break
                    else:
                        self.current_scene = selected["next"]
                else:
                    print("Unknown input! Please enter a valid one.")
            else:
                print("Unknown input! Please enter a valid one.")


def greeting() -> None:
    print("***Welcome to the Journey to Mount Qaf***\n")


def show_menu():
    print("""1. Start a new game (START)
2. Load your progress (LOAD)
3. Quit the game (QUIT)""")


def start_game() -> bool:
    print("Starting a new game...")
    username = create_username()
    if not username:
        return False  # User backed out

    character = create_character()
    user_profiles[username] = character  # Store in dict {"username" : Character.instance}

    # Output comprehensive info about created character at the beginning
    print(f"\nGood luck on your journey, {username}!")
    print(f"Your character: {character.name}, {character.species}, {character.gender}")
    print(f"Your inventory:",", ".join(character.inventory["content"]))
    print(f"Difficulty: {character.difficulty.lower()}")
    print(f"Number of lives: {character.lives}")
    print("-" * 27)

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


def load_game() -> Game| None:
    print("No saved data found")

user_profiles = {}


def main():
    while True:
        greeting()
        show_menu()
        user_input = input()
        if user_input == "1" or user_input.casefold() == "start":
            if start_game():
                break
        elif user_input == "2" or user_input.casefold() == "load":
            load_game()
            exit(0)
        elif user_input == "3" or user_input.casefold() in ["quit", "exit"]:
            print("Goodbye!")
            return
        else:
            print("Unknown input! Please enter a valid one.")


if __name__ == "__main__":
    main()
