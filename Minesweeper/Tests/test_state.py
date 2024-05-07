import unittest
from unittest.mock import MagicMock
import unittest.mock
from hypothesis import given, strategies as st  # type: ignore
from typing import Tuple
from state import State


class ConcreteState(State):  # pragma: no cover
    __test__ = False

    def handle_click(self, position: Tuple[int, int]) -> None:
        print(f"Click handled at: {position}")

    def enter(self) -> None:
        print("Entering state")

    def exit(self) -> None:
        print("Exiting state")


class StateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game = MagicMock()
        self.state = ConcreteState(self.game)

    @given(position=st.tuples(st.integers(), st.integers()))  # type: ignore
    def test_handle_click(self, position: Tuple[int, int]) -> None:
        with unittest.mock.patch.object(self.state,
                                        "handle_click") as mock_handle_click:
            self.state.handle_click(position)
            mock_handle_click.assert_called_with(position)

    def test_enter_is_callable(self) -> None:
        with unittest.mock.patch.object(self.state, "enter") as mock_enter:
            self.state.enter()
            mock_enter.assert_called_once()

    def test_exit_is_callable(self) -> None:
        with unittest.mock.patch.object(self.state, "exit") as mock_exit:
            self.state.exit()
            mock_exit.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
