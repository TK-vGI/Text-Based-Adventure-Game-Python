class Character:
    def __init__(self, name: str, species: str, gender: str,
                 snack: str, weapon: str, tool: str,
                 difficulty: str, lives: int):
        self.name = name
        self.species = species
        self.gender = gender
        self.inventory = {
            "snack_name": snack,
            "weapon_name": weapon,
            "tool_name": tool,
            "content": [snack, weapon, tool]
        }
        self.difficulty = difficulty
        self.lives = lives

    def update_item(self, item_type: str, new_item: str):
        if item_type in self.inventory:
            self.inventory[item_type] = new_item


    def __str__(self):
        return f"{self.name} the {self.species} ({self.gender}) with {self.inventory}"
