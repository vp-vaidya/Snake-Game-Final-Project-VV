# Snake Game

A classic grid-based Snake game built with Python and Tkinter. Control a growing snake to eat food and power-ups while avoiding obstacles and walls.

## Files

**Files**
- `configuration.py` - Game settings (board size, speed, power-ups, obstacles)
- `game.py` - Game logic (movement, collisions, scoring)
- `draw.py` - Rendering layer using Tkinter Canvas
- `main.py` - Main application window and game loop
- `test_snake.py` - unit tests

## Code Classes

**Configuration** - Settings container (board dimensions, speeds, probabilities)
**Game** - Game logic (snake position, collisions, scoring, state management)
**Draw** - Game rendering (converts game to Tkinter Canvas drawings)
**Combined** - Tkinter application window and game loop


## Features

The game includes:
- Grid-based snake movement with continuous gameplay
- Food (+1 point, +1 growth) and power-ups (+2 points, +2 growth)
- Randomly generated 2×2 obstacle blocks
- Wrap Walls - Snake wraps around board edges instead of dying
- Invincible Mode - Snake bounces off obstacles/walls and can intersect itself
- Configurable board size, speed, obstacle density, and power-up frequency
- Pause/Resume functionality


## Usage

To run the game download all files as a, type "python3 main.py" in the Terminal and a window will open with the game board and controls.

## Keyboard Controls
- Arrow keys: Move snake
- Space bar: Pause/Resume

## GUI Controls
- Obstacle blobs: Enable/disable random obstacles
- Wrap walls: Enable wrapping around walls
- Invincible: Enable invincibility
- Start/Reset: New game
- Pause/Resume: Pause the game

## Testing
To run unit tests, type "python3 test_snake.py" in the Terminal


## Customization

Adjustable in `configuration.py`:
- `grid_width`, `grid_height` - Board dimensions
- `cell_size` - Visual size of each grid cell
- `step_delay` - delay between each step of game
- `obstacle_density` - Fraction of board filled with obstacles (0-1)
- `powerup_chance` - Probability of power-up spawning each step (0-1)

## Author

Vedant Vaidya

EN.540.635 Software Carpentry, Johns Hopkins University

## License

MIT License