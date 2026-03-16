from __future__ import annotations

import tkinter as tk
from random import Random

from snake_logic import GameState, create_initial_state, set_direction, tick


CELL_SIZE = 22
GRID_WIDTH = 20
GRID_HEIGHT = 20
TICK_MS = 140

BG_COLOR = "#101418"
GRID_COLOR = "#1b2229"
SNAKE_COLOR = "#3ddc84"
FOOD_COLOR = "#ff5f56"
TEXT_COLOR = "#e6edf3"


class SnakeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Classic Snake")
        self.root.configure(bg=BG_COLOR)

        self.rng = Random()
        self.state: GameState = create_initial_state(GRID_WIDTH, GRID_HEIGHT, self.rng)
        self.paused = False

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            fg=TEXT_COLOR,
            bg=BG_COLOR,
            font=("Arial", 12, "bold"),
        )
        self.score_label.pack(pady=(10, 6))

        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg=BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=(0, 10))

        control_row = tk.Frame(root, bg=BG_COLOR)
        control_row.pack(pady=(0, 10))

        tk.Button(control_row, text="Restart (R)", command=self.restart).grid(row=0, column=0, padx=4)
        tk.Button(control_row, text="Pause (P)", command=self.toggle_pause).grid(row=0, column=1, padx=4)

        mobile_controls = tk.Frame(root, bg=BG_COLOR)
        mobile_controls.pack(pady=(0, 10))
        tk.Button(mobile_controls, text="↑", width=4, command=lambda: self.change_dir("UP")).grid(row=0, column=1)
        tk.Button(mobile_controls, text="←", width=4, command=lambda: self.change_dir("LEFT")).grid(row=1, column=0)
        tk.Button(mobile_controls, text="↓", width=4, command=lambda: self.change_dir("DOWN")).grid(row=1, column=1)
        tk.Button(mobile_controls, text="→", width=4, command=lambda: self.change_dir("RIGHT")).grid(row=1, column=2)

        self.root.bind("<Key>", self._on_key)

        self.draw()
        self.schedule_tick()

    def schedule_tick(self) -> None:
        self.root.after(TICK_MS, self.game_loop)

    def _on_key(self, event: tk.Event[tk.Misc]) -> None:
        key = event.keysym.lower()
        mapping = {
            "up": "UP",
            "w": "UP",
            "down": "DOWN",
            "s": "DOWN",
            "left": "LEFT",
            "a": "LEFT",
            "right": "RIGHT",
            "d": "RIGHT",
        }
        if key in mapping:
            self.change_dir(mapping[key])
        elif key == "r":
            self.restart()
        elif key == "p":
            self.toggle_pause()

    def change_dir(self, direction: str) -> None:
        set_direction(self.state, direction)

    def toggle_pause(self) -> None:
        if not self.state.game_over:
            self.paused = not self.paused

    def restart(self) -> None:
        self.state = create_initial_state(GRID_WIDTH, GRID_HEIGHT, self.rng)
        self.paused = False
        self.draw()

    def game_loop(self) -> None:
        if not self.paused:
            tick(self.state, self.rng)
            self.draw()
        self.schedule_tick()

    def _draw_grid(self) -> None:
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(x, 0, x, GRID_HEIGHT * CELL_SIZE, fill=GRID_COLOR)
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(0, y, GRID_WIDTH * CELL_SIZE, y, fill=GRID_COLOR)

    def _draw_cell(self, point: tuple[int, int], color: str) -> None:
        x, y = point
        self.canvas.create_rectangle(
            x * CELL_SIZE + 1,
            y * CELL_SIZE + 1,
            (x + 1) * CELL_SIZE - 1,
            (y + 1) * CELL_SIZE - 1,
            fill=color,
            outline=color,
        )

    def draw(self) -> None:
        self.canvas.delete("all")
        self._draw_grid()

        for segment in self.state.snake:
            self._draw_cell(segment, SNAKE_COLOR)

        if self.state.food != (-1, -1):
            self._draw_cell(self.state.food, FOOD_COLOR)

        status = "Score: {}".format(self.state.score)
        if self.paused:
            status += "  |  Paused"
        if self.state.game_over:
            status += "  |  Game Over (press R to restart)"
        self.score_label.config(text=status)


def main() -> None:
    root = tk.Tk()
    SnakeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
