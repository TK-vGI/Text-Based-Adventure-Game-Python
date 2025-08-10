from termcolor import colored
from config import COLOR_SCHEMES


class Character:
    def __init__(self, name: str, species: str, gender: str,
                 snack: str, weapon: str, tool: str,
                 difficulty: str, lives: int, content:list=None):
        self.name = name
        self.species = species
        self.gender = gender
        self.inventory = {
            "snack_name": snack,
            "weapon_name": weapon,
            "tool_name": tool,
            "content": [snack, weapon, tool] if content is None else content
        }
        self.difficulty = difficulty
        self.lives = lives

    def update_item(self, item_type: str, new_item: str):
        if item_type in self.inventory:
            old_item = self.inventory[item_type]
            self.inventory[item_type] = new_item
            # Update the content list to reflect the change
            if old_item in self.inventory["content"]:
                index = self.inventory["content"].index(old_item)
                self.inventory["content"][index] = new_item

    def add_item(self, item: str):
        self.inventory["content"].append(item)
        print(colored(f"------ Item added: {item} ------", *COLOR_SCHEMES["item_added"]))

    def remove_item(self, item: str) -> bool:
        if item in self.inventory["content"]:
            self.inventory["content"].remove(item)
            print(colored(f"------ Item removed: {item} ------", *COLOR_SCHEMES["item_removed"]))
            return True
        return False

    def __str__(self):
        return f"{self.name} the {self.species} ({self.gender}) with {", ".join(self.inventory["content"])}"

    def character_summary(self):
        scheme = COLOR_SCHEMES["character_summary"]
        print(colored(f"Your character: {self.name}, {self.species}, {self.gender}",*scheme))
        inventory_content = ", ".join(self.inventory["content"])
        print(colored(f"Your inventory: {inventory_content}",*scheme))
        print(colored(f"Difficulty: {self.difficulty.lower()}",*scheme))
        print(colored(f"Number of lives: {self.lives}",*scheme))
        print("-" * 27)