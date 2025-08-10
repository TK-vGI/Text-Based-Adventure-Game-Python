import unittest
from unittest.mock import mock_open, patch
import json
from story import Story

class TestStory(unittest.TestCase):
    def setUp(self):
        """Set up a mock story file for testing."""
        self.test_story_data = {
            "level1": {
                "scenes": {
                    "scene1": {
                        "text": "You are at the start.",
                        "options": [
                            {
                                "option_text": "Go forward",
                                "result_text": "You move forward.",
                                "next": "scene2",
                                "actions": []
                            }
                        ]
                    },
                    "scene2": {
                        "text": "You reached the end.",
                        "options": []
                    }
                },
                "next": "level2"
            },
            "level2": {
                "scenes": {
                    "scene1": {
                        "text": "Level 2 start.",
                        "options": []
                    }
                },
                "next": None
            }
        }

    def test_get_scene_valid(self):
        """Test retrieving a valid scene."""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_story_data))):
            story = Story()
            scene = story.get_scene("level1", "scene1")
            self.assertEqual(scene["text"], "You are at the start.")
            self.assertEqual(len(scene["options"]), 1)
            self.assertEqual(scene["options"][0]["next"], "scene2")

    def test_get_scene_invalid_level(self):
        """Test retrieving a scene from an invalid level."""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_story_data))):
            story = Story()
            with self.assertRaises(ValueError) as cm:
                story.get_scene("invalid_level", "scene1")
            self.assertEqual(str(cm.exception), "Level 'invalid_level' not found in story.")

    def test_get_scene_invalid_scene(self):
        """Test retrieving an invalid scene from a valid level."""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_story_data))):
            story = Story()
            with self.assertRaises(ValueError) as cm:
                story.get_scene("level1", "invalid_scene")
            self.assertEqual(str(cm.exception), "Scene 'invalid_scene' not found in level 'level1'.")

    def test_advance_level_valid(self):
        """Test advancing to a valid next level."""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_story_data))):
            story = Story()
            next_level = story.advance_level("level1")
            self.assertEqual(next_level, "level2")

    def test_advance_level_last(self):
        """Test advancing from the last level."""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_story_data))):
            story = Story()
            next_level = story.advance_level("level2")
            self.assertIsNone(next_level)

if __name__ == "__main__":
    unittest.main()