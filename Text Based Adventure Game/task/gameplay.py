from termcolor import colored
from config import COMMANDS,COLOR_SCHEMES,DIFFICULTY_MAP
from save_load import save_game
from story import Story

class Game:
    def __init__(self, username, character, game_state=None):
        self.username = username
        self.character = character
        self.running = True

        if game_state is None:
            game_state = ["level1", "scene1"]
        self.current_level = game_state[0]
        self.current_scene = game_state[1]

        self.story = Story()

    def replace_placeholders(self, text):
        return text.replace("{tool}", self.character.inventory["tool_name"]) \
            .replace("{weapon}", self.character.inventory["weapon_name"]) \
            .replace("{snack}", self.character.inventory["snack_name"])

    def get_current_scene(self):
        return self.story.get_scene(self.current_level, self.current_scene)

    def display_scene(self, scene):
        print(self.replace_placeholders(scene["text"]))
        color = ["blue", "magenta", "cyan"]
        for i, opt in enumerate(scene["options"]):
            print(colored(f"{i + 1}. {self.replace_placeholders(opt['option_text'])}", color[i]))

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
                self.character.add_item(item)
            elif action.startswith("-"):
                item = action[1:]
                self.character.remove_item(item)
            elif action == "hit":
                self.character.lives -= 1
                if self.character.lives > 0:
                    print(colored(f"------ Lives remaining: {self.character.lives} ------", *COLOR_SCHEMES["hit"]))
            elif action == "heal":
                self.character.lives += 1
                print(colored(f"------ Lives remaining: {self.character.lives} ------", *COLOR_SCHEMES["heal"]))

    def check_lives(self) -> bool:
        if self.character.lives <= 0:
            print(colored("------ You died ------", *COLOR_SCHEMES["died"]))
            return False
        return True

    def restart_level(self):
        self.character.lives = DIFFICULTY_MAP[self.character.difficulty.lower()][1]
        self.current_scene = "scene1"

    def play(self) -> str|bool:
        while self.running:
            if not self.check_lives():
                self.restart_level()

            scene = self.get_current_scene()
            self.display_scene(scene)
            print()

            user_input = input("> ").strip().lower()

            while user_input in COMMANDS:
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
                    save_game(self)
                    print(colored(f"Game saved!","yellow"))
                print()
                user_input = input("> ").strip().lower()

            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(scene["options"]):
                    selected = scene["options"][index]
                    print()
                    text = self.replace_placeholders(selected["result_text"])
                    print(colored(text,*COLOR_SCHEMES["result_text"]))

                    if len(selected["actions"]) != 0:
                        self.apply_actions(selected["actions"])

                    if self.check_lives():
                        if selected["next"].lower() == "end":
                            next_level = self.story.advance_level(self.current_level)
                            if next_level:
                                print(f"------ Level {next_level[-1]} ------", *COLOR_SCHEMES["level_header"])
                                self.current_level = next_level
                                self.current_scene = "scene1"
                            else:
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