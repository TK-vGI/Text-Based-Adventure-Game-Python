import json
import os

from character import Character
from config import SAVE_DIR, SAVE_FILE_EXTENSION


def save_game(game):
    try:
        data = {
            "character": {
                "name": game.character.name,
                "species": game.character.species,
                "gender": game.character.gender
            },
            "inventory": {
                "snack_name": game.character.inventory["snack_name"],
                "weapon_name": game.character.inventory["weapon_name"],
                "tool_name": game.character.inventory["tool_name"],
                "content": game.character.inventory["content"]
            },
            "progress": {
                "level": game.current_level,
                "scene": game.current_scene
            },
            "lives": game.character.lives,
            "difficulty": game.character.difficulty
        }
        os.makedirs(SAVE_DIR, exist_ok=True)  # Use SAVE_DIR
        save_path = os.path.join(SAVE_DIR, f"{game.username}{SAVE_FILE_EXTENSION}")
        with open(save_path, "w") as fd:
            json.dump(data, fd, indent=4)

    except PermissionError:
        print("Error: Unable to save game due to permission issues.")
        return False

    except Exception as e:
        print(f"Error saving game: {str(e)}")
        return False
    return True

def load_game():
    from gameplay import Game
    try:
        files = [f[:-len(SAVE_FILE_EXTENSION)] for f in os.listdir(SAVE_DIR) if f.endswith(SAVE_FILE_EXTENSION)]
    except FileNotFoundError:
        print(f"Error: Save directory '{SAVE_DIR}' not found.")
        return None

    if not files:
        print("No saved games available.")
        return None

    print("Choose username (/b - back):\n")
    for f in files:
        print(f)
    print()

    while True:
        user_input = input("> ").strip().lower()
        if user_input == "/b":
            return None
        elif user_input in [name.lower() for name in files]:
            filename = f"{user_input}{SAVE_FILE_EXTENSION}"
            filepath = os.path.join(SAVE_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                print("Loading your progress...\n")
            except FileNotFoundError:
                print(f"Error: Save file '{filename}' not found.")
                return None
            except json.JSONDecodeError:
                print(f"Error: Save file '{filename}' is corrupted.")
                return None
            except Exception as e:
                print(f"Error loading save file: {str(e)}")
                return None

            try:
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
                game_state = [data["progress"]["level"], data["progress"]["scene"]]
                game_loaded = Game(username, character, game_state)
                print(f"------ Level {game_loaded.current_level[-1]} ------")
                return game_loaded
            except KeyError as e:
                print(f"Error: Save file missing required field: {str(e)}")
                return None
        else:
            print("Unknown input! Please enter a valid one.")