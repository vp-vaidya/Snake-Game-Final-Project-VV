# Snake Game

This is an implementation of the classic Snake game built with Python and Tkinter. Control a snake in a grid with arrow keys to eat food and power-ups while avoiding obstacles and walls. Obstacles can be toggled off but it is set as default. Default configuration can be changed in configuration.py. Game is played until snake hits a wall, obstacle or itself. With invincibility function on game can go on indefinetly.

## Features

The game includes:
- Grid-based snake movement
- Food (+1 point, +1 growth) and power-ups (+2 points, +2 growth)
- Randomly generated 2×2 obstacle blocks (On as a default but can be toggled on/off)
- Wrap Walls - Snake wraps around board edges instead of dying (Can be toggled on/off)
- Invincible Mode - Snake bounces off obstacles/walls and can intersect itself (Can be toggled on/off) (The game can go on forever with invincibility on)
- Configurable speed, obstacle density, and power-up frequency in configuration.py (default settings are already entered) (reduce step_delay for faster snake) (keep grid_width = grid_height=15)
- Pause/Resume functionality

## Keyboard Controls
- Arrow keys: Move snake
- Space bar: Pause/Resume

## Files

**Files**
- `configuration.py` - Game settings (board size, speed, power-ups, obstacles)
- `game.py` - Game logic (movement, collisions, scoring)
- `draw.py` - Rendering layer
- `main.py` - Main application window using Tkinter Canvas and game loop
- `test_snake.py` - unit tests

## Classes

**Configuration** - Settings container (board dimensions, speeds, probabilities, etc.)
**Game** - Game logic (snake position, collisions, scoring, etc.)
**Draw** - Game rendering (draws out snake, food, obstacles, etc.)
**Combined** - Tkinter application window and main game loop


## Usage
To run the game download all files and type "python3 main.py" in the Terminal and a window will open with the game board and controls.

## Testing
To run unit tests, type "python3 test_snake.py" in the Terminal

## Author

Vedant Vaidya

EN.540.635 Software Carpentry, Johns Hopkins University

## License

MIT License
