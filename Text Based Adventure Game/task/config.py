# Existing commands
COMMANDS = {"/i": "Shows inventory.",
            "/q": "Exits the game.",
            "/c": "Shows the character traits.",
            "/s": "Save the game.",
            "/h": "Shows help."}

# File paths
STORY_FILE_PATH = "data/story.json"
SAVE_DIR = "data/saves"
SAVE_FILE_EXTENSION = ".json"  # For consistency in save file naming

# Difficulty settings
DIFFICULTY_MAP = {
    "1": ("easy", 5),
    "2": ("medium", 3),
    "3": ("hard", 1),
    "easy": ("easy", 5),
    "medium": ("medium", 3),
    "hard": ("hard", 1)
}

# Color schemes for termcolor (keys: message type, values: tuple of (color, on_color, attrs))
COLOR_SCHEMES = {
    "character_summary": ("green", None, None),  # e.g., for character_summary prints
    "inventory": ((255, 105, 180), None, None),  # RGB for custom colors
    "success": ("light_green", None, None),
    "warning": ("light_yellow", None, None),
    "error": ("white", "on_red", ["bold"]),

    "item_added": ("black", "on_green", None),
    "item_removed": ("white", "on_red", None),
    "hit": ("light_yellow", None),
    "heal": ("light_green", None),
    "died": ("black", "on_red", ["bold"]),

    "result_text": ("magenta", None, ["dark", "blink", "concealed"]),
    "commands_help": ("yellow", None, None),
    "level_header": ("cyan", None, ["bold"])  # For level announcements
}

# Other game settings
MAX_INVENTORY_SIZE = 10  # Example: Limit inventory items
DEFAULT_PROMPT = "> "  # Customizable input prompt