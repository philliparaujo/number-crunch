# Number Crunch
## Screenshots
Click here to see pictures of the game in action: https://imgur.com/a/Teacntl
## Description
Number Crunch is a singleplayer, turn-based strategy game in a similar style to [Backpack Battles](https://store.steampowered.com/app/2427700/Backpack_Battles/). Every turn, use your three actions to reroll and purchase increasingly large numbers. Try to match the target score every turn. You get bonuses for matching numbers. 
## Installation
- Download the zip folder and extract
- Install [python](https://www.python.org/downloads/)
- Navigate to the extracted folder directory in a terminal: `cd <path/to/folder>/number-crunch-main`
- Run the game: `python3 main.py`
   - If error `ModuleNotFoundError: No module named 'pygame'`, then run `pip install pygame`
## Project Structure

### Main loop
- `main.py`: handles global mouse variables and important gameplay procedures

### Important classes and objects
- `components.py`: defines essential UI classes (Button, Cell, DraggableText)
- `GameState.py`: defines GameState class that holds all game variables and logic

### Helpful functions for drawing and simple logic
- `drawer.py`: contains simple functions for drawing text and rectangles
- `utils.py`: contains various general helper functins

### Visual, auditory, and gameplay constants
- `colors.py`: defines all colors used in the UI
- `features.py`: defines all shop weights, target scores, and starting game state values
- `ui.py`: defines all sizes and positions of components
- `sounds.py`: defines and initializes all sounds used in the game
  - `sounds/`: folder with all mp3 files used
