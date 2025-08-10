import json
import os
from termcolor import colored
from config import COMMANDS

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

        with open(save_path, "w") as fd:
            json.dump(data, fd, indent=4)

    def replace_placeholders(self, text):
        return text.replace("{tool}", self.character.inventory["tool_name"]) \
            .replace("{weapon}", self.character.inventory["weapon_name"]) \
            .replace("{snack}", self.character.inventory["snack_name"])

    def get_current_scene(self):
        scenes = self.story[self.current_level]["scenes"]
        return scenes[self.current_scene]

    def display_scene(self,scene):
        print(self.replace_placeholders(scene["text"]))
        color = ["blue", "magenta", "cyan"]
        for i, opt in enumerate(scene["options"]):
            print(colored(f"{i + 1}. {self.replace_placeholders(opt['option_text'])}", color[i]))

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
                if self.character.lives > 0:
                    print(colored(f"------ Lives remaining: {self.character.lives} ------","light_yellow"))
            elif action == "heal":
                self.character.lives += 1
                print(colored(f"------ Lives remaining: {self.character.lives} ------","light_green"))

            else:
                return

    def advance_level(self):
        next_level = self.story[self.current_level]["next"]
        print()
        if next_level in self.story:
            print(f"------ Level {next_level[-1]} ------")
            self.current_level = next_level
            self.current_scene = "scene1"
            return True
        else:
            print("You've completed the adventure!\n")
            return False

    def check_lives(self) -> bool:
        if self.character.lives <= 0:
            print(colored("------ You died ------", "black", "on_red", attrs=["bold"]))
            return False
        return True

    def restart_level(self): # Restart character lives, restart from the current level scene1
        self.character.lives = {
            "easy": 5,
            "medium": 3,
            "hard": 1
        }[self.character.difficulty.lower()]  # Reset lives
        self.current_scene = "scene1"  # Reset to "scene 1"

    def play(self) -> str|bool:
        while self.running:
            if not self.check_lives():  # Check health before starting scene
                self.restart_level()

            scene = self.get_current_scene() # Get current scene from story.json
            self.display_scene(scene) # Display current scene
            print() # Display empty line

            user_input = input("> ").strip().lower() # Get player input

            while user_input in COMMANDS: # User chooses game commands
                if user_input in ["/h", "help"]:
                    print(colored("Type the number of the option you want to choose.\nCommands you can use:", "yellow"))
                    print(
                        colored("/i => Shows inventory\n/q => Exits the game.\n/c => Shows the character traits.\n/s => Save the game.\n/h => Shows help.","yellow"))
                elif user_input in ["/q", "quit", "exit"]:
                    print(colored("Thanks for playing!","yellow"))
                    self.running = False
                    exit(0)
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

                    if len(selected["actions"]) != 0 :
                        self.apply_actions(selected["actions"])

                    if self.check_lives():
                        if selected["next"].lower() == "end":
                            if not self.advance_level():
                                return True
                        else:
                            self.current_scene = selected["next"]
                    else:
                        self.restart_level()
                else:
                    print("Unknown input! Please enter a valid one.")
            else:
                print("Unknown input! Please enter a valid one.")

        return True