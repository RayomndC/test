from random import Random
import unittest

from snake_logic import GameState, create_initial_state, place_food, set_direction, tick


class SnakeLogicTests(unittest.TestCase):
    def test_initial_state_has_snake_and_food(self) -> None:
        rng = Random(1)
        state = create_initial_state(10, 10, rng)

        self.assertEqual(state.direction, "RIGHT")
        self.assertEqual(len(state.snake), 3)
        self.assertNotIn(state.food, state.snake)

    def test_direction_cannot_reverse_immediately(self) -> None:
        state = create_initial_state(10, 10, Random(1))
        set_direction(state, "LEFT")
        self.assertEqual(state.next_direction, "RIGHT")

    def test_tick_moves_forward(self) -> None:
        state = create_initial_state(10, 10, Random(1))
        old_head = state.snake[0]

        tick(state, Random(1))

        self.assertEqual(state.snake[0], (old_head[0] + 1, old_head[1]))
        self.assertEqual(len(state.snake), 3)

    def test_eating_food_grows_and_scores(self) -> None:
        state = GameState(
            width=8,
            height=8,
            snake=[(3, 3), (2, 3), (1, 3)],
            direction="RIGHT",
            next_direction="RIGHT",
            food=(4, 3),
        )

        tick(state, Random(2))

        self.assertEqual(state.score, 1)
        self.assertEqual(len(state.snake), 4)
        self.assertNotEqual(state.food, (4, 3))

    def test_wall_collision_sets_game_over(self) -> None:
        state = GameState(
            width=5,
            height=5,
            snake=[(4, 2), (3, 2), (2, 2)],
            direction="RIGHT",
            next_direction="RIGHT",
            food=(0, 0),
        )

        tick(state, Random(3))

        self.assertTrue(state.game_over)

    def test_self_collision_sets_game_over(self) -> None:
        state = GameState(
            width=6,
            height=6,
            snake=[(2, 2), (2, 3), (3, 3), (3, 2), (4, 2)],
            direction="UP",
            next_direction="RIGHT",
            food=(0, 0),
        )

        tick(state, Random(4))

        self.assertTrue(state.game_over)

    def test_place_food_returns_sentinel_when_board_full(self) -> None:
        blocked = [(x, y) for y in range(3) for x in range(3)]
        food = place_food(3, 3, blocked, Random(1))
        self.assertEqual(food, (-1, -1))


if __name__ == "__main__":
    unittest.main()
