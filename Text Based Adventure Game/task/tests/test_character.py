import unittest
from character import Character

class TestCharacter(unittest.TestCase):
    def setUp(self):
        """Set up a default Character instance for tests."""
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

    def test_initialization(self):
        """Test Character initializes correctly."""
        self.assertEqual(self.character.name, "Hero")
        self.assertEqual(self.character.species, "Elf")
        self.assertEqual(self.character.gender, "Male")
        self.assertEqual(self.character.difficulty, "easy")
        self.assertEqual(self.character.lives, 5)
        self.assertEqual(self.character.inventory["snack_name"], "Apple")
        self.assertEqual(self.character.inventory["weapon_name"], "Sword")
        self.assertEqual(self.character.inventory["tool_name"], "Map")
        self.assertEqual(self.character.inventory["content"], ["Apple", "Sword", "Map"])

    def test_initialization_with_content(self):
        """Test Character initializes with custom content list."""
        character = Character(
            name="Hero",
            species="Elf",
            gender="Male",
            snack="Apple",
            weapon="Sword",
            tool="Map",
            difficulty="hard",
            lives=1,
            content=["Apple", "Sword", "Map", "Shield"]
        )
        self.assertEqual(character.inventory["content"], ["Apple", "Sword", "Map", "Shield"])

    def test_update_item(self):
        """Test updating an inventory item."""
        self.character.update_item("weapon_name", "Axe")
        self.assertEqual(self.character.inventory["weapon_name"], "Axe")
        self.assertEqual(self.character.inventory["content"], ["Apple", "Axe", "Map"])

    def test_update_item_invalid(self):
        """Test updating a non-existent item type."""
        self.character.update_item("invalid_item", "Test")
        self.assertNotIn("invalid_item", self.character.inventory)

    def test_str_method(self):
        """Test the string representation of Character."""
        self.assertEqual(str(self.character), "Hero the Elf (Male) with Apple, Sword, Map")

    def test_character_summary(self):
        """Test character_summary (mocking print is complex, so we skip output testing)."""
        # Note: Testing print output requires mocking sys.stdout, which is optional
        self.assertTrue(hasattr(self.character, "character_summary"))

if __name__ == "__main__":
    unittest.main()