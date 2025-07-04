# Maze Game

A simple Python maze game built with Pygame. Navigate through a randomly generated maze, leave a glowing trail, and reach the goal.

## Features

- Smooth player movement
- Fading golden trail behind the player
- Multiple color themes
- Instruction popup at start
- Step counter (ignores bumping into walls)
- Fully adaptive to your screen size

## Controls

- **Arrow keys / WASD**: Move player
- **R**: Restart the maze
- **1–5**: Switch color theme
- **Space**: Close instructions modal at start
- **T**: Toggle step counter
- **ESC** or window close: Quit the game

## Requirements

- Python 3.x
- `pygame`

## Setup

1. Install Pygame:
   ```bash
   pip install pygame
   ```

2. Run the game:
   ```bash
   python main.py
   ```

## Notes

- The default maze grid is 30x30 cells for a balanced challenge.
- Adjust `ROWS` and `COLS` in the script for different difficulty (they do not have to be the same, the maze can also be a rectangle)
- The player leaves a golden trail that fades over time.
- Switch between unique color themes anytime using the number keys.

Enjoy exploring the maze!
