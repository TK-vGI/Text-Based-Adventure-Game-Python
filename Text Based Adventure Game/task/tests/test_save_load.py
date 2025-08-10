# test_save_load.py
import unittest
from unittest.mock import mock_open, patch
import json
from character import Character
from gameplay import Game
from save_load import save_game, load_game

class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        """Set up a Game instance for testing save_game."""
        self.character = Character(
            name="Hero",
            species="Elf",
            gender="Male",
            snack="Apple",
            weapon="Sword",
            tool="Map",
            difficulty="easy",
            lives=5
        )
        self.game = Game(username="test_user", character=self.character, game_state=["level1", "scene1"])

    def test_save_game_success(self):
        """Test save_game writes correct JSON data."""
        expected_data = {
            "character": {
                "name": "Hero",
                "species": "Elf",
                "gender": "Male"
            },
            "inventory": {
                "snack_name": "Apple",
                "weapon_name": "Sword",
                "tool_name": "Map",
                "content": ["Apple", "Sword", "Map"]
            },
            "progress": {
                "level": "level1",
                "scene": "scene1"
            },
            "lives": 5,
            "difficulty": "easy"
        }
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch("os.makedirs"):
                result = save_game(self.game)
        self.assertTrue(result)
        # Combine all write calls and compare with expected JSON
        written_data = "".join(call[0][0] for call in mock_file().write.call_args_list)
        self.assertEqual(json.loads(written_data), expected_data)

    def test_save_game_permission_error(self):
        """Test save_game handles PermissionError."""
        with patch("builtins.open", side_effect=PermissionError):
            with patch("os.makedirs"):
                result = save_game(self.game)
        self.assertFalse(result)

    def test_save_game_generic_error(self):
        """Test save_game handles unexpected errors."""
        with patch("builtins.open", side_effect=Exception("Unknown error")):
            with patch("os.makedirs"):
                result = save_game(self.game)
        self.assertFalse(result)

    def test_load_game_success(self):
        """Test load_game loads a valid save file."""
        save_data = {
            "character": {
                "name": "Hero",
                "species": "Elf",
                "gender": "Male"
            },
            "inventory": {
                "snack_name": "Apple",
                "weapon_name": "Sword",
                "tool_name": "Map",
                "content": ["Apple", "Sword", "Map"]
            },
            "progress": {
                "level": "level1",
                "scene": "scene1"
            },
            "lives": 5,
            "difficulty": "easy"
        }
        with patch("os.listdir", return_value=["test_user.json"]):
            with patch("builtins.open", mock_open(read_data=json.dumps(save_data))):
                with patch("builtins.input", return_value="test_user"):
                    game = load_game()
        self.assertIsNotNone(game)
        self.assertEqual(game.username, "test_user")
        self.assertEqual(game.character.name, "Hero")
        self.assertEqual(game.current_level, "level1")
        self.assertEqual(game.current_scene, "scene1")

if __name__ == "__main__":
    unittest.main()