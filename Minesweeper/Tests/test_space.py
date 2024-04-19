import unittest
from typing import List
from hypothesis import given, strategies as st
from space import Space


class TestSpace(unittest.TestCase):
    def test_toggle_flag_initial_state(self) -> None:
        space: Space = Space(has_bomb=False)
        self.assertFalse(space.get_flagged(), "Initially, space should not be flagged.")
    
    def test_toggle_flag_action(self) -> None:
        space: Space = Space(has_bomb=False)
        space.toggle_flag()
        self.assertTrue(space.get_flagged(), "Flag should be True after toggling.")
    
    def test_toggle_flag_double_action(self) -> None:
        space: Space = Space(has_bomb=False)
        space.toggle_flag()
        space.toggle_flag()
        self.assertFalse(space.get_flagged(), "Flag should be False after toggling twice.")
    
    def test_handle_click_initial_state(self) -> None:
        space: Space = Space(has_bomb=False)
        self.assertFalse(space.get_clicked(), "Initially, space should not be clicked.")
    
    def test_handle_click_action(self) -> None:
        space: Space = Space(has_bomb=False)
        space.handle_click()
        self.assertTrue(space.get_clicked(), "Space should be clicked after handling click.")
    
    @given(st.lists(st.booleans(), min_size=0, max_size=8))
    def test_set_sum_around(self, has_bomb_list: List[bool]) -> None:
        neighbors: List[Space] = [Space(has_bomb=bomb_status) for bomb_status in has_bomb_list]
        space: Space = Space(has_bomb=False)
        space.set_neighbors(neighbors)
        space.set_num_around()
        expected_bombs_around: int = sum(has_bomb_list)
        self.assertEqual(space.get_num_around(), expected_bombs_around, "Number of bombs around doesn't match expected value.")

    def test_str_representation(self) -> None:
        space_with_bomb: Space = Space(has_bomb=True)
        self.assertEqual(str(space_with_bomb), "True", "String representation of space with bomb should be 'True'.")
        space_without_bomb: Space = Space(has_bomb=False)
        self.assertEqual(str(space_without_bomb), "False", "String representation of space without bomb should be 'False'.")
    
    def test_get_neighbors(self) -> None:
        space: Space = Space(has_bomb=False)
        neighbor1: Space = Space(has_bomb=True)
        neighbor2: Space = Space(has_bomb=False)
        space.set_neighbors([neighbor1, neighbor2])
        self.assertEqual(space.get_neighbors(), [neighbor1, neighbor2], "Neighbors should match the ones set.")

if __name__ == "__main__":  # pragma: no cover
    unittest.main()