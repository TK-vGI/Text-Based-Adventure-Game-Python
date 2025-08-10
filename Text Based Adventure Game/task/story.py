import json
from config import STORY_FILE_PATH

class Story:
    def __init__(self, story_file: str = STORY_FILE_PATH):
        try:
            with open(story_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Story file '{story_file}' not found.")
            raise
        except json.JSONDecodeError:
            print(f"Error: Story file '{story_file}' is corrupted or invalid JSON.")
            raise
        except Exception as e:
            print(f"Error loading story file: {str(e)}")
            raise

        self.validate_story()

    def validate_story(self):
        """Validate the structure of story.json."""
        required_level_keys = ["scenes", "next"]
        required_scene_keys = ["text", "options"]
        required_option_keys = ["option_text", "result_text", "next", "actions"]

        for level, level_data in self.data.items():
            if not isinstance(level_data, dict):
                raise ValueError(f"Level '{level}' must be a dictionary.")
            for key in required_level_keys:
                if key not in level_data:
                    raise ValueError(f"Level '{level}' missing required key: {key}")

            if not isinstance(level_data["scenes"], dict):
                raise ValueError(f"Level '{level}' scenes must be a dictionary.")

            for scene, scene_data in level_data["scenes"].items():
                for key in required_scene_keys:
                    if key not in scene_data:
                        raise ValueError(f"Scene '{scene}' in level '{level}' missing required key: {key}")
                if not isinstance(scene_data["options"], list):
                    raise ValueError(f"Scene '{scene}' options must be a list.")

                for option in scene_data["options"]:
                    for key in required_option_keys:
                        if key not in option:
                            raise ValueError(f"Option in scene '{scene}' (level '{level}') missing required key: {key}")
                    if not isinstance(option["actions"], list):
                        raise ValueError(f"Option actions in scene '{scene}' (level '{level}') must be a list.")

    def get_scene(self, level: str, scene: str) -> dict:
        if level not in self.data:
            raise ValueError(f"Level '{level}' not found in story.")
        if scene not in self.data[level]["scenes"]:
            raise ValueError(f"Scene '{scene}' not found in level '{level}'.")
        return self.data[level]["scenes"][scene]

    def advance_level(self, current_level: str) -> str | None:
        if current_level not in self.data:
            raise ValueError(f"Level '{current_level}' not found in story.")
        next_level = self.data[current_level]["next"]
        if next_level in self.data:
            return next_level
        else:
            print("You've completed the adventure!\n")
            return None