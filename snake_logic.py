from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable


Point = tuple[int, int]


DIRECTION_VECTORS: dict[str, Point] = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

OPPOSITE_DIRECTION = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}


@dataclass
class GameState:
    width: int
    height: int
    snake: list[Point]
    direction: str
    next_direction: str
    food: Point
    score: int = 0
    game_over: bool = False


def _initial_snake(width: int, height: int) -> list[Point]:
    center_x = width // 2
    center_y = height // 2
    return [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]


def create_initial_state(width: int, height: int, rng: Random | None = None) -> GameState:
    if width < 5 or height < 5:
        raise ValueError("Grid must be at least 5x5")

    rng = rng or Random()
    snake = _initial_snake(width, height)
    food = place_food(width, height, snake, rng)
    return GameState(
        width=width,
        height=height,
        snake=snake,
        direction="RIGHT",
        next_direction="RIGHT",
        food=food,
    )


def set_direction(state: GameState, requested: str) -> None:
    requested = requested.upper()
    if requested not in DIRECTION_VECTORS:
        return

    if requested == OPPOSITE_DIRECTION[state.direction]:
        return

    state.next_direction = requested


def _next_head(head: Point, direction: str) -> Point:
    dx, dy = DIRECTION_VECTORS[direction]
    return head[0] + dx, head[1] + dy


def place_food(width: int, height: int, blocked: Iterable[Point], rng: Random) -> Point:
    blocked_set = set(blocked)
    candidates = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in blocked_set
    ]

    if not candidates:
        return (-1, -1)

    return rng.choice(candidates)


def tick(state: GameState, rng: Random | None = None) -> None:
    if state.game_over:
        return

    rng = rng or Random()
    state.direction = state.next_direction

    new_head = _next_head(state.snake[0], state.direction)
    x, y = new_head

    if not (0 <= x < state.width and 0 <= y < state.height):
        state.game_over = True
        return

    grows = new_head == state.food
    body_to_check = state.snake if grows else state.snake[:-1]
    if new_head in body_to_check:
        state.game_over = True
        return

    state.snake.insert(0, new_head)

    if grows:
        state.score += 1
        state.food = place_food(state.width, state.height, state.snake, rng)
    else:
        state.snake.pop()
