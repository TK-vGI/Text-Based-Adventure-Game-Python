from termcolor import colored

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
            self.inventory[item_type] = new_item

    def __str__(self):
        return f"{self.name} the {self.species} ({self.gender}) with {", ".join(self.inventory["content"])}"

    def character_summary(self):
        print(colored(f"Your character: {self.name}, {self.species}, {self.gender}","green"))
        inventory_content = ", ".join(self.inventory["content"])
        print(colored(f"Your inventory: {inventory_content}","green"))
        print(colored(f"Difficulty: {self.difficulty.lower()}","green"))
        print(colored(f"Number of lives: {self.lives}","green"))
        print("-" * 27)
