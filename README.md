# Classic Snake (Python)

Minimal classic Snake implementation for CodeSandbox-friendly Python environments.

## Run

```bash
python snake_game.py
```

This opens a Tkinter window with the game.

## Controls

- Keyboard: Arrow keys or `W/A/S/D`
- Pause: `P`
- Restart: `R`
- On-screen buttons: arrow controls + pause/restart buttons

## Manual verification checklist

- [ ] Snake moves one cell per tick and follows current direction.
- [ ] Pressing opposite direction (e.g., left while moving right) is ignored.
- [ ] Eating food increases score and grows snake by one segment.
- [ ] Hitting wall or snake body ends game.
- [ ] Restart resets snake, score, and game-over state.
- [ ] Pause freezes movement until resumed.

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
